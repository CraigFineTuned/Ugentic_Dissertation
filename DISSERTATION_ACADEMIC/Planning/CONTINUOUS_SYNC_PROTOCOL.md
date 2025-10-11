# CONTINUOUS SYNC PROTOCOL
**Purpose:** Guarantee consistency across forced conversation cutoffs
**Status:** MANDATORY - Replaces previous checkpoint approach
**Date:** October 1, 2025

---

## 🎯 THE CORE PROBLEM

**What Craig needs:** Absolute certainty that we're always synced, even after forced cutoffs
**Current weakness:** Checkpoint might be out of sync with reality
**Root cause:** Updates happen at end of response, not after each action

---

## ✅ THE SOLUTION: VERIFY-THEN-CHECKPOINT

### New Rule: AFTER EVERY SINGLE ACTION

**Step 1: Complete the action** (create file, edit file, etc.)

**Step 2: Verify it worked**
```
- Run filesystem check to confirm file exists
- Read first/last lines to confirm content correct
- Check file size is reasonable
```

**Step 3: Update checkpoint IMMEDIATELY**
```
Add line to checkpoint:
"✅ [Action] - VERIFIED at [timestamp] - File: [path] - Size: [bytes]"
```

**Step 4: Continue to next action**

**If cutoff happens:** Checkpoint shows exactly what was verified complete

---

## 📋 VERIFICATION COMMANDS (Mandatory After Each Action)

### After Creating a File:
```
1. filesystem:get_file_info [path] → Confirm exists + get size
2. filesystem:read_file [path] (head: 10) → Confirm content correct
3. Update checkpoint with: "✅ Created + verified"
```

### After Editing a File:
```
1. filesystem:read_file [path] (sections around edit) → Confirm edit applied
2. Update checkpoint with: "✅ Edited + verified"
```

### After Multi-Step Process:
```
1. Verify each step individually
2. Update checkpoint after EACH step (not after all steps)
3. Mark overall process complete only when all steps verified
```

---

## 🔄 SESSION START VERIFICATION (Every Time)

When you provide SESSION_ENTRY.md, Claude MUST:

**Step 0a: Read checkpoint**
```
Get list of all "✅ COMPLETED" actions
```

**Step 0b: RE-VERIFY each completed action**
```
For each ✅ action:
1. Check file still exists
2. Check timestamp matches checkpoint
3. If verification fails → Flag immediately: "Action X marked complete but file missing"
```

**Step 0c: Identify next incomplete action**
```
Find first "⏳" action in checkpoint
Read RESUME_FROM marker for exact starting point
```

**Step 1-2: Read context and summary** (as before)

**Step 3: EXECUTE from exact resume point** (not ask)

---

## 📝 CHECKPOINT FORMAT (New Structure)

```markdown
## VERIFIED COMPLETE ACTIONS (✅):

1. ✅ Proposal corrected
   - Verified: Oct 1, 10:15 AM
   - File: Honours_Research_Proposal_C_Vraagom_Oct1_2025.pdf
   - Size: 2.4 MB
   - Verification: File exists + opens correctly

2. ✅ EMAIL_TO_JEMINI_SEND_NOW.md created
   - Verified: Oct 1, 3:45 PM
   - File: Planning/EMAIL_TO_JEMINI_SEND_NOW.md
   - Size: 2.1 KB
   - Verification: File exists + contains complete email

## NEXT INCOMPLETE ACTION (⏳):

⏳ Send emails (3 emails, 40 min)
   Status: Files ready, waiting for Craig to send
   
   When complete, next action:
   ⏳ Begin Chapter 1, Section 1.1
   
   RESUME_FROM: "Create file: Chapters/Chapter_1_Introduction.md
                Section 1.1: Research Context
                Start with: Literature gap paragraph (multi-agent + Ubuntu + organizational)"

## VERIFICATION RULES:

- Every ✅ must have timestamp + file path + verification note
- Re-verify all ✅ actions at session start
- If verification fails, action becomes ⏳ incomplete
- RESUME_FROM must be specific: file, section, paragraph, starting text
```

---

## 🎯 PRACTICAL EXAMPLE

