import asyncio

from fastmcp import FastMCP

from .settings import Settings

settings = Settings()

mcp = FastMCP("MCP server voor het zoeken naar boodschappen")


# @mcp.custom_route("/health", methods=["GET"], include_in_schema=False)
# async def health(request: Request) -> JSONResponse:
#     """Simple health endpoint."""
#     return JSONResponse({"status": "OK"}, status_code=200)


def main() -> None:
    asyncio.run(
        mcp.run_async(
            transport="http",
            host=settings.mcp_host,
            port=settings.mcp_port,
        )
    )
