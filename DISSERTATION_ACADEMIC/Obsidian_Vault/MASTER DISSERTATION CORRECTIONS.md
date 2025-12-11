# 🔧 MASTER DISSERTATION CORRECTIONS
> **Comprehensive Audit & Correction Guide**
> Created: Session 84 | December 11, 2025
> For: Craig Vraagom | Student 402415017

---

## ⚡ CRITICAL STATUS

| Metric | Current | Required | Status |
|--------|---------|----------|--------|
| Words | 22,179 | 20,000-25,000 | ✅ OK |
| Pages | ~75 | 80-120 | ⚠️ Close |
| Structure | Issues found | Per Sample | ❌ Fix |
| SA English | Partial | Full compliance | ⚠️ Fix |
| Citations | 2020-2025 | 2020-2025 | ✅ Verify |

---

## 🚨 STRUCTURAL ERRORS (Fix First)

### Error 1: Section Order in Chapter 1
**Current (WRONG):**
```
1.1 BACKGROUND
1.2 Introduction  ← WRONG - Introduction should come FIRST
```

**Required (CORRECT):**
```
1.1 Introduction
1.2 Background to the Study
```

**Action:** Swap sections 1.1 and 1.2

---

### Error 2: Duplicate Section Heading in Chapter 3
**Current (WRONG):**
```
3.4 SPECIFIC PROBLEM DIMENSIONS
   3.4.1 The Bridging Mechanism Model
   3.4.2 The Three-Level Analysis Framework
3.5 SPECIFIC PROBLEM DIMENSIONS  ← DUPLICATE HEADING!
   3.5.1 The Theoretical Gap
   3.5.2 The Operational Gap
   3.5.3 The Empirical Gap
```

**Required (CORRECT):**
```
3.4 PROBLEM DIMENSIONS AND MODELS
   3.4.1 The Bridging Mechanism Model
   3.4.2 The Three-Level Analysis Framework
3.5 SPECIFIC GAPS ADDRESSED
   3.5.1 The Theoretical Gap
   3.5.2 The Operational Gap
   3.5.3 The Empirical Gap
```

---

### Error 3: Jemini's Required Order
**Jemini Email (Dec 11):** AIM → QUESTIONS → OBJECTIVES

**Current:**
```
1.3 AIM
1.4 OBJECTIVES  ← Should be after Questions
1.5 Research Questions
```

**Required:**
```
1.3 AIM
1.4 Research Questions  ← Move up
1.5 OBJECTIVES  ← Move down
```

---

## 📝 SA ENGLISH SPELLING CORRECTIONS

### Words to Find & Replace (Use Ctrl+H in Word)

| Find (US) | Replace (SA/UK) | Instances |
|-----------|-----------------|----------|
| prioritize | prioritise | 12 |
| prioritizing | prioritising | check |
| organize | organise | 5 |
| organized | organised | 3 |
| organizing | organising | check |
| optimize | optimise | check |
| optimizing | optimising | check |
| optimization | optimisation | ✅ already correct |
| characterize | characterise | 1 |
| characterized | characterised | 1 |
| specialize | specialise | check |
| specialized | specialised | 1 |
| standardize | standardise | check |
| utilize | utilise | check |
| recognize | recognise | check |
| emphasize | emphasise | check |
| maximize | maximise | check |
| minimize | minimise | check |
| center | centre | check |
| behavior | behaviour | ✅ already correct |
| labor | labour | ✅ already correct |

**IMPORTANT:** Run Find & Replace with "Match case" OFF to catch all variants.

---

## 🎯 UGENTIC TEST RESULTS TO ADD

Your test demonstrated Ubuntu orchestration perfectly. Add this to **Chapter 5, Section 5.X**:

### New Section: 5.5 UGENTIC System Validation

The UGENTIC system was empirically tested with scenarios reflecting real IT department challenges at GrandWest. When presented with a multi-domain issue involving slow application performance, network disconnections, and loyalty card failures on the slot floor, the system demonstrated Ubuntu principles in action.

The investigation proceeded through multiple specialist agents. IT Support first attempted initial triage, gathering information before recognising the need for specialist expertise. The Service Desk Manager then routed the escalation to Network Support, who conducted connectivity diagnostics revealing stable but slightly elevated latency. Recognising the multi-domain nature of the problem, Infrastructure triggered the Ubuntu Orchestrator.

