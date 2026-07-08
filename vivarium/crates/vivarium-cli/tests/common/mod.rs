#![allow(dead_code)]

use std::fs;
use std::path::{Path, PathBuf};

use assert_cmd::Command;

pub fn repo_root() -> PathBuf {
    PathBuf::from(env!("CARGO_MANIFEST_DIR"))
        .ancestors()
        .nth(3)
        .unwrap()
        .to_path_buf()
}

pub fn stubs_dir() -> PathBuf {
    PathBuf::from(env!("CARGO_MANIFEST_DIR")).join("tests/stubs")
}

pub fn vivarium_cmd() -> Command {
    let mut cmd = Command::cargo_bin("vivarium").unwrap();
    let path = std::env::var("PATH").unwrap_or_default();
    cmd.env("PATH", format!("{}:{path}", stubs_dir().display()));
    cmd
}

pub fn project_with_preset(root: &Path, mode: &str, sector: Option<&str>) -> PathBuf {
    let project = root.join("project");
    fs::create_dir_all(project.join(".specify/presets/writeonmars")).unwrap();
    fs::create_dir_all(project.join(".specify/memory")).unwrap();
    fs::create_dir_all(project.join(".vivarium")).unwrap();
    fs::create_dir_all(project.join("specs/001-demo")).unwrap();
    copy_dir(
        &repo_root().join("writeonmars"),
        &project.join(".specify/presets/writeonmars"),
    );
    fs::write(
        project.join(".specify/memory/constitution.md"),
        "# Constitucion\n\n**Version**: 1.6.0\n",
    )
    .unwrap();
    let mut manifest = serde_json::json!({
        "framework_version": "0.1.0",
        "constitution_version": "1.6.0",
        "agent_target": "claude-code",
        "language_primary": "es",
        "skills": [{"name":"x","version":"1.0.0","source":"bundled"}],
        "research_mode": "byom",
        "signing_matrix": {
            "pasada_1_estructura": "autonomous",
            "pasada_2_utilidad": "autonomous",
            "pasada_3_naturalidad": "autonomous",
            "pasada_4_precision": "autonomous",
            "pasada_5_formato": "autonomous"
        },
        "human_operators": [{"id":"test","role":"author"}],
        "citation_contract_version": "1.0",
        "project_type": "editorial",
        "mode": mode,
        "sector": sector
    });
    if sector.is_none() {
        manifest["sector"] = serde_json::Value::Null;
    }
    fs::write(
        project.join(".writeonmars-manifest.json"),
        serde_json::to_string_pretty(&manifest).unwrap(),
    )
    .unwrap();
    fs::write(project.join("decisions.jsonl"), "").unwrap();
    fs::write(
        project.join("specs/001-demo/spec.md"),
        "# Feature Specification: Demo\n\nBrief firmado.\n",
    )
    .unwrap();
    fs::write(
        project.join("specs/001-demo/research.md"),
        "# Research\n\nFuentes.\n",
    )
    .unwrap();
    fs::write(
        project.join("specs/001-demo/plan.md"),
        "# Plan\n\n## Temario\n\n| # | Titulo | Promesa |\n|---|--------|---------|\n| 1 | Uno | A |\n| 2 | Dos | B |\n| 3 | Tres | C |\n",
    )
    .unwrap();
    write_config(&project, false);
    stub_export(&project);
    project
}

pub fn write_config(project: &Path, shell_wrapped: bool) {
    let red = stubs_dir().join("redactora-stub.sh");
    let mesa = stubs_dir().join("mesa-stub.sh");
    let doc = stubs_dir().join("doc-stub.sh");
    let text = if shell_wrapped {
        format!(
            r#"
version = 1
[roles.redactora]
command = ["/bin/sh", "{}", "{{prompt_file}}"]
[roles.editora_mesa]
command = ["/bin/sh", "{}", "{{prompt_file}}"]
[roles.documentalista]
command = ["/bin/sh", "{}", "{{prompt_file}}"]
"#,
            red.display(),
            mesa.display(),
            doc.display()
        )
    } else {
        format!(
            r#"
version = 1
[roles.redactora]
command = ["{}", "{{prompt_file}}"]
[roles.editora_mesa]
command = ["{}", "{{prompt_file}}"]
[roles.documentalista]
command = ["{}", "{{prompt_file}}"]
"#,
            red.display(),
            mesa.display(),
            doc.display()
        )
    };
    fs::write(project.join(".vivarium/config.toml"), text).unwrap();
}

pub fn stub_export(project: &Path) {
    fs::write(
        project.join(".specify/presets/writeonmars/scripts/export.py"),
        "from pathlib import Path\nPath('demo.pdf').write_bytes(b'%PDF-1.4\\n')\n",
    )
    .unwrap();
}

pub fn copy_dir(src: &Path, dst: &Path) {
    fs::create_dir_all(dst).unwrap();
    for entry in fs::read_dir(src).unwrap() {
        let entry = entry.unwrap();
        let from = entry.path();
        let to = dst.join(entry.file_name());
        if from.is_dir() {
            copy_dir(&from, &to);
        } else {
            fs::copy(&from, &to).unwrap();
        }
    }
}
