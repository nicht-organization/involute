import asyncio
from typing import List
from .mmap import stream_file
from ..core.ffi import GATE_ALL


async def stream_file_async(
    filepath: str, 
    num_triples: int = 10_000_000, 
    flags: int = GATE_ALL
) -> List[bool]:
    """Asynchronously dispatches the zero-copy mmap C execution off the main event loop thread."""
    return await asyncio.to_thread(stream_file, filepath, num_triples, flags)
