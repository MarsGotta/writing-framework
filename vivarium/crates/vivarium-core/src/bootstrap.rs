use std::env;
use std::fs;
use std::path::{Path, PathBuf};
use std::process::Command;

use git2::{IndexAddOption, Repository, Signature};

use crate::decisions;
use crate::dispatch;
use crate::error::{Result, VivariumError};
use crate::manifest::{self, Mode};
use crate::sidecar;

#[derive(Debug, Clone)]
pub struct BootstrapOptions {
    pub target: PathBuf,
    pub kind: String,
    pub mode: Option<Mode>,
    pub sector: Option<String>,
    pub preset: Option<PathBuf>,
    pub operator: Option<String>,
    pub email: Option<String>,
    pub agents: String,
}

impl BootstrapOptions {
    pub fn resolved_mode(&self) -> Result<Mode> {
        Ok(self
            .mode
            .unwrap_or(manifest::default_mode_for_kind(&self.kind)?))
    }

    pub fn resolved_preset(&self) -> PathBuf {
        self.preset.clone().unwrap_or_else(default_preset_path)
    }
}

pub fn new_project(options: &BootstrapOptions) -> Result<PathBuf> {
    verify_environment()?;
    let target = absolutize(&options.target)?;
    if target.exists() && !target.is_dir() {
        return Err(VivariumError::Validation(format!(
            "{} existe y no es directorio",
            target.display()
        )));
    }
    fs::create_dir_all(&target)?;
    let preset = options.resolved_preset();
    if !preset.join("scripts/bootstrap.py").is_file() {
        return Err(VivariumError::Validation(format!(
            "{} no parece el preset writeonmars (falta scripts/bootstrap.py)",
            preset.display()
        )));
    }

    init_git(&target)?;
    ensure_specify(&target, &preset, &options.agents)?;

    // Idempotencia con procedencia: un manifiesto existente conserva su mode.
    // Cambiarlo es acción explícita de `vivarium mode set` (FR-009), nunca un
    // efecto lateral de re-ejecutar `vivarium new`.
    let manifest_pre_existing = manifest::manifest_path(&target).is_file();
    if manifest_pre_existing {
        let existing = manifest::load_project(&target)?;
        if let Some(requested) = options.mode {
            if requested != existing.mode() {
                return Err(VivariumError::Validation(format!(
                    "el proyecto ya existe con mode={}; usa `vivarium mode set {}` para cambiarlo",
                    existing.mode(),
                    requested
                )));
            }
        }
    }

    let (operator, email) = resolve_identity(options.operator.as_deref(), options.email.as_deref());
    discard_placeholder_constitution(&target)?;
    run_bootstrap_py(
        &target,
        &operator,
        email.as_deref(),
        options.resolved_mode()?,
    )?;

    // El mode del manifiesto fresco lo escribe bootstrap.py (--mode); aquí solo
    // se completa el sector cuando falta, sin pisar uno ya fijado.
    let manifest_now = manifest::load_project(&target)?;
    let sector_absent = matches!(
        manifest_now.raw().get("sector"),
        None | Some(serde_json::Value::Null)
    );
    if sector_absent {
        if let Some(sector) = manifest::default_sector_for(
            &options.kind,
            manifest_now.mode(),
            options.sector.as_deref(),
        ) {
            manifest::set_sector_field(&target, Some(&sector))?;
        }
    }

    ensure_roots(&target)?;
    decisions::ensure(&target)?;
    ensure_vivarium_files(&target)?;
    ensure_context_file(&target)?;
    sidecar::run_status(&target)?;
    commit_base(&target, &operator, email.as_deref())?;
    Ok(target)
}

