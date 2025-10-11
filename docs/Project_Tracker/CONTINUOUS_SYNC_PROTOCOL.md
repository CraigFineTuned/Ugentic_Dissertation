# CONTINUOUS SYNC PROTOCOL (v1.0)

**Purpose:** To ensure perfect, lossless session continuity.

---

## Core Principles

1.  **Assume Interruption:** Every session may be the one that gets cut off. Plan accordingly.
2.  **Verify, Don't Trust:** Before starting new work, verify the outcome of the last action from the previous session.
3.  **Single Source of Truth:** `CURRENT_SESSION_CHECKPOINT.md` is the only source of truth for what has been completed.

## Verification Protocol

- **File Creation/Modification:** Check that the file exists at the specified path and that its content matches the expected output. Check the timestamp.
- **Shell Commands:** Check for expected output logs, created artifacts, or resulting changes in the environment.
- **Analysis/Questions:** The question being answered or the analysis being performed is the checkpoint.

If verification for a supposedly 'COMPLETE' action fails, its status must be immediately reverted to incomplete, and it must be re-executed.
