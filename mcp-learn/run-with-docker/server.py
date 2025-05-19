from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv

load_dotenv("../.env")

mcp = FastMCP(
    name="Calculator",
    host="0.0.0.0",
    port=8050,
)


@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers together"""
    return a + b


if __name__ == "__main__":
    print("Running server with SSE transport")
    mcp.run(transport="sse")