fn verify_environment() -> Result<()> {
    for command in ["git", "specify"] {
        if !dispatch::command_resolves(command) {
            return Err(VivariumError::EnvironmentIncomplete(format!(
                "falta {command} en PATH"
            )));
        }
    }
    let python = sidecar::resolve_python();
    if !dispatch::command_resolves(&python) {
        return Err(VivariumError::EnvironmentIncomplete(format!(
            "falta intérprete Python: {python}"
        )));
    }
    Ok(())
}

fn init_git(target: &Path) -> Result<()> {
    if target.join(".git").is_dir() {
        return Ok(());
    }
    Repository::init(target)?;
    Ok(())
}

fn ensure_specify(target: &Path, preset: &Path, agents: &str) -> Result<()> {
    let primary = agents.split(',').next().unwrap_or("claude");
    if !target.join(".specify").is_dir() {
        run_checked(
            Command::new("specify")
                .arg("init")
                .arg("--here")
                .arg("--force")
                .arg("--ignore-agent-tools")
                .arg("--integration")
                .arg(primary)
                .current_dir(target),
            "specify init",
        )?;
    }
    if !target.join(".specify").is_dir() {
        return Err(VivariumError::EnvironmentIncomplete(
            "specify init no creó .specify/".to_string(),
        ));
    }
    if !target.join(".specify/presets/writeonmars").is_dir() {
        run_checked(
            Command::new("specify")
                .arg("preset")
                .arg("add")
                .arg("--dev")
                .arg(preset)
                .current_dir(target),
            "specify preset add",
        )?;
    }
    if !target.join(".specify/presets/writeonmars").is_dir() {
        return Err(VivariumError::EnvironmentIncomplete(
            "specify preset add no instaló .specify/presets/writeonmars".to_string(),
        ));
    }
    Ok(())
}

fn discard_placeholder_constitution(target: &Path) -> Result<()> {
    let path = target.join(".specify/memory/constitution.md");
    if path.is_file() {
        let text = fs::read_to_string(&path)?;
        if text.contains("[PROJECT_NAME]") {
            fs::remove_file(path)?;
        }
    }
    Ok(())
}

fn run_bootstrap_py(target: &Path, operator: &str, email: Option<&str>, mode: Mode) -> Result<()> {
    let script = sidecar::scripts_dir(target).join("bootstrap.py");
    let mut command = Command::new(sidecar::resolve_python_for(target));
    command
        .arg(script)
        .arg("--project-dir")
        .arg(target)
        .arg("--operator")
        .arg(operator)
        .arg("--mode")
        .arg(mode.as_str())
        .current_dir(target);
    if let Some(email) = email {
        if !email.is_empty() {
            command.arg("--email").arg(email);
        }
    }
    run_checked(&mut command, "bootstrap.py")
}

fn ensure_roots(target: &Path) -> Result<()> {
    let roots = target.join("roots");
    fs::create_dir_all(&roots)?;
    let readme = roots.join("README.md");
    if !readme.exists() {
        fs::write(
            readme,
            "# Roots\n\nUn concepto por archivo Markdown. Frontmatter minimo:\n\n```markdown\n---\ntype: fuente\nalias: []\n---\n```\n\nUsa `personaje`, `lugar`, `fuente`, `cita` o `evento` cuando aplique.\n",
        )?;
    }
    Ok(())
}

fn ensure_vivarium_files(target: &Path) -> Result<()> {
    let vivarium = target.join(".vivarium");
    fs::create_dir_all(&vivarium)?;
    let example = vivarium.join("config.toml.example");
    if !example.exists() {
        fs::write(example, dispatch::example_config())?;
    }
    append_unique_line(&target.join(".gitignore"), ".vivarium/")?;
    append_unique_line(&target.join(".gitignore"), ".DS_Store")?;
    append_unique_line(&target.join(".gitignore"), ".writeonmars-index.json")?;
    Ok(())
}

fn ensure_context_file(target: &Path) -> Result<()> {
    let path = target.join("AGENTS.md");
    if !path.exists() {
        fs::write(
            path,
            "## Proyecto editorial Write.OnMars\n\nLee `.specify/presets/writeonmars/AGENTS.md` y opera siempre sobre archivos del proyecto.\n",
        )?;
    }
    Ok(())
}

