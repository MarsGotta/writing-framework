use std::collections::HashMap;
use std::env;
use std::fs::{self, File};
use std::path::{Path, PathBuf};
use std::process::{Command, Stdio};

use serde::Deserialize;

use crate::error::{Result, VivariumError};

pub const CONFIG_FILE: &str = ".vivarium/config.toml";

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum Role {
    Redactora,
    EditoraMesa,
    Documentalista,
    Sidecar,
}

impl Role {
    pub fn as_str(self) -> &'static str {
        match self {
            Self::Redactora => "redactora",
            Self::EditoraMesa => "editora_mesa",
            Self::Documentalista => "documentalista",
            Self::Sidecar => "sidecar",
        }
    }
}

#[derive(Debug, Clone, Deserialize)]
pub struct ByomConfig {
    pub version: u32,
    #[serde(default)]
    pub python: Option<PythonConfig>,
    pub roles: HashMap<String, RoleConfig>,
}

// [python].interpreter lo consume sidecar::resolve_python_for; se declara aquí
// para que el TOML valide con la sección presente.
#[derive(Debug, Clone, Deserialize)]
pub struct PythonConfig {
    #[serde(default)]
    pub interpreter: Option<String>,
}

#[derive(Debug, Clone, Deserialize)]
pub struct RoleConfig {
    pub command: Vec<String>,
    #[serde(default)]
    pub stdin: Option<String>,
}

impl ByomConfig {
    pub fn load(project: impl AsRef<Path>) -> Result<Self> {
        let path = project.as_ref().join(CONFIG_FILE);
        let text = fs::read_to_string(&path).map_err(|e| {
            VivariumError::Validation(format!("no puedo leer {}: {e}", path.display()))
        })?;
        let cfg: Self = toml::from_str(&text)?;
        cfg.validate()?;
        Ok(cfg)
    }

    pub fn role(&self, role: Role) -> Result<&RoleConfig> {
        self.roles
            .get(role.as_str())
            .ok_or_else(|| VivariumError::Validation(format!("falta [roles.{}]", role.as_str())))
    }

    pub fn validate(&self) -> Result<()> {
        if self.version != 1 {
            return Err(VivariumError::Validation(format!(
                "config BYOM version={} no soportada",
                self.version
            )));
        }
        for role in [Role::Redactora, Role::EditoraMesa, Role::Documentalista] {
            let cfg = self.role(role)?;
            cfg.validate(role)?;
        }
        Ok(())
    }
}

impl RoleConfig {
    fn validate(&self, role: Role) -> Result<()> {
        if self.command.is_empty() {
            return Err(VivariumError::Validation(format!(
                "roles.{}.command no puede estar vacío",
                role.as_str()
            )));
        }
        let passes_prompt = self
            .command
            .iter()
            .any(|part| part.contains("{prompt_file}"))
            || self.stdin.as_deref() == Some("prompt_file");
        if !passes_prompt {
            return Err(VivariumError::Validation(format!(
                "roles.{} debe usar {{prompt_file}} o stdin = \"prompt_file\"",
                role.as_str()
            )));
        }
        if !command_resolves(&self.command[0]) {
            return Err(VivariumError::EnvironmentIncomplete(format!(
                "no encuentro el binario del rol {}: {}",
                role.as_str(),
                self.command[0]
            )));
        }
        Ok(())
    }
}

#[derive(Debug, Clone)]
pub struct DispatchRequest {
    pub step: String,
    pub chapter: Option<String>,
    pub role: Role,
    pub detail: String,
}

#[derive(Debug, Clone)]
pub struct DispatchResult {
    pub prompt_file: PathBuf,
    pub status_code: Option<i32>,
    pub stdout: String,
    pub stderr: String,
}

