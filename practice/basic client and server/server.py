from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv
import os

load_dotenv()
# Create an MCP server
mcp = FastMCP(
    name="Veronica",
    host="0.0.0.0",
    port=8050,
)

# Add a tool
@mcp.tool()
def hello(name: str):
    return f"Hello {name}"

# Run the server
if __name__ == "__main__":
    transport = "stdio"
    if transport == "stdio":
        print("Running server with stdio transport")
        mcp.run(transport="stdio")
    elif transport == "sse":
        print("Running server with SSE transport")
        mcp.run(transport="sse")
    else:
        raise ValueError(f"Unknown transport: {transport}")

