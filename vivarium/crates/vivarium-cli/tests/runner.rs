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
fn estudio_con_capitulos_pendientes_espera_write() {
    let tmp = tempfile::tempdir().unwrap();
    let project = common::project_with_preset(tmp.path(), "estudio", Some("tecnologia"));

    common::vivarium_cmd()
        .args(["step", "--project", project.to_str().unwrap()])
        .assert()
        .code(10);

    assert!(!project.join("chapters").exists());
    let decisions = fs::read_to_string(project.join("decisions.jsonl")).unwrap();
    assert!(decisions.contains(r#""event":"checkpoint""#));
    assert!(decisions.contains(r#""step":"write""#));
    assert!(!decisions.contains(r#""event":"dispatch""#));
}

#[test]
fn estudio_con_hallazgos_espera_dispose() {
    let tmp = tempfile::tempdir().unwrap();
    let project = common::project_with_preset(tmp.path(), "estudio", Some("tecnologia"));
    write_known_chapter(&project);
    write_findings_for_one(&project, true, true);

    common::vivarium_cmd()
        .args(["step", "--project", project.to_str().unwrap()])
        .assert()
        .code(10);

    let decisions = fs::read_to_string(project.join("decisions.jsonl")).unwrap();
    assert!(decisions.contains(r#""step":"dispose""#));
    assert!(!decisions.contains(r#""step":"revise""#));
}

#[test]
fn estudio_global_sin_readme_espera_intro_humano() {
    let tmp = tempfile::tempdir().unwrap();
    let project = common::project_with_preset(tmp.path(), "estudio", Some("tecnologia"));
    fs::write(
        project.join("specs/001-demo/plan.md"),
        "# Plan\n\n## Temario\n\n| # | Titulo | Promesa |\n|---|--------|---------|\n| 1 | Uno | A |\n",
    )
    .unwrap();
    write_known_chapter(&project);
    write_findings_for_one(&project, false, true);

    common::vivarium_cmd()
        .args(["step", "--project", project.to_str().unwrap()])
        .assert()
        .code(10);

    let decisions = fs::read_to_string(project.join("decisions.jsonl")).unwrap();
    assert!(decisions.contains(r#""step":"intro""#));
    assert!(!decisions.contains(r#""step":"intro","chapter":"global","role":"redactora""#));
}

#[test]
fn corta_sin_readme_despacha_export_nunca_intro() {
    // Pista corta con la pieza escrita y revisada (pasadas 1-4 + 5), sin
    // README.md: el ejecutor salta `intro` y despacha `export`. Único cambio de
    // comportamiento del ejecutor (T020).
    let tmp = tempfile::tempdir().unwrap();
    let project = common::project_with_preset(tmp.path(), "produccion", Some("tecnologia"));
    make_corta(&project);
    write_known_chapter(&project);
    write_findings_for_one(&project, false, true);

    common::vivarium_cmd()
        .args(["run", "--project", project.to_str().unwrap()])
        .assert()
        .code(10); // se detiene en el checkpoint humano `feedback`

    assert!(project.join("demo.pdf").is_file());
    assert!(!project.join("README.md").exists());
    let dispatches = dispatch_keys(&project);
    assert!(
        dispatches.contains(&"export:global".to_string()),
        "debe despachar export: {dispatches:?}"
    );
    assert!(
        !dispatches.iter().any(|d| d.starts_with("intro")),
        "corta no debe despachar intro: {dispatches:?}"
    );
}

#[test]
fn corta_combinada_despacha_review4_documentalista() {
    // La combinada registra 1·2·3·5 en un run; el ejecutor (sin cambios en
    // choose_review_action) encuentra la pasada 4 ausente y la despacha a la
    // documentalista, nunca la 2 ni la 3.
    let tmp = tempfile::tempdir().unwrap();
    let project = common::project_with_preset(tmp.path(), "produccion", Some("tecnologia"));
    make_corta(&project);
    write_known_chapter(&project);
    write_combined_pass(&project);

    common::vivarium_cmd()
        .args(["step", "--project", project.to_str().unwrap()])
        .assert()
        .success();

    let dispatches = dispatch_keys(&project);
    assert_eq!(
        dispatches,
        vec!["review-4:1".to_string()],
        "el único despacho tras la combinada debe ser review-4: {dispatches:?}"
    );
    let decisions = fs::read_to_string(project.join("decisions.jsonl")).unwrap();
    assert!(decisions.contains(r#""step":"review-4""#));
    assert!(decisions.contains(r#""role":"documentalista""#));
    assert!(!decisions.contains(r#""step":"review-2""#));
    assert!(!decisions.contains(r#""step":"review-3""#));
}

/// Convierte el proyecto del preset en pista corta: temario de una fila
/// (`chapters_expected == 1`) y `track: corta` en el manifiesto.
fn make_corta(project: &std::path::Path) {
    fs::write(
        project.join("specs/001-demo/plan.md"),
        "# Plan\n\n## Temario\n\n| # | Titulo | Promesa |\n|---|--------|---------|\n| 1 | Uno | A |\n",
    )
    .unwrap();
    let manifest_path = project.join(".writeonmars-manifest.json");
    let mut manifest: serde_json::Value =
        serde_json::from_str(&fs::read_to_string(&manifest_path).unwrap()).unwrap();
    manifest["track"] = serde_json::Value::String("corta".to_string());
    fs::write(
        &manifest_path,
        serde_json::to_string_pretty(&manifest).unwrap(),
    )
    .unwrap();
}

/// La pasada combinada de pista corta: bloques 1·2·3 (capítulo 1) + 5 (global)
/// en un único `findings.md`, sin la pasada 4 (precisión, relevo aparte).
fn write_combined_pass(project: &std::path::Path) {
    let hash = "6107a3a4e12a9d55ea3365dc69783c8bb3f565cf7eaf4f8c39c9ea3f5099ddaa";
    let mut text = String::from("# Findings\n\n");
    for pass in [1, 2, 3] {
        text.push_str(&format!(
            "## Pasada {pass} - Combinada\n\n\
<!-- pass-output-schema: v1.2 -->\n\n\
**Estado pasada**: passed\n\
**Capítulos cubiertos**: [1]\n\
**Firma**:\n  - tipo: autonomous\n  - actor: mesa-stub\n\n\
### Hallazgos\n\n\
| ID | Capítulo | Severidad | Frase | Problema | Reescritura | Estado | Citas |\n\
|----|----------|-----------|-------|----------|-------------|--------|-------|\n\
\n<!-- huellas: {{\"1\": \"{hash}\"}} -->\n\n",
        ));
    }
    text.push_str(
        "## Pasada 5 - Combinada\n\n\
<!-- pass-output-schema: v1.2 -->\n\n\
**Estado pasada**: passed\n\
**Capítulos cubiertos**: global\n\
**Firma**:\n  - tipo: autonomous\n  - actor: mesa-stub\n\n\
### Hallazgos\n\n\
| ID | Capítulo | Severidad | Frase | Problema | Reescritura | Estado | Citas |\n\
|----|----------|-----------|-------|----------|-------------|--------|-------|\n\n\
<!-- huellas: {\"global\": \"placeholder\"} -->\n",
    );
    fs::write(project.join("specs/001-demo/findings.md"), text).unwrap();
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

fn write_known_chapter(project: &std::path::Path) {
    fs::create_dir_all(project.join("chapters")).unwrap();
    fs::write(
        project.join("chapters/001-uno-humano.md"),
        "# Uno humano\n\nTexto humano del capítulo uno.\n\n## Fuentes\n\n- Fuente A\n",
    )
    .unwrap();
}

fn write_findings_for_one(project: &std::path::Path, open: bool, include_global: bool) {
    let hash = "6107a3a4e12a9d55ea3365dc69783c8bb3f565cf7eaf4f8c39c9ea3f5099ddaa";
    let row = if open {
        "| F-1.1 | 1 | medio | frase | problema | propuesta | abierto | [] |\n"
    } else {
        ""
    };
    let mut text = String::from("# Findings\n\n");
    for pass in 1..=4 {
        text.push_str(&format!(
            "## Pasada {pass} - Stub\n\n\
<!-- pass-output-schema: v1.2 -->\n\n\
**Estado pasada**: passed\n\
**Capítulos cubiertos**: [1]\n\
**Firma**:\n  - tipo: autonomous\n  - actor: stub\n\n\
### Hallazgos\n\n\
| ID | Capítulo | Severidad | Frase | Problema | Reescritura | Estado | Citas |\n\
|----|----------|-----------|-------|----------|-------------|--------|-------|\n\
{}\
\n<!-- huellas: {{\"1\": \"{hash}\"}} -->\n\n",
            if pass == 1 { row } else { "" }
        ));
    }
    if include_global {
        text.push_str(
            "## Pasada 5 - Stub\n\n\
<!-- pass-output-schema: v1.2 -->\n\n\
**Estado pasada**: passed\n\
**Capítulos cubiertos**: global\n\
**Firma**:\n  - tipo: autonomous\n  - actor: stub\n\n\
### Hallazgos\n\n\
| ID | Capítulo | Severidad | Frase | Problema | Reescritura | Estado | Citas |\n\
|----|----------|-----------|-------|----------|-------------|--------|-------|\n\n\
<!-- huellas: {\"global\": \"placeholder\"} -->\n",
        );
    }
    fs::write(project.join("specs/001-demo/findings.md"), text).unwrap();
}
