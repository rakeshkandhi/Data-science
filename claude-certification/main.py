import asyncio
import sys
from contextlib import AsyncExitStack

from core.claude import Claude
from core.cli import CliApp
from core.cli_chat import CliChat
from mcp_client import MCPClient

from config import settings


async def main():
    claude_service = Claude(model=settings.claude_model)

    server_scripts = sys.argv[1:]
    clients = {}

    command, args = (
        ("uv", ["run", "mcp_server.py"])
        if settings.use_uv
        else ("python", ["mcp_server.py"])
    )

    async with AsyncExitStack() as stack:
        doc_client = await stack.enter_async_context(
            MCPClient(command=command, args=args)
        )
        clients["doc_client"] = doc_client

        for i, server_script in enumerate(server_scripts):
            client_id = f"client_{i}_{server_script}"
            client = await stack.enter_async_context(
                MCPClient(command="uv", args=["run", server_script])
            )
            clients[client_id] = client

        chat = CliChat(
            doc_client=doc_client,
            clients=clients,
            claude_service=claude_service,
        )

        cli = CliApp(chat)
        await cli.initialize()
        await cli.run()


if __name__ == "__main__":
    # loop_factory replaces the deprecated set_event_loop_policy (removed in 3.16)
    loop_factory = (
        getattr(asyncio, "ProactorEventLoop", None) if sys.platform == "win32" else None
    )
    asyncio.run(main(), loop_factory=loop_factory)
