use std::path::PathBuf;

use thiserror::Error;

pub type Result<T> = std::result::Result<T, VivariumError>;

#[derive(Debug, Error)]
pub enum VivariumError {
    #[error("uso inválido: {0}")]
    InvalidUsage(String),
    #[error("entorno incompleto: {0}")]
    EnvironmentIncomplete(String),
    #[error("confirmación requerida: {0}")]
    ConfirmationRequired(String),
    #[error("validación fallida: {0}")]
    Validation(String),
    #[error("otro runner ya tiene el lock de {0}")]
    LockTaken(PathBuf),
    #[error("checkpoint humano: {0}")]
    Checkpoint(String),
    #[error("sidecar falló: {0}")]
    Sidecar(String),
    #[error("despacho falló: {0}")]
    Dispatch(String),
    #[error("io: {0}")]
    Io(#[from] std::io::Error),
    #[error("json: {0}")]
    Json(#[from] serde_json::Error),
    #[error("toml: {0}")]
    Toml(#[from] toml::de::Error),
    #[error("git: {0}")]
    Git(#[from] git2::Error),
}

impl VivariumError {
    pub fn exit_code(&self) -> i32 {
        match self {
            Self::InvalidUsage(_) => 2,
            Self::EnvironmentIncomplete(_) => 3,
            Self::ConfirmationRequired(_) => 4,
            Self::Validation(_) => 5,
            Self::LockTaken(_) => 6,
            Self::Checkpoint(_) => 10,
            Self::Sidecar(_) => 5,
            Self::Dispatch(_) => 12,
            Self::Io(_) | Self::Json(_) | Self::Toml(_) | Self::Git(_) => 5,
        }
    }
}
