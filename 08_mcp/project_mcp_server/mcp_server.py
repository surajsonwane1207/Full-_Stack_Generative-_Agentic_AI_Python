import asyncio
from mcp.server.fastmcp import FastMCP

# Create an MCP server
mcp = FastMCP("System Stats Server")

@mcp.tool()
def get_system_time() -> str:
    """Returns the current system time."""
    from datetime import datetime
    return datetime.now().isoformat()

@mcp.tool()
def get_cpu_count() -> int:
    """Returns the number of CPU cores on the host machine."""
    import os
    return os.cpu_count() or 1

@mcp.tool()
def echo_message(message: str) -> str:
    """Returns the message back, useful for testing connection."""
    return f"MCP Server Echo: {message}"

if __name__ == "__main__":
    # Run the MCP server over standard input/output
    print("Starting MCP Server on STDIO...", flush=True)
    mcp.run(transport='stdio')
