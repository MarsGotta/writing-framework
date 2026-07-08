use std::path::PathBuf;
use std::process;
use std::str::FromStr;

use clap::{Parser, Subcommand};
use serde_json::Value;
use vivarium_core::bootstrap::{self, BootstrapOptions};
use vivarium_core::decisions;
use vivarium_core::error::{Result, VivariumError};
use vivarium_core::manifest::{self, Mode};
use vivarium_core::{runner, sidecar};

#[derive(Debug, Parser)]
#[command(
    name = "vivarium",
    version,
    about = "Ejecutor headless de Write.OnMars"
)]
struct Cli {
    #[command(subcommand)]
    command: Option<Commands>,
}

#[derive(Debug, Subcommand)]
enum Commands {
    New {
        dir: PathBuf,
        #[arg(long)]
        kind: String,
        #[arg(long)]
        mode: Option<String>,
        #[arg(long)]
        sector: Option<String>,
        #[arg(long)]
        preset: Option<PathBuf>,
        #[arg(long)]
        operator: Option<String>,
        #[arg(long)]
        email: Option<String>,
        #[arg(long, default_value = "claude,gemini,codex")]
        agents: String,
        #[arg(long)]
        json: bool,
    },
    Status {
        #[arg(long, default_value = ".")]
        project: PathBuf,
        #[arg(long)]
        json: bool,
    },
    Step {
        #[arg(long, default_value = ".")]
        project: PathBuf,
        #[arg(long)]
        json: bool,
    },
    Run {
        #[arg(long, default_value = ".")]
        project: PathBuf,
        #[arg(long)]
        json: bool,
    },
    Check {
        #[arg(long, default_value = ".")]
        project: PathBuf,
        #[arg(long)]
        json: bool,
    },
    Mode {
        #[command(subcommand)]
        command: ModeCommands,
    },
}

#[derive(Debug, Subcommand)]
enum ModeCommands {
    Set {
        mode: String,
        #[arg(long, default_value = ".")]
        project: PathBuf,
        #[arg(long)]
        yes: bool,
        #[arg(long)]
        json: bool,
    },
}

fn main() {
    let cli = Cli::parse();
    match run(cli) {
        Ok(code) => process::exit(code),
        Err(err) => {
            eprintln!("[vivarium] error: {err}");
            process::exit(err.exit_code());
        }
    }
}

fn run(cli: Cli) -> Result<i32> {
    match cli.command {
        None => {
            println!("vivarium {}", env!("CARGO_PKG_VERSION"));
            Ok(0)
        }
        Some(Commands::New {
            dir,
            kind,
            mode,
            sector,
            preset,
            operator,
            email,
            agents,
            json,
        }) => {
            let mode = match mode {
                Some(value) => Some(parse_mode_arg(&value)?),
                None => None,
            };
            let target = bootstrap::new_project(&BootstrapOptions {
                target: dir,
                kind,
                mode,
                sector,
                preset,
                operator,
                email,
                agents,
            })?;
            if json {
                println!("{}", serde_json::json!({"ok": true, "project": target}));
            } else {
                println!("proyecto creado: {}", target.display());
            }
            Ok(0)
        }
        Some(Commands::Status { project, json: _ }) => {
            let value = status_value(&project)?;
            println!("{}", serde_json::to_string_pretty(&value)?);
            Ok(0)
        }
        Some(Commands::Step { project, json }) => {
            let result = runner::step(project)?;
            print_runner_result(&result, json)?;
            Ok(result.exit_code())
        }
        Some(Commands::Run { project, json }) => {
            let result = runner::run(project)?;
            print_runner_result(&result, json)?;
            Ok(result.exit_code())
        }
        Some(Commands::Check { project, json }) => {
            runner::check(project)?;
            if json {
                println!("{}", serde_json::json!({"ok": true}));
            } else {
                println!("ok");
            }
            Ok(0)
        }
        Some(Commands::Mode { command }) => match command {
            ModeCommands::Set {
                mode,
                project,
                yes,
                json,
            } => {
                let to = parse_mode_arg(&mode)?;
                if !yes {
                    let consequence = consequence_text(to);
                    if json {
                        println!(
                            "{}",
                            serde_json::json!({
                                "ok": false,
                                "confirmation_required": true,
                                "consequence": consequence
                            })
                        );
                    } else {
                        println!("{consequence}");
                        println!("Repite con --yes para aplicar el cambio.");
                    }
                    return Ok(VivariumError::ConfirmationRequired(consequence).exit_code());
                }
                let change = manifest::set_mode(project, to)?;
                if json {
                    println!("{}", serde_json::to_string_pretty(&change)?);
                } else {
                    println!("mode cambiado: {} -> {}", change.from, change.to);
                }
                Ok(0)
            }
        },
    }
}

// Un mode mal escrito es un error de argumentos (exit 2), no de validación de
// proyecto (exit 5) — mismo trato que un --kind inválido.
fn parse_mode_arg(value: &str) -> Result<Mode> {
    Mode::from_str(value)
        .map_err(|_| VivariumError::InvalidUsage(format!("mode inválido: {value} (produccion|estudio)")))
}

fn status_value(project: &PathBuf) -> Result<Value> {
    let status = sidecar::run_status(project)?;
    let manifest = manifest::load_project(project)?;
    let in_flight = decisions::in_flight(project)?;
    let blocked_by_mode = runner::blocked_by_mode(project, &status)?;
    let mut value = serde_json::to_value(status)?;
    let obj = value.as_object_mut().ok_or_else(|| {
        VivariumError::Validation("status.py --json no produjo objeto".to_string())
    })?;
    obj.insert(
        "mode".to_string(),
        Value::String(manifest.mode().as_str().to_string()),
    );
    obj.insert(
        "in_flight".to_string(),
        serde_json::to_value(in_flight).map_err(VivariumError::from)?,
    );
    obj.insert("blocked_by_mode".to_string(), Value::Bool(blocked_by_mode));
    Ok(value)
}

fn print_runner_result(result: &runner::StepResult, json: bool) -> Result<()> {
    if json {
        println!(
            "{}",
            serde_json::json!({
                "exit_code": result.exit_code(),
                "message": result.message()
            })
        );
    } else {
        println!("{}", result.message());
    }
    Ok(())
}

fn consequence_text(mode: Mode) -> String {
    match mode {
        Mode::Produccion => "Cambiar a produccion permite despachar redaccion con IA; desde ese momento se pierde la demostrabilidad de autoria humana para la prosa que la IA redacte.".to_string(),
        Mode::Estudio => "Cambiar a estudio bloquea cualquier redaccion de manuscrito por IA; el humano escribe y las ayudas quedan limitadas a revision, verificacion y anotacion.".to_string(),
    }
}