fn commit_base(target: &Path, operator: &str, email: Option<&str>) -> Result<()> {
    let repo = Repository::open(target)?;
    let mut index = repo.index()?;
    index.add_all(["."].iter(), IndexAddOption::DEFAULT, None)?;
    index.write()?;
    let tree_id = index.write_tree()?;
    let tree = repo.find_tree(tree_id)?;
    let email = email
        .filter(|value| !value.is_empty())
        .unwrap_or("autor@example.invalid");
    let sig = Signature::now(operator, email)?;
    let parent = repo
        .head()
        .ok()
        .and_then(|head| head.target())
        .and_then(|oid| repo.find_commit(oid).ok());
    if let Some(parent) = parent {
        if parent.tree_id() == tree_id {
            return Ok(());
        }
        repo.commit(
            Some("HEAD"),
            &sig,
            &sig,
            "scaffold proyecto Vivarium: preset + manifest",
            &tree,
            &[&parent],
        )?;
    } else {
        repo.commit(
            Some("HEAD"),
            &sig,
            &sig,
            "scaffold proyecto Vivarium: preset + manifest",
            &tree,
            &[],
        )?;
    }
    Ok(())
}

fn run_checked(command: &mut Command, label: &str) -> Result<()> {
    let output = command.output().map_err(|e| {
        VivariumError::EnvironmentIncomplete(format!("no puedo ejecutar {label}: {e}"))
    })?;
    if !output.status.success() {
        return Err(VivariumError::EnvironmentIncomplete(format!(
            "{label} falló: {}",
            String::from_utf8_lossy(&output.stderr).trim()
        )));
    }
    Ok(())
}

fn resolve_identity(operator: Option<&str>, email: Option<&str>) -> (String, Option<String>) {
    let email = email
        .map(str::to_string)
        .or_else(|| git_config_value("user.email"));
    let operator = operator
        .map(str::to_string)
        .or_else(|| {
            email
                .as_ref()
                .and_then(|value| value.split('@').next())
                .filter(|value| !value.is_empty())
                .map(str::to_string)
        })
        .or_else(|| git_config_value("user.name"))
        .unwrap_or_else(|| "autor".to_string());
    (operator, email)
}

fn git_config_value(key: &str) -> Option<String> {
    git2::Config::open_default()
        .ok()
        .and_then(|cfg| cfg.get_string(key).ok())
        .filter(|value| !value.trim().is_empty())
}

fn append_unique_line(path: &Path, line: &str) -> Result<()> {
    let current = fs::read_to_string(path).unwrap_or_default();
    if current.lines().any(|existing| existing == line) {
        return Ok(());
    }
    let mut next = current;
    if !next.is_empty() && !next.ends_with('\n') {
        next.push('\n');
    }
    next.push_str(line);
    next.push('\n');
    fs::write(path, next)?;
    Ok(())
}

fn default_preset_path() -> PathBuf {
    PathBuf::from(env!("CARGO_MANIFEST_DIR"))
        .ancestors()
        .nth(3)
        .map(|p| p.join("writeonmars"))
        .unwrap_or_else(|| PathBuf::from("writeonmars"))
}

fn absolutize(path: &Path) -> Result<PathBuf> {
    if path.is_absolute() {
        Ok(path.to_path_buf())
    } else {
        Ok(env::current_dir()?.join(path))
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn default_mode_respeta_kind() {
        let opts = BootstrapOptions {
            target: PathBuf::from("demo"),
            kind: "novela".to_string(),
            mode: None,
            sector: None,
            preset: None,
            operator: None,
            email: None,
            agents: "claude,codex".to_string(),
        };
        assert_eq!(opts.resolved_mode().unwrap(), Mode::Estudio);
    }
}
