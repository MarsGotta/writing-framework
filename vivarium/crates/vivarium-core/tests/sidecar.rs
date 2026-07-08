use std::fs;
use std::path::{Path, PathBuf};

#[test]
fn status_py_json_del_fixture_real_deserializa() {
    let tmp = tempfile::tempdir().unwrap();
    let project = tmp.path().join("project");
    copy_dir(
        &repo_root().join("tests/fixtures/003-factualidad/project"),
        &project,
    );
    let scripts = project.join(".specify/presets/writeonmars/scripts");
    fs::create_dir_all(&scripts).unwrap();
    fs::copy(
        repo_root().join("writeonmars/scripts/status.py"),
        scripts.join("status.py"),
    )
    .unwrap();

    let status = vivarium_core::sidecar::run_status(&project).unwrap();
    assert_eq!(status.chapters_expected, 3);
    assert_eq!(status.by_chapter.len(), 3);
    assert!(status.by_chapter["1"].drafted);
    assert!(matches!(
        status.next_step.as_str(),
        "setup"
            | "constitution"
            | "specify"
            | "research"
            | "plan"
            | "implement"
            | "review"
            | "revise"
            | "close"
    ));
}

fn repo_root() -> PathBuf {
    PathBuf::from(env!("CARGO_MANIFEST_DIR"))
        .ancestors()
        .nth(3)
        .unwrap()
        .to_path_buf()
}

fn copy_dir(src: &Path, dst: &Path) {
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
