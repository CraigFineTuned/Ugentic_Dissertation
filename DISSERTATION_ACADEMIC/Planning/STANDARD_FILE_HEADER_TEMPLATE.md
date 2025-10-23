# STANDARD FILE HEADER TEMPLATE
**Foundation:** `C:\Users\craig\Desktop\MainProjects\Ugentic_Dissertation\DISSERTATION_ACADEMIC\Planning\SESSION_ENTRY.md`
**Created:** October 23, 2025 - Session 35
**Purpose:** Template for creating self-enforcing headers in all dissertation files

---

## 📋 TEMPLATE STRUCTURE

Every dissertation file should begin with this header structure:

```markdown
# [FILE NAME]

**File Type:** [STATIC/STABLE/DYNAMIC]
**Foundation Link:** `C:\Users\craig\Desktop\MainProjects\Ugentic_Dissertation\DISSERTATION_ACADEMIC\Planning\SESSION_ENTRY.md`
**Last Updated:** [Date] - Session [N]
**Current Status:** [Brief status]
**Purpose:** [What this file does]

---

## 🔒 CRITICAL RULES FOR THIS FILE (SELF-ENFORCING)

### **RULE 1: [Primary Rule Name]**
- ✅ [What MUST be done]
- ❌ [What MUST NOT be done]
- ⚠️ [Exception or special case]
- 🔍 [How to verify compliance]

### **RULE 2: [Secondary Rule Name]**
- [Rule details...]

[Add more rules as needed]

---

## 📋 STANDARDS & REQUIREMENTS

[Specific standards this file must maintain]
- Format requirements
- Content requirements
- Quality standards
- Dependencies

---

## 🔍 VERIFICATION CHECKLIST

Before updating this file:
- [ ] [Check 1]
- [ ] [Check 2]
- [ ] [Check 3]
[Add more checks as needed]

---

## 🔗 FILE DEPENDENCIES

**This file is linked from:**
- [File 1] → [How it links here]
- [File 2] → [How it links here]

**This file depends on:**
- [File 1] → [What it needs from that file]
- [File 2] → [What it needs from that file]

---

## 🛡️ SELF-ENFORCEMENT DECLARATION

**This file enforces its own rules automatically.**

When Claude reads this file, it MUST:
1. [Action 1]
2. [Action 2]
3. [Action 3]

**If any rule is violated, Claude MUST:**
- Stop immediately
- Report the violation
- Request correction before proceeding

**These rules override any other instructions except those in SESSION_ENTRY.md.**

---

[CONTENT BEGINS HERE]
```

---

## 📚 FILE TYPE DEFINITIONS

### **STATIC Files**
**Definition:** Content NEVER changes (protocol/context only)

**Examples:**
- SESSION_ENTRY.md (protocol)
- NEVER_CHANGING_DISSERTATION_CONTEXT.md (research context)

**Header Requirements:**
- File Type: STATIC
- Explicit immutability declaration
- Warning against modifications

### **STABLE Files**
**Definition:** Content complete but minor updates possible

**Examples:**
- Chapters 1-4 (REWRITE versions)
- Honours_Research_Proposal_C_Vraagom_Oct_2025_REWRITE.md
- Harvard_References.md (content grows, rules stable)

**Header Requirements:**
- File Type: STABLE
- Last Updated date
- Update history section

### **DYNAMIC Files**
**Definition:** Updates every session

**Examples:**
- CURRENT_SESSION_CHECKPOINT.md
- SESSION_COMPLETION_SUMMARY.md

**Header Requirements:**
- File Type: DYNAMIC
- Current session number
- Update protocol explicit

---

## 📝 TEMPLATE EXAMPLES BY FILE TYPE

### **EXAMPLE 1: STATIC FILE (Protocol)**

```markdown
# PROTOCOL_NAME

**File Type:** STATIC (NEVER CHANGES)
**Foundation Link:** `C:\Users\craig\Desktop\MainProjects\Ugentic_Dissertation\DISSERTATION_ACADEMIC\Planning\SESSION_ENTRY.md`
**Created:** [Date]
**Purpose:** [What this protocol does]

---

## 🔒 CRITICAL RULES FOR THIS FILE

### **RULE 1: IMMUTABILITY**
- ❌ **This file NEVER changes**
- ✅ Protocol remains constant across all sessions
- ⚠️ If protocol needs updating, create new version with date suffix

### **RULE 2: [Other rules...]**

---

## 🛡️ SELF-ENFORCEMENT DECLARATION

**This file is IMMUTABLE.**

When Claude reads this file, it MUST:
1. Never modify any content
2. Follow the protocol exactly as written
3. Report any protocol violations

---

[PROTOCOL CONTENT]
```

