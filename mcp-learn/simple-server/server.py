from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv

load_dotenv("../.env")


mcp = FastMCP(
    name="Calculator",
    host="0.0.0.0", # only used for SSE transport (localhost)
    port=8050 # only used for SSE transport 
)

@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers together"""
    return a + b

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
