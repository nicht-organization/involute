import pytest
from involute.core.ffi import GATE_ALL
from involute.stream.async_mmap import stream_file_async


@pytest.mark.asyncio
async def test_stream_file_async_execution(tmp_path):
    bin_file = tmp_path / "async_triples.bin"

    # Pack 2 valid triples into a binary stream
    raw_bytes = (
        (2).to_bytes(8, "little") + (3).to_bytes(8, "little") + (5).to_bytes(8, "little") +
        (4).to_bytes(8, "little") + (5).to_bytes(8, "little") + (9).to_bytes(8, "little")
    )
    bin_file.write_bytes(raw_bytes)

    # Await the non-blocking thread execution
    results = await stream_file_async(str(bin_file), flags=GATE_ALL)
    
    assert len(results) == 2
    assert isinstance(results[0], bool)