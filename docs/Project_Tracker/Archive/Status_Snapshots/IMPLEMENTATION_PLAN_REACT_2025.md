# UGENTIC IMPLEMENTATION PLAN - ReAct Architecture
**Based on Session 8 Architectural Understanding**

**Date:** October 8, 2025  
**Pattern:** ReAct (Reasoning + Acting) with Ubuntu Orchestration  
**Timeline:** 6 weeks (4 sprints of 1.5 weeks each)  
**Status:** READY FOR IMPLEMENTATION

---

## 🎯 CORE DESIGN PRINCIPLE

**EACH AGENT:**
- Uses LLM for reasoning (NOT hardcoded rules)
- Has domain-specific diagnostic TOOLS
- Follows ReAct pattern: Thought → Action → Observation → Reflection
- Investigates problems (doesn't just route)
- Calls tools via function calling
- Works for ANY problem in their domain

**SYSTEM:**
- General-purpose diagnostic system
- LLM-guided investigation
- Multi-dimensional architecture (7 layers)
- Ubuntu orchestration for complex issues
- Continuous learning from resolutions

---

## 📋 SPRINT 1: Core ReAct Infrastructure (1.5 weeks)

### Goal
Implement ReAct loop foundation that works for ANY problem type

### Components

#### 1. ReAct Engine Core

```python
class ReactEngine:
    """
    Core ReAct (Reasoning + Acting) engine
    Works for ANY problem domain
    """
    
    def __init__(self, agent_name, tools, llm):
        self.agent_name = agent_name
        self.tools = tools  # Domain-specific diagnostic tools
        self.llm = llm
        self.max_iterations = 10
    
    def investigate(self, problem_report):
        """
        General-purpose investigation using ReAct pattern
        Works for ANY problem in agent's domain
        """
        history = []
        
        for iteration in range(self.max_iterations):
            # THOUGHT: LLM reasons about current state
            thought = self.llm.reason({
                'agent': self.agent_name,
                'problem': problem_report,
                'history': history,
                'available_tools': self.tools.list(),
                'question': '''
                Based on the problem and investigation so far:
                1. What do I currently know?
                2. What is my current hypothesis?
                3. What should I check next?
                4. Which tool should I use?
                5. What do I expect to find?
                '''
            })
            
            # Check if done
            if thought['status'] == 'ROOT_CAUSE_FOUND':
                return self.synthesize_solution(history, thought)
            
            # ACTION: LLM decides which tool to use
            action = thought['next_action']
            
            # EXECUTE: Call the tool
            observation = self.tools.execute(
                action['tool_name'],
                action['parameters']
            )
            
            # REFLECTION: LLM interprets results
            reflection = self.llm.reflect({
                'expected': thought['expectation'],
                'observed': observation,
                'question': '''
                What does this observation tell me?
                - Does it confirm or refute my hypothesis?
                - What should I investigate next?
                - Do I need help from other agents?
                '''
            })
            
            # Store step
            history.append({
                'iteration': iteration,
                'thought': thought,
                'action': action,
                'observation': observation,
                'reflection': reflection
            })
            
            # If hypothesis wrong, LLM will pivot next iteration
            if reflection['hypothesis_refuted']:
                continue
            
            # If needs collaboration
            if reflection['needs_collaboration']:
                return self.request_ubuntu_collaboration(history, reflection)
        
        # Max iterations reached
        return self.escalate_to_human(history)
```

#### 2. Tool Registry & Execution

```python
class ToolRegistry:
    """
    Manages domain-specific diagnostic tools
    Each agent has their own tool registry
    """
    
    def __init__(self, domain):
        self.domain = domain
        self.tools = {}
    
    def register(self, tool_func, description, parameters):
        """
        Register a diagnostic tool
        LLM uses description to decide when to call it
        """
        self.tools[tool_func.__name__] = {
            'function': tool_func,
            'description': description,
            'parameters': parameters,
            'domain': self.domain
        }
    
    def list(self):
        """
        Returns tool descriptions for LLM
        """
        return [
            {
                'name': name,
                'description': info['description'],
                'parameters': info['parameters']
            }
            for name, info in self.tools.items()
        ]
    
    def execute(self, tool_name, params):
        """
        Execute tool and return observation
        """
        if tool_name not in self.tools:
            return {'error': f'Tool {tool_name} not found'}
        
        try:
            result = self.tools[tool_name]['function'](**params)
            return {'success': True, 'data': result}
        except Exception as e:
            return {'error': str(e)}
```

#### 3. Basic Diagnostic Tools (Start with 10-15)

**Infrastructure Tools:**
```python
@tool(description="Checks actual server CPU, memory, disk usage")
def check_server_metrics(server_name):
    """Gets real-time server performance data"""
    return {
        'cpu_percent': get_cpu_usage(server_name),
        'memory_percent': get_memory_usage(server_name),
        'disk_io': get_disk_io(server_name),
        'status': 'normal' | 'degraded' | 'critical'
    }

@tool(description="Reads server error logs for timeframe")
def check_server_logs(server_name, hours=1):
    """Gets actual error logs"""
    return {
        'total_errors': count,
        'top_errors': [...],
        'recent_logs': [...]
    }

@tool(description="Checks if specific service is running")
def check_service_status(server_name, service_name):
    """Verifies service state"""
    return {
        'running': bool,
        'uptime': seconds,
        'restarts_today': count
    }
```

**Network Tools:**
```python
@tool(description="Measures actual network bandwidth and latency")
def check_network_bandwidth(interface="eth0"):
    """Runs bandwidth test"""
    return {
        'download_mbps': float,
        'upload_mbps': float,
        'latency_ms': float,
        'packet_loss_percent': float,
        'status': 'normal' | 'degraded' | 'poor'
    }

@tool(description="Tests connectivity to host with ping")
def ping_test(host, count=10):
    """Measures latency and packet loss"""
    return {
        'packets_sent': int,
        'packets_received': int,
        'packet_loss_percent': float,
        'avg_latency_ms': float
    }
```

**Application Tools:**
```python
@tool(description="Gets application logs for user/timeframe")
def query_app_logs(app_name, user_id, hours=1):
    """Retrieves actual application logs"""
    return {
        'total_entries': int,
        'errors': [...],
        'warnings': [...],
        'crashes': [...]
    }

@tool(description="Measures application response time")
def check_app_response_time(app_name):
    """Tests app performance"""
    return {
        'avg_response_ms': float,
        'status': 'normal' | 'slow' | 'very_slow'
    }
```

### Deliverables

- [x] ReactEngine core class
- [x] ToolRegistry system
- [ ] 10-15 basic diagnostic tools implemented
- [ ] LLM integration (gemma3:4b for reasoning)
- [ ] Test with 3 different problem types
- [ ] Validate ReAct loop works correctly

### Testing

**Test Cases:**
1. **Network Issue:** User reports "network slow" → System checks bandwidth, finds it's actually fast, investigates application/server instead
2. **Application Crash:** User reports "app crashes" → System checks logs, finds memory issue, identifies root cause
3. **Server Performance:** User reports "system slow" → System checks CPU/memory, finds database fragmentation

**Success Criteria:**
- ReAct loop runs without hardcoded routing
- LLM successfully calls appropriate tools
- System pivots when hypothesis wrong
- Finds actual root cause (not assumed cause)

---

## 📋 SPRINT 2: Agent Tool Libraries (1.5 weeks)

### Goal
Each agent has comprehensive domain-specific tool library

### Infrastructure Agent Tools (15 tools)

```python
# Server Monitoring
check_server_metrics(server_name)
check_server_logs(server_name, hours)
check_service_status(server_name, service_name)
get_process_list(server_name)
check_disk_space(server_name)

# Performance
measure_server_response_time(server_name)
check_resource_allocation(server_name)
get_performance_history(server_name, days)

# Maintenance
check_backup_status(server_name)
check_update_status(server_name)
get_uptime(server_name)

# Diagnostics
run_health_check(server_name)
check_hardware_health(server_name)
get_system_alerts(server_name)
check_capacity_planning(server_name)
```

### Network Agent Tools (12 tools)

```python
# Connectivity
check_network_bandwidth(interface)
ping_test(host, count)
traceroute(destination)
check_dns_resolution(domain)

# Performance
measure_network_latency(source, destination)
check_packet_loss(interface)
get_network_utilization(interface)

# Security
check_firewall_rules(host)
scan_open_ports(host)
check_vpn_status(user_id)

# Diagnostics
get_network_topology(segment)
check_routing_table(host)
```

### App Support Agent Tools (12 tools)

```python
# Application Monitoring
query_app_logs(app_name, user_id, hours)
check_app_response_time(app_name)
get_app_error_rate(app_name)
check_app_availability(app_name)

# User Experience
get_user_session_data(user_id, app_name)
check_app_crashes(app_name, hours)
measure_app_load_time(app_name)

# Diagnostics
get_app_dependencies(app_name)
check_integration_status(app_name, integration)
query_app_database_performance(app_name)

# Configuration
check_app_configuration(app_name)
verify_app_licenses(app_name)
```

### Service Desk Manager Tools (8 tools)

```python
# Team Management
get_technician_workload()
get_team_availability()
check_skill_match(issue_type)

# Issue Tracking
get_open_tickets()
get_sla_status(ticket_id)
get_escalation_history()

# Knowledge
search_knowledge_base(query)
get_similar_past_issues(description)
```

### IT Support Tools (10 tools)

```python
# User Support
get_user_profile(user_id)
check_user_permissions(user_id, resource)
reset_user_password(user_id)
unlock_user_account(user_id)

# Client Diagnostics
get_client_metrics(user_id)
check_client_software(user_id)
get_client_network_config(user_id)

# Common Issues
check_printer_status(printer_name)
verify_email_config(user_id)
test_remote_access(user_id)
```

### Deliverables

- [ ] All agent tool libraries implemented
- [ ] Each tool returns real diagnostic data
- [ ] Tool descriptions optimized for LLM
- [ ] Tools tested individually
- [ ] Documentation for each tool

---

## 📋 SPRINT 3: Ubuntu Orchestration (1.5 weeks)

### Goal
Multi-agent coordination for complex issues using 2025 patterns

### Pattern: Orchestrator-Subagent (Sequential)

```python
class UbuntuOrchestrator:
    """
    Implements 2025 orchestrator-subagent pattern
    Sequential execution (not parallel)
    One lead orchestrator coordinates
    """
    
    def orchestrate(self, complex_issue, lead_agent, investigation_history):
        """
        Lead agent coordinates investigation
        Based on Anthropic 2025 pattern
        """
        
        # STEP 1: LLM analyzes issue
        analysis = self.llm.analyze_complexity({
            'issue': complex_issue,
            'lead_findings': investigation_history,
            'question': '''
            This issue spans multiple domains.
            Which specialist agents should investigate?
            What should each one check?
            In what sequence?
            '''
        })
        
        # STEP 2: Create orchestration plan
        plan = {
            'lead': lead_agent.name,
            'collaborators': analysis['required_agents'],
            'tasks': analysis['agent_tasks'],
            'sequence': analysis['execution_order']  # Sequential
        }
        
        # STEP 3: Execute tasks SEQUENTIALLY
        findings = {lead_agent.name: investigation_history}
        
        for agent_name in plan['sequence']:
            agent = self.get_agent(agent_name)
            task = plan['tasks'][agent_name]
            
            # Agent investigates their domain
            result = agent.investigate_subtask(
                issue=complex_issue,
                task=task,
                prior_findings=findings  # See what others found
            )
            
            findings[agent_name] = result
        
        # STEP 4: Lead agent synthesizes
        synthesis = lead_agent.llm.synthesize({
            'issue': complex_issue,
            'all_findings': findings,
            'question': '''
            Based on collective investigation:
            - What is the root cause?
            - What is the solution?
            - How did each agent contribute?
            - What did we learn together?
            '''
        })
        
        return {
            'root_cause': synthesis['cause'],
            'solution': synthesis['solution'],
            'collaboration': synthesis['contributions'],
            'ubuntu_value': synthesis['collective_learning']
        }
```

### Collaboration Detection

```python
class CollaborationDetector:
    """
    LLM determines when collaboration needed
    """
    
    def should_collaborate(self, agent, investigation_history):
        """
        LLM decides based on investigation findings
        """
        decision = agent.llm.reason({
            'agent': agent.name,
            'investigation': investigation_history,
            'question': '''
            Based on my investigation:
            1. Does this problem span multiple domains?
            2. Do I need expertise from other agents?
            3. Which agents would help?
            4. What should they investigate?
            
            Examples needing collaboration:
            - Network + Application issue
            - Server + Database issue
            - Multiple symptoms across domains
            '''
        })
        
        return decision['collaborate'], decision['required_agents']
```

### Deliverables

- [ ] UbuntuOrchestrator implementation
- [ ] CollaborationDetector with LLM decision
- [ ] Sequential execution framework
- [ ] Agent communication protocol
- [ ] Test 3 multi-domain scenarios
- [ ] Validate synthesis quality

### Testing

**Multi-Domain Scenarios:**
1. **Network + App:** Users report slowness → Network is fine, App slow due to database
2. **Server + Network:** System inaccessible → Server running, network config issue
3. **App + Infrastructure:** Application errors → Server resources exhausted

---

## 📋 SPRINT 4: Learning & Polish (1.5 weeks)

### Goal
System learns from resolutions and improves over time

### Experience Memory

```python
class ExperienceMemory:
    """
    Stores and retrieves past resolutions
    System learns patterns
    """
    
    def store_resolution(self, investigation):
        """
        Store what was learned
        """
        self.vector_store.add({
            'symptom_reported': investigation['user_report'],
            'actual_root_cause': investigation['root_cause'],
            'deceptive_symptoms': investigation['false_leads'],
            'diagnostic_path': investigation['tools_used'],
            'solution': investigation['solution'],
            'effectiveness': investigation['resolved'],
            'time_to_resolve': investigation['duration'],
            'agents_involved': investigation['collaborators'],
            'key_lesson': investigation['learning']
        })
    
    def query_similar(self, current_issue):
        """
        Find similar past issues
        """
        similar = self.vector_store.similarity_search(
            current_issue, k=5
        )
        
        return [
            {
                'past_symptom': case['symptom_reported'],
                'actual_cause': case['actual_root_cause'],
                'lesson': case['key_lesson'],
                'similarity': case['score']
            }
            for case in similar
        ]
```

### Communication Layer

```python
class UbuntuCommunicator:
    """
    Ubuntu-based user communication
    """
    
    def investigation_update(self, agent, step):
        """
        Keep user informed with Ubuntu values
        """
        return f"""
        {agent.name} Update:
        
        Investigating: {step['action']}
        Found: {step['finding']}
        
        {"Collaborating with " + step['collaborators'] if step['collaboration'] else ""}
        
        Next: {step['next_action']}
        """
    
    def final_resolution(self, investigation):
        """
        Ubuntu-framed final message
        """
        return f"""
        Issue Resolved: {investigation['issue']}
        
        Root Cause: {investigation['root_cause']}
        Solution Applied: {investigation['solution']}
        
        Investigation Journey:
        {self.format_journey(investigation['history'])}
        
        {self.format_collaboration(investigation['agents']) if investigation['collaborated'] else ""}
        
        This knowledge now benefits our entire team.
        """
```

### Deliverables

- [ ] ExperienceMemory implemented
- [ ] Learning from each resolution
- [ ] Pattern recognition working
- [ ] UbuntuCommunicator complete
- [ ] Performance metrics collection
- [ ] System optimization

---

## 🎯 AGENT SPECIFICATIONS

### IT Manager (Strategic Router)

**Role:** Intelligent delegation to appropriate agent  
**Pattern:** Simple routing (not full ReAct)  
**Decision:** LLM analyzes issue and delegates

```python
class ITManagerAgent:
    def delegate(self, user_issue):
        decision = self.llm.decide({
            'issue': user_issue,
            'available_agents': self.agents,
            'question': '''
            Which agent should handle this?
            - Simple user issue: Service Desk Manager
            - Complex server: Infrastructure
            - Network issue: Network Support
            - App issue: App Support
            '''
        })
        
        agent = self.get_agent(decision['agent'])
        return agent.investigate(user_issue)
```

### Infrastructure Agent (Lead Orchestrator)

**Role:** Server/infrastructure issues + orchestrates complex problems  
**Pattern:** Full ReAct + Ubuntu Orchestration  
**Tools:** 15 server/infrastructure diagnostic tools

### Network Support Agent

**Role:** Network connectivity and performance  
**Pattern:** Full ReAct in network domain  
**Tools:** 12 network diagnostic tools

### App Support Agent

**Role:** Application issues  
**Pattern:** Full ReAct in application domain  
**Tools:** 12 application diagnostic tools

### Service Desk Manager

**Role:** Coordinates IT Support team, handles escalations  
**Pattern:** Team coordination + simple ReAct  
**Tools:** 8 team management tools

### IT Support Agent

**Role:** Front-line user support  
**Pattern:** ReAct for user issues  
**Tools:** 10 user support tools

---

## 📊 IMPLEMENTATION PRIORITIES

### Week 1-1.5 (Sprint 1)
1. ReAct engine core
2. Tool registry system
3. 10-15 basic tools
4. LLM integration
5. Initial testing

### Week 2-3 (Sprint 2)
1. Complete all agent tool libraries
2. 60+ total tools across domains
3. Tool descriptions optimized
4. Individual tool testing

### Week 3-4.5 (Sprint 3)
1. Ubuntu orchestrator
2. Collaboration detection
3. Multi-agent coordination
4. Sequential execution

### Week 4.5-6 (Sprint 4)
1. Experience memory
2. Learning system
3. Communication layer
4. Performance optimization
5. Final testing

---

## ✅ SUCCESS CRITERIA

### System Level
- [ ] Handles ANY IT problem (not just pre-defined)
- [ ] LLM reasoning drives investigation
- [ ] Tools verify claims (doesn't assume)
- [ ] Pivots when hypothesis wrong
- [ ] Finds actual root causes
- [ ] Collaboration works for complex issues
- [ ] Learns from each resolution

### Agent Level
- [ ] Each agent uses ReAct pattern correctly
- [ ] Domain tools work reliably
- [ ] LLM function calling accurate
- [ ] Investigation history maintained
- [ ] Ubuntu values in all interactions

### Performance
- [ ] 90%+ root cause identification
- [ ] Average 5-8 ReAct iterations per issue
- [ ] Collaboration improves complex issue resolution
- [ ] Diagnostic efficiency improves over time

---

## 🎓 FOR DISSERTATION

**What This Demonstrates:**
1. LLM-guided diagnostic system (not rule-based)
2. General-purpose (handles ANY IT problem)
3. ReAct pattern (2024/2025 research)
4. Ubuntu orchestration (collective expertise)
5. Continuous learning (organizational benefit)

**Evidence for Interviews:**
- Staff report ANY problem
- System investigates intelligently
- Collaboration feels natural
- Solutions are effective
- Knowledge preserved and shared

---

**Status:** READY FOR SPRINT 1 IMPLEMENTATION  
**Timeline:** 6 weeks total  
**Confidence:** HIGH - Research-backed, properly designed  
**Next Action:** Begin Sprint 1 - ReAct engine core
