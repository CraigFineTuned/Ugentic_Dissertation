class Tool:
    """Base class for all MCP tools."""

    def __init__(self, name, description):
        self.name = name
        self.description = description

    def __call__(self, *args, **kwargs):
        raise NotImplementedError("Tool must implement __call__ method.")

    

    
