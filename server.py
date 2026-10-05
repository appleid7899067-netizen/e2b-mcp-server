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

@mcp.tool()
def run_shell(command: str) -> str:
    """Run a shell command in an E2B sandbox."""
    with Sandbox.create() as sandbox:
        result = sandbox.commands.run(command)
        return f"STDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"

@mcp.tool()
def install_pip(package: str) -> str:
    """Install a pip package in an E2B sandbox."""
    with Sandbox.create() as sandbox:
        result = sandbox.commands.run(f"pip install {package}")
        return f"STDOUT:\n{result.stdout}\nSTDERR:\n{result.stderr}"

@mcp.tool()
def read_file(path: str) -> str:
    """Read a file from an E2B sandbox."""
    with Sandbox.create() as sandbox:
        content = sandbox.files.read(path)
        return content

@mcp.tool()
def write_file(path: str, content: str) -> str:
    """Write content to a file in an E2B sandbox."""
    with Sandbox.create() as sandbox:
        sandbox.files.write(path, content)
        return f"Written {len(content)} bytes to {path}"

@mcp.tool()
def list_files(path: str = "/home/user") -> str:
    """List files in an E2B sandbox directory."""
    with Sandbox.create() as sandbox:
        result = sandbox.commands.run(f"ls -la {path}")
        return result.stdout

if __name__ == "__main__":
    import uvicorn
    app = mcp.streamable_http_app()
    port = int(os.environ.get("PORT", 10000))
    uvicorn.run(app, host="0.0.0.0", port=port)
