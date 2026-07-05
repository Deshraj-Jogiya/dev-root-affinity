# Zero-Copy Binary Parsing in Python with `memoryview`

When processing large binary files or network packets in Python, slicing bytes objects (e.g., `data[4:12]`) creates expensive memory copies and triggers garbage collection overhead. By leveraging Python's built-in `memoryview` along with the `struct` module, we can slice and unpack binary buffers without copying the underlying bytes. This "zero-copy" approach drastically reduces memory fragmentation and CPU overhead in high-throughput data pipelines.

## Key Takeaways
- `memoryview` exposes Python's internal buffer protocol, allowing slice operations to return a new view pointing to the existing memory buffer rather than allocating and copying data.
- Combining `memoryview` with `struct.unpack_from` allows direct parsing of structured binary data from specific offsets without allocating temporary substring objects.
- This technique is highly effective for writing high-performance network parsers, custom database file readers, or handling large scientific datasets in memory-constrained environments.

## Code Example
```python
import struct

# Simulate a binary stream (e.g., read from a socket or file)
# Header: Magic (4 bytes), Packet ID (2-byte uint), Payload Length (2-byte uint)
# Followed by the payload: "DEADBEEF"
raw_buffer = b"MZ\x00\x00\x01\x02\x00\x04DEADBEEF"

# Create a memoryview over the read-only bytes buffer
view = memoryview(raw_buffer)

# Define the header format using struct.Struct (compiled for reuse)
# '>' = big-endian, 'I' = 4-byte uint, 'H' = 2-byte uint, 'H' = 2-byte uint
header_format = struct.Struct(">IHH")

# Unpack directly from the memoryview without slicing the buffer
magic, packet_id, payload_len = header_format.unpack_from(view, 0)

print(f"Magic: {magic:#x}, ID: {packet_id}, Length: {payload_len}")

# Slice the payload using memoryview (zero-copy slice)
payload_offset = header_format.size
payload_view = view[payload_offset : payload_offset + payload_len]

# Convert to bytes/string only when absolutely necessary (e.g., for output)
print(f"Payload: {payload_view.tobytes().decode('ascii')}")
```

---
*Logged on 2026-03-02 22:15:00 (UTC)*
