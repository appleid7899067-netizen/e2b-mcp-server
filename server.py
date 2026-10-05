from mcp.server.fastmcp import FastMCP
from mcp.server.transport_security import TransportSecuritySettings
from e2b_code_interpreter import Sandbox
import os

mcp = FastMCP(
    "E2B Runner",
    transport_security=TransportSecuritySettings(
        enable_dns_rebinding_protection=False,
    ),
)

@mcp.tool()
def run_code(code: str) -> str:
    """Execute Python code in an E2B sandbox."""
    with Sandbox.create() as sandbox:
        execution = sandbox.run_code(code)
        stdout = "".join(execution.logs.stdout or [])
        stderr = "".join(execution.logs.stderr or [])
        return f"STDOUT:\n{stdout}\nSTDERR:\n{stderr}"

if __name__ == "__main__":
    import uvicorn
    app = mcp.streamable_http_app()
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)
