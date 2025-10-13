"""
Tool Registry - Manages domain-specific diagnostic tools
Enables LLM function calling for ReAct pattern
"""

from typing import Dict, List, Any, Callable, Optional
from dataclasses import dataclass
import inspect


@dataclass
class Tool:
    """Represents a diagnostic tool"""
    name: str
    function: Callable
    description: str
    parameters: Dict[str, Any]
    domain: str


class ToolRegistry:
    """
    Manages domain-specific diagnostic tools
    Each agent has their own tool registry
    """
    
    def __init__(self, domain: str):
        """
        Initialize tool registry
        
        Args:
            domain: Domain of tools (e.g., 'infrastructure', 'network', 'application')
        """
        self.domain = domain
        self.tools: Dict[str, Tool] = {}
    
    def register(self, 
                 function: Callable,
                 description: str,
                 parameters: Optional[Dict[str, Any]] = None) -> None:
        """
        Register a diagnostic tool
        LLM uses description to decide when to call it
        
        Args:
            function: The diagnostic function to register
            description: Clear description for LLM
            parameters: Parameter schema (auto-generated if None)
        """
        tool_name = function.__name__
        
        # Auto-generate parameter schema if not provided
        if parameters is None:
            parameters = self._extract_parameters(function)
        
        tool = Tool(
            name=tool_name,
            function=function,
            description=description,
            parameters=parameters,
            domain=self.domain
        )
        
        self.tools[tool_name] = tool
        print(f"Registered tool: {tool_name} ({self.domain})")
    
    def list(self) -> List[Dict[str, Any]]:
        """
        Returns tool descriptions for LLM
        Format optimized for function calling
        """
        return [
            {
                'name': tool.name,
                'description': tool.description,
                'parameters': tool.parameters,
                'domain': tool.domain
            }
            for tool in self.tools.values()
        ]
    
    def execute(self, tool_name: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute tool and return observation
        
        Args:
            tool_name: Name of tool to execute
            params: Parameters for the tool
            
        Returns:
            Tool execution result
        """
        if tool_name not in self.tools:
            return {
                'success': False,
                'error': f'Tool {tool_name} not found in {self.domain} registry',
                'available_tools': list(self.tools.keys())
            }
        
        tool = self.tools[tool_name]
        
        try:
            # Validate and clean parameters
            cleaned_params = self._validate_parameters(tool, params)
            
            # Execute the tool
            result = tool.function(**cleaned_params)
            
            return {
                'success': True,
                'tool': tool_name,
                'domain': self.domain,
                'data': result
            }
        except Exception as e:
            # Provide helpful error with parameter guidance
            sig = inspect.signature(tool.function)
            expected_params = list(sig.parameters.keys())
            
            return {
                'success': False,
                'tool': tool_name,
                'error': str(e),
                'error_type': type(e).__name__,
                'expected_parameters': expected_params,
                'provided_parameters': list(params.keys()),
                'hint': self._generate_parameter_hint(tool, params)
            }
    
    def get_tool(self, tool_name: str) -> Optional[Tool]:
        """Get tool by name"""
        return self.tools.get(tool_name)
    
    def _extract_parameters(self, function: Callable) -> Dict[str, Any]:
        """
        Auto-extract parameter schema from function signature
        """
        sig = inspect.signature(function)
        parameters = {}
        
        for param_name, param in sig.parameters.items():
            param_info = {
                'type': self._get_param_type(param),
                'required': param.default == inspect.Parameter.empty
            }
            
            if param.default != inspect.Parameter.empty:
                param_info['default'] = param.default
            
            parameters[param_name] = param_info
        
        return parameters
    
    def _get_param_type(self, param: inspect.Parameter) -> str:
        """Get parameter type as string"""
        if param.annotation != inspect.Parameter.empty:
            annotation = param.annotation
            if hasattr(annotation, '__name__'):
                return annotation.__name__
            return str(annotation)
        return 'any'
    
    def _validate_parameters(self, tool: Tool, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate and clean parameters to match function signature
        Removes unknown params, adds defaults, provides helpful errors
        
        Args:
            tool: Tool to execute
            params: Parameters provided by LLM
            
        Returns:
            Cleaned parameters that match function signature
        """
        sig = inspect.signature(tool.function)
        cleaned = {}
        
        # Get all expected parameters
        for param_name, param in sig.parameters.items():
            if param_name in params:
                # Use provided parameter (with network validation if applicable)
                value = params[param_name]
                cleaned[param_name] = self._validate_network_parameter(param_name, value, tool)
            elif param.default != inspect.Parameter.empty:
                # Use default value for optional parameter
                cleaned[param_name] = param.default
            else:
                # Required parameter missing - try to infer or use smart defaults
                inferred = self._infer_missing_parameter(param_name, tool, params)
                cleaned[param_name] = self._validate_network_parameter(param_name, inferred, tool)
        
        return cleaned
    
    def _infer_missing_parameter(self, param_name: str, tool: Tool, provided_params: Dict) -> Any:
        """
        Infer missing required parameters using smart defaults
        
        Common patterns:
        - user_id: Extract from context or use 'default'
        - app_name/server_name/resource: Use 'default' or first tool-specific value
        - hours/timeframe: Use 1 as default
        - test_operation: Use 'login' as default
        """
        # First check if there's a 'context' key in provided_params that might have the value
        if 'context' in provided_params and isinstance(provided_params['context'], dict):
            if param_name in provided_params['context']:
                return provided_params['context'][param_name]
        
        # Common defaults for typical IT support parameters
        defaults = {
            'user_id': 'default_user',
            'app_name': 'default_app',
            'server_name': 'localhost',
            'resource': 'default_resource',
            'printer_name': 'default_printer',
            'software_name': 'default_software',
            'hours': 1,
            'test_operation': 'login',
            'interface': 'eth0',
            # Network-specific defaults (Session 12 - Priority 1 enhancement)
            'host': 'localhost',
            'destination': '8.8.8.8',  # Google DNS
            'domain': 'google.com',
            'source': 'localhost',
            'count': 10,
            'max_hops': 15
        }
        
        # Return smart default if available
        if param_name in defaults:
            return defaults[param_name]
        
        # Check if similar parameter was provided (e.g., start_time instead of hours)
        if 'time' in param_name and ('start_time' in provided_params or 'end_time' in provided_params):
            # LLM wanted time range, but we need hours
            return 1  # Default to 1 hour
        
        # Last resort: empty string or None
        return ''
    
    def _validate_network_parameter(self, param_name: str, value: Any, tool: Tool) -> Any:
        """
        Validate and sanitize network-specific parameters
        Session 12 - Priority 1 enhancement
        
        Args:
            param_name: Name of the parameter
            value: Value to validate
            tool: Tool being executed
            
        Returns:
            Validated/sanitized value
        """
        import re
        
        # Only validate for network domain tools
        if tool.domain != 'network':
            return value
        
        # IP address validation
        if param_name in ['host', 'destination', 'source']:
            # Allow special hostnames
            if value in ['localhost', '127.0.0.1', '0.0.0.0']:
                return value
            
            # Check if it looks like a hostname (not IP)
            if not re.match(r'^\d+\.\d+\.\d+\.\d+$', str(value)):
                # Assume it's a valid hostname, no validation needed
                return value
            
            # Validate IP address format
            try:
                octets = str(value).split('.')
                if len(octets) == 4:
                    if all(0 <= int(octet) <= 255 for octet in octets):
                        return value
            except (ValueError, AttributeError):
                pass
            
            # Invalid IP - return safe default
            print(f"Warning: Invalid IP address '{value}' for {param_name}, using 'localhost'")
            return 'localhost'
        
        # Domain name validation (basic)
        if param_name == 'domain':
            if re.match(r'^[a-zA-Z0-9][a-zA-Z0-9-\.]*[a-zA-Z0-9]$', str(value)):
                return value
            print(f"Warning: Invalid domain '{value}', using 'google.com'")
            return 'google.com'
        
        # Interface name validation
        if param_name == 'interface':
            if re.match(r'^[a-zA-Z]+\d*$', str(value)):
                return value
            print(f"Warning: Invalid interface '{value}', using 'eth0'")
            return 'eth0'
        
        # Integer range validation for network tools
        if param_name == 'count':
            try:
                count = int(value)
                if 1 <= count <= 100:
                    return count
                print(f"Warning: count {count} out of range (1-100), using 10")
                return 10
            except (ValueError, TypeError):
                return 10
        
        if param_name == 'max_hops':
            try:
                hops = int(value)
                if 1 <= hops <= 30:
                    return hops
                print(f"Warning: max_hops {hops} out of range (1-30), using 15")
                return 15
            except (ValueError, TypeError):
                return 15
        
        # No validation needed for this parameter
        return value
    
    def _generate_parameter_hint(self, tool: Tool, provided_params: Dict) -> str:
        """
        Generate helpful hint for LLM about correct parameters
        """
        sig = inspect.signature(tool.function)
        required = []
        optional = []
        
        for param_name, param in sig.parameters.items():
            if param.default == inspect.Parameter.empty:
                required.append(param_name)
            else:
                optional.append(f"{param_name}={param.default}")
        
        hint = f"Tool '{tool.name}' expects: "
        if required:
            hint += f"Required: {', '.join(required)}. "
        if optional:
            hint += f"Optional: {', '.join(optional)}."
        
        # Identify what went wrong
        provided = set(provided_params.keys())
        expected = set(sig.parameters.keys())
        unexpected = provided - expected
        missing = expected - provided
        
        if unexpected:
            hint += f" Unexpected parameters: {', '.join(unexpected)}."
        if missing:
            hint += f" Missing parameters: {', '.join(missing)}."
        
        return hint
    
    def count(self) -> int:
        """Get number of registered tools"""
        return len(self.tools)
    
    def __repr__(self) -> str:
        return f"ToolRegistry(domain='{self.domain}', tools={self.count()})"


def tool(description: str, parameters: Optional[Dict] = None):
    """
    Decorator for registering tools
    
    Usage:
        @tool(description="Checks server metrics")
        def check_server_metrics(server_name: str):
            return {...}
    """
    def decorator(func: Callable) -> Callable:
        func._tool_description = description
        func._tool_parameters = parameters
        func._is_tool = True
        return func
    return decorator
