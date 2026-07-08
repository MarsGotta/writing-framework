mod common;

use std::fs;

#[test]
fn mode_set_sin_yes_no_aplica_y_sale_4() {
    let tmp = tempfile::tempdir().unwrap();
    let project = common::project_with_preset(tmp.path(), "estudio", Some("tecnologia"));

    common::vivarium_cmd()
        .args([
            "mode",
            "set",
            "produccion",
            "--project",
            project.to_str().unwrap(),
        ])
        .assert()
        .code(4);

    let manifest: serde_json::Value = serde_json::from_str(
        &fs::read_to_string(project.join(".writeonmars-manifest.json")).unwrap(),
    )
    .unwrap();
    assert_eq!(manifest["mode"], "estudio");
}

#[test]
fn mode_set_con_yes_actualiza_manifest_y_decisions() {
    let tmp = tempfile::tempdir().unwrap();
    let project = common::project_with_preset(tmp.path(), "estudio", Some("tecnologia"));

    common::vivarium_cmd()
        .args([
            "mode",
            "set",
            "produccion",
            "--project",
            project.to_str().unwrap(),
            "--yes",
        ])
        .assert()
        .success();

    let manifest: serde_json::Value = serde_json::from_str(
        &fs::read_to_string(project.join(".writeonmars-manifest.json")).unwrap(),
    )
    .unwrap();
    assert_eq!(manifest["mode"], "produccion");
    assert_eq!(manifest["mode_history"][0]["from"], "estudio");
    assert_eq!(manifest["mode_history"][0]["to"], "produccion");
    assert!(manifest["mode_history"][0]["date"]
        .as_str()
        .unwrap()
        .contains('T'));

    let decisions = fs::read_to_string(project.join("decisions.jsonl")).unwrap();
    assert!(decisions.contains(r#""event":"mode_change""#));
    assert!(decisions.contains("estudio"));
    assert!(decisions.contains("produccion"));
}
