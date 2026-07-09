use std::collections::HashMap;
use std::env;
use std::path::{Path, PathBuf};
use std::process::Command;

use serde::{Deserialize, Serialize};

use crate::error::{Result, VivariumError};

#[derive(Debug, Clone, Deserialize, Serialize, Default)]
pub struct PassStatus {
    pub num: i64,
    pub name: String,
    pub estado: String,
    pub firma: String,
    pub actor: String,
    #[serde(default)]
    pub firma_disp: String,
    #[serde(default)]
    pub required: Option<String>,
    #[serde(default)]
    pub signed: Option<bool>,
    #[serde(default)]
    pub severidades: HashMap<String, i64>,
    #[serde(default)]
    pub abiertos: i64,
}

#[derive(Debug, Clone, Deserialize, Serialize, Default)]
pub struct ChapterStatus {
    pub drafted: bool,
    #[serde(default)]
    pub passes_done: Vec<u8>,
    pub revise_pending: u32,
    pub advisory: u32,
    pub approved: bool,
}

#[derive(Debug, Clone, Deserialize, Serialize, Default)]
pub struct Gates {
    pub no_open_criticals: bool,
    pub human_signatures: bool,
    pub guide_complete: bool,
    #[serde(default)]
    pub factuality: Option<bool>,
}

#[derive(Debug, Clone, Deserialize, Serialize, Default)]
pub struct Status {
    pub spec: String,
    #[serde(default)]
    pub mode: Option<String>,
    #[serde(default)]
    pub chapters: Vec<String>,
    pub chapters_written: u32,
    pub chapters_expected: u32,
    #[serde(default)]
    pub passes: Vec<PassStatus>,
    pub criticals_open: u32,
    pub open_findings_total: u32,
    pub revise_pending: u32,
    #[serde(default)]
    pub revise_by_chapter: HashMap<String, u32>,
    #[serde(default)]
    pub pending_chapters: Vec<u32>,
    #[serde(default)]
    pub pending_dispositions: Vec<String>,
    #[serde(default)]
    pub deferred_findings: Vec<String>,
    #[serde(default)]
    pub reopened_chapters: Vec<String>,
    pub advisory_open_bajo: u32,
    #[serde(default)]
    pub sign_violations: Vec<String>,
    pub gates: Gates,
    pub closeable: bool,
    pub has_manifest: bool,
    #[serde(default)]
    pub by_chapter: HashMap<String, ChapterStatus>,
    pub all_chapters_approved: bool,
    pub next_step: String,
    pub next_detail: String,
}

pub fn resolve_python() -> String {
    env::var("VIVARIUM_PYTHON").unwrap_or_else(|_| "python3".to_string())
}

/// Precedencia del contrato BYOM: `VIVARIUM_PYTHON` → `[python].interpreter`
/// de `.vivarium/config.toml` → `python3`.
pub fn resolve_python_for(project: &Path) -> String {
    if let Ok(value) = env::var("VIVARIUM_PYTHON") {
        if !value.is_empty() {
            return value;
        }
    }
    if let Some(interpreter) = config_python_interpreter(project) {
        return interpreter;
    }
    "python3".to_string()
}

// Lectura laxa a propósito: aquí solo importa [python].interpreter; la
// validación completa del config la hace ByomConfig::load antes de despachar.
fn config_python_interpreter(project: &Path) -> Option<String> {
    let text = std::fs::read_to_string(project.join(crate::dispatch::CONFIG_FILE)).ok()?;
    let value: toml::Value = toml::from_str(&text).ok()?;
    value
        .get("python")?
        .get("interpreter")?
        .as_str()
        .map(str::to_string)
        .filter(|s| !s.is_empty())
}

pub fn scripts_dir(project: &Path) -> PathBuf {
    project.join(".specify/presets/writeonmars/scripts")
}

pub fn status_script(project: &Path) -> PathBuf {
    scripts_dir(project).join("status.py")
}

/// Valida el manifiesto contra el schema delegando en el `validate_manifest`
/// de bootstrap.py (el sidecar es la verdad compartida; sin `jsonschema`
/// instalado degrada a claves requeridas, igual que el propio bootstrap).
pub fn validate_manifest(project: &Path) -> Result<()> {
    let manifest = project.join(".writeonmars-manifest.json");
    if !manifest.is_file() {
        return Err(VivariumError::Validation(format!(
            "falta {}",
            manifest.display()
        )));
    }
    let code = "import json, sys\n\
                sys.path.insert(0, sys.argv[1])\n\
                import bootstrap\n\
                bootstrap.validate_manifest(json.load(open(sys.argv[2], encoding='utf-8')))\n";
    let output = Command::new(resolve_python_for(project))
        .arg("-c")
        .arg(code)
        .arg(scripts_dir(project))
        .arg(&manifest)
        .current_dir(project)
        .output()
        .map_err(|e| {
            VivariumError::EnvironmentIncomplete(format!("no puedo ejecutar python: {e}"))
        })?;
    if output.status.success() {
        Ok(())
    } else {
        Err(VivariumError::Validation(format!(
            "el manifiesto no valida contra el schema: {}",
            String::from_utf8_lossy(&output.stderr).trim()
        )))
    }
}

pub fn run_status(project: impl AsRef<Path>) -> Result<Status> {
    let project = project.as_ref();
    let script = status_script(project);
    if !script.is_file() {
        return Err(VivariumError::Validation(format!(
            "no encuentro status.py en {}",
            script.display()
        )));
    }
    let output = Command::new(resolve_python_for(project))
        .arg(&script)
        .arg("--json")
        .current_dir(project)
        .output()
        .map_err(|e| {
            VivariumError::EnvironmentIncomplete(format!("no puedo ejecutar python/status.py: {e}"))
        })?;
    if !output.status.success() {
        let stderr = String::from_utf8_lossy(&output.stderr).trim().to_string();
        return Err(VivariumError::Sidecar(if stderr.is_empty() {
            format!("status.py salió con {}", output.status)
        } else {
            stderr
        }));
    }
    serde_json::from_slice(&output.stdout).map_err(VivariumError::from)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn deserializa_contrato_status() {
        let json = r#"{
          "spec":"001-demo",
          "mode":"estudio",
          "chapters":["01-a.md"],
          "chapters_written":1,
          "chapters_expected":1,
          "passes":[],
          "criticals_open":0,
          "open_findings_total":0,
          "revise_pending":0,
          "revise_by_chapter":{},
          "pending_chapters":[],
          "pending_dispositions":[],
          "deferred_findings":[],
          "reopened_chapters":[],
          "advisory_open_bajo":0,
          "sign_violations":[],
          "gates":{"no_open_criticals":true,"human_signatures":true,"guide_complete":true,"factuality":null},
          "closeable":true,
          "has_manifest":true,
          "by_chapter":{"1":{"drafted":true,"passes_done":[1,2,3,4],"revise_pending":0,"advisory":0,"approved":true}},
          "all_chapters_approved":true,
          "next_step":"close",
          "next_detail":"gates en verde"
        }"#;
        let status: Status = serde_json::from_str(json).unwrap();
        assert!(status.by_chapter["1"].approved);
        assert_eq!(status.next_step, "close");
        assert_eq!(status.mode.as_deref(), Some("estudio"));
    }
}
