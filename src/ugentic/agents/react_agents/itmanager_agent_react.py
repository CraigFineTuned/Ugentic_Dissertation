"""
IT Manager Agent - Optimized Delegation Pattern (SESSION 30)
Strategic oversight with hybrid rule-based + LLM routing

SESSION 30 OPTIMIZATION:
- Added rule-based triage for 70-80% of common issues (instant delegation)
- LLM reasoning reserved for ambiguous cases (20-30%)
- Expected improvement: 80% faster delegation (2-5s → <1s for most cases)

SESSION 31 FIX:
- Added upfront collaboration triage to detect multi-domain issues immediately
- Moves triage to IT Manager (entry point) instead of Infrastructure (too deep)
"""

import logging
import json
from typing import Dict, Any, Optional

from ...core.collaboration_triage_engine import CollaborationTriageEngine


class ITManagerAgentReAct:
    """
    IT Manager Agent - Strategic Router with Optimized Delegation
    
    Role: Strategic oversight, delegation, resource allocation
    Pattern: Hybrid routing (rule-based + LLM) - optimal efficiency
    Domain: Strategic decisions, agent coordination
    
    Ubuntu Principles:
    - Collective Problem-Solving: Ensures right agent handles each issue
    - Knowledge Sharing: Facilitates cross-team collaboration
    - Mutual Support: Supports all teams
    - Consensus Building: Strategic decisions involve teams
    
    SESSION 30 OPTIMIZATION & SESSION 31 FIX:
    - Upfront collaboration triage to detect multi-domain issues immediately (SESSION 31 FIX)
    - Rule-based delegation for clear-cut cases (instant, efficient)
    - LLM reasoning for ambiguous scenarios (flexible, adaptive)
    - Combines organizational triage practices with AI intelligence
    """
    
    def __init__(self, llm, name="IT Manager", agents=None, logger=None):
        """
        Initialize IT Manager agent with optimized delegation
        
        Args:
            llm: Language model for reasoning
            name: Agent name
            agents: Dictionary of available agents to delegate to
            logger: Investigation logger (optional)
        """
        self.name = name
        self.agent_type = "Strategic"
        self.specialization = "Strategic Oversight, Delegation, Resource Allocation"
        self.llm = llm
        self.agents = agents or {}
        self.logger = logger
        
        # Ubuntu principles
        self.ubuntu_principles = {
            "collective_problem_solving": True,
            "knowledge_sharing": True,
            "mutual_support": True,
            "consensus_building": True,
            "strategic_vision": True
        }
        
        # SESSION 31 FIX: Upfront collaboration triage
        self.triage_engine = CollaborationTriageEngine()
        self.orchestrator = None  # Will be set after Infrastructure is created
        
        # SESSION 30: Rule-based triage patterns (mirrors real IT department triage)
        self.triage_rules = {
            'IT Support': [
                # User account issues
                'password', 'login', 'locked', 'unlock', 'account', 'locked out',
                'cannot log', 'cant log', 'sign in', 'authentication',
                # Device/printer issues
                'printer', 'print', 'printing', 'cant print', 'cannot print',
                # Email basics
                'email config', 'outlook', 'email setup', 'email client',
                # Access issues
                'permissions', 'access denied', 'cant access', 'cannot access',
                'permission denied', 'no access',
                # Remote access
                'remote access', 'vpn', 'remote desktop', 'rdp',
                # Software basics
                'software install', 'install software', 'program install'
            ],
            'Network Support': [
                # Connectivity
                'network', 'connectivity', 'internet', 'wifi', 'wireless',
                'ethernet', 'cant connect', 'cannot connect', 'connection',
                # Network services
                'dns', 'domain name', 'name resolution', 'resolve',
                # Security
                'firewall', 'blocked', 'port', 'firewall rule',
                # Network issues
                'slow network', 'network slow', 'latency', 'ping',
                'bandwidth', 'speed', 'traceroute',
                # Infrastructure
                'router', 'switch', 'gateway', 'subnet'
            ],
            'App Support': [
                # Application issues
                'application', 'app', 'software', 'program',
                # Errors
                'crash', 'crashing', 'error', 'bug', 'exception',
                'error message', 'application error',
                # Performance
                'slow performance', 'app slow', 'slow app', 'hanging',
                'freeze', 'frozen', 'not responding',
                # Database
                'database', 'query', 'sql', 'data',
                # Business apps
                'report', 'dashboard', 'form', 'workflow'
            ],
            'Infrastructure': [
                # Server issues
                'server', 'servers', 'server down', 'server problem',
                # Resources
                'cpu', 'memory', 'disk', 'storage', 'ram',
                'disk space', 'out of space', 'full disk',
                # Services
                'service', 'service down', 'service not running',
                'daemon', 'process',
                # Backup/system
                'backup', 'restore', 'recovery',
                # Virtualization
                'virtual machine', 'vm', 'container', 'docker',
                # System
                'system', 'uptime', 'reboot', 'restart'
            ]
        }
        
        logging.info(f"✨ {self.name} Agent initialized (SESSION 30/31 OPTIMIZED)")
        logging.info(f"   Available agents: {list(self.agents.keys())}")
        logging.info(f"   🎯 Upfront Triage: PENDING LINK")
        logging.info(f"   🎯 Rule-based triage: ENABLED (70-80% instant delegation)")
        logging.info(f"   🤖 LLM fallback: ENABLED (20-30% ambiguous cases)")

    def set_orchestrator(self, orchestrator):
        """
        Set orchestrator reference after Infrastructure agent is created.
        
        SESSION 31 FIX: Enables upfront triage at the delegation layer.
        This allows IT Manager to detect multi-domain issues and skip delegation,
        routing directly to Infrastructure for immediate orchestration.
        
        Args:
            orchestrator: InfrastructureAgentReAct instance with orchestration enabled
        """
        self.orchestrator = orchestrator
        logging.info(f"✨ {self.name}: Orchestrator reference set (SESSION 31 FIX)")
        logging.info(f"   Upfront Triage: ENABLED")
        logging.info(f"   Multi-domain issues will be detected immediately")

    def delegate(self, user_issue: str, context: Dict = None) -> Dict[str, Any]:
        """
        SESSION 31 OPTIMIZED: Hybrid delegation strategy with upfront triage
        
        Strategy:
        0. Check upfront triage for obvious multi-domain issues (IMMEDIATE orchestration)
        1. Try rule-based triage (instant, efficient) - handles 70-80% of cases
        2. Fall back to LLM reasoning (flexible, adaptive) - handles 20-30% ambiguous cases
        
        This mirrors real IT department triage:
        - Experienced managers route clear-cut issues instantly (rules)
        - Triage emergency/multi-domain issues before delegation (upfront triage)
        - Complex/ambiguous issues require analytical thinking (LLM)
        
        Args:
            user_issue: User's problem description
            context: Additional context
            
        Returns:
            Dictionary with agent name, reasoning, and delegation method used
        """
        logging.info(f"\n{'='*60}")
        logging.info(f"🎯 {self.name} - Strategic Triage (SESSION 31 OPTIMIZED)")
        logging.info(f"{'='*60}")
        logging.info(f"Issue: {user_issue}")
        logging.info(f"{'='*60}\n")

        # STEP 0: Upfront Collaboration Triage (SESSION 31 FIX)
        # Check if this is obviously multi-domain BEFORE any delegation
        if self.triage_engine and self.orchestrator:
            should_orchestrate, reason, confidence = self.triage_engine.should_orchestrate_immediately(user_issue)
            
            if should_orchestrate:
                logging.info(f"⚡ UPFRONT TRIAGE: Immediate orchestration detected!")
                logging.info(f"   Reason: {reason}")
                logging.info(f"   Confidence: {confidence:.2f}")
                logging.info(f"   🚀 Routing to {self.orchestrator.name} for immediate orchestration")
                logging.info(f"   Skipping specialist delegation - Going straight to Ubuntu orchestration\n")
                
                # Return routing slip pointing to Infrastructure orchestrator
                return {
                    'agent': self.orchestrator.name,
                    'reasoning': reason,
                    'method': 'upfront_triage',
                    'confidence': confidence
                }
            else:
                logging.info(f"📋 Upfront triage: Specialist delegation appropriate")
                logging.info(f"   Confidence: {confidence:.2f}")
                logging.info(f"   Proceeding with normal delegation...\n")

        # STEP 1: Try rule-based triage (instant, efficient)
        logging.info(f"📋 STEP 1: Rule-based triage...")
        agent_name = self._rule_based_triage(user_issue)
        
        if agent_name:
            logging.info(f"✅ Rule-based Match Found!")
            logging.info(f"   Agent: {agent_name}")
            logging.info(f"   Method: Keyword pattern matching (instant)")
            logging.info(f"   ⏱️  Delegation time: <100ms\n")
            
            return {
                "agent": agent_name,
                "reasoning": f"Rule-based triage: Issue pattern matches {agent_name} expertise",
                "method": "rule_based",
                "confidence": "high"
            }
        
        # STEP 2: No clear rule match → Use LLM reasoning (ambiguous case)
        logging.info(f"🤔 No clear rule match - using LLM analysis...")
        logging.info(f"   Reason: Issue is ambiguous or multi-domain")
        logging.info(f"   ⏱️  Fallback to LLM reasoning...\n")
        
        result = self._llm_delegate(user_issue, context)
        
        logging.info(f"🤖 LLM Delegation Complete")
        logging.info(f"   Agent: {result['agent']}")
        logging.info(f"   Method: {result['method']}")
        logging.info(f"   Confidence: {result.get('confidence', 'unknown')}")
        if 'reasoning' in result and result['reasoning']:
            logging.info(f"   Reasoning: {result.get('reasoning', 'N/A')[:100]}...\n")
        
        return result

    def _rule_based_triage(self, user_issue: str) -> Optional[str]:
        """
        SESSION 30: Rule-based delegation using keyword matching
        Mirrors real IT department triage procedures
        
        This method implements organizational knowledge:
        - Clear-cut issues routed instantly (no LLM needed)
        - Pattern matching based on IT department experience
        - Confidence scoring to avoid mis-routing
        
        Args:
            user_issue: User's problem description
            
        Returns:
            Agent name if clear match found, None for ambiguous cases (LLM decides)
        """
        issue_lower = user_issue.lower()
        
        # Count keyword matches for each agent (scoring mechanism)
        match_scores = {}
        for agent_name, keywords in self.triage_rules.items():
            # Only consider agents that are registered
            if agent_name not in self.agents:
                continue
            
            # Count how many keywords match this issue
            score = sum(1 for keyword in keywords if keyword in issue_lower)
            if score > 0:
                match_scores[agent_name] = score
        
        # No matches → ambiguous, needs LLM reasoning
        if not match_scores:
            return None
        
        # Find agent with highest match score
        best_agent = max(match_scores, key=match_scores.get)
        best_score = match_scores[best_agent]
        
        # Confidence check: Require either strong match (2+ keywords) OR unique match
        # This prevents mis-routing when issue mentions multiple domains briefly
        if best_score >= 2:
            # Strong confidence: multiple keyword matches
            return best_agent
        elif len(match_scores) == 1:
            # Unique match: only one agent has any keywords
            return best_agent
        else:
            # Multiple agents with weak matches (1 keyword each) → ambiguous
            # Example: "network application error" could be Network OR App Support
            # Let LLM decide based on context and reasoning
            return None

    def _llm_delegate(self, user_issue: str, context: Dict = None) -> Dict[str, Any]:
        """
        SESSION 30: LLM-based delegation for ambiguous cases
        Used when rule-based triage cannot determine clear routing
        
        This method implements adaptive intelligence:
        - Context-aware reasoning for complex issues
        - Handles edge cases and unusual scenarios
        - Provides detailed reasoning for delegation decision
        
        Args:
            user_issue: User's problem description
            context: Additional context
            
        Returns:
            Dictionary with agent, reasoning, and method used
        """
        delegation_prompt = f"""You are the IT Manager performing strategic triage. This issue is AMBIGUOUS (no clear keyword match).

Issue: {user_issue}

Available Agents:
{self._format_agents()}

This issue reached LLM analysis because:
- No strong keyword match to any single domain
- May involve multiple domains or be unusual
- Requires contextual reasoning to route correctly

Your task:
1. Analyze the core technical problem (not just keywords)
2. Consider which agent's expertise is PRIMARY
3. If truly multi-domain, choose the LEAD investigator

Guidelines:
- User account/access → IT Support
- Application errors/performance → App Support  
- Network connectivity/security → Network Support
- Server/system/infrastructure → Infrastructure
- Unclear or department-wide → Infrastructure (can orchestrate)

Respond in JSON format:
{{
    "selected_agent": "agent_name",
    "reasoning": "Why this agent's expertise is primary for this issue",
    "confidence": "high/medium/low",
    "multi_domain": true/false
}}"""

        try:
            response = self.llm.invoke(delegation_prompt)
            response_text = response.content if hasattr(response, 'content') else str(response)
            
            if '{' in response_text:
                start = response_text.find('{')
                end = response_text.rfind('}') + 1
                decision = json.loads(response_text[start:end])
            else:
                # Fallback parsing if JSON not found
                decision = {
                    "selected_agent": "Infrastructure",  # Safe default (can orchestrate)
                    "reasoning": "LLM response parsing failed, using Infrastructure (can orchestrate if needed)",
                    "confidence": "low"
                }
            
            selected_agent_name = decision.get('selected_agent')
            
            # Validate agent exists
            if selected_agent_name not in self.agents:
                logging.warning(f"⚠️  LLM selected invalid agent '{selected_agent_name}'. Defaulting to Infrastructure.")
                selected_agent_name = "Infrastructure"
            
            return {
                "agent": selected_agent_name,
                "reasoning": decision.get('reasoning', 'LLM analysis completed'),
                "method": "llm",
                "confidence": decision.get('confidence', 'unknown'),
                "multi_domain": decision.get('multi_domain', False)
            }
        
        except Exception as e:
            logging.error(f"❌ LLM delegation error: {e}")
            # Ultimate fallback: Infrastructure (can orchestrate if needed)
            return {
                "agent": "Infrastructure",
                "reasoning": f"LLM error: {str(e)[:100]}. Infrastructure default (can orchestrate).",
                "method": "fallback",
                "error": str(e)
            }

    def _format_agents(self) -> str:
        """Format available agents for LLM prompt"""
        agent_descriptions = []
        for name, agent in self.agents.items():
            if hasattr(agent, 'specialization'):
                agent_descriptions.append(f"- {name}: {agent.specialization}")
            else:
                agent_descriptions.append(f"- {name}")
        return "\n".join(agent_descriptions)
    
    def register_agent(self, name: str, agent):
        """Register an agent for delegation"""
        self.agents[name] = agent
        logging.info(f"✅ Registered agent: {name}")
    
    def get_status(self) -> Dict[str, Any]:
        """Get agent status"""
        return {
            "agent_name": self.name,
            "agent_type": self.agent_type,
            "specialization": self.specialization,
            "available_agents": list(self.agents.keys()),
            "ubuntu_principles": self.ubuntu_principles,
            "reports_to": "Executive Management",
            "manages": list(self.agents.keys()),
            "pattern": "Hybrid Delegation (Upfront Triage + Rule-based + LLM)",
            "optimization": "SESSION 30 + SESSION 31 FIX",
            "upfront_triage_enabled": self.orchestrator is not None,
            "triage_rules_enabled": True,
            "expected_upfront_triage_rate": "5-10% (multi-domain only)",
            "expected_rule_based_rate": "70-80%",
            "expected_llm_rate": "10-20%"
        }