The Ubuntu Orchestrator coordinated Network Support, App Support, and Infrastructure agents in collective investigation. Each agent contributed domain-specific findings: Network Support identified latency patterns, App Support discovered application log errors and crashes, and Infrastructure synthesised these findings into a unified root cause analysis.

The collective diagnosis identified a broadcast storm from a misconfigured switch flooding ARP requests across VLANs, which overwhelmed the loyalty card authentication servers' connection pools. This network-layer flooding caused the intermittent disconnections and cascading application timeouts that players experienced as slow performance and failed card reads.

The Ubuntu Value articulated by the system stated: "The collective approach revealed your problem was a cascading failure invisible to any single specialist. Network saw connectivity issues but not the app impact, App saw timeouts but not the network cause, and only Infrastructure could connect these dots across domains. Together we traced the complete failure chain from physical network misconfiguration to player-facing symptoms, which no individual expert could have fully diagnosed alone."

This empirical validation directly supports P07's assertion that Ubuntu represents "remembering who we are" rather than creating something new. The system operationalised collective problem-solving, knowledge sharing, and consensus building precisely as interview participants described authentic Ubuntu practice should function.

---

## 📊 FIGURES CHECKLIST

| Figure | Location | Status |
|--------|----------|--------|
| Figure 4.1: DSR Methodology Process | Chapter 4 | ⚠️ Verify exists |
| Figure 4.2: UGENTIC Architecture | Chapter 4 | ⚠️ Verify exists |
| Figure 5.1: Participant Distribution | Chapter 5 | ⚠️ Verify exists |
| Figure 5.2: Theme Support Strength | Chapter 5 | ⚠️ Verify exists |
| Figure 5.3: RQ Coverage Matrix | Chapter 5 | ⚠️ Verify exists |
| **NEW: Figure 5.4: UGENTIC Test Flow** | Chapter 5 | ❌ Add (from test) |

**Action:** Insert screenshot of UGENTIC test output as Figure 5.4

---

## 📚 CITATION VERIFICATION

### Check All Citations Are 2020-2025

Run through References section and verify:
- [ ] No sources before 2020
- [ ] All in-text citations exist in References
- [ ] All References entries are cited in-text
- [ ] Harvard format correct

### Key Citations to Verify:
- Mhlambi (2020) ✅
- Moore (2025) ✅
- Krishnan (2025) ✅
- Braun & Clarke (2024) ✅
- Mutswiri et al. (2025) ✅

---

## 🔍 FIND & REMOVE

### Em-dashes and Special Characters
- Find: — (em-dash)
- Replace with: , or ; or . (context-dependent)

### Informal Language to Formalise
| Find | Replace |
|------|---------|
| "can't" | "cannot" |
| "don't" | "do not" |
| "won't" | "will not" |
| "it's" (contraction) | "it is" |
| "what's" | "what is" |

---

## ✅ FINAL PROOFREADING CHECKLIST

### Before Submission:

**Structure**
- [ ] 1.1 Introduction before 1.2 Background
- [ ] 1.4 Questions before 1.5 Objectives (per Jemini)
- [ ] No duplicate section headings
- [ ] All sections numbered correctly
- [ ] Table of Contents regenerated

**Formatting**
- [ ] Times New Roman 12pt
- [ ] 1.5 line spacing
- [ ] 2.54cm margins
- [ ] Page numbers in footer
- [ ] Headings styled consistently

**Language**
- [ ] All SA English spellings (-ise, -our, -re)
- [ ] No contractions
- [ ] No bullet points in body text
- [ ] Formal academic tone throughout

**Citations**
- [ ] All 2020-2025
- [ ] Harvard format
- [ ] In-text matches References
- [ ] References alphabetised

**Content**
- [ ] UGENTIC test results added to Chapter 5
- [ ] All figures properly placed and numbered
- [ ] Tables formatted consistently
- [ ] Definitions only in Key Terms section

**Final Steps**
- [ ] Sign Declaration
- [ ] Insert Ethics Clearance Letter (Appendix A)
- [ ] Regenerate Table of Contents
- [ ] Export to PDF
- [ ] Final read-through

---

## 🔗 Related
- [[00_COMMAND_CENTER]]
- [[Sample Dissertation Structure]]
- [[Jemini Feedback Tracker]]
- [[UGENTIC Test Scenarios]]