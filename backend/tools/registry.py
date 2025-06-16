_tool_registry = {}

def register_tool(name=None, description=None, parameters=None):
    def decorator(func):
        _tool_registry[name or func.__name__] = {
            "function": func,
            "spec": {
                "type": "function",
                "function": {
                    "name": name or func.__name__,
                    "description": description or func.__doc__ or "",
                    "parameters": parameters or {}
                }
            }
        }
        return func
    return decorator

def get_registered_tools():
    return [tool["spec"] for tool in _tool_registry.values()]

def call_tool_by_name(name, args):
    tool = _tool_registry.get(name)
    if not tool:
        return f"[Tool não encontrada: {name}]"
    return tool["function"](**args)
