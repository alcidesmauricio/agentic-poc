import inspect

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

def register_built_in_tools():
    import backend.tools.builtin_tools

def get_registered_tools():
    return [tool["spec"] for tool in _tool_registry.values()]

async def call_tool_by_name(name, args):
    tool = _tool_registry.get(name)
    if not tool:
        return f"[Tool não encontrada: {name}]"
    func = tool["function"]
    if inspect.iscoroutinefunction(func):
        return await func(**args)
    else:
        return func(**args)

