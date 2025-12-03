# User Feedback Loop - Implementation Specification

**Document Version:** 1.0
**Created:** December 3, 2025
**Status:** DESIGN PHASE - Awaiting Code Unfreeze
**Priority:** MEDIUM (Creative Innovation #3)
**Complexity:** MEDIUM (Est. 3-5 files modified, 300-400 LOC)
**Dependencies:** Escalation Pattern Learning (optional, enhances training data)

---

## 1. EXECUTIVE SUMMARY

**Problem:**
Currently, the system measures success purely through technical metrics (resolution status, escalation count, iteration count). It has no visibility into the most important metric: **user satisfaction**. This creates blind spots:
- Was the solution actually helpful to the user?
- Did the resolution time meet user expectations?
- Was the agent's communication clear and professional?
- Would the user be satisfied with this outcome in real IT support?

**Proposed Solution:**
Implement "User Feedback Loop" - a mechanism to collect user feedback after each investigation and use it to train/improve the system. The feedback becomes part of the learning data for Escalation Pattern Learning and general system optimization.

**Business Value:**
- **User-Centric Optimization:** System learns what users actually value, not just technical completion
- **Quality Improvement:** Identify agents/approaches that lead to high satisfaction
- **Problem Detection:** Catch issues that technically "resolved" but left users unsatisfied
- **Continuous Learning:** Feedback corpus grows over time, improving recommendations

---

## 2. CURRENT STATE (NO FEEDBACK MECHANISM)

### 2.1 Existing Success Criteria

**Technical Metrics Only:**
```python
# Current investigation outcome evaluation
if result['status'] == 'RESOLVED':
    outcome = 'success'
elif result['status'] == 'ESCALATED':
    outcome = 'escalated'
else:
    outcome = 'failure'

# NO USER SATISFACTION MEASURED
```

**Problems with Technical-Only Metrics:**
1. **False Positives:** Issue marked "RESOLVED" but user still has problem
2. **Slow Resolutions:** Technically correct but took too long (user frustrated)
3. **Poor Communication:** Solution works but explanation unclear
4. **Missed Root Causes:** Symptom fixed, underlying issue remains
5. **No Quality Signal:** Can't distinguish "acceptable" from "excellent" resolutions

**Example Scenario:**
```
Issue: "Can't access shared drive"
Agent Solution: "Reset network adapter"
Technical Status: RESOLVED (adapter reset successfully)
Reality: User still can't access drive (permission issue, not network)
Current System: ✅ Success (incorrect!)
With Feedback: ❌ User reports "still not working" → Flags for review
```

---

## 3. PROPOSED FEEDBACK SYSTEM

### 3.1 Feedback Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                  Investigation Complete                     │
│              User Issue → Resolution/Escalation             │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│                  Feedback Collection                        │
│  • Satisfaction rating (1-5 stars)                          │
│  • Resolution effectiveness (did it work?)                  │
│  • Time satisfaction (fast enough?)                         │
│  • Optional comments                                        │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│                  Feedback Analysis                          │
│  • Calculate satisfaction scores per agent/category         │
│  • Identify low-satisfaction patterns                       │
│  • Detect false-positive resolutions                        │
│  • Extract improvement insights                             │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│                  System Optimization                        │
│  • Weight outcomes by satisfaction (learning)               │
│  • Flag investigations for review                           │
│  • Adjust agent strategies                                  │
│  • Generate quality reports                                 │
└─────────────────────────────────────────────────────────────┘
```

### 3.2 Feedback Collection Modes

**Mode 1: Interactive (Real User)**
- Prompt user after investigation completes
- Simple 1-5 star rating + optional comment
- Quick (< 30 seconds to provide feedback)

**Mode 2: Simulated (Evaluation)**
- Use LLM to evaluate solution quality
- Compare agent's solution to expected best practice
- Useful for testing/validation without real users

**Mode 3: Delayed (Follow-Up)**
- Re-prompt user after 24 hours
- "Did the solution work long-term?"
- Catches issues that resurface

---

## 4. DETAILED DESIGN

### 4.1 Data Model

**Feedback Record**
```python
@dataclass
class UserFeedback:
    """User feedback for completed investigation"""
    id: str
    investigation_id: str  # Links to investigation outcome
    timestamp: datetime

    # Core feedback
    satisfaction_rating: int  # 1-5 stars
    resolution_effective: bool  # "Did this solve your problem?"
    resolution_time_acceptable: bool  # "Was resolution time reasonable?"

    # Optional detailed feedback
    communication_rating: Optional[int]  # 1-5, clarity of explanation
    would_recommend: Optional[bool]  # "Would you recommend this to colleagues?"
    comment: Optional[str]  # Free-form feedback

    # Context
    user_id: str
    agent_name: str
    problem_category: str
    resolution_type: str  # "resolved_level1", "escalated", etc.

    # Metadata
    feedback_mode: str  # "interactive", "simulated", "delayed"
    response_time_seconds: int  # Time user took to provide feedback
```

**Feedback Aggregate**
```python
@dataclass
class FeedbackAggregate:
    """Aggregated feedback statistics"""
    category: str  # "printer", "vpn", "email", etc.
    agent_name: Optional[str]  # Specific agent or all
    time_period: str  # "last_7_days", "last_30_days", "all_time"

    # Satisfaction metrics
    avg_satisfaction: float  # 1.0-5.0
    satisfaction_distribution: Dict[int, int]  # {1: 5, 2: 10, 3: 20, 4: 30, 5: 35}

    # Effectiveness metrics
    resolution_effective_rate: float  # % that actually solved problem
    false_positive_rate: float  # % marked resolved but weren't

    # Performance metrics
    avg_resolution_time: int  # Seconds
    time_satisfaction_rate: float  # % satisfied with speed

    # Quality metrics
    avg_communication_rating: float
    recommendation_rate: float  # % that would recommend

    # Sample data
    total_feedback_count: int
    sample_comments: List[str]  # Top 5 representative comments

    # Trends
    trend: str  # "improving", "stable", "declining"
    comparison_to_baseline: float  # +/- % vs system average
```

**Quality Alert**
```python
@dataclass
class QualityAlert:
    """Alert for low-quality investigations requiring review"""
    id: str
    investigation_id: str
    timestamp: datetime

    # Alert criteria
    alert_type: str  # "low_satisfaction", "false_positive", "timeout", "negative_comment"
    severity: str  # "low", "medium", "high", "critical"

    # Details
    satisfaction_rating: int
    user_comment: Optional[str]
    agent_name: str
    problem_category: str

    # Recommended action
    recommended_action: str  # "review_solution", "retrain_agent", "update_knowledge_base"
    status: str  # "pending", "reviewed", "resolved", "dismissed"
```

---

### 4.2 Architecture & Integration

**Modified Files:**

**1. `src/ugentic/core/feedback_collector.py` (NEW)**
```python
class FeedbackCollector:
    """
    Collects user feedback after investigations
    Supports multiple collection modes
    """

    def __init__(self, storage_backend='sqlite'):
        self.storage = self._init_storage(storage_backend)
        self.logger = logging.getLogger('feedback_collector')
        self.collection_mode = 'interactive'  # or 'simulated' for testing

    def collect_feedback_interactive(self, investigation: Dict) -> Optional[UserFeedback]:
        """
        Prompt user for feedback after investigation completes

        Args:
            investigation: Complete investigation data

        Returns:
            UserFeedback object or None if user declined
        """
        print("\n" + "="*60)
        print("INVESTIGATION COMPLETE - Please provide feedback")
        print("="*60)
        print(f"Issue: {investigation['problem_report'][:80]}...")
        print(f"Resolution: {investigation.get('solution', 'Escalated')[:80]}...")
        print()

        # Core question: Satisfaction rating
        satisfaction = self._prompt_rating(
            "How satisfied are you with this resolution?",
            scale=5
        )

        # Effectiveness check
        effective = self._prompt_yes_no(
            "Did this solution actually solve your problem?"
        )

        # Time satisfaction
        time_acceptable = self._prompt_yes_no(
            f"Was the resolution time ({investigation.get('duration', 0)}s) acceptable?"
        )

        # Optional comment
        comment = input("\nOptional: Any additional feedback? (press Enter to skip): ").strip()
        if not comment:
            comment = None

        feedback = UserFeedback(
            id=str(uuid.uuid4()),
            investigation_id=investigation['id'],
            timestamp=datetime.now(),
            satisfaction_rating=satisfaction,
            resolution_effective=effective,
            resolution_time_acceptable=time_acceptable,
            comment=comment,
            user_id=investigation.get('user', 'unknown'),
            agent_name=investigation['agent_name'],
            problem_category=investigation.get('category', 'unknown'),
            resolution_type=investigation.get('status', 'unknown'),
            feedback_mode='interactive',
            response_time_seconds=0  # Could track this
        )

        self.storage.save(feedback)
        print("\n✅ Thank you for your feedback!\n")
        return feedback

    def collect_feedback_simulated(self, investigation: Dict) -> UserFeedback:
        """
        Use LLM to simulate user feedback (for testing/evaluation)

        Evaluates solution quality and generates realistic feedback
        """
        prompt = f"""You are evaluating IT support quality.

ISSUE: {investigation['problem_report']}

AGENT'S SOLUTION: {investigation.get('solution', 'Escalated to specialist')}

ACTIONS TAKEN: {', '.join(investigation.get('tools_used', []))}

TIME TO RESOLVE: {investigation.get('duration', 0)} seconds
ITERATIONS: {investigation.get('iterations', 0)}

Rate this resolution (1-5 stars):
1 = Completely unhelpful/wrong
2 = Partially helpful but issues remain
3 = Acceptable, solved problem
4 = Good, solved problem efficiently
5 = Excellent, fast and thorough

Also answer:
- Did this likely solve the actual problem? (yes/no)
- Was resolution time reasonable? (yes/no)
- Brief comment (user perspective, 1 sentence)

Return JSON format:
{{
  "satisfaction_rating": <1-5>,
  "resolution_effective": <true/false>,
  "resolution_time_acceptable": <true/false>,
  "comment": "<user comment>"
}}"""

        # Call LLM to evaluate
        response = self.llm_client.generate(prompt)
        feedback_data = json.loads(response)

        feedback = UserFeedback(
            id=str(uuid.uuid4()),
            investigation_id=investigation['id'],
            timestamp=datetime.now(),
            satisfaction_rating=feedback_data['satisfaction_rating'],
            resolution_effective=feedback_data['resolution_effective'],
            resolution_time_acceptable=feedback_data['resolution_time_acceptable'],
            comment=feedback_data.get('comment'),
            user_id=investigation.get('user', 'simulated'),
            agent_name=investigation['agent_name'],
            problem_category=investigation.get('category', 'unknown'),
            resolution_type=investigation.get('status', 'unknown'),
            feedback_mode='simulated',
            response_time_seconds=0
        )

        self.storage.save(feedback)
        return feedback

    def _prompt_rating(self, question: str, scale: int = 5) -> int:
        """Helper: Prompt user for numeric rating"""
        while True:
            try:
                print(f"\n{question}")
                print(f"(1 = Very Unsatisfied, {scale} = Very Satisfied)")
                rating = int(input(f"Rating (1-{scale}): "))
                if 1 <= rating <= scale:
                    return rating
                print(f"Please enter a number between 1 and {scale}")
            except ValueError:
                print("Please enter a valid number")

    def _prompt_yes_no(self, question: str) -> bool:
        """Helper: Prompt user for yes/no response"""
        while True:
            response = input(f"\n{question} (y/n): ").strip().lower()
            if response in ['y', 'yes']:
                return True
            elif response in ['n', 'no']:
                return False
            print("Please enter 'y' or 'n'")
```

**2. `src/ugentic/core/feedback_analyzer.py` (NEW)**
```python
class FeedbackAnalyzer:
    """
    Analyzes feedback to identify patterns and quality issues
    Generates aggregates and alerts
    """

    def __init__(self, feedback_collector: FeedbackCollector):
        self.feedback_collector = feedback_collector
        self.logger = logging.getLogger('feedback_analyzer')

        # Thresholds for alerts
        self.low_satisfaction_threshold = 2.5  # Avg rating below this = alert
        self.false_positive_threshold = 0.3  # >30% ineffective = alert

    def calculate_aggregate(self, category: str = None,
                           agent_name: str = None,
                           time_period: str = "last_30_days") -> FeedbackAggregate:
        """
        Calculate aggregated feedback statistics

        Args:
            category: Filter by problem category (or None for all)
            agent_name: Filter by agent (or None for all)
            time_period: Time window for analysis
        """
        # Get all feedback matching filters
        feedbacks = self._get_filtered_feedback(category, agent_name, time_period)

        if not feedbacks:
            return None  # No data

        # Calculate satisfaction metrics
        ratings = [f.satisfaction_rating for f in feedbacks]
        avg_satisfaction = np.mean(ratings)
        satisfaction_dist = {i: ratings.count(i) for i in range(1, 6)}

        # Calculate effectiveness metrics
        effective_count = sum(1 for f in feedbacks if f.resolution_effective)
        resolution_effective_rate = effective_count / len(feedbacks)
        false_positive_rate = 1.0 - resolution_effective_rate

        # Calculate time metrics
        time_satisfied_count = sum(1 for f in feedbacks if f.resolution_time_acceptable)
        time_satisfaction_rate = time_satisfied_count / len(feedbacks)

        # Detect trend (compare to previous period)
        previous_period_avg = self._get_previous_period_avg(category, agent_name, time_period)
        if previous_period_avg:
            if avg_satisfaction > previous_period_avg + 0.3:
                trend = "improving"
            elif avg_satisfaction < previous_period_avg - 0.3:
                trend = "declining"
            else:
                trend = "stable"
        else:
            trend = "insufficient_data"

        aggregate = FeedbackAggregate(
            category=category or "all",
            agent_name=agent_name,
            time_period=time_period,
            avg_satisfaction=avg_satisfaction,
            satisfaction_distribution=satisfaction_dist,
            resolution_effective_rate=resolution_effective_rate,
            false_positive_rate=false_positive_rate,
            time_satisfaction_rate=time_satisfaction_rate,
            total_feedback_count=len(feedbacks),
            sample_comments=self._get_sample_comments(feedbacks, n=5),
            trend=trend,
            comparison_to_baseline=avg_satisfaction - 3.5  # 3.5 is baseline "acceptable"
        )

        return aggregate

    def generate_quality_alerts(self) -> List[QualityAlert]:
        """
        Identify investigations requiring review due to quality issues

        Returns list of QualityAlert objects
        """
        alerts = []

        # Get recent low-satisfaction feedback
        recent_feedback = self._get_filtered_feedback(
            category=None,
            agent_name=None,
            time_period="last_7_days"
        )

        for feedback in recent_feedback:
            # Alert Type 1: Low satisfaction rating
            if feedback.satisfaction_rating <= 2:
                severity = "high" if feedback.satisfaction_rating == 1 else "medium"
                alerts.append(QualityAlert(
                    id=str(uuid.uuid4()),
                    investigation_id=feedback.investigation_id,
                    timestamp=datetime.now(),
                    alert_type="low_satisfaction",
                    severity=severity,
                    satisfaction_rating=feedback.satisfaction_rating,
                    user_comment=feedback.comment,
                    agent_name=feedback.agent_name,
                    problem_category=feedback.problem_category,
                    recommended_action="review_solution",
                    status="pending"
                ))

            # Alert Type 2: False positive (marked resolved but wasn't)
            if not feedback.resolution_effective and feedback.resolution_type == "resolved_level1":
                alerts.append(QualityAlert(
                    id=str(uuid.uuid4()),
                    investigation_id=feedback.investigation_id,
                    timestamp=datetime.now(),
                    alert_type="false_positive",
                    severity="high",
                    satisfaction_rating=feedback.satisfaction_rating,
                    user_comment=feedback.comment,
                    agent_name=feedback.agent_name,
                    problem_category=feedback.problem_category,
                    recommended_action="review_solution",
                    status="pending"
                ))

            # Alert Type 3: Negative comment
            if feedback.comment and self._is_negative_comment(feedback.comment):
                alerts.append(QualityAlert(
                    id=str(uuid.uuid4()),
                    investigation_id=feedback.investigation_id,
                    timestamp=datetime.now(),
                    alert_type="negative_comment",
                    severity="medium",
                    satisfaction_rating=feedback.satisfaction_rating,
                    user_comment=feedback.comment,
                    agent_name=feedback.agent_name,
                    problem_category=feedback.problem_category,
                    recommended_action="review_solution",
                    status="pending"
                ))

        return alerts

    def _is_negative_comment(self, comment: str) -> bool:
        """Detect negative sentiment in comment"""
        negative_keywords = [
            'still not working', 'didn\'t help', 'made it worse',
            'waste of time', 'unhelpful', 'wrong solution',
            'problem persists', 'not fixed', 'still broken'
        ]
        comment_lower = comment.lower()
        return any(keyword in comment_lower for keyword in negative_keywords)
```

**3. `src/ugentic/core/feedback_trainer.py` (NEW)**
```python
class FeedbackTrainer:
    """
    Uses feedback to improve system performance
    Integrates with Escalation Pattern Learning
    """

    def __init__(self, feedback_analyzer: FeedbackAnalyzer,
                 outcome_tracker: 'OutcomeTracker'):
        self.feedback_analyzer = feedback_analyzer
        self.outcome_tracker = outcome_tracker
        self.logger = logging.getLogger('feedback_trainer')

    def weight_outcomes_by_satisfaction(self) -> None:
        """
        Adjust learning weights based on user satisfaction

        High-satisfaction resolutions weighted more heavily
        Low-satisfaction resolutions weighted less or excluded
        """
        # Get all investigations with feedback
        investigations_with_feedback = self._get_investigations_with_feedback()

        for inv_id, feedback in investigations_with_feedback:
            # Calculate weight based on satisfaction (1-5 → 0.2-1.0)
            weight = feedback.satisfaction_rating / 5.0

            # Boost weight if resolution was effective
            if feedback.resolution_effective:
                weight *= 1.2

            # Reduce weight if resolution ineffective (false positive)
            if not feedback.resolution_effective:
                weight *= 0.3

            # Update outcome record with satisfaction weight
            self.outcome_tracker.update_weight(inv_id, weight)

            logging.info(f"Investigation {inv_id}: satisfaction={feedback.satisfaction_rating}, weight={weight:.2f}")

    def generate_improvement_recommendations(self) -> List[Dict]:
        """
        Analyze feedback patterns and suggest improvements

        Returns list of actionable recommendations
        """
        recommendations = []

        # Analyze per-agent performance
        for agent_name in ['IT Support', 'Network Support', 'Application Support', 'Infrastructure']:
            aggregate = self.feedback_analyzer.calculate_aggregate(
                agent_name=agent_name,
                time_period="last_30_days"
            )

            if not aggregate or aggregate.total_feedback_count < 10:
                continue  # Not enough data

            # Recommendation: Low satisfaction agent
            if aggregate.avg_satisfaction < 3.0:
                recommendations.append({
                    'type': 'low_satisfaction_agent',
                    'agent': agent_name,
                    'current_rating': aggregate.avg_satisfaction,
                    'recommendation': f'Review {agent_name} decision logic and tool selection',
                    'priority': 'high'
                })

            # Recommendation: High false positive rate
            if aggregate.false_positive_rate > 0.3:
                recommendations.append({
                    'type': 'high_false_positive_rate',
                    'agent': agent_name,
                    'false_positive_rate': aggregate.false_positive_rate,
                    'recommendation': f'{agent_name} marking issues resolved prematurely - adjust completion criteria',
                    'priority': 'high'
                })

            # Recommendation: Time dissatisfaction
            if aggregate.time_satisfaction_rate < 0.7:
                recommendations.append({
                    'type': 'slow_resolution',
                    'agent': agent_name,
                    'time_satisfaction_rate': aggregate.time_satisfaction_rate,
                    'recommendation': f'{agent_name} taking too long - optimize iteration count or escalate faster',
                    'priority': 'medium'
                })

        # Analyze per-category performance
        for category in ['printer', 'vpn', 'email', 'account', 'network']:
            aggregate = self.feedback_analyzer.calculate_aggregate(
                category=category,
                time_period="last_30_days"
            )

            if not aggregate or aggregate.total_feedback_count < 5:
                continue

            if aggregate.avg_satisfaction < 3.0:
                recommendations.append({
                    'type': 'low_satisfaction_category',
                    'category': category,
                    'current_rating': aggregate.avg_satisfaction,
                    'recommendation': f'Review knowledge base and tools for {category} issues',
                    'priority': 'medium'
                })

        return recommendations
```

**4. `app.py` (MODIFIED) - Integration Point**
```python
# Add feedback collection after investigation completes

def main():
    # ... existing setup ...

    # NEW: Initialize feedback system
    feedback_enabled = config.get('features', {}).get('user_feedback', {}).get('enabled', False)

    if feedback_enabled:
        feedback_collector = FeedbackCollector()
        feedback_analyzer = FeedbackAnalyzer(feedback_collector)
        feedback_trainer = FeedbackTrainer(feedback_analyzer, outcome_tracker)

    while True:
        user_input = input("\nDescribe your IT issue: ")

        # Process investigation (existing logic)
        result = process_request(user_input)

        # NEW: Collect feedback
        if feedback_enabled:
            investigation_data = {
                'id': result['investigation_id'],
                'problem_report': user_input,
                'solution': result.get('solution', 'Escalated'),
                'status': result['status'],
                'agent_name': result['agent_name'],
                'tools_used': result.get('tools_used', []),
                'iterations': result.get('iterations', 0),
                'duration': result.get('duration_seconds', 0),
                'category': result.get('category', 'unknown')
            }

            # Collect feedback based on mode
            mode = config.get('features', {}).get('user_feedback', {}).get('mode', 'interactive')

            if mode == 'interactive':
                feedback = feedback_collector.collect_feedback_interactive(investigation_data)
            elif mode == 'simulated':
                feedback = feedback_collector.collect_feedback_simulated(investigation_data)

            # Log feedback
            if feedback:
                logging.info(f"Feedback collected: satisfaction={feedback.satisfaction_rating}/5, effective={feedback.resolution_effective}")
```

---

## 5. IMPLEMENTATION PHASES

### Phase 1: Basic Feedback Collection (Priority: HIGH)
**Time Estimate:** 2-3 hours

**Tasks:**
- [ ] Create `feedback_collector.py` with interactive mode
- [ ] Integrate with app.py (prompt after investigation)
- [ ] Create database schema for feedback records
- [ ] Implement simple 1-5 rating + effectiveness question
- [ ] Add feature toggle in config.json

**Success Criteria:**
- Feedback collected after each investigation
- Data stored in database
- User experience smooth (< 30 seconds to provide feedback)

---

### Phase 2: Simulated Feedback (Priority: HIGH)
**Time Estimate:** 2-3 hours

**Tasks:**
- [ ] Implement LLM-based feedback simulation
- [ ] Create evaluation prompts for solution quality
- [ ] Add simulated mode to config
- [ ] Test on existing investigation logs
- [ ] Validate simulated ratings vs expected quality

**Success Criteria:**
- Simulated feedback generated for any investigation
- Ratings correlate with solution quality (manual validation)
- Useful for testing without real users

---

### Phase 3: Feedback Analysis (Priority: HIGH)
**Time Estimate:** 2-3 hours

**Tasks:**
- [ ] Create `feedback_analyzer.py`
- [ ] Implement aggregate calculation per agent/category
- [ ] Create quality alert generation
- [ ] Build dashboard/reporting (optional CLI)
- [ ] Generate sample analytics reports

**Success Criteria:**
- Aggregates calculated correctly
- Alerts generated for low satisfaction (<3.0 avg)
- False positives detected (marked resolved but ineffective)

---

### Phase 4: Integration with Learning System (Priority: MEDIUM)
**Time Estimate:** 2-3 hours

**Tasks:**
- [ ] Create `feedback_trainer.py`
- [ ] Integrate with Outcome Tracker (weight by satisfaction)
- [ ] Modify Pattern Learning to consider satisfaction
- [ ] Generate improvement recommendations
- [ ] Test that high-satisfaction patterns preferred

**Success Criteria:**
- Outcome weights adjusted by feedback
- Pattern Learning prioritizes high-satisfaction approaches
- Low-satisfaction patterns flagged/avoided

---

### Phase 5: Advanced Features (Priority: LOW)
**Time Estimate:** 3-4 hours

**Tasks:**
- [ ] Delayed feedback collection (24-hour follow-up)
- [ ] Communication quality rating (separate metric)
- [ ] Sentiment analysis on comments (NLP)
- [ ] Feedback trends visualization
- [ ] Automated improvement actions (not just recommendations)

**Success Criteria:**
- Delayed feedback captures long-term effectiveness
- Sentiment analysis accurate (80%+ correlation with ratings)
- Trends detected early (degrading performance flagged)

---

## 6. CONFIGURATION

### 6.1 config.json Structure

```json
{
  "features": {
    "user_feedback": {
      "enabled": true,
      "mode": "interactive",
      "prompt_timing": "immediate",
      "delayed_follow_up": false,
      "delayed_follow_up_hours": 24,
      "min_satisfaction_threshold": 3.0,
      "alert_on_low_satisfaction": true
    }
  },
  "feedback": {
    "storage_backend": "sqlite",
    "database_path": "data/feedback.db",
    "simulated_llm_model": "kimi-k2-thinking:cloud",
    "require_comment": false,
    "anonymous_mode": false
  }
}
```

---

## 7. TESTING STRATEGY

### 7.1 Unit Tests

**Test 1: Feedback Collection**
```python
def test_feedback_collector_stores_feedback():
    collector = FeedbackCollector(storage_backend='memory')

    investigation = {
        'id': 'test-001',
        'problem_report': 'Printer not working',
        'solution': 'Reset print spooler',
        'status': 'resolved_level1',
        'agent_name': 'IT Support',
        'tools_used': ['check_printer_status', 'restart_print_spooler'],
        'iterations': 2,
        'duration': 120
    }

    # Simulate user input (mock stdin)
    with mock_stdin(['4', 'y', 'y', '']):  # 4 stars, yes effective, yes fast, no comment
        feedback = collector.collect_feedback_interactive(investigation)

    assert feedback.satisfaction_rating == 4
    assert feedback.resolution_effective == True
    assert feedback.resolution_time_acceptable == True
```

**Test 2: Simulated Feedback Quality**
```python
def test_simulated_feedback_detects_poor_solution():
    collector = FeedbackCollector()

    # Investigation with obviously wrong solution
    investigation = {
        'problem_report': 'User cannot access shared drive Z:',
        'solution': 'Reset network adapter',  # Wrong approach!
        'status': 'resolved_level1'
    }

    feedback = collector.collect_feedback_simulated(investigation)

    # LLM should recognize this is likely ineffective
    assert feedback.satisfaction_rating <= 2
    assert feedback.resolution_effective == False
```

**Test 3: Quality Alert Generation**
```python
def test_analyzer_generates_alert_for_low_satisfaction():
    analyzer = FeedbackAnalyzer(feedback_collector)

    # Add low-satisfaction feedback
    feedback = UserFeedback(
        investigation_id='test-002',
        satisfaction_rating=1,
        resolution_effective=False,
        comment='Didnt help at all',
        agent_name='IT Support'
    )
    feedback_collector.storage.save(feedback)

    alerts = analyzer.generate_quality_alerts()

    assert len(alerts) >= 1
    alert = next(a for a in alerts if a.investigation_id == 'test-002')
    assert alert.alert_type == 'low_satisfaction'
    assert alert.severity == 'high'
```

### 7.2 Integration Tests

**Test 4: End-to-End Feedback Loop**
```
SCENARIO: User feedback improves future resolutions

SETUP:
- Process 20 printer issues
- Collect feedback for all
- 10 have high satisfaction (4-5 stars), approach: restart spooler
- 10 have low satisfaction (1-2 stars), approach: driver reinstall

PHASE 1: Feedback Collection
1. All 20 feedbacks recorded in database
2. Aggregates show pattern difference

PHASE 2: Weighted Learning
3. Run feedback trainer
4. High-satisfaction outcomes weighted 0.8-1.0
5. Low-satisfaction outcomes weighted 0.2-0.4

PHASE 3: Pattern Recognition (Escalation Pattern Learning integration)
6. Pattern Learning discovers "restart spooler" has high satisfaction
7. Pattern Learning discovers "driver reinstall" has low satisfaction

PHASE 4: Future Investigations
8. New printer issue arrives
9. System prefers "restart spooler" approach (weighted higher)
10. Avoids "driver reinstall" unless necessary

SUCCESS CRITERIA:
✅ All feedback captured correctly
✅ Weights applied to outcomes
✅ Pattern Learning considers satisfaction
✅ Future decisions favor high-satisfaction approaches
```

**Test 5: False Positive Detection**
```
SCENARIO: System detects and corrects false-positive resolution

INVESTIGATION:
- User: "Can't access email"
- Agent: "Network connectivity restored" (reset adapter)
- Technical Status: RESOLVED
- Feedback: satisfaction=1, effective=false, comment="Still can't access email"

EXPECTED BEHAVIOR:
1. Feedback Analyzer generates "false_positive" alert (severity: high)
2. Investigation flagged for review
3. Outcome weight reduced to 0.3 (don't learn from this)
4. Alert sent to system admin (if configured)
5. Recommendation: "Review IT Support email troubleshooting logic"

SUCCESS CRITERIA:
✅ False positive detected automatically
✅ Alert generated with correct severity
✅ Outcome weight reduced
✅ Investigation excluded from positive training examples
```

---

## 8. SUCCESS METRICS

### 8.1 Feedback Quality
- **Collection Rate:** 70%+ of users provide feedback
- **Response Quality:** 50%+ provide optional comments
- **Simulated Accuracy:** 80%+ correlation with manual evaluation

### 8.2 System Improvement
- **Satisfaction Trend:** Average rating increases over time (3.5 → 4.0+ over 3 months)
- **False Positive Reduction:** 30-40% reduction in "resolved" but ineffective cases
- **Pattern Learning Enhancement:** High-satisfaction patterns weighted 2x vs low-satisfaction

### 8.3 Operational Impact
- **Quality Alerts:** 5-10% of investigations flagged for review (catches real issues)
- **Recommendation Accuracy:** 70%+ of generated recommendations actionable
- **User Trust:** Recommendation rate (would recommend) > 80%

---

## 9. RISKS & MITIGATION

### 9.1 Technical Risks

**RISK: Low feedback collection rate (users skip)**
- **Severity:** HIGH
- **Mitigation:**
  - Keep feedback quick (< 30 seconds, 2-3 questions)
  - Make feedback optional (don't block workflow)
  - Use simulated feedback as fallback
  - Gamification: "Your feedback helps improve the system!"

**RISK: Biased feedback (only angry users respond)**
- **Severity:** MEDIUM
- **Mitigation:**
  - Track response rates per satisfaction level
  - Weight by response likelihood (statistical correction)
  - Use simulated feedback to fill gaps
  - Delayed follow-up catches satisfied users

**RISK: Feedback manipulation (gaming the system)**
- **Severity:** LOW (internal system)
- **Mitigation:**
  - Outlier detection (suspicious patterns)
  - Weight by user history
  - Admin review of extreme ratings

### 9.2 Operational Risks

**RISK: Overwhelming number of quality alerts**
- **Severity:** MEDIUM
- **Mitigation:**
  - Severity-based filtering (only show high/critical)
  - Aggregation: Group similar alerts
  - Auto-dismiss: Resolved investigations
  - Configurable thresholds

**RISK: Negative feedback demotivates development**
- **Severity:** LOW
- **Mitigation:**
  - Frame as improvement opportunities
  - Show trends (improvement over time)
  - Highlight high-satisfaction cases
  - Focus on actionable insights

---

## 10. INTEGRATION WITH OTHER ENHANCEMENTS

### 10.1 Escalation Pattern Learning + Feedback
**Synergy:** Feedback provides quality signal for pattern learning

**Integration:**
- Weight outcomes by user satisfaction
- Prefer high-satisfaction patterns in threshold optimization
- Detect when escalation thresholds are too aggressive (low satisfaction)
- Learn optimal escalation timing based on user feedback

### 10.2 Consultation Mode + Feedback
**Synergy:** Measure consultation effectiveness vs full escalation

**Integration:**
- Compare satisfaction: consultations vs escalations
- Learn when consultation is sufficient (high satisfaction, no escalation needed)
- Identify consultations that should have been escalations (low satisfaction)

---

## 11. FUTURE ENHANCEMENTS

### 11.1 Advanced Analytics

**Satisfaction Prediction:**
- Train ML model to predict satisfaction before user provides it
- Early warning: "This solution likely to be unsatisfying"
- Proactive fixes before user reports dissatisfaction

**Root Cause Analysis:**
- Cluster low-satisfaction cases by root cause
- "Network Support has low satisfaction on VPN issues" → specific training need
- Generate targeted improvement plans

### 11.2 Automated Improvements

**Self-Healing:**
- Automatically adjust agent strategies based on feedback
- "Printer issues: switch from driver reinstall to spooler restart"
- No human intervention required (with safety bounds)

**Dynamic Knowledge Base:**
- Add high-satisfaction solutions to knowledge base
- Remove low-satisfaction solutions
- Continuous refinement without manual curation

---

## 12. IMPLEMENTATION CHECKLIST

**Before Implementation:**
- [ ] User approval obtained for code unfreeze
- [ ] Escalation Pattern Learning implemented (optional but beneficial)
- [ ] Database backend available
- [ ] LLM access for simulated feedback

**During Implementation:**
- [ ] Follow phased approach (Phases 1-4)
- [ ] Write unit tests for each component
- [ ] Test with simulated feedback first
- [ ] Pilot with real users (small group)
- [ ] Collect 50+ feedback samples before analysis

**After Implementation:**
- [ ] Monitor feedback collection rate (target 70%+)
- [ ] Validate simulated feedback accuracy
- [ ] Review quality alerts (ensure actionable)
- [ ] Integrate with Pattern Learning
- [ ] Generate first improvement recommendations report

---

## 13. REFERENCES

**Related Documents:**
- `docs/CONSULTATION_MODE_SPEC.md` - Priority #1 enhancement
- `docs/ESCALATION_PATTERN_LEARNING_SPEC.md` - Priority #2 enhancement (strong integration)
- `docs/SESSION_ENTRY.md` - Project nucleus
- `docs/AGENTS.md` - Current agent capabilities

**Key Concepts:**
- **User-Centric Design:** Optimize for actual user satisfaction, not just technical metrics
- **Feedback Loop:** Continuous improvement from real-world outcomes
- **Quality Signals:** Satisfaction as training signal for ML systems
- **False Positive Detection:** Catch "resolved" cases that didn't actually work

**Technologies:**
- **LLM Evaluation:** Use LLM to simulate user perspective
- **Sentiment Analysis:** NLP for comment analysis (spaCy, VADER)
- **Statistical Analysis:** NumPy/Pandas for aggregates
- **Database:** SQLite/PostgreSQL for feedback storage

---

**Document Status:** ✅ COMPLETE - Ready for Implementation Review
**Next Action:** Await user approval for code unfreeze, then proceed with Phase 1 (Basic Collection)
**Estimated Total Implementation Time:** 8-12 hours (Phases 1-4), 11-16 hours (all phases)
**Implementation Order:** After Escalation Pattern Learning (integrates with weighted outcomes)

---
*Specification authored by: Claude Sonnet 4.5*
*Project: UGENTIC - Ubuntu-Driven Multi-Agent IT Support System*
*Dissertation: Craig Vraagom (402415017)*
