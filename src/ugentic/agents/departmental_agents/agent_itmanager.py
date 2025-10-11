# IT Manager Agent - The Strategic Orchestrator
# UGENTIC Framework

from ...core.agent_framework import Agent
import logging

class Agent_ITManager(Agent):
    """
    The IT Manager agent acts as the strategic orchestrator for the entire IT department.
    It receives high-level goals, interprets them, and delegates them to the appropriate
    tactical or operational agents.
    
    Ubuntu Principles Integration:
    - Collective Problem-Solving: Strategic decisions involve team consultation
    - Knowledge Sharing: Strategic insights shared with entire department
    - Mutual Support: Facilitates cross-functional collaboration
    - Consensus Building: Major decisions reflect collective wisdom
    """
    def __init__(self, name="ITManager", persona="A strategic orchestrator for the IT department.", tools=None, rag_system=None, llm_model=None, departmental_relationships=None):
        super().__init__(name, persona, tools, rag_system, llm_model)
        self.agent_type = "Strategic"
        self.departmental_relationships = departmental_relationships or {}
        self.ubuntu_principles = {
            "collective_problem_solving": True,
            "knowledge_sharing": True,
            "mutual_support": True,
            "consensus_building": True
        }

    def decide_and_delegate(self, goal: str):
        """
        Analyzes a high-level goal and delegates it to the appropriate subordinate agent.
        
        This is the core logic of the IT Manager.
        """
        logging.info(f"IT Manager '{self.name}' received goal: '{goal}'")
        
        # Use the LLM to decide which agent is best suited for the goal.
        available_agents = ["ITSupport", "Infrastructure", "ServiceDeskManager"] # TODO: This should be dynamic later
        
        prompt = f"""You are a strategic IT Manager. Your task is to delegate a goal to the most appropriate team.
        The goal is: '{goal}'
        
        Choose the best team from the following options:
        - ITSupport: Handles user-facing issues, application problems, and access requests.
        - Infrastructure: Handles issues related to servers, networks, and core hardware.
        - ServiceDeskManager: Manages the service desk, oversees ticket escalations, and ensures operational efficiency.

        Respond with ONLY the name of the chosen team (e.g., "ITSupport", "Infrastructure", or "ServiceDeskManager").
        """
        
        try:
            # Assuming self.llm_model.invoke exists and returns a string response
            llm_response = self.llm_model.invoke(prompt).strip()
            
            if llm_response in available_agents:
                delegation_target = llm_response
            else:
                logging.warning(f"LLM chose an invalid agent '{llm_response}'. Defaulting to ITSupport.")
                delegation_target = "ITSupport"

        except Exception as e:
            logging.error(f"LLM decision-making failed: {e}. Defaulting to ITSupport.")
            delegation_target = "ITSupport"

        logging.info(f"Delegating goal to: {delegation_target}")
        
        # TODO: Implement the actual delegation mechanism.
        
        return {
            "decision": "Delegate",
            "target_agent": delegation_target,
            "task": goal,
            "status": "Pending Delegation"
        }

    def ubuntu_collaborate(self, issue: str, target_agents: list, collaboration_type: str = "strategic"):
        """
        Initiates Ubuntu collaboration with multiple agents for strategic problem-solving.
        
        This is the IT Manager's primary collaboration method for complex issues requiring
        multi-domain expertise or strategic consensus.
        
        Args:
            issue: The strategic issue or decision requiring collaboration
            target_agents: List of agent names to involve
            collaboration_type: Type of collaboration (strategic, tactical, emergency)
            
        Returns:
            dict: Collaboration session details
        """
        logging.info(f"IT Manager '{self.name}' initiating Ubuntu collaboration: '{issue}'")
        
        collaboration_session = {
            "collaboration_id": f"ubuntu_collab_{len(target_agents)}_agents",
            "initiated_by": self.name,
            "issue": issue,
            "type": collaboration_type,
            "participants": target_agents,
            "status": "initiated"
        }
        
        # Craft strategic collaboration message
        collaboration_message = f"""
 STRATEGIC UBUNTU COLLABORATION INITIATED by IT Manager

Issue/Decision: {issue}
Type: {collaboration_type.upper()}

Strategic Context:
- This requires our collective expertise and wisdom
- Multiple perspectives will create a better outcome
- Each domain brings unique insights to the solution

Participating Agents:
{chr(10).join([f"- {agent}: Your domain expertise is crucial for complete understanding" for agent in target_agents])}

Ubuntu Principles in Action:
✓ Collective Problem-Solving: Together we build comprehensive solutions
✓ Knowledge Sharing: All insights shared in real-time
✓ Mutual Support: Supporting each other's success
✓ Consensus Building: Decisions reflect our collective wisdom

Expectations:
1. Share your domain perspective openly
2. Listen to all viewpoints before forming conclusions
3. Build on each other's insights
4. Reach consensus on the best path forward
5. Document learnings for future benefit

"I am because we are" - Let's solve this together.
        """
        
        collaboration_session["message"] = collaboration_message
        logging.info(f"Ubuntu collaboration session '{collaboration_session['collaboration_id']}' created")
        
        return collaboration_session
    
    def build_strategic_consensus(self, decision: str, stakeholders: list, context: dict):
        """
        Builds consensus on strategic decisions by involving all relevant stakeholders.
        
        This embodies Ubuntu's consensus-building principle at the strategic level.
        
        Args:
            decision: The strategic decision to be made
            stakeholders: List of agents/teams whose input is needed
            context: Context dict with decision factors, constraints, options
            
        Returns:
            dict: Consensus-building session details
        """
        logging.info(f"IT Manager '{self.name}' building strategic consensus: '{decision}'")
        
        consensus_session = {
            "decision": decision,
            "stakeholders": stakeholders,
            "context": context,
            "phase": "gathering_input",
            "ubuntu_principle": "Decisions are stronger when they reflect collective wisdom"
        }
        
        consensus_message = f"""
 STRATEGIC CONSENSUS BUILDING by IT Manager

Decision: {decision}

Why Your Input Matters:
This decision affects all of us, and your expertise is crucial for the right outcome.
We build consensus not because we must, but because together we decide better.

Context and Factors:
{chr(10).join([f"- {key}: {value}" for key, value in context.items()])}

Stakeholder Consultation:
{chr(10).join([f"- {stakeholder}: Your perspective on how this affects your domain" for stakeholder in stakeholders])}

Consensus Process:
1. Each stakeholder analyzes impact on their domain
2. All perspectives shared in open discussion
3. Options evaluated collectively
4. Common ground identified
5. Agreement built on best path forward
6. Decision rationale documented transparently

Ubuntu Principle: "Decisions made together are owned by all"

Let's hear from everyone before we decide.
        """
        
        consensus_session["message"] = consensus_message
        logging.info(f"Consensus building initiated with {len(stakeholders)} stakeholders")
        
        return consensus_session
    
    def share_strategic_knowledge(self, topic: str, insights: str, target_audience: str = "all_department"):
        """
        Shares strategic knowledge and insights with the department.
        
        Embodies Ubuntu knowledge sharing principle - strategic insights belong to the collective.
        
        Args:
            topic: The knowledge topic
            insights: Strategic insights to share
            target_audience: Who should receive this (default: all department)
            
        Returns:
            dict: Knowledge sharing confirmation
        """
        logging.info(f"IT Manager '{self.name}' sharing strategic knowledge: '{topic}'")
        
        knowledge_package = {
            "topic": topic,
            "insights": insights,
            "shared_by": self.name,
            "audience": target_audience,
            "knowledge_type": "strategic",
            "ubuntu_principle": "Knowledge belongs to the community, learning benefits everyone"
        }
        
        sharing_message = f"""
 STRATEGIC KNOWLEDGE SHARING from IT Manager

Topic: {topic}

Strategic Insights:
{insights}

Why This Matters:
Sharing strategic thinking helps everyone make better aligned decisions,
even when I'm not involved. Our collective wisdom grows when we share openly.

How to Apply:
- Use these insights when making decisions in your domain
- Build on this knowledge with your own expertise  
- Share what you learn as you apply these principles
- Ask questions if anything is unclear

Ubuntu Principle: "Knowledge shared is knowledge multiplied"

This knowledge now belongs to all of us.
        """
        
        knowledge_package["message"] = sharing_message
        logging.info(f"Strategic knowledge '{topic}' shared with {target_audience}")
        
        return knowledge_package
    
    def facilitate_cross_department_collaboration(self, departments: list, objective: str, coordination_plan: dict):
        """
        Facilitates collaboration across different IT departments/teams.
        
        Breaks down silos by creating structured cross-functional collaboration.
        
        Args:
            departments: List of departments/agents involved
            objective: The collaborative objective
            coordination_plan: Dict with timeline, responsibilities, checkpoints
            
        Returns:
            dict: Cross-department collaboration framework
        """
        logging.info(f"IT Manager '{self.name}' facilitating cross-department collaboration")
        
        collaboration_framework = {
            "objective": objective,
            "departments": departments,
            "coordination_plan": coordination_plan,
            "ubuntu_principle": "Together we break silos and build bridges",
            "status": "active"
        }
        
        facilitation_message = f"""
 CROSS-DEPARTMENT COLLABORATION facilitated by IT Manager

Objective: {objective}

Departments Collaborating:
{chr(10).join([f"- {dept}: Essential contributor to achieving our objective" for dept in departments])}

Coordination Plan:
{chr(10).join([f"- {key}: {value}" for key, value in coordination_plan.items()])}

Collaboration Principles:
1. No silos - share information freely across departments
2. Mutual support - help each other succeed
3. Common goal - we succeed together or not at all
4. Open communication - transparent progress and blockers
5. Knowledge sharing - learnings benefit all departments

My Role as Facilitator:
- Remove barriers to collaboration
- Ensure all voices are heard
- Coordinate resources and support
- Track progress and celebrate milestones
- Document learnings for future initiatives

Ubuntu Principle: "We are stronger when departments work as one"

Let's break down the walls and build something great together.
        """
        
        collaboration_framework["message"] = facilitation_message
        logging.info(f"Cross-department collaboration active with {len(departments)} departments")
        
        return collaboration_framework
    
    def get_agent_status(self):
        """Returns the current status of the agent."""
        return {
            "agent_id": self.name,
            "agent_type": self.agent_type,
            "status": "active",
            "ubuntu_principles_active": self.ubuntu_principles,
            "manages": list(self.departmental_relationships.keys()) if self.departmental_relationships else [],
            "collaboration_capabilities": [
                "ubuntu_collaborate",
                "build_strategic_consensus",
                "share_strategic_knowledge",
                "facilitate_cross_department_collaboration"
            ]
        }