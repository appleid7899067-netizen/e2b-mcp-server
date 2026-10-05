from mcp.server.fastmcp import FastMCP
from e2b_code_interpreter import Sandbox

mcp = FastMCP("E2B Runner")

@mcp.tool()
def run_code(code: str) -> str:
    """Execute Python code in an E2B sandbox."""
    with Sandbox.create() as sandbox:
        execution = sandbox.run_code(code)
        stdout = "".join(execution.logs.stdout or [])
        stderr = "".join(execution.logs.stderr or [])
        return f"STDOUT:\n{stdout}\nSTDERR:\n{stderr}"
if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 10000))
    mcp.run(transport="streamable-http", host="0.0.0.0", port=port)
if __name__ == "__main__":
    mcp.run(transport="streamable-http")
