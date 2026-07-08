use std::fs::{self, OpenOptions};
use std::io::{BufRead, BufReader, Write};
use std::path::{Path, PathBuf};

use chrono::Utc;
use serde::{Deserialize, Serialize};

use crate::error::{Result, VivariumError};
use crate::manifest::Mode;

pub const DECISIONS_FILE: &str = "decisions.jsonl";

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
#[serde(rename_all = "snake_case")]
pub enum DecisionEvent {
    Dispatch,
    Disposition,
    ModeChange,
    Checkpoint,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
#[serde(rename_all = "lowercase")]
pub enum Outcome {
    Ok,
    Revise,
    Failed,
}

#[derive(Debug, Clone, PartialEq, Eq, Serialize, Deserialize)]
pub struct DecisionRecord {
    pub v: u8,
    pub ts: String,
    pub event: DecisionEvent,
    #[serde(default)]
    pub step: Option<String>,
    #[serde(default)]
    pub chapter: Option<String>,
    #[serde(default)]
    pub role: Option<String>,
    #[serde(default)]
    pub outcome: Option<Outcome>,
    #[serde(default)]
    pub detail: Option<String>,
}

impl DecisionRecord {
    pub fn new(event: DecisionEvent) -> Self {
        Self {
            v: 1,
            ts: Utc::now().to_rfc3339(),
            event,
            step: None,
            chapter: None,
            role: None,
            outcome: None,
            detail: None,
        }
    }
}

pub fn path(project: &Path) -> PathBuf {
    project.join(DECISIONS_FILE)
}

pub fn ensure(project: &Path) -> Result<()> {
    let p = path(project);
    if !p.exists() {
        fs::write(p, "")?;
    }
    Ok(())
}

pub fn append(project: impl AsRef<Path>, record: &DecisionRecord) -> Result<()> {
    let project = project.as_ref();
    ensure(project)?;
    let mut file = OpenOptions::new()
        .create(true)
        .append(true)
        .open(path(project))?;
    let line = serde_json::to_string(record)?;
    writeln!(file, "{line}")?;
    Ok(())
}

pub fn read(project: impl AsRef<Path>) -> Result<Vec<DecisionRecord>> {
    let p = path(project.as_ref());
    if !p.exists() {
        return Ok(Vec::new());
    }
    let file = fs::File::open(&p)?;
    let mut out = Vec::new();
    for (idx, line) in BufReader::new(file).lines().enumerate() {
        let line = line?;
        if line.trim().is_empty() {
            continue;
        }
        let record: DecisionRecord = serde_json::from_str(&line).map_err(|e| {
            VivariumError::Validation(format!(
                "{}:{} no es DecisionRecord válido: {e}",
                p.display(),
                idx + 1
            ))
        })?;
        out.push(record);
    }
    Ok(out)
}

pub fn in_flight(project: impl AsRef<Path>) -> Result<Vec<DecisionRecord>> {
    let mut open: Vec<DecisionRecord> = Vec::new();
    for record in read(project)? {
        match record.event {
            DecisionEvent::Dispatch => open.push(record),
            DecisionEvent::Disposition => {
                if let Some(pos) = open.iter().position(|candidate| {
                    candidate.step == record.step && candidate.chapter == record.chapter
                }) {
                    open.remove(pos);
                }
            }
            DecisionEvent::ModeChange | DecisionEvent::Checkpoint => {}
        }
    }
    Ok(open)
}

pub fn append_dispatch(
    project: impl AsRef<Path>,
    step: &str,
    chapter: Option<&str>,
    role: &str,
    detail: Option<String>,
) -> Result<()> {
    let mut record = DecisionRecord::new(DecisionEvent::Dispatch);
    record.step = Some(step.to_string());
    record.chapter = chapter.map(str::to_string);
    record.role = Some(role.to_string());
    record.detail = detail;
    append(project, &record)
}

pub fn append_disposition(
    project: impl AsRef<Path>,
    step: &str,
    chapter: Option<&str>,
    role: &str,
    outcome: Outcome,
    detail: Option<String>,
) -> Result<()> {
    let mut record = DecisionRecord::new(DecisionEvent::Disposition);
    record.step = Some(step.to_string());
    record.chapter = chapter.map(str::to_string);
    record.role = Some(role.to_string());
    record.outcome = Some(outcome);
    record.detail = detail;
    append(project, &record)
}

pub fn append_checkpoint(project: impl AsRef<Path>, step: &str, detail: &str) -> Result<()> {
    let mut record = DecisionRecord::new(DecisionEvent::Checkpoint);
    record.step = Some(step.to_string());
    record.detail = Some(detail.to_string());
    append(project, &record)
}

/// Como `append_checkpoint`, pero no duplica: si el último registro del log ya
/// es este mismo checkpoint, la espera continuada al humano no añade líneas.
pub fn append_checkpoint_once(project: impl AsRef<Path>, step: &str, detail: &str) -> Result<()> {
    let project = project.as_ref();
    if let Some(last) = read(project)?.last() {
        if last.event == DecisionEvent::Checkpoint && last.step.as_deref() == Some(step) {
            return Ok(());
        }
    }
    append_checkpoint(project, step, detail)
}

pub fn append_mode_change(project: impl AsRef<Path>, from: Mode, to: Mode) -> Result<()> {
    let mut record = DecisionRecord::new(DecisionEvent::ModeChange);
    record.detail = Some(format!("{}\u{2192}{}", from.as_str(), to.as_str()));
    append(project, &record)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn append_y_lee_decisiones() {
        let tmp = tempfile::tempdir().unwrap();
        append_dispatch(tmp.path(), "implement", Some("1"), "redactora", None).unwrap();
        let records = read(tmp.path()).unwrap();
        assert_eq!(records.len(), 1);
        assert_eq!(records[0].event, DecisionEvent::Dispatch);
    }

    #[test]
    fn correlacion_in_flight_por_orden() {
        let tmp = tempfile::tempdir().unwrap();
        append_dispatch(tmp.path(), "implement", Some("1"), "redactora", None).unwrap();
        append_dispatch(tmp.path(), "implement", Some("2"), "redactora", None).unwrap();
        append_disposition(
            tmp.path(),
            "implement",
            Some("1"),
            "redactora",
            Outcome::Ok,
            None,
        )
        .unwrap();
        let open = in_flight(tmp.path()).unwrap();
        assert_eq!(open.len(), 1);
        assert_eq!(open[0].chapter.as_deref(), Some("2"));
    }
}
