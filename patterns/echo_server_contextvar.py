from __future__ import annotations

import asyncio
from contextvars import ContextVar

StreamReader = asyncio.streams.StreamReader
StreamWriter = asyncio.streams.StreamWriter

client_addr_var = ContextVar("client_addr")  # type: ContextVar


def render_goodbye() -> bytes:
    # The address of the currently handled client can be accessed
    # without passing it explicitly to this function.

    client_addr = client_addr_var.get()
    return f"Good bye, client @ {client_addr}\n".encode()


async def handle_request(reader: StreamReader, writer: StreamWriter) -> None:
    addr = writer.transport.get_extra_info("socket").getpeername()
    client_addr_var.set(addr)

    # In any code that we call is now possible to get
    # client's address by calling 'client_addr_var.get()'.

    while True:
        line = await reader.readline()
        print(line)
        if not line.strip():
            break
        writer.write(line)

    writer.write(render_goodbye())
    writer.close()


async def main() -> None:
    srv = await asyncio.start_server(handle_request, "127.0.0.1", 8081)

    async with srv:
        await srv.serve_forever()


asyncio.run(main())
