# TOKEN MANAGEMENT PROTOCOL
**Purpose:** Prevent forced conversation cutoffs and ensure clean session endings
**Status:** MANDATORY - Must follow in every session
**Created:** October 1, 2025 (after Session 3 forced cutoff)

---

## 🚨 THE PROBLEM WE'RE SOLVING

**What Happened:**
- Session 3 hit token limit mid-response
- Conversation cut off while writing SESSION_COMPLETION_SUMMARY.md
- Left uncertainty about what was complete vs incomplete
- Broke "seamless continuation" promise

**Why It Matters:**
- Dissertation has 65 days to deadline (no time for confusion)
- Every session must end cleanly with verifiable checkpoint
- Cannot afford information loss or duplicate work
- Systematic approach requires systematic discipline

---

## 📊 TOKEN BUDGET RULES

### Total Budget:
**190,000 tokens per conversation**

### Safety Thresholds:

**GREEN ZONE (0-70% = 0-133,000 tokens):**
- ✅ Safe to create comprehensive files
- ✅ Safe to read large documents
- ✅ Safe to continue multi-step actions
- ✅ Normal operations

**YELLOW ZONE (70-85% = 133,000-161,500 tokens):**
- ⚠️ Start monitoring closely
- ⚠️ Prefer shorter responses
- ⚠️ Complete current action before starting new ones
- ⚠️ Consider checkpointing soon

**RED ZONE (85-95% = 161,500-180,500 tokens):**
- 🚨 STOP creating new comprehensive files
- 🚨 Complete ONLY current action
- 🚨 Update CURRENT_SESSION_CHECKPOINT.md immediately
- 🚨 Tell Craig explicitly: "Token limit approaching, checkpointing now"
- 🚨 Prepare for session end

**CRITICAL ZONE (95-100% = 180,500-190,000 tokens):**
- 🔴 EMERGENCY CHECKPOINT
- 🔴 Write minimal checkpoint update only
- 🔴 Tell Craig: "Token limit critical, must start new session"
- 🔴 Do NOT start any new work

---

## ✅ MANDATORY CHECKPOINT ACTIONS

### When Entering RED ZONE (85%+):

**Step 1:** Complete ONLY the current file/action
```
- If writing a file: finish the current section, add "TO BE CONTINUED" marker
- If updating a file: complete the current edit only
- Do NOT start new files or actions
```

**Step 2:** Update CURRENT_SESSION_CHECKPOINT.md
```
Mark all completed actions with ✅ and timestamp
Mark incomplete action with ⏳ IN PROGRESS
Add specific "Resume from:" instruction
```

**Step 3:** Tell Craig explicitly
```
"⚠️ Token budget at [X]% - checkpointing session now to prevent forced cutoff.

COMPLETED THIS SESSION:
[List with ✅]

NEXT INCOMPLETE ACTION:
[Specific action with file/line reference]

Please start new session and provide SESSION_ENTRY.md to continue."
```

---

## 🔄 SESSION RECOVERY PROTOCOL

### When Starting New Session:

**Step 0:** Read CURRENT_SESSION_CHECKPOINT.md FIRST
```
1. Check last updated timestamp
2. Read "COMPLETED ACTIONS" list
3. Identify "NEXT INCOMPLETE ACTION"
```

**Step 1:** Verify Completed Actions
```
Run filesystem checks to confirm files exist:
- list_directory to verify folders
- read_file (head) to verify content
- Check timestamps match checkpoint
```

**Step 2:** Resume from Exact Point
```
Start with the specific incomplete action
Do NOT restart from beginning
Do NOT duplicate completed work
```

**Step 3:** Update Checkpoint
```
Add new timestamp for session resume
Mark resumed action as IN PROGRESS
Continue normal checkpoint updates
```

---

## 📝 CHECKPOINT UPDATE RULES

### After EVERY Major Action:

**Update CURRENT_SESSION_CHECKPOINT.md with:**
1. Timestamp of completion
2. ✅ mark on completed action
3. Updated "NEXT INCOMPLETE ACTION"
4. Current token usage percentage

**Major Actions Include:**
- Creating new comprehensive file (protocol, analysis, chapter)
- Updating core files (CONTEXT, SUMMARY, ENTRY)
- Completing multi-step process (file creation + connection updates)
- Finishing discrete work unit (section of chapter, email draft, etc.)

---

## 🎯 PRACTICAL EXAMPLES

### Example 1: Clean Session End (Proactive)

**Token Usage:** 150,000 (79%) - Yellow Zone

