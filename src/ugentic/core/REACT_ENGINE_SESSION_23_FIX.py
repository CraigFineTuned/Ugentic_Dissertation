"""
ReAct Engine Tool Selection Fix - Session 23

This patch adds intelligent tool selection constraints to prevent repeated tool calls.
The fix modifies _generate_thought to include:
1. Recent tool history in the prompt
2. Explicit "DO NOT use" constraints
3. Action validation to enforce diversity

Apply this as an override to the _generate_thought method in react_engine.py
"""

# Add this helper method to ReactEngine class:

def _get_tools_to_avoid(self) -> List[str]:
    """
    FIXED Session 23: Identify tools to avoid (recently used)
    Prevents consecutive tool calls and promotes diversity
    """
    tools_to_avoid = []
    
    if len(self.tool_usage_history) >= 1:
        # Never use the last tool again immediately
        tools_to_avoid.append(self.tool_usage_history[-1])
    
    if len(self.tool_usage_history) >= 2:
        # Avoid last 2 if they're the same (pattern detection)
        if self.tool_usage_history[-1] == self.tool_usage_history[-2]:
            # Add both to strongly discourage this pattern
            tools_to_avoid.extend([self.tool_usage_history[-1], self.tool_usage_history[-2]])
    
    if len(self.tool_usage_history) >= 3:
        # Avoid tools used 3+ times total
        from collections import Counter
        tool_counts = Counter(self.tool_usage_history)
        for tool, count in tool_counts.items():
            if count >= 3:
                tools_to_avoid.append(tool)
    
    return list(set(tools_to_avoid))  # Remove duplicates


def _generate_thought(self, problem_report: str, context: Dict) -> Dict[str, Any]:
    """
    FIXED Session 23: LLM generates reasoning with tool diversity constraints
    
    Now includes:
    - Recent tool history
    - Explicit forbidden tools
    - Alternative suggestions
    - Tool diversity scoring
    """
    context_hints = self._extract_context_hints(context)
    
    # Get tools to avoid
    tools_to_avoid = self._get_tools_to_avoid()
    all_tools = [t['name'] for t in self.tools.list()]
    alternative_tools = [t for t in all_tools if t not in tools_to_avoid]
    
    # Build recent tool history
    recent_tools_str = ", ".join(self.tool_usage_history[-3:]) if self.tool_usage_history else "None"
    
    constraint_text = ""
    if tools_to_avoid:
        constraint_text = f"""
⚠️  TOOL CONSTRAINTS (Session 23 Fix):
- DO NOT use these tools (just used): {', '.join(tools_to_avoid)}
- MUST try alternative tools: {', '.join(alternative_tools[:4])}
- Recent tools used: {recent_tools_str}
- Tool diversity is CRITICAL for investigation success
"""
    
    prompt = f"""You are {self.agent_name}, investigating this problem:
Problem: {problem_report}

Context Information: {json.dumps(context, indent=2)}
{context_hints}

Investigation History (last 3 steps):
{self._format_history()}
{constraint_text}

Available Tools:
{self._format_tools()}

STRATEGIC THINKING:
1. What angles haven't I explored yet?
   - User account/permissions status?
   - System/hardware configuration?
   - Network connectivity?
   - Application state?
2. What tool would provide NEW information (not repeat what I just checked)?
3. What is my updated hypothesis after recent findings?
4. If the printer is offline, could the issue be USER PERMISSIONS rather than printer status?
5. If the user has permission issues, have I checked USER ACCOUNT STATUS?

MANDATORY REQUIREMENTS:
- DO NOT repeat tools from the constraint list above
- MUST choose from the alternative tools suggested
- Explain WHY this tool is different from recent ones
- Use specific values from Context Information
- This is your LAST CHANCE to fix tool diversity - you will be intercepted if you try to reuse a tool

Respond in JSON format:
{{
    "reasoning": "Your strategic reasoning, explaining tool diversity approach",
    "why_this_tool": "Why this tool is different from what you just used",
    "current_hypothesis": "Your current working hypothesis",
    "next_action": {{
        "tool_name": "tool_to_use (MUST be from alternatives if constraints exist)",
        "parameters": {{"param1": "specific_value_from_context"}},
        "expectation": "What you expect to find"
    }},
    "status": "INVESTIGATING" or "ROOT_CAUSE_FOUND" or "NEEDS_COLLABORATION"
}}"""
    
    try:
        response = self.llm.invoke(prompt)
        response_text = response.content if hasattr(response, 'content') else str(response)
        
        if '{' in response_text:
            start = response_text.find('{')
            end = response_text.rfind('}') + 1
            json_str = response_text[start:end]
            thought = json.loads(json_str)
            
            # VALIDATION: Check if LLM tried to violate constraints
            tool_name = thought.get('next_action', {}).get('tool_name', '')
            if tool_name in tools_to_avoid:
                print(f"   [TOOL OVERRIDE] LLM tried '{tool_name}' (forbidden), forcing alternative...")
                if alternative_tools:
                    thought['next_action']['tool_name'] = alternative_tools[0]
                    thought['next_action']['parameters'] = {}
                    print(f"   [FORCED] Now using: {alternative_tools[0]}")
                else:
                    thought['next_action']['tool_name'] = self._select_default_tool()
            
            return thought
        else:
            return {
                "reasoning": response_text,
                "current_hypothesis": "Investigation",
                "next_action": {
                    "tool_name": (alternative_tools[0] if alternative_tools else self._select_default_tool()),
                    "parameters": {},
                    "expectation": "Gather information"
                },
                "status": "INVESTIGATING"
            }
    except Exception as e:
        print(f" Error generating thought: {e}")
        return {
            "reasoning": f"Error: {e}",
            "status": "INVESTIGATING",
            "next_action": {
                "tool_name": (alternative_tools[0] if alternative_tools else self._select_default_tool()),
                "parameters": {},
                "expectation": "Basic diagnostic check"
            }
        }
