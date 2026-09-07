import ctypes
from ..core.ffi import _lib, GATE_ALL


def stream_file(filepath: str, num_triples: int = 10_000_000, flags: int = GATE_ALL) -> list[bool]:
    out_buffer = (ctypes.c_uint8 * num_triples)()
    processed = _lib.export_involute_mmap_stream_eval(
        filepath.encode("utf-8"), out_buffer, flags
    )
    return [bool(x) for x in out_buffer[:processed]]
