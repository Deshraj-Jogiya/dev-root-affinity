# Zero-Copy Binary Parsing in Python with memoryview

When processing large binary payloads (such as network packets, custom file formats, or IPC buffers), copying byte slices creates significant memory overhead and triggers frequent garbage collection. Python's built-in `memoryview` allows you to access and slice underlying buffer data without duplicating the bytes in memory, enabling C-like zero-copy performance. Combining this with the `struct` module allows for safe, ultra-fast parsing of binary structures.

## Key Takeaways
- `memoryview` exposes Python's buffer protocol, allowing slice operations to return a new view pointing to the same underlying memory segment rather than allocating and copying new byte objects.
- Using `struct.unpack_from()` allows you to read typed binary data directly from a `memoryview` at a specific offset, eliminating the need to slice the buffer before parsing.
- This pattern is critical for high-throughput network applications (e.g., custom TCP protocol parsers or WebSocket frames) where minimizing allocations directly impacts request latency and CPU usage.

## Code Example
```python
import struct

# Simulate a large binary packet stream (e.g., received from a socket)
# Packet structure: Magic bytes (4B), Version (2B), Payload Length (4B), Payload (variable)
HEADER_FORMAT = "!4sHI"
HEADER_SIZE = struct.calcsize(HEADER_FORMAT)

def parse_packet_zero_copy(raw_data: bytes) -> dict:
    # Create a memoryview over the raw byte array (no allocation)
    view = memoryview(raw_data)

    # Unpack header fields directly from the buffer at offset 0
    magic, version, payload_len = struct.unpack_from(HEADER_FORMAT, view, 0)

    if magic != b"PACK":
        raise ValueError("Invalid protocol magic bytes")

    # Slice the memoryview to get the payload.
    # This returns a new memoryview object pointing to the original buffer.
    # Crucially, it does NOT copy the underlying bytes of the payload.
    payload_view = view[HEADER_SIZE : HEADER_SIZE + payload_len]

    return {
        "version": version,
        "payload_len": payload_len,
        "payload": payload_view,  # Downstream code can process this without copy overhead
    }

# Example usage with a mock buffer
binary_stream = b"PACK\x00\x02\x00\x00\x00\x0bHello World"
packet = parse_packet_zero_copy(binary_stream)

print(f"Parsed Version: {packet['version']}")
print(f"Payload (zero-copy): {packet['payload'].tobytes().decode('utf-8')}")
```

---
*Logged on 2024-05-24 16:30:00 (UTC)*