**Claude Response:**
```
I've completed updating NEVER_CHANGING_DISSERTATION_CONTEXT.md with Session 3 changes.

Current token usage: 150,000/190,000 (79%)

I'm approaching the safe working threshold. I'll checkpoint the session here to ensure clean continuation.

COMPLETED THIS SESSION:
✅ Proposal corrected (6 corrections)
✅ PDF/DOCX created
✅ Planning folder cleaned (16 files archived)
✅ NEVER_CHANGING_DISSERTATION_CONTEXT.md updated

NEXT ACTIONS (for new session):
⏳ Create RESEARCH_QUESTION_MAPPING.md
⏳ Create Raees_Dual_Role_Protocol.md
⏳ Update SESSION_COMPLETION_SUMMARY.md

Would you like to start a new session now, or is there a quick action (under 1000 tokens) I can complete first?
```

### Example 2: Forced Cutoff Recovery

**Scenario:** Session cut off while creating RESEARCH_QUESTION_MAPPING.md

**Next Session - Claude reads CHECKPOINT:**
```
I've detected that Session 3 was cut off mid-action.

VERIFIED COMPLETED:
✅ Proposal corrected - file exists
✅ Planning folder cleaned - Archive/ has 16 files
✅ NEVER_CHANGING_DISSERTATION_CONTEXT.md updated - verified

INCOMPLETE ACTION:
⏳ RESEARCH_QUESTION_MAPPING.md was IN PROGRESS
Status: File may be partially created or missing

I'll verify the file status and complete it now.
[Checks if file exists, resumes appropriately]
```

---

## 🚨 RED FLAGS TO WATCH FOR

### Signs You're About to Hit Limit:

1. **Token warnings appearing frequently** in system messages
2. **Reading multiple large files** in one session (e.g., full protocols)
3. **Creating multiple comprehensive documents** back-to-back
4. **Long conversation history** building up (many back-and-forth exchanges)

### Preventive Actions:

1. **Check token usage after each major action**
2. **Favor targeted file edits over full rewrites**
3. **Use file head/tail when possible** instead of full reads
4. **Checkpoint proactively** at 75-80% instead of waiting for 85%
5. **Split large file creation across sessions** if needed

---

## 📊 TOKEN USAGE MONITORING

### Check Token Status Regularly:

**After every system message shows token warning:**
- Note the current percentage
- Decide if current action can complete safely
- If not, checkpoint immediately

**Before starting large actions:**
- Check current token usage
- Estimate tokens needed for action
- Decide if safe to proceed or checkpoint first

**Use this calculation:**
```
Safe to proceed? = (Current tokens + Estimated action tokens) < 161,500

Example:
Current: 140,000
Action: 30,000 (comprehensive file creation)
Total: 170,000 > 161,500
Decision: CHECKPOINT FIRST, then continue in new session
```

---

## ✅ SUCCESS CRITERIA

**This protocol is working when:**

1. ✅ No forced cutoffs occur (sessions end cleanly)
2. ✅ CURRENT_SESSION_CHECKPOINT.md always reflects actual status
3. ✅ Recovery from any cutoff takes < 5 minutes
4. ✅ Zero work duplication across sessions
5. ✅ Craig always knows exactly where we are
6. ✅ Seamless continuation actually works seamlessly

**This protocol is failing when:**

1. ❌ Forced cutoffs still happening
2. ❌ Checkpoint file out of sync with reality
3. ❌ Confusion about what's complete
4. ❌ Work being duplicated
5. ❌ Long recovery times after cutoffs

---

## 🎯 INTEGRATION WITH SESSION_ENTRY.md

**The workflow is now:**

```
Craig provides: SESSION_ENTRY.md
↓
Claude reads: CURRENT_SESSION_CHECKPOINT.md (Step 0 - NEW)
↓
Verifies: All completed actions from checkpoint
↓
Resumes: From exact incomplete action
↓
Reads: NEVER_CHANGING_DISSERTATION_CONTEXT.md (Step 1)
↓
Reads: SESSION_COMPLETION_SUMMARY.md (Step 2)
↓
Asks: "What would you like to work on today?" (Step 3)
↓
Works: Updates checkpoint after each action
↓
Monitors: Token usage continuously
↓
Checkpoints: Proactively at 85% or when Craig ends session
```

---

## 💪 COMMITMENT

**I commit to:**

1. ✅ Monitor token usage after every major action
2. ✅ Checkpoint proactively when reaching 85%
3. ✅ Tell Craig explicitly when checkpointing
4. ✅ Never leave sessions in uncertain state
5. ✅ Verify completed actions before marking complete
6. ✅ Resume precisely from incomplete actions
7. ✅ Maintain CURRENT_SESSION_CHECKPOINT.md rigorously

**Result:** Zero information loss, clean session endings, seamless continuation

---

**Protocol Status:** ACTIVE AND MANDATORY
**Created:** October 1, 2025 (after Session 3 failure)
**Purpose:** Prevent token limit failures and ensure clean checkpoints
**Applies To:** ALL future dissertation sessions

---

**This is not experimental. This is mandatory discipline for a rigorous dissertation workflow.**