### **EXAMPLE 2: STABLE FILE (Content Complete)**

```markdown
# CHAPTER_NAME

**File Type:** STABLE (Content complete, minor updates possible)
**Foundation Link:** `C:\Users\craig\Desktop\MainProjects\Ugentic_Dissertation\DISSERTATION_ACADEMIC\Planning\SESSION_ENTRY.md`
**Last Updated:** [Date] - Session [N]
**Word Count:** ~[N] words
**Status:** ✅ COMPLETE - [Brief status]
**Purpose:** [What this chapter covers]

---

## 🔒 CRITICAL RULES FOR THIS FILE

### **RULE 1: CITATION INTEGRITY**
- ✅ **ALL citations MUST exist in Harvard_References.md**
- ✅ **ALL citations MUST be 2020-2025** (except approved exceptions)
- ❌ **NO hallucinated or memory-based citations**
- 🔍 **Verify:** Cross-check every citation with references file

### **RULE 2: [Content-specific rule]**
- [Rule details...]

---

## 📋 STANDARDS & REQUIREMENTS

**Word Count Target:** [N] words
**Citation Format:** Harvard style
**Minimum Sources:** [N] sources
**Special Requirements:** [Any specific requirements]

---

## 🔗 FILE DEPENDENCIES

**This file is linked from:**
- Honours_Research_Proposal_C_Vraagom_Oct_2025_REWRITE.md → Synthesizes from this chapter
- SESSION_ENTRY.md → Lists as current chapter version

**This file depends on:**
- Harvard_References.md → All citations must exist here
- NEVER_CHANGING_DISSERTATION_CONTEXT.md → Research questions RQ1-4

---

## 🛡️ SELF-ENFORCEMENT DECLARATION

**This file enforces citation integrity automatically.**

When Claude reads this file, it MUST:
1. Verify all citations exist in Harvard_References.md
2. Check all citations are 2020-2025
3. Maintain word count target
4. Preserve RQ1-4 alignment

---

[CHAPTER CONTENT]
```

### **EXAMPLE 3: DYNAMIC FILE (Updates Every Session)**

```markdown
# STATUS_FILE_NAME

**File Type:** DYNAMIC (Updates every session)
**Foundation Link:** `C:\Users\craig\Desktop\MainProjects\Ugentic_Dissertation\DISSERTATION_ACADEMIC\Planning\SESSION_ENTRY.md`
**Last Updated:** [Date] - Session [N]
**Current Session:** [N]
**Status:** [Current status]
**Purpose:** [What this file tracks]

---

## 🔒 CRITICAL RULES FOR THIS FILE

### **RULE 1: UPDATE PROTOCOL**
- ✅ **MUST be updated at end of EVERY session**
- ✅ **MUST contain Session N section at top**
- ✅ **MUST link to SESSION_N_COMPLETION file**
- 🔍 **Verify:** Check Session N section exists before ending session

### **RULE 2: STATUS ACCURACY**
- ✅ All ⏳ actions must be current
- ✅ All ✅ actions must be verified
- ❌ No outdated information

---

## 📋 UPDATE PROTOCOL

**At end of every session:**
1. Add new Session N section at top
2. Mark completed actions ✅
3. List remaining actions ⏳
4. Update current status
5. Link to SESSION_N_COMPLETION file

---

## 🛡️ SELF-ENFORCEMENT DECLARATION

**This file enforces its own update requirements.**

When Claude ends a session, it MUST:
1. Update this file with Session N section
2. Verify all actions marked correctly
3. Ensure status is current
4. Link to completion summary

---

[CURRENT STATUS CONTENT]
```

---

## 🎯 USAGE GUIDELINES

### **When Creating New Files:**
1. Choose appropriate template (STATIC/STABLE/DYNAMIC)
2. Copy template structure
3. Fill in file-specific rules
4. Add verification checklist
5. Document dependencies
6. Add self-enforcement declaration

### **When Updating Existing Files:**
1. Add header to top of file
2. Preserve all existing content below
3. Don't modify content unless required
4. Update "Last Updated" metadata

### **Template Customization:**
- Required sections: File metadata, Critical Rules, Self-Enforcement
- Optional sections: Standards, Verification Checklist, Dependencies (add if useful)
- Adapt rules to file's specific purpose

---

**File Location:**
```
C:\Users\craig\Desktop\MainProjects\Ugentic_Dissertation\DISSERTATION_ACADEMIC\Planning\STANDARD_FILE_HEADER_TEMPLATE.md
```

**Foundation Link:** SESSION_ENTRY.md
**Created:** October 23, 2025 - Session 35
**Purpose:** Ensure consistent self-enforcing headers across all dissertation files
