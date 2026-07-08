use std::fs::{self, OpenOptions};
use std::path::{Path, PathBuf};
use std::process::Command;

use fd_lock::RwLock;

use crate::decisions::{self, DecisionEvent, Outcome};
use crate::dispatch::{self, DispatchRequest, Role};
use crate::error::{Result, VivariumError};
use crate::manifest::{self, Mode};
use crate::sidecar::{self, Status};

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum StepResult {
    Progress(String),
    Complete(String),
    BlockedByMode(String),
}

impl StepResult {
    pub fn exit_code(&self) -> i32 {
        match self {
            StepResult::Progress(_) | StepResult::Complete(_) => 0,
            StepResult::BlockedByMode(_) => 11,
        }
    }

    pub fn message(&self) -> &str {
        match self {
            StepResult::Progress(msg)
            | StepResult::Complete(msg)
            | StepResult::BlockedByMode(msg) => msg,
        }
    }
}

#[derive(Debug, Clone)]
struct Action {
    step: String,
    chapter: Option<String>,
    role: Role,
    detail: String,
    kind: ActionKind,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
enum ActionKind {
    Agent,
    Sidecar,
}

/// Resultado del planificador puro: qué haría el runner con este estado.
/// Separado de la ejecución para que `vivarium status` pueda consultarlo sin
/// efectos laterales (mismo predicado para status y para step/run).
#[derive(Debug, Clone)]
enum Planned {
    Act(Action),
    Checkpoint {
        step: &'static str,
        detail: &'static str,
        message: &'static str,
    },
    Done(String),
}

pub fn step(project: impl AsRef<Path>) -> Result<StepResult> {
    with_lock(project.as_ref(), || step_unlocked(project.as_ref()))
}

pub fn run(project: impl AsRef<Path>) -> Result<StepResult> {
    with_lock(project.as_ref(), || {
        for _ in 0..100 {
            let result = step_unlocked(project.as_ref())?;
            match result {
                StepResult::Progress(_) => continue,
                other => return Ok(other),
            }
        }
        Err(VivariumError::Dispatch(
            "run alcanzó 100 pasos sin bloquearse ni cerrar".to_string(),
        ))
    })
}

pub fn check(project: impl AsRef<Path>) -> Result<()> {
    let project = project.as_ref();
    manifest::load_project(project)?;
    sidecar::validate_manifest(project)?;
    sidecar::run_status(project)?;
    dispatch::ByomConfig::load(project)?;
    Ok(())
}

/// Predicado compartido runner/status: ¿el plan actual quedaría bloqueado por
/// `mode: estudio`? Evalúa la acción sintetizada (no el `next_step` crudo),
/// así cubre también implement/revise derivados de un `close` incompleto.
pub fn blocked_by_mode(project: impl AsRef<Path>, status: &Status) -> Result<bool> {
    let project = project.as_ref();
    if manifest::load_project(project)?.mode() != Mode::Estudio {
        return Ok(false);
    }
    match plan_action(project, status)? {
        Planned::Act(action) => Ok(writes_manuscript(&action)),
        Planned::Checkpoint { .. } | Planned::Done(_) => Ok(false),
    }
}

fn step_unlocked(project: &Path) -> Result<StepResult> {
    decisions::ensure(project)?;
    let status = sidecar::run_status(project)?;
    reconcile_in_flight(project, &status)?;
    match plan_action(project, &status)? {
        Planned::Done(msg) => Ok(StepResult::Complete(msg)),
        Planned::Checkpoint {
            step,
            detail,
            message,
        } => {
            decisions::append_checkpoint_once(project, step, detail)?;
            Err(VivariumError::Checkpoint(message.to_string()))
        }
        Planned::Act(action) => {
            let mode = manifest::load_project(project)?.mode();
            if mode == Mode::Estudio && writes_manuscript(&action) {
                return Ok(StepResult::BlockedByMode(format!(
                    "mode=estudio prohíbe despachar {} {}",
                    action.step,
                    action.chapter.as_deref().unwrap_or("global")
                )));
            }
            match action.kind {
                ActionKind::Agent => run_agent_action(project, &action, &status),
                ActionKind::Sidecar => run_sidecar_action(project, &action),
            }
        }
    }
}

fn implement_action(chapter: &str) -> Action {
    Action {
        step: "implement".to_string(),
        chapter: Some(chapter.to_string()),
        role: Role::Redactora,
        detail: format!("Ejecutar speckit.implement para el capítulo {chapter}."),
        kind: ActionKind::Agent,
    }
}

fn revise_action(chapter: &str) -> Action {
    Action {
        step: "revise".to_string(),
        chapter: Some(chapter.to_string()),
        role: Role::Redactora,
        detail: format!("Aplicar hallazgos accionables del capítulo {chapter}."),
        kind: ActionKind::Agent,
    }
}

fn plan_action(project: &Path, status: &Status) -> Result<Planned> {
    // status.py puede decir "close" con capítulos aún incompletos (va por
    // delante del trabajo en vuelo): normaliza al paso por capítulo pendiente.
    if status.next_step == "close" && !status.all_chapters_approved {
        if let Some(chapter) = first_chapter(status, |c| !c.drafted) {
            if is_estudio(status) {
                return Ok(checkpoint_write());
            }
            return Ok(Planned::Act(implement_action(&chapter)));
        }
        if let Some(chapter) = first_revise_chapter(status) {
            if is_estudio(status) {
                return Ok(checkpoint_dispose());
            }
            return Ok(Planned::Act(revise_action(&chapter)));
        }
        if let Some(action) = choose_review_action(status)? {
            return Ok(Planned::Act(action));
        }
    }
    match status.next_step.as_str() {
        "setup" => Ok(Planned::Act(Action {
            step: "setup".to_string(),
            chapter: None,
            role: Role::Sidecar,
            detail: "Ejecutar bootstrap.py para materializar constitución y manifest.".to_string(),
            kind: ActionKind::Sidecar,
        })),
        "constitution" => Ok(Planned::Act(Action {
            step: "constitution".to_string(),
            chapter: None,
            role: Role::Documentalista,
            detail: "Configurar adendas del proyecto desde el sector declarado.".to_string(),
            kind: ActionKind::Agent,
        })),
        "specify" => Ok(Planned::Checkpoint {
            step: "specify",
            detail: "brief firmado por la operadora",
            message: "checkpoint humano: falta brief/spec.md firmado",
        }),
        "research" => Ok(Planned::Act(Action {
            step: "research".to_string(),
            chapter: None,
            role: Role::Documentalista,
            detail: "Ejecutar speckit.research y escribir research.md con fuentes.".to_string(),
            kind: ActionKind::Agent,
        })),
        "plan" => Ok(Planned::Act(Action {
            step: "plan".to_string(),
            chapter: None,
            role: Role::Redactora,
            detail: "Ejecutar speckit.plan y materializar el temario.".to_string(),
            kind: ActionKind::Agent,
        })),
        "implement" => Ok(match first_chapter(status, |c| !c.drafted) {
            Some(chapter) => Planned::Act(implement_action(&chapter)),
            None => Planned::Done("no hay capítulos pendientes de redacción".to_string()),
        }),
        "write" => Ok(checkpoint_write()),
        "review" => Ok(match choose_review_action(status)? {
            Some(action) => Planned::Act(action),
            None => Planned::Done("no hay pasadas locales pendientes".to_string()),
        }),
        "revise" => Ok(match first_revise_chapter(status) {
            Some(chapter) => Planned::Act(revise_action(&chapter)),
            None => Planned::Done("no hay revisiones pendientes".to_string()),
        }),
        "dispose" => Ok(checkpoint_dispose()),
        "close" => plan_global(project, status),
        other => Err(VivariumError::Validation(format!(
            "next_step desconocido: {other}"
        ))),
    }
}

fn is_estudio(status: &Status) -> bool {
    status.mode.as_deref() == Some("estudio")
}

fn checkpoint_write() -> Planned {
    Planned::Checkpoint {
        step: "write",
        detail: "faltan capítulos por escribir (modo estudio)",
        message: "checkpoint humano: faltan capítulos por escribir (modo estudio)",
    }
}

fn checkpoint_dispose() -> Planned {
    Planned::Checkpoint {
        step: "dispose",
        detail: "hallazgos a la espera de disposición humana (scripts/dispose.py)",
        message:
            "checkpoint humano: hallazgos a la espera de disposición humana (scripts/dispose.py)",
    }
}

fn choose_review_action(status: &Status) -> Result<Option<Action>> {
    let Some(chapter) = first_chapter(status, |c| {
        c.drafted && !c.approved && c.revise_pending == 0
    }) else {
        return Ok(None);
    };
    let c = &status.by_chapter[&chapter];
    for pass in 1..=4u8 {
        if !c.passes_done.contains(&pass) {
            let role = if pass == 4 {
                Role::Documentalista
            } else {
                Role::EditoraMesa
            };
            return Ok(Some(Action {
                step: format!("review-{pass}"),
                chapter: Some(chapter.clone()),
                role,
                detail: format!("Ejecutar pasada {pass} para el capítulo {chapter}."),
                kind: ActionKind::Agent,
            }));
        }
    }
    Ok(None)
}

fn plan_global(project: &Path, status: &Status) -> Result<Planned> {
    if !status.passes.iter().any(|p| p.num == 5) {
        return Ok(Planned::Act(Action {
            step: "review-5".to_string(),
            chapter: Some("global".to_string()),
            role: Role::EditoraMesa,
            detail: "Ejecutar pasada 5 global de formato/coherencia.".to_string(),
            kind: ActionKind::Agent,
        }));
    }
    if !project.join("README.md").is_file() {
        if is_estudio(status) {
            return Ok(Planned::Checkpoint {
                step: "intro",
                detail: "README.md escrito por la humana (modo estudio)",
                message: "checkpoint humano: falta README.md escrito por la humana (modo estudio)",
            });
        }
        return Ok(Planned::Act(Action {
            step: "intro".to_string(),
            chapter: Some("global".to_string()),
            role: Role::Redactora,
            detail: "Generar README.md de presentación antes del export.".to_string(),
            kind: ActionKind::Agent,
        }));
    }
    if !has_pdf(project)? {
        return Ok(Planned::Act(Action {
            step: "export".to_string(),
            chapter: Some("global".to_string()),
            role: Role::Sidecar,
            detail: "Ejecutar export.py para producir el PDF.".to_string(),
            kind: ActionKind::Sidecar,
        }));
    }
    // Checkpoint 2 SIEMPRE, aunque los gates estén en verde (FR-013): la
    // evidencia en disco de que el humano lo atendió es el feedback.md que
    // escribe feedback_intake.py sobre el PDF anotado.
    if spec_file(project, status, "feedback.md").is_none() {
        return Ok(Planned::Checkpoint {
            step: "feedback",
            detail: "PDF anotado por la operadora",
            message: "checkpoint humano: falta PDF anotado/feedback (feedback_intake.py)",
        });
    }
    if status.closeable {
        if already_closed(project)? {
            return Ok(Planned::Done(
                "proyecto ya cerrado (close.py OK)".to_string(),
            ));
        }
        return Ok(Planned::Act(Action {
            step: "close".to_string(),
            chapter: Some("global".to_string()),
            role: Role::Sidecar,
            detail: "Ejecutar close.py: gates en verde, cierre del proyecto.".to_string(),
            kind: ActionKind::Sidecar,
        }));
    }
    // Inalcanzable en la práctica (next_step=close implica closeable), pero si
    // status.py cambiara, mejor esperar que inventar un paso.
    Ok(Planned::Done(
        "feedback recibido; gates aún no en verde (sigue el next_step de status.py)".to_string(),
    ))
}

fn already_closed(project: &Path) -> Result<bool> {
    Ok(decisions::read(project)?.iter().any(|record| {
        record.event == DecisionEvent::Disposition
            && record.step.as_deref() == Some("close")
            && record.outcome == Some(Outcome::Ok)
    }))
}

fn run_agent_action(project: &Path, action: &Action, before: &Status) -> Result<StepResult> {
    let config = dispatch::ByomConfig::load(project)?;
    decisions::append_dispatch(
        project,
        &action.step,
        action.chapter.as_deref(),
        action.role.as_str(),
        Some(action.detail.clone()),
    )?;
    let request = DispatchRequest {
        step: action.step.clone(),
        chapter: action.chapter.clone(),
        role: action.role,
        detail: action.detail.clone(),
    };
    // Un fallo de spawn también cierra el dispatch: sin disposición quedaría
    // un in-flight huérfano que la reconciliación marcaría Failed igualmente,
    // pero con menos contexto del error real.
    let result = match dispatch::dispatch(project, &config, &request) {
        Ok(result) => result,
        Err(err) => {
            decisions::append_disposition(
                project,
                &action.step,
                action.chapter.as_deref(),
                action.role.as_str(),
                Outcome::Failed,
                Some(err.to_string()),
            )?;
            return Err(err);
        }
    };
    if result.status_code != Some(0) {
        decisions::append_disposition(
            project,
            &action.step,
            action.chapter.as_deref(),
            action.role.as_str(),
            Outcome::Failed,
            Some(result.stderr),
        )?;
        return Err(VivariumError::Dispatch(format!(
            "{} falló con {:?}",
            action.step, result.status_code
        )));
    }
    let after = sidecar::run_status(project)?;
    if !effect_satisfied(project, &after, &action.step, action.chapter.as_deref())? {
        decisions::append_disposition(
            project,
            &action.step,
            action.chapter.as_deref(),
            action.role.as_str(),
            Outcome::Failed,
            Some("el efecto esperado no apareció en disco".to_string()),
        )?;
        return Err(VivariumError::Dispatch(format!(
            "{} no produjo el efecto esperado",
            action.step
        )));
    }
    let outcome = if after.revise_pending > before.revise_pending {
        Outcome::Revise
    } else {
        Outcome::Ok
    };
    decisions::append_disposition(
        project,
        &action.step,
        action.chapter.as_deref(),
        action.role.as_str(),
        outcome,
        None,
    )?;
    Ok(StepResult::Progress(format!(
        "despachado {} {}",
        action.step,
        action.chapter.as_deref().unwrap_or("global")
    )))
}

fn run_sidecar_action(project: &Path, action: &Action) -> Result<StepResult> {
    decisions::append_dispatch(
        project,
        &action.step,
        action.chapter.as_deref(),
        action.role.as_str(),
        Some(action.detail.clone()),
    )?;
    let rc = match action.step.as_str() {
        "setup" => run_sidecar_script(project, "bootstrap.py", &[]),
        "export" => run_sidecar_script(project, "export.py", &[]),
        "close" => run_sidecar_script(project, "close.py", &[]),
        other => Err(VivariumError::Validation(format!(
            "sidecar desconocido: {other}"
        ))),
    };
    match rc {
        Ok(()) => {
            let after = sidecar::run_status(project)?;
            if !effect_satisfied(project, &after, &action.step, action.chapter.as_deref())? {
                decisions::append_disposition(
                    project,
                    &action.step,
                    action.chapter.as_deref(),
                    action.role.as_str(),
                    Outcome::Failed,
                    Some("el efecto esperado no apareció en disco".to_string()),
                )?;
                return Err(VivariumError::Dispatch(format!(
                    "{} no produjo el efecto esperado",
                    action.step
                )));
            }
            decisions::append_disposition(
                project,
                &action.step,
                action.chapter.as_deref(),
                action.role.as_str(),
                Outcome::Ok,
                None,
            )?;
            if action.step == "close" {
                Ok(StepResult::Complete(
                    "close.py completado: proyecto cerrado".to_string(),
                ))
            } else {
                Ok(StepResult::Progress(format!(
                    "sidecar {} completado",
                    action.step
                )))
            }
        }
        Err(err) => {
            decisions::append_disposition(
                project,
                &action.step,
                action.chapter.as_deref(),
                action.role.as_str(),
                Outcome::Failed,
                Some(err.to_string()),
            )?;
            Err(err)
        }
    }
}

fn run_sidecar_script(project: &Path, script: &str, extra: &[&str]) -> Result<()> {
    let script_path = sidecar::scripts_dir(project).join(script);
    let output = Command::new(sidecar::resolve_python_for(project))
        .arg(&script_path)
        .args(extra)
        .current_dir(project)
        .output()
        .map_err(|e| {
            VivariumError::EnvironmentIncomplete(format!("no puedo ejecutar {script}: {e}"))
        })?;
    if output.status.success() {
        Ok(())
    } else {
        // Fallo del script = fallo de despacho (exit 12 del contrato): el
        // estado en disco queda intacto y el reintento es seguro.
        Err(VivariumError::Dispatch(format!(
            "{script} falló: {}",
            String::from_utf8_lossy(&output.stderr).trim()
        )))
    }
}

/// Cierra los despachos que quedaron sin disposición (runner interrumpido):
/// efecto en disco → Ok reconciliado; efecto ausente → Failed y re-despacho
/// seguro por el flujo normal. Nunca deja el proyecto bloqueado (FR-006).
fn reconcile_in_flight(project: &Path, status: &Status) -> Result<()> {
    let open = decisions::in_flight(project)?;
    for record in open {
        let step = record.step.as_deref().unwrap_or("");
        let chapter = record.chapter.as_deref();
        let role = record.role.as_deref().unwrap_or("sidecar");
        if effect_satisfied(project, status, step, chapter)? {
            decisions::append_disposition(
                project,
                step,
                chapter,
                role,
                Outcome::Ok,
                Some("reconciliado tras relanzar runner".to_string()),
            )?;
        } else {
            decisions::append_disposition(
                project,
                step,
                chapter,
                role,
                Outcome::Failed,
                Some("interrumpido sin efecto en disco; re-despacho seguro".to_string()),
            )?;
        }
    }
    Ok(())
}

fn effect_satisfied(
    project: &Path,
    status: &Status,
    step: &str,
    chapter: Option<&str>,
) -> Result<bool> {
    let chapter = chapter.unwrap_or("global");
    if step == "setup" {
        return Ok(project.join(".writeonmars-manifest.json").is_file());
    }
    if step == "constitution" {
        let manifest = manifest::load_project(project)?;
        return Ok(!matches!(
            manifest.raw().get("sector"),
            None | Some(serde_json::Value::Null)
        ));
    }
    if step == "research" {
        return Ok(spec_file(project, status, "research.md").is_some());
    }
    if step == "plan" {
        return Ok(status.chapters_expected > 0 || spec_file(project, status, "plan.md").is_some());
    }
    if step == "implement" {
        return Ok(status
            .by_chapter
            .get(chapter)
            .map(|c| c.drafted)
            .unwrap_or(false));
    }
    if let Some(pass) = step
        .strip_prefix("review-")
        .and_then(|s| s.parse::<u8>().ok())
    {
        if pass == 5 {
            return Ok(status.passes.iter().any(|p| p.num == 5));
        }
        return Ok(status
            .by_chapter
            .get(chapter)
            .map(|c| c.passes_done.contains(&pass))
            .unwrap_or(false));
    }
    if step == "revise" {
        return Ok(status
            .by_chapter
            .get(chapter)
            .map(|c| c.revise_pending == 0)
            .unwrap_or(false));
    }
    if step == "intro" {
        return Ok(project.join("README.md").is_file());
    }
    if step == "export" {
        return has_pdf(project);
    }
    if step == "close" {
        return Ok(status.closeable);
    }
    Ok(false)
}

/// Pasos cuya salida es prosa del manuscrito o del PDF publicado. En
/// `mode: estudio` el runner no los despacha jamás (FR-008): `intro` incluido
/// porque el README de presentación acaba embebido en el PDF.
fn writes_manuscript(action: &Action) -> bool {
    matches!(action.step.as_str(), "implement" | "revise" | "intro")
}

fn first_chapter<F>(status: &Status, predicate: F) -> Option<String>
where
    F: Fn(&crate::sidecar::ChapterStatus) -> bool,
{
    let mut keys: Vec<_> = status
        .by_chapter
        .keys()
        .filter(|key| key.chars().all(|c| c.is_ascii_digit()))
        .cloned()
        .collect();
    keys.sort_by_key(|key| key.parse::<u32>().unwrap_or(u32::MAX));
    keys.into_iter()
        .find(|key| status.by_chapter.get(key).map(&predicate).unwrap_or(false))
}

fn first_revise_chapter(status: &Status) -> Option<String> {
    let mut keys: Vec<_> = status.revise_by_chapter.keys().cloned().collect();
    keys.sort_by_key(|key| key.parse::<u32>().unwrap_or(u32::MAX));
    keys.into_iter().next()
}

fn has_pdf(project: &Path) -> Result<bool> {
    if !project.is_dir() {
        return Ok(false);
    }
    for entry in fs::read_dir(project)? {
        let entry = entry?;
        if entry
            .path()
            .extension()
            .and_then(|s| s.to_str())
            .map(|ext| ext.eq_ignore_ascii_case("pdf"))
            .unwrap_or(false)
        {
            return Ok(true);
        }
    }
    Ok(false)
}

fn spec_file(project: &Path, status: &Status, filename: &str) -> Option<PathBuf> {
    if status.spec.starts_with("(sin spec") {
        return None;
    }
    let path = project.join("specs").join(&status.spec).join(filename);
    path.is_file().then_some(path)
}

fn with_lock<F, T>(project: &Path, f: F) -> Result<T>
where
    F: FnOnce() -> Result<T>,
{
    let vivarium = project.join(".vivarium");
    fs::create_dir_all(&vivarium)?;
    let lock_path = vivarium.join("lock");
    let file = OpenOptions::new()
        .create(true)
        .truncate(false)
        .read(true)
        .write(true)
        .open(&lock_path)?;
    let mut lock = RwLock::new(file);
    let _guard = lock.try_write().map_err(|e| {
        if e.kind() == std::io::ErrorKind::WouldBlock {
            VivariumError::LockTaken(lock_path.clone())
        } else {
            VivariumError::Io(e)
        }
    })?;
    f()
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::sidecar::PassStatus;

    fn status_closeable() -> Status {
        Status {
            spec: "001-demo".to_string(),
            closeable: true,
            all_chapters_approved: true,
            next_step: "close".to_string(),
            passes: vec![PassStatus {
                num: 5,
                ..Default::default()
            }],
            ..Default::default()
        }
    }

    fn status_estudio(next_step: &str) -> Status {
        Status {
            spec: "001-demo".to_string(),
            mode: Some("estudio".to_string()),
            next_step: next_step.to_string(),
            ..Default::default()
        }
    }

    fn scaffold_global_done(project: &Path) {
        fs::write(project.join("README.md"), "# intro\n").unwrap();
        fs::write(project.join("guia.pdf"), "%PDF-1.4\n").unwrap();
        fs::create_dir_all(project.join("specs/001-demo")).unwrap();
        fs::write(project.join("specs/001-demo/feedback.md"), "# Feedback\n").unwrap();
    }

    #[test]
    fn intro_cuenta_como_manuscrito() {
        let action = Action {
            step: "intro".to_string(),
            chapter: Some("global".to_string()),
            role: Role::Redactora,
            detail: String::new(),
            kind: ActionKind::Agent,
        };
        assert!(writes_manuscript(&action));
    }

    #[test]
    fn plan_global_checkpoint_sin_feedback_aunque_closeable() {
        let tmp = tempfile::tempdir().unwrap();
        fs::write(tmp.path().join("README.md"), "# intro\n").unwrap();
        fs::write(tmp.path().join("guia.pdf"), "%PDF-1.4\n").unwrap();
        // Sin specs/001-demo/feedback.md: el checkpoint 2 manda sobre los gates.
        let planned = plan_global(tmp.path(), &status_closeable()).unwrap();
        assert!(matches!(
            planned,
            Planned::Checkpoint {
                step: "feedback",
                ..
            }
        ));
    }

    #[test]
    fn plan_global_despacha_close_cuando_closeable() {
        let tmp = tempfile::tempdir().unwrap();
        scaffold_global_done(tmp.path());
        let planned = plan_global(tmp.path(), &status_closeable()).unwrap();
        match planned {
            Planned::Act(action) => {
                assert_eq!(action.step, "close");
                assert_eq!(action.kind, ActionKind::Sidecar);
            }
            other => panic!("esperaba Act(close), fue {other:?}"),
        }
    }

    #[test]
    fn write_y_dispose_son_checkpoints_en_estudio() {
        let tmp = tempfile::tempdir().unwrap();
        let write = plan_action(tmp.path(), &status_estudio("write")).unwrap();
        assert!(matches!(write, Planned::Checkpoint { step: "write", .. }));
        let dispose = plan_action(tmp.path(), &status_estudio("dispose")).unwrap();
        assert!(matches!(
            dispose,
            Planned::Checkpoint {
                step: "dispose",
                ..
            }
        ));
    }

    #[test]
    fn normalizacion_close_incompleto_respeta_checkpoints_estudio() {
        let tmp = tempfile::tempdir().unwrap();
        let mut status = status_estudio("close");
        status.all_chapters_approved = false;
        status.by_chapter.insert(
            "1".to_string(),
            crate::sidecar::ChapterStatus {
                drafted: false,
                ..Default::default()
            },
        );
        let planned = plan_action(tmp.path(), &status).unwrap();
        assert!(matches!(planned, Planned::Checkpoint { step: "write", .. }));

        status.by_chapter.get_mut("1").unwrap().drafted = true;
        status.revise_by_chapter.insert("1".to_string(), 1);
        let planned = plan_action(tmp.path(), &status).unwrap();
        assert!(matches!(
            planned,
            Planned::Checkpoint {
                step: "dispose",
                ..
            }
        ));
    }

    #[test]
    fn intro_global_es_checkpoint_en_estudio() {
        let tmp = tempfile::tempdir().unwrap();
        let mut status = status_closeable();
        status.mode = Some("estudio".to_string());
        let planned = plan_global(tmp.path(), &status).unwrap();
        assert!(matches!(planned, Planned::Checkpoint { step: "intro", .. }));
    }

    #[test]
    fn implement_imposible_sigue_bloqueado_por_guardarrail() {
        let tmp = tempfile::tempdir().unwrap();
        fs::write(
            tmp.path().join(".writeonmars-manifest.json"),
            r#"{"mode":"estudio"}"#,
        )
        .unwrap();
        let mut status = status_estudio("implement");
        status.by_chapter.insert(
            "1".to_string(),
            crate::sidecar::ChapterStatus {
                drafted: false,
                ..Default::default()
            },
        );
        assert!(blocked_by_mode(tmp.path(), &status).unwrap());
    }

    #[test]
    fn plan_global_no_redespacha_close_ya_cerrado() {
        let tmp = tempfile::tempdir().unwrap();
        scaffold_global_done(tmp.path());
        decisions::append_disposition(
            tmp.path(),
            "close",
            Some("global"),
            "sidecar",
            Outcome::Ok,
            None,
        )
        .unwrap();
        let planned = plan_global(tmp.path(), &status_closeable()).unwrap();
        assert!(matches!(planned, Planned::Done(_)));
    }

    #[test]
    fn reconcile_cierra_huerfanos_sin_bloquear() {
        let tmp = tempfile::tempdir().unwrap();
        decisions::append_dispatch(tmp.path(), "implement", Some("1"), "redactora", None).unwrap();
        // Capítulo no redactado → efecto ausente → Failed, no error duro.
        reconcile_in_flight(tmp.path(), &Status::default()).unwrap();
        assert!(decisions::in_flight(tmp.path()).unwrap().is_empty());
        let last = decisions::read(tmp.path()).unwrap().pop().unwrap();
        assert_eq!(last.outcome, Some(Outcome::Failed));
    }

    #[test]
    fn checkpoint_no_se_duplica_en_esperas() {
        let tmp = tempfile::tempdir().unwrap();
        decisions::append_checkpoint_once(tmp.path(), "specify", "brief").unwrap();
        decisions::append_checkpoint_once(tmp.path(), "specify", "brief").unwrap();
        assert_eq!(decisions::read(tmp.path()).unwrap().len(), 1);
    }
}
