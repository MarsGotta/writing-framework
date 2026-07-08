mod common;

use std::collections::HashSet;
use std::fs;

#[test]
fn run_completa_tres_capitulos_y_se_detiene_en_checkpoint_pdf() {
    let tmp = tempfile::tempdir().unwrap();
    let project = common::project_with_preset(tmp.path(), "produccion", Some("tecnologia"));

    common::vivarium_cmd()
        .env("VIVARIUM_STUB_DOC_REVISE_ONCE", "1")
        .args(["run", "--project", project.to_str().unwrap()])
        .assert()
        .code(10);

    for n in 1..=3 {
        assert!(project
            .join(format!("chapters/{n:02}-capitulo-{n}.md"))
            .is_file());
    }
    assert!(project.join("README.md").is_file());
    assert!(project.join("demo.pdf").is_file());

    let dispatches = dispatch_keys(&project);
    let unique: HashSet<_> = dispatches.iter().cloned().collect();
    assert_eq!(
        dispatches.len(),
        unique.len(),
        "despachos duplicados: {dispatches:?}"
    );
    assert!(dispatches.contains(&"review-5:global".to_string()));
    assert!(dispatches.contains(&"intro:global".to_string()));
    assert!(dispatches.contains(&"export:global".to_string()));
}

#[test]
fn agente_que_falla_registra_disposition_failed_y_no_escribe_capitulo() {
    let tmp = tempfile::tempdir().unwrap();
    let project = common::project_with_preset(tmp.path(), "produccion", Some("tecnologia"));
    let fail = common::stubs_dir().join("fail-stub.sh");
    fs::write(
        project.join(".vivarium/config.toml"),
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
            fail.display(),
            fail.display(),
            fail.display()
        ),
    )
    .unwrap();

    common::vivarium_cmd()
        .args(["step", "--project", project.to_str().unwrap()])
        .assert()
        .code(12);

    assert!(!project.join("chapters/01-capitulo-1.md").exists());
    let decisions = fs::read_to_string(project.join("decisions.jsonl")).unwrap();
    assert!(decisions.contains(r#""outcome":"failed""#));
}

#[test]
fn segunda_config_byom_corre_el_mismo_ciclo() {
    let tmp = tempfile::tempdir().unwrap();
    let project = common::project_with_preset(tmp.path(), "produccion", Some("tecnologia"));
    common::write_config(&project, true);

    common::vivarium_cmd()
        .args(["run", "--project", project.to_str().unwrap()])
        .assert()
        .code(10);

    assert!(project.join("chapters/03-capitulo-3.md").is_file());
    assert!(project.join("demo.pdf").is_file());
}

#[test]
fn estudio_bloquea_redaccion_de_manuscrito() {
    let tmp = tempfile::tempdir().unwrap();
    let project = common::project_with_preset(tmp.path(), "estudio", Some("tecnologia"));

    common::vivarium_cmd()
        .args(["step", "--project", project.to_str().unwrap()])
        .assert()
        .code(11);

    assert!(!project.join("chapters").exists());
    let decisions = fs::read_to_string(project.join("decisions.jsonl")).unwrap();
    assert!(!decisions.contains(r#""event":"dispatch""#));
}

fn dispatch_keys(project: &std::path::Path) -> Vec<String> {
    fs::read_to_string(project.join("decisions.jsonl"))
        .unwrap()
        .lines()
        .filter_map(|line| serde_json::from_str::<serde_json::Value>(line).ok())
        .filter(|value| value["event"] == "dispatch")
        .map(|value| {
            format!(
                "{}:{}",
                value["step"].as_str().unwrap(),
                value["chapter"].as_str().unwrap_or("global")
            )
        })
        .collect()
}
