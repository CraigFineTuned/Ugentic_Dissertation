# Service Desk Manager Agent - The Tactical Coordinator
# UGENTIC Framework

from ...core.agent_framework import Agent
import logging

class Agent_Service_Desk_Manager(Agent):
    """
    The Service Desk Manager agent is responsible for overseeing the Service Desk operations,
    managing escalations, and ensuring that incidents are resolved efficiently.
    
    Ubuntu Principles Integration:
    - Collective Problem-Solving: Facilitates team collaboration on complex issues
    - Knowledge Sharing: Creates knowledge-sharing infrastructure and culture
    - Mutual Support: Balances workload and supports team wellbeing
    - Consensus Building: Involves team in process decisions
    """
    def __init__(self, name="Service Desk Manager", persona="A tactical coordinator, focused on operational efficiency and user satisfaction.", tools=None, rag_system=None, llm_model=None, departmental_relationships=None):
        super().__init__(name, persona, tools, rag_system, llm_model)
        self.agent_type = "Tactical"
        self.departmental_relationships = departmental_relationships or {}
        self.ubuntu_principles = {
            "collective_problem_solving": True,
            "knowledge_sharing": True,
            "mutual_support": True,
            "consensus_building": True
        }
        self.team_workload = {}  # Track IT Support team workload

    def decide_and_delegate(self, task: str):
        """
        Analyzes a task and delegates it to the appropriate subordinate agent.
        """
        logging.info(f"Service Desk Manager '{self.name}' received task: '{task}'")
        
        # For now, the Service Desk Manager will always delegate to ITSupport.
        delegation_target = "ITSupport"

        logging.info(f"Delegating task to: {delegation_target}")
        
        return {
            "decision": "Delegate",
            "target_agent": delegation_target,
            "task": task,
            "status": "Pending Delegation"
        }

    def ubuntu_collaborate(self, issue: str, team_members: list, collaboration_pattern: str = "peer_support"):
        """
        Initiates Ubuntu collaboration among IT Support team members.
        
        As tactical coordinator, facilitates team collaboration on complex support issues.
        
        Args:
            issue: The issue requiring team collaboration
            team_members: List of IT Support technicians to involve
            collaboration_pattern: Type (peer_support, mentoring, collective_diagnosis)
            
        Returns:
            dict: Team collaboration session details
        """
        logging.info(f"Service Desk Manager '{self.name}' initiating team collaboration: '{issue}'")
        
        collaboration_session = {
            "collaboration_id": f"team_collab_{len(team_members)}_members",
            "coordinated_by": self.name,
            "issue": issue,
            "pattern": collaboration_pattern,
            "team_members": team_members,
            "status": "active"
        }
        
        collaboration_message = f"""
 TEAM UBUNTU COLLABORATION coordinated by Service Desk Manager

Issue: {issue}
Pattern: {collaboration_pattern.upper()}

Team Collaboration Purpose:
When we work together, we solve problems faster and everyone learns.
This is a great opportunity for collective problem-solving.

Team Members Involved:
{chr(10).join([f"- {member}: Your expertise and perspective are valuable" for member in team_members])}

Collaboration Guidelines:
1. Share your findings and observations openly
2. Build on each other's ideas
3. Ask questions when something is unclear
4. Support each other's learning
5. Document insights for the whole team's benefit

My Role as Coordinator:
- Facilitate smooth collaboration
- Remove any obstacles you encounter
- Ensure everyone's voice is heard
- Help capture learnings for future use

Ubuntu Principle: "Together we are stronger"

Let's work on this as a team!
        """
        
        collaboration_session["message"] = collaboration_message
        logging.info(f"Team collaboration '{collaboration_session['collaboration_id']}' initiated")
        
        return collaboration_session
    
    def coordinate_team_response(self, request: str, urgency: str, required_skills: list):
        """
        Coordinates multi-agent task distribution across IT Support team.
        
        Applies Ubuntu principles to assign work fairly and create learning opportunities.
        
        Args:
            request: The support request to coordinate
            urgency: Urgency level (low, normal, high, critical)
            required_skills: List of skills needed for resolution
            
        Returns:
            dict: Team coordination plan
        """
        logging.info(f"Service Desk Manager '{self.name}' coordinating team response")
        
        coordination_plan = {
            "request": request,
            "urgency": urgency,
            "required_skills": required_skills,
            "coordination_approach": "ubuntu_based",
            "status": "coordinating"
        }
        
        # Ubuntu-based assignment logic considerations
        assignment_considerations = [
            "Workload balance - who has capacity to help?",
            "Skill match - who has the expertise needed?",
            "Learning opportunity - who could grow from this?",
            "Mentoring potential - can we pair experienced with growing?",
            "Team development - how does this strengthen collective capability?"
        ]
        
        coordination_message = f"""
 TEAM RESPONSE COORDINATION by Service Desk Manager

Request: {request}
Urgency: {urgency.upper()}
Required Skills: {', '.join(required_skills)}

Coordination Approach (Ubuntu Principles):
{chr(10).join([f"✓ {consideration}" for consideration in assignment_considerations])}

Team Assignment Strategy:
I'm considering:
- Current workload distribution (mutual support)
- Skill match and learning opportunities (knowledge sharing)
- Collaboration potential (collective problem-solving)
- Fair distribution of challenging work (team equity)

This ensures:
1. Right skills applied to the problem
2. Workload stays balanced across team
3. Learning opportunities are shared
4. No one struggles alone when help is available

Ubuntu Principle: "Fair distribution strengthens the whole team"

Assignments coming shortly based on current team state.
        """
        
        coordination_plan["message"] = coordination_message
        logging.info(f"Team coordination plan created for: {request}")
        
        return coordination_plan
    
    def share_team_knowledge(self, knowledge_topic: str, source: str, knowledge_content: str, relevance: str = "all_team"):
        """
        Facilitates knowledge sharing across the IT Support team.
        
        Ensures valuable learnings are captured and distributed to strengthen collective capability.
        
        Args:
            knowledge_topic: Topic of the knowledge
            source: Who discovered/created this knowledge
            knowledge_content: The actual knowledge to share
            relevance: Who should know this (all_team, specific_roles, etc.)
            
        Returns:
            dict: Knowledge sharing package
        """
        logging.info(f"Service Desk Manager '{self.name}' facilitating knowledge sharing: '{knowledge_topic}'")
        
        knowledge_package = {
            "topic": knowledge_topic,
            "discovered_by": source,
            "content": knowledge_content,
            "relevance": relevance,
            "shared_by": self.name,
            "knowledge_type": "team_best_practice",
            "ubuntu_principle": "Knowledge shared is knowledge multiplied"
        }
        
        sharing_message = f"""
 TEAM KNOWLEDGE SHARING facilitated by Service Desk Manager

Topic: {knowledge_topic}
Discovered by: {source}
Relevance: {relevance}

Knowledge Content:
{knowledge_content}

Why This Matters:
{source} discovered this while solving a real problem. Rather than keeping it
to themselves, they're sharing it so the whole team benefits. This is Ubuntu
knowledge sharing in action!

How to Apply:
- Integrate this into your troubleshooting approach
- Try it next time you encounter similar issues
- Build on this with your own insights
- Share your experiences applying it

Recognition:
Thank you {source} for strengthening our collective capability! When one of
us learns, we all become smarter.

Ubuntu Principle: "Your knowledge helps us all succeed"

This knowledge is now part of our team's expertise.
        """
        
        knowledge_package["message"] = sharing_message
        logging.info(f"Team knowledge '{knowledge_topic}' shared across {relevance}")
        
        return knowledge_package
    
    def facilitate_peer_learning(self, learning_opportunity: str, mentor: str, mentee: str, context: dict):
        """
        Creates structured peer learning opportunities within the team.
        
        Pairs experienced technicians with those developing skills for mutual growth.
        
        Args:
            learning_opportunity: What the learning opportunity is
            mentor: Experienced team member sharing expertise
            mentee: Team member developing skills
            context: Dict with issue details, learning objectives, support offered
            
        Returns:
            dict: Peer learning arrangement
        """
        logging.info(f"Service Desk Manager '{self.name}' facilitating peer learning")
        
        learning_arrangement = {
            "opportunity": learning_opportunity,
            "mentor": mentor,
            "mentee": mentee,
            "context": context,
            "facilitated_by": self.name,
            "ubuntu_principle": "We grow by helping each other learn",
            "status": "active"
        }
        
        learning_message = f"""
 PEER LEARNING OPPORTUNITY facilitated by Service Desk Manager

Learning Opportunity: {learning_opportunity}

Peer Learning Partnership:
- Mentor: {mentor} - Sharing expertise and experience
- Mentee: {mentee} - Developing new skills and capabilities

Context:
{chr(10).join([f"- {key}: {value}" for key, value in context.items()])}

How This Works (Ubuntu Peer Learning):

For {mentee}:
- This is a safe space to learn and ask questions
- Work alongside {mentor}, observe their approach
- Ask "why" to understand reasoning, not just "how"
- Share your perspective - you might see things differently!
- Mistakes are learning opportunities, not failures

For {mentor}:
- Share your expertise generously and patiently
- Explain your reasoning, not just your actions
- Encourage questions and experimentation
- Learn from fresh perspectives {mentee} brings
- Teaching others deepens your own understanding

For Both:
- Work collaboratively, not hierarchically
- Both of you will learn and grow from this
- Document insights for the whole team
- Build relationship that strengthens team cohesion

My Role as Facilitator:
- Create safe learning environment
- Remove pressure and obstacles
- Ensure time and space for learning
- Celebrate growth and knowledge sharing

Ubuntu Principle: "Teaching is learning twice, learning together makes us all stronger"

Let's grow together!
        """
        
        learning_arrangement["message"] = learning_message
        logging.info(f"Peer learning facilitated: {mentor} mentoring {mentee}")
        
        return learning_arrangement
    
    def get_agent_status(self):
        """Returns the current status of the agent."""
        return {
            "agent_id": self.name,
            "agent_type": self.agent_type,
            "status": "active",
            "ubuntu_principles_active": self.ubuntu_principles,
            "manages": "IT Support Team",
            "reports_to": "IT Manager",
            "coordination_capabilities": [
                "ubuntu_collaborate",
                "coordinate_team_response",
                "share_team_knowledge",
                "facilitate_peer_learning"
            ],
            "team_workload_tracking": len(self.team_workload) if self.team_workload else 0
        }
