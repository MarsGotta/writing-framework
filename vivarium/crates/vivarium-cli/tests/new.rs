mod common;

use std::fs;
use std::process::Command as StdCommand;

use predicates::prelude::*;

#[test]
fn new_guia_crea_proyecto_produccion_operativo() {
    let tmp = tempfile::tempdir().unwrap();
    let project = tmp.path().join("guia");
    let preset = common::repo_root().join("writeonmars");
    common::vivarium_cmd()
        .args([
            "new",
            project.to_str().unwrap(),
            "--kind",
            "guia",
            "--preset",
            preset.to_str().unwrap(),
            "--operator",
            "test",
            "--email",
            "test@example.com",
        ])
        .assert()
        .success()
        .stdout(predicate::str::contains("proyecto creado"));

    let manifest: serde_json::Value = serde_json::from_str(
        &fs::read_to_string(project.join(".writeonmars-manifest.json")).unwrap(),
    )
    .unwrap();
    assert_eq!(manifest["mode"], "produccion");
    assert_eq!(manifest["sector"], "tecnologia");
    assert!(project.join("roots/README.md").is_file());
    assert!(project.join("decisions.jsonl").is_file());
    assert!(project.join(".vivarium/config.toml.example").is_file());
    assert!(project
        .join(".specify/presets/writeonmars/scripts/status.py")
        .is_file());

    let git = StdCommand::new("git")
        .args([
            "-C",
            project.to_str().unwrap(),
            "rev-parse",
            "--verify",
            "HEAD",
        ])
        .output()
        .unwrap();
    assert!(git.status.success(), "git rev-parse falló: {:?}", git);
}

#[test]
fn new_novela_default_estudio() {
    let tmp = tempfile::tempdir().unwrap();
    let project = tmp.path().join("novela");
    let preset = common::repo_root().join("writeonmars");
    common::vivarium_cmd()
        .args([
            "new",
            project.to_str().unwrap(),
            "--kind",
            "novela",
            "--preset",
            preset.to_str().unwrap(),
        ])
        .assert()
        .success();

    let manifest: serde_json::Value = serde_json::from_str(
        &fs::read_to_string(project.join(".writeonmars-manifest.json")).unwrap(),
    )
    .unwrap();
    assert_eq!(manifest["mode"], "estudio");
}

#[test]
fn manifest_sin_mode_se_lee_como_produccion() {
    let tmp = tempfile::tempdir().unwrap();
    let project = tmp.path().join("legacy");
    let preset = common::repo_root().join("writeonmars");
    common::vivarium_cmd()
        .args([
            "new",
            project.to_str().unwrap(),
            "--kind",
            "guia",
            "--preset",
            preset.to_str().unwrap(),
        ])
        .assert()
        .success();
    let manifest_path = project.join(".writeonmars-manifest.json");
    let mut manifest: serde_json::Value =
        serde_json::from_str(&fs::read_to_string(&manifest_path).unwrap()).unwrap();
    manifest.as_object_mut().unwrap().remove("mode");
    fs::write(
        &manifest_path,
        serde_json::to_string_pretty(&manifest).unwrap(),
    )
    .unwrap();

    let output = common::vivarium_cmd()
        .args(["status", "--project", project.to_str().unwrap(), "--json"])
        .assert()
        .success()
        .get_output()
        .stdout
        .clone();
    let status: serde_json::Value = serde_json::from_slice(&output).unwrap();
    assert_eq!(status["mode"], "produccion");
}

#[test]
fn new_es_idempotente() {
    let tmp = tempfile::tempdir().unwrap();
    let project = tmp.path().join("guia");
    let preset = common::repo_root().join("writeonmars");
    for _ in 0..2 {
        common::vivarium_cmd()
            .args([
                "new",
                project.to_str().unwrap(),
                "--kind",
                "guia",
                "--preset",
                preset.to_str().unwrap(),
            ])
            .assert()
            .success();
    }
    assert!(project.join("roots/README.md").is_file());
}
