# Zero-Copy Binary Parsing with Python's memoryview

Python's `memoryview` object allows direct, zero-copy sharing of memory buffers between objects that support the buffer protocol (such as `bytes`, `bytearray`, or `array.array`). This is highly critical when writing high-performance binary parsers, network protocols, or file processors, as it avoids expensive allocations and CPU cycles spent copying byte arrays. By combining `memoryview` slicing with `struct.unpack_from`, you can parse complex binary headers and stream payloads at near-C speeds.

## Key Takeaways
- **Zero Memory Allocation:** Slicing a `memoryview` creates a new view referencing the original buffer instead of allocating new memory and copying bytes, keeping the memory footprint constant even with gigabyte-sized payloads.
- **Buffer Protocol Integration:** Standard library modules like `struct`, `socket`, and `io` natively accept `memoryview` objects, allowing you to read directly from network buffers or files into pre-allocated memory.
- **Writable Slices:** If the underlying object is mutable (like a `bytearray`), modifications made through a sliced `memoryview` directly mutate the source buffer, enabling efficient in-place data transformation.

## Code Example

```python
import struct

def parse_network_stream(stream_buffer: bytearray) -> list[tuple[int, memoryview]]:
    """Parses a stream of packets framed as [Length (4 bytes, Big-Endian) | Payload (N bytes)]
    without copying any underlying bytes.
    """
    # Wrap the bytearray in a memoryview to prevent copies during slicing
    view = memoryview(stream_buffer)
    packets = []
    offset = 0
    total_len = len(view)

    while offset + 4 <= total_len:
        # Read the 4-byte length prefix using struct.unpack_from (zero-copy)
        (payload_len,) = struct.unpack_from(">I", view, offset)
        
        if offset + 4 + payload_len > total_len:
            break  # Incomplete packet, wait for more data
        
        # Create a zero-copy slice of the payload
        payload_view = view[offset + 4 : offset + 4 + payload_len]
        packets.append((payload_len, payload_view))
        
        # Advance the offset pointer
        offset += 4 + payload_len

    return packets

# Demonstration of the zero-copy parser
if __name__ == "__main__":
    # Simulate an incoming TCP buffer containing two packets
    raw_buffer = bytearray()
    
    # Packet 1: 5 bytes payload -> "hello"
    raw_buffer.extend(struct.pack(">I", 5) + b"hello")
    # Packet 2: 12 bytes payload -> "zero-copy-io"
    raw_buffer.extend(struct.pack(">I", 12) + b"zero-copy-io")

    # Parse the stream
    parsed_packets = parse_network_stream(raw_buffer)

    for idx, (length, payload) in enumerate(parsed_packets, 1):
        # payload is a memoryview slice; no string copy has occurred yet
        print(f"Packet {idx} | Length: {length} bytes | Data: {payload.tobytes().decode('utf-8')}")
```

---
*Logged on 2024-10-27 16:00:00 (UTC)*
