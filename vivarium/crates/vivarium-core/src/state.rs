use crate::sidecar::{ChapterStatus, Status};

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum ChapterState {
    Drafting,
    InReview,
    NeedsRevise,
    Approved,
}

pub fn derive_chapter_state(chapter: &ChapterStatus) -> ChapterState {
    if chapter.approved {
        ChapterState::Approved
    } else if !chapter.drafted {
        ChapterState::Drafting
    } else if chapter.revise_pending > 0 {
        ChapterState::NeedsRevise
    } else {
        ChapterState::InReview
    }
}

pub fn all_chapters_approved(status: &Status) -> bool {
    status.all_chapters_approved
}

#[cfg(test)]
mod tests {
    use super::*;

    fn c(drafted: bool, revise_pending: u32, approved: bool) -> ChapterStatus {
        ChapterStatus {
            drafted,
            revise_pending,
            approved,
            advisory: 0,
            passes_done: Vec::new(),
        }
    }

    #[test]
    fn deriva_estados_basicos() {
        assert_eq!(
            derive_chapter_state(&c(false, 0, false)),
            ChapterState::Drafting
        );
        assert_eq!(
            derive_chapter_state(&c(true, 0, false)),
            ChapterState::InReview
        );
        assert_eq!(
            derive_chapter_state(&c(true, 1, false)),
            ChapterState::NeedsRevise
        );
        assert_eq!(
            derive_chapter_state(&c(true, 0, true)),
            ChapterState::Approved
        );
    }
}
