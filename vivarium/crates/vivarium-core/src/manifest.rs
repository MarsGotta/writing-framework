use std::fmt;
use std::fs;
use std::path::{Path, PathBuf};
use std::str::FromStr;

use chrono::Utc;
use serde::{Deserialize, Serialize};
use serde_json::{Map, Value};

use crate::decisions;
use crate::error::{Result, VivariumError};

pub const MANIFEST_FILE: &str = ".writeonmars-manifest.json";

#[derive(Debug, Clone, Copy, PartialEq, Eq, Serialize, Deserialize)]
#[serde(rename_all = "lowercase")]
pub enum Mode {
    Produccion,
    Estudio,
}

impl Mode {
    pub fn as_str(self) -> &'static str {
        match self {
            Self::Produccion => "produccion",
            Self::Estudio => "estudio",
        }
    }
}

impl fmt::Display for Mode {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        f.write_str(self.as_str())
    }
}

impl FromStr for Mode {
    type Err = VivariumError;

    fn from_str(value: &str) -> Result<Self> {
        match value {
            "produccion" => Ok(Self::Produccion),
            "estudio" => Ok(Self::Estudio),
            other => Err(VivariumError::Validation(format!(
                "mode inválido: {other} (esperado produccion|estudio)"
            ))),
        }
    }
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct ModeChange {
    pub from: Mode,
    pub to: Mode,
    pub date: String,
}

#[derive(Debug, Clone)]
pub struct ProjectManifest {
    path: PathBuf,
    data: Map<String, Value>,
    mode: Mode,
}

impl ProjectManifest {
    pub fn path(&self) -> &Path {
        &self.path
    }

    pub fn mode(&self) -> Mode {
        self.mode
    }

    pub fn raw(&self) -> &Map<String, Value> {
        &self.data
    }

    pub fn mode_history(&self) -> Result<Vec<ModeChange>> {
        match self.data.get("mode_history") {
            None | Some(Value::Null) => Ok(Vec::new()),
            Some(value) => serde_json::from_value(value.clone()).map_err(VivariumError::from),
        }
    }

    pub fn write_atomic(&self) -> Result<()> {
        write_json_atomic(&self.path, &Value::Object(self.data.clone()))
    }
}

pub fn manifest_path(project: &Path) -> PathBuf {
    project.join(MANIFEST_FILE)
}

pub fn load_project(project: impl AsRef<Path>) -> Result<ProjectManifest> {
    load_path(manifest_path(project.as_ref()))
}

pub fn load_path(path: impl AsRef<Path>) -> Result<ProjectManifest> {
    let path = path.as_ref().to_path_buf();
    let text = fs::read_to_string(&path)
        .map_err(|e| VivariumError::Validation(format!("no puedo leer {}: {e}", path.display())))?;
    let value: Value = serde_json::from_str(&text)?;
    let data = value.as_object().cloned().ok_or_else(|| {
        VivariumError::Validation(format!("{} no es un objeto JSON", path.display()))
    })?;
    let mode = match data.get("mode") {
        None => Mode::Produccion,
        Some(Value::String(value)) => Mode::from_str(value)?,
        Some(_) => {
            return Err(VivariumError::Validation(
                "mode debe ser string produccion|estudio".to_string(),
            ))
        }
    };
    Ok(ProjectManifest { path, data, mode })
}

pub fn set_mode(project: impl AsRef<Path>, to: Mode) -> Result<ModeChange> {
    let project = project.as_ref();
    let mut manifest = load_project(project)?;
    let from = manifest.mode;
    let change = ModeChange {
        from,
        to,
        date: Utc::now().to_rfc3339(),
    };
    manifest
        .data
        .insert("mode".to_string(), Value::String(to.as_str().to_string()));
    let mut history = manifest.mode_history()?;
    history.push(change.clone());
    manifest.data.insert(
        "mode_history".to_string(),
        serde_json::to_value(history).map_err(VivariumError::from)?,
    );
    manifest.mode = to;
    manifest.write_atomic()?;
    decisions::append_mode_change(project, from, to)?;
    Ok(change)
}

pub fn set_sector_field(project: impl AsRef<Path>, sector: Option<&str>) -> Result<()> {
    let path = manifest_path(project.as_ref());
    let mut manifest = load_path(&path)?;
    manifest.data.insert(
        "sector".to_string(),
        sector
            .map(|s| Value::String(s.to_string()))
            .unwrap_or(Value::Null),
    );
    manifest.write_atomic()
}

pub fn default_mode_for_kind(kind: &str) -> Result<Mode> {
    match kind {
        "guia" | "tutorial" | "documentacion" | "no-ficcion" => Ok(Mode::Produccion),
        "novela" | "relato" | "poesia" | "guion" | "academico" => Ok(Mode::Estudio),
        other => Err(VivariumError::InvalidUsage(format!(
            "kind inválido: {other}"
        ))),
    }
}

pub fn default_sector_for(kind: &str, mode: Mode, sector: Option<&str>) -> Option<String> {
    if let Some(sector) = sector {
        return Some(sector.to_string());
    }
    match (kind, mode) {
        ("guia" | "tutorial" | "documentacion" | "no-ficcion", Mode::Produccion) => {
            Some("tecnologia".to_string())
        }
        _ => None,
    }
}

fn write_json_atomic(path: &Path, value: &Value) -> Result<()> {
    let tmp = path.with_extension("json.tmp");
    let text = serde_json::to_string_pretty(value)?;
    fs::write(&tmp, format!("{text}\n"))?;
    fs::rename(tmp, path)?;
    Ok(())
}

#[cfg(test)]
mod tests {
    use super::*;

    fn base_manifest() -> Value {
        serde_json::json!({
            "framework_version":"0.1.0",
            "constitution_version":"1.6.0"
        })
    }

    #[test]
    fn ausencia_de_mode_es_produccion() {
        let tmp = tempfile::tempdir().unwrap();
        let path = tmp.path().join(MANIFEST_FILE);
        fs::write(&path, serde_json::to_string(&base_manifest()).unwrap()).unwrap();
        assert_eq!(load_path(path).unwrap().mode(), Mode::Produccion);
    }

    #[test]
    fn mode_explicito_estudio() {
        let tmp = tempfile::tempdir().unwrap();
        let path = tmp.path().join(MANIFEST_FILE);
        let mut value = base_manifest();
        value["mode"] = Value::String("estudio".to_string());
        fs::write(&path, serde_json::to_string(&value).unwrap()).unwrap();
        assert_eq!(load_path(path).unwrap().mode(), Mode::Estudio);
    }

    #[test]
    fn mode_invalido_falla() {
        let tmp = tempfile::tempdir().unwrap();
        let path = tmp.path().join(MANIFEST_FILE);
        let mut value = base_manifest();
        value["mode"] = Value::String("demo".to_string());
        fs::write(&path, serde_json::to_string(&value).unwrap()).unwrap();
        assert!(matches!(load_path(path), Err(VivariumError::Validation(_))));
    }
}
