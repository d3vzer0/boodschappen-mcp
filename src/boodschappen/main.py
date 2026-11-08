import asyncio

from fastmcp import FastMCP
from starlette.requests import Request
from starlette.responses import JSONResponse

from boodschappen.settings import Settings
from boodschappen.winkels.albert_heijn import main as albert_heijn
from boodschappen.winkels.jumbo import main as jumbo

settings = Settings()

mcp = FastMCP("MCP server voor het zoeken naar boodschappen")
mcp.mount(albert_heijn.mcp, namespace="ah")
mcp.mount(jumbo.mcp, namespace="jumbo")


@mcp.custom_route("/health", methods=["GET"], include_in_schema=False)
async def health(request: Request) -> JSONResponse:
    return JSONResponse({"status": "Ok"}, status_code=200)


if __name__ == "__main__":
    asyncio.run(
        mcp.run_async(
            transport="http",
            host=settings.mcp_host,
            port=settings.mcp_port,
        )
    )
