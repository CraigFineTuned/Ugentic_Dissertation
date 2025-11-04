"""
Collaboration Triage Engine (SESSION 30 + SESSION 31 FIX)
Upfront detection of multi-domain issues before investigation starts

SESSION 30 OPTIMIZATION:
- Detect multi-domain complexity BEFORE solo investigation
- Skip wasteful investigation cycles for obvious multi-domain issues
- Expected improvement: 50% cycle reduction (5 cycles → 2-3 cycles)

SESSION 31 FIX:
- Fixed KeyError: 'matches' in _build_orchestration_reason method
- Heuristic categories (long_description, multi_sentence) now properly skipped
"""

import logging
from typing import Tuple, List, Dict, Any


class CollaborationTriageEngine:
    """
    Upfront Multi-Domain Detection Engine
    
    Purpose: Identify issues requiring immediate Ubuntu orchestration
    BEFORE starting solo investigation (optimization for Session 29 finding)
    
    Philosophy:
    Some problems are OBVIOUSLY multi-domain from the problem statement alone.
    Real IT managers recognize these patterns instantly and assemble teams
    upfront rather than attempting solo investigation first.
    
    Example patterns:
    - "Finance app crashing for entire department" → Department-wide = multi-domain
    - "Integration between HR system and payroll failing" → Integration = multi-domain
    - "Since server upgrade, multiple applications affected" → Cascading = multi-domain
    """
    
    def __init__(self):
        """Initialize collaboration triage engine with pattern definitions"""
        
        # Define multi-domain indicators (patterns that signal complexity)
        self.multi_domain_patterns = {
            # Department/team-wide issues (affects many users)
            'department_wide': [
                'entire department', 'all users', 'whole team', 'everyone in',
                'entire team', 'whole department', 'all staff', 'everyone',
                'finance team', 'finance department', 'hr department', 
                'hr team', 'marketing team', 'sales department',
                'accounting team', 'it department', 'operations team',
                'division', 'business unit', 'all employees', 'company-wide'
            ],
            
            # Multiple systems mentioned (cross-domain indicators)
            'multiple_systems': [
                'and', 'both', 'between', 'integration',
                'connection between', 'sync between', 'linked',
                'app and server', 'application and database',
                'network and application', 'server and network',
                'email and vpn', 'multiple systems', 'several systems',
                'various applications', 'different services'
            ],
            
            # Cascading/ripple effects (systemic issues)
            'cascading_failure': [
                'ripple effect', 'affecting multiple', 'spread to',
                'impacting', 'cascading', 'domino effect',
                'since server', 'after server', 'since upgrade',
                'after update', 'after patch', 'after maintenance',
                'everything', 'widespread', 'systemic', 'across'
            ],
            
            # Data synchronization/integration (classic multi-domain)
            'data_sync': [
                'synchronization', 'sync', 'syncing', 'synch',
                'integration', 'integrating', 'data flow',
                'data transfer', 'replication', 'mirroring',
                'hr system', 'payroll system', 'crm system',
                'erp', 'active directory', 'ldap', 'sso',
                'single sign-on', 'federation', 'provisioning'
            ],
            
            # Complex/unusual descriptions (ambiguity signals)
            'complexity_signals': [
                'strange', 'unusual', 'weird', 'odd', 'mysterious',
                'complex', 'complicated', 'difficult to explain',
                'hard to describe', 'intermittent', 'random',
                'sometimes works', 'unpredictable', 'sporadic'
            ]
        }
        
        # Pattern weights (some patterns are stronger indicators than others)
        self.pattern_weights = {
            'department_wide': 2.0,      # Strong indicator (whole team affected)
            'multiple_systems': 1.5,     # Strong indicator (cross-domain)
            'cascading_failure': 2.0,    # Strong indicator (systemic)
            'data_sync': 1.8,            # Strong indicator (integration)
            'complexity_signals': 1.0    # Moderate indicator (ambiguity)
        }
        
        # Confidence thresholds
        self.HIGH_CONFIDENCE_THRESHOLD = 2.0    # Score >= 2.0 → immediate orchestration
        self.MEDIUM_CONFIDENCE_THRESHOLD = 1.5   # Score >= 1.5 → consider orchestration
        
        logging.info("✨ CollaborationTriageEngine initialized (SESSION 30 + SESSION 31 FIX)")
        logging.info(f"   Pattern categories: {len(self.multi_domain_patterns)}")
        logging.info(f"   High confidence threshold: {self.HIGH_CONFIDENCE_THRESHOLD}")
    
    def should_orchestrate_immediately(self, problem_report: str) -> Tuple[bool, str, float]:
        """
        Determine if problem requires immediate Ubuntu orchestration
        
        Args:
            problem_report: User's problem description
            
        Returns:
            Tuple of (should_orchestrate, reason, confidence_score)
        """
        try:
            problem_lower = problem_report.lower()
            
            # Analyze patterns
            matched_patterns = {}
            total_score = 0.0
            
            # Check each pattern category
            for category, keywords in self.multi_domain_patterns.items():
                matches = [kw for kw in keywords if kw in problem_lower]
                if matches:
                    weight = self.pattern_weights.get(category, 1.0)
                    category_score = len(matches) * weight
                    total_score += category_score
                    
                    matched_patterns[category] = {
                        'matches': matches[:3],  # Top 3 matches for brevity
                        'count': len(matches),
                        'weight': weight,
                        'score': category_score
                    }
            
            # Add heuristic scores (complexity indicators)
            word_count = len(problem_report.split())
            if word_count > 40:
                total_score += 0.5
                matched_patterns['long_description'] = {'score': 0.5}  # No 'matches' key!
            
            sentence_count = problem_report.count('.') + problem_report.count('?')
            if sentence_count >= 3:
                total_score += 0.3
                matched_patterns['multi_sentence'] = {'score': 0.3}  # No 'matches' key!
            
            # Make decision based on confidence thresholds
            if total_score >= self.HIGH_CONFIDENCE_THRESHOLD:
                reason = self._build_orchestration_reason(matched_patterns, "high")
                return (True, reason, total_score)
            elif total_score >= self.MEDIUM_CONFIDENCE_THRESHOLD:
                reason = self._build_orchestration_reason(matched_patterns, "medium")
                return (True, reason, total_score)
            else:
                reason = "No strong multi-domain indicators. Single-domain investigation appropriate."
                return (False, reason, total_score)
        
        except Exception as e:
            logging.error(f"[FATAL] Exception in should_orchestrate_immediately: {e}", exc_info=True)
            # Fallback to safe delegation (don't block system if triage fails)
            return (False, "Error during triage analysis.", 0.0)
    
    def _build_orchestration_reason(self, matched_patterns: Dict, confidence_level: str) -> str:
        """
        Build detailed reason for orchestration recommendation
        
        SESSION 31 FIX: Properly handle heuristic categories that don't have 'matches' key
        
        Args:
            matched_patterns: Dictionary of matched pattern categories
            confidence_level: "high" or "medium"
            
        Returns:
            Human-readable explanation string
        """
        if confidence_level == "high":
            intro = "HIGH CONFIDENCE multi-domain issue detected."
        else:
            intro = "MEDIUM CONFIDENCE multi-domain complexity detected."
        
        # List detected patterns (skip heuristic categories)
        pattern_descriptions = []
        for category, details in matched_patterns.items():
            # SESSION 31 FIX: Skip heuristic categories - they don't have 'matches' key
            if category in ['long_description', 'multi_sentence']:
                continue
            
            # Only process pattern categories that have 'matches' key
            if 'matches' in details and 'count' in details:
                examples = ', '.join(details['matches'])
                pattern_descriptions.append(f"{category} ({details['count']} matches): '{examples}'")
        
        # Build reason string
        if pattern_descriptions:
            patterns_str = "; ".join(pattern_descriptions[:3])  # Limit to top 3 for readability
            reason = f"{intro} Indicators: {patterns_str}. Immediate Ubuntu orchestration recommended to avoid wasteful solo investigation cycles."
        else:
            # Fallback if only heuristic patterns matched (long description, multiple sentences)
            reason = f"{intro} Complexity indicators detected. Immediate Ubuntu orchestration recommended to avoid wasteful solo investigation cycles."
        
        return reason
    
    def analyze_problem_complexity(self, problem_report: str) -> Dict[str, Any]:
        """
        Comprehensive complexity analysis (for logging/debugging)
        
        Returns detailed breakdown of pattern matches and scores.
        Useful for understanding triage decisions and tuning thresholds.
        
        Args:
            problem_report: User's problem description
            
        Returns:
            Dictionary with detailed analysis
        """
        should_orchestrate, reason, score = self.should_orchestrate_immediately(problem_report)
        
        problem_lower = problem_report.lower()
        pattern_analysis = {}
        
        for category, keywords in self.multi_domain_patterns.items():
            matches = [kw for kw in keywords if kw in problem_lower]
            if matches:
                pattern_analysis[category] = {
                    'matches': matches,
                    'count': len(matches),
                    'weight': self.pattern_weights.get(category, 1.0)
                }
        
        return {
            'should_orchestrate': should_orchestrate,
            'reason': reason,
            'confidence_score': score,
            'threshold_high': self.HIGH_CONFIDENCE_THRESHOLD,
            'threshold_medium': self.MEDIUM_CONFIDENCE_THRESHOLD,
            'pattern_analysis': pattern_analysis,
            'word_count': len(problem_report.split()),
            'decision': 'IMMEDIATE_ORCHESTRATION' if should_orchestrate else 'SOLO_INVESTIGATION'
        }
    
    def get_status(self) -> Dict[str, Any]:
        """Get triage engine status"""
        return {
            "engine": "CollaborationTriageEngine",
            "optimization": "SESSION 30 + SESSION 31 FIX",
            "pattern_categories": list(self.multi_domain_patterns.keys()),
            "high_threshold": self.HIGH_CONFIDENCE_THRESHOLD,
            "medium_threshold": self.MEDIUM_CONFIDENCE_THRESHOLD,
            "purpose": "Upfront multi-domain detection (avoid wasteful investigation cycles)"
        }