pub fn dispatch(
    project: impl AsRef<Path>,
    config: &ByomConfig,
    request: &DispatchRequest,
) -> Result<DispatchResult> {
    let project = project.as_ref();
    let role_config = config.role(request.role)?;
    let prompt = write_task_file(project, request)?;
    let argv = render_argv(
        &role_config.command,
        &prompt,
        project,
        request.chapter.as_deref(),
    );
    let mut command = Command::new(&argv[0]);
    command.args(&argv[1..]).current_dir(project);
    if role_config.stdin.as_deref() == Some("prompt_file") {
        command.stdin(Stdio::from(File::open(&prompt)?));
    }
    let output = command.output().map_err(|e| {
        VivariumError::Dispatch(format!(
            "no puedo ejecutar rol {} ({}): {e}",
            request.role.as_str(),
            argv[0]
        ))
    })?;
    Ok(DispatchResult {
        prompt_file: prompt,
        status_code: output.status.code(),
        stdout: String::from_utf8_lossy(&output.stdout).to_string(),
        stderr: String::from_utf8_lossy(&output.stderr).to_string(),
    })
}

pub fn write_task_file(project: &Path, request: &DispatchRequest) -> Result<PathBuf> {
    let tasks = project.join(".vivarium/tasks");
    fs::create_dir_all(&tasks)?;
    let chapter = request.chapter.as_deref().unwrap_or("global");
    let filename = format!(
        "{}-{}-{}.md",
        chrono::Utc::now().timestamp_nanos_opt().unwrap_or_default(),
        sanitize(&request.step),
        sanitize(chapter)
    );
    let path = tasks.join(filename);
    let body = format!(
        "# Vivarium task\n\nstep: {}\nchapter: {}\nrole: {}\nproject_dir: {}\n\n{}\n",
        request.step,
        request.chapter.as_deref().unwrap_or("global"),
        request.role.as_str(),
        project.display(),
        request.detail
    );
    fs::write(&path, body)?;
    Ok(path)
}

pub fn example_config() -> &'static str {
    r#"# .vivarium/config.toml
version = 1

# Opcional: intérprete Python del sidecar. Precedencia:
# VIVARIUM_PYTHON (env) > [python].interpreter > python3 del PATH.
# [python]
# interpreter = "/usr/local/bin/python3"

[roles.redactora]
command = ["claude", "-p", "@{prompt_file}", "--permission-mode", "acceptEdits"]

[roles.editora_mesa]
command = ["codex", "exec", "--cd", "{project_dir}", "-"]
stdin = "prompt_file"

[roles.documentalista]
command = ["codex", "exec", "--cd", "{project_dir}", "{prompt_file}"]
"#
}

fn render_argv(
    template: &[String],
    prompt: &Path,
    project: &Path,
    chapter: Option<&str>,
) -> Vec<String> {
    let prompt = prompt.to_string_lossy();
    let project = project.to_string_lossy();
    let chapter = chapter.unwrap_or("");
    template
        .iter()
        .map(|part| {
            part.replace("{prompt_file}", &prompt)
                .replace("{project_dir}", &project)
                .replace("{chapter}", chapter)
        })
        .collect()
}

pub(crate) fn command_resolves(command: &str) -> bool {
    let path = Path::new(command);
    if path.components().count() > 1 {
        return path.exists();
    }
    env::var_os("PATH")
        .map(|paths| env::split_paths(&paths).any(|p| p.join(command).is_file()))
        .unwrap_or(false)
}

fn sanitize(value: &str) -> String {
    value
        .chars()
        .map(|c| if c.is_ascii_alphanumeric() { c } else { '-' })
        .collect()
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn valida_config_minima_con_binario_absoluto() {
        let sh = if Path::new("/bin/sh").exists() {
            "/bin/sh"
        } else {
            "/usr/bin/sh"
        };
        let toml = format!(
            r#"
version = 1
[roles.redactora]
command = ["{sh}", "{{prompt_file}}"]
[roles.editora_mesa]
command = ["{sh}", "{{prompt_file}}"]
[roles.documentalista]
command = ["{sh}", "{{prompt_file}}"]
"#
        );
        let cfg: ByomConfig = toml::from_str(&toml).unwrap();
        cfg.validate().unwrap();
    }
}