### Bad (Current):
```
✅ Created email files
✅ Updated checkpoint
⏳ Craig needs to send emails
```
**Problem:** No verification, no specifics, can't confirm what's actually done

### Good (New):
```
✅ EMAIL_TO_JEMINI_SEND_NOW.md created + verified
   - File: Planning/EMAIL_TO_JEMINI_SEND_NOW.md
   - Size: 2,143 bytes
   - Verified: Oct 1, 3:47 PM
   - Content check: Contains "Dear Jemini" + attachment instruction ✓

✅ ETHICS_SUBMISSION_INSTRUCTIONS.md created + verified
   - File: Planning/ETHICS_SUBMISSION_INSTRUCTIONS.md  
   - Size: 1,876 bytes
   - Verified: Oct 1, 3:49 PM
   - Content check: Contains 3-step submission process ✓

⏳ NEXT ACTION: Craig sends emails
   After sending, verify by checking:
   - Gmail sent folder for 3 sent emails
   - Then proceed to Chapter 1 creation

RESUME_FROM: "Create Chapters/Chapter_1_Introduction.md
              Start Section 1.1: Research Context
              First paragraph topic: AI adoption challenges in IT departments
              Reference: Aldoseri et al. (2024) + Ju et al. (2025)"
```

---

## 🔄 SESSION CONTINUITY GUARANTEE

### How We Stay Synced:

**Session N (Before Cutoff):**
```
Action 1 → Verify → Update checkpoint → 
Action 2 → Verify → Update checkpoint →
Action 3 → Verify → [CUTOFF HAPPENS]
```

**Session N+1 (After Cutoff):**
```
Read checkpoint → Shows Actions 1-2 complete + verified
Re-verify Actions 1-2 → Both confirmed present
See Action 3 incomplete → Resume from RESUME_FROM marker
Continue exactly where left off
```

**Result:** Zero ambiguity, zero information loss

---

## 📊 FILE HIERARCHY (How They Connect)

```
SESSION_ENTRY.md (You provide this)
    ↓
    Step 0: CURRENT_SESSION_CHECKPOINT.md (Read + Re-verify all ✅)
    ↓
    Step 1: NEVER_CHANGING_DISSERTATION_CONTEXT.md (System state)
    ↓
    Step 2: SESSION_COMPLETION_SUMMARY.md (Last session detail)
    ↓
    Step 3: EXECUTE next ⏳ action from checkpoint
    ↓
    After each action: VERIFY + UPDATE checkpoint immediately
    ↓
    Continue until session ends (natural or forced)
```

**Key change:** Checkpoint is updated DURING work, not after work

---

## 🚨 CRITICAL RULES

### Claude MUST:

1. **Update checkpoint AFTER EVERY action** (not at end of response)
2. **Verify each action** before marking ✅
3. **Include file path + size + timestamp** in every ✅
4. **Re-verify all ✅ actions** at session start
5. **Make RESUME_FROM hyper-specific** (file, section, paragraph, starting text)
6. **Never assume** something is complete without verification

### Checkpoint is:
- ✅ **Source of truth** for what's complete
- ✅ **Updated in real-time** during work
- ✅ **Verified at session start** every time
- ✅ **Specific about resume points** for seamless continuation

---

## 💪 WHAT THIS GUARANTEES

**For Craig:**
1. ✅ Always know exactly what's complete (verified proof)
2. ✅ Always know exactly where to resume (specific marker)
3. ✅ Zero ambiguity about session state
4. ✅ Confidence that cutoffs won't cause information loss
5. ✅ Trust that next session continues seamlessly

**For Claude:**
1. ✅ Clear verification steps after each action
2. ✅ Checkpoint always reflects reality
3. ✅ Re-verification at session start catches any issues
4. ✅ Specific resume markers prevent confusion
5. ✅ System is foolproof, not just "pretty good"

---

## 🎯 IMPLEMENTATION STATUS

**This protocol:** ACTIVE NOW
**Replaces:** Previous checkpoint approach (which lacked verification)
**Applies to:** ALL future actions, starting immediately
**Test:** Next action I take will follow this protocol exactly

---

**Status:** ACTIVE AND MANDATORY
**Purpose:** Guarantee consistency across forced cutoffs
**Result:** Craig and Claude always in sync, no exceptions
