# Zero-Copy Binary Parsing in Python using memoryview

Python's `memoryview` allows safe, zero-copy sharing of memory between data structures by exposing the buffer protocol at the C-level. When parsing massive binary payloads—such as network packets, database files, or serialized ML tensors—standard slicing on `bytes` creates physical memory copies, which degrades performance and triggers garbage collection. Utilizing `memoryview` alongside the `struct` module allows you to slice, cast, and mutate raw byte buffers in-place with zero allocation overhead.

## Key Takeaways
- Slicing standard Python `bytes` or `bytearray` objects creates physical memory copies, whereas slicing a `memoryview` produces a new view pointing to the exact same underlying buffer.
- The `.cast()` method on a `memoryview` allows you to reinterpret block memory into different C-types (e.g., casting bytes to 32-bit floats) without iterating or copying.
- Combining `memoryview` with `struct.unpack_from` allows you to extract structured binary headers at arbitrary offsets while avoiding intermediate substring allocations.

## Code Example
```python
import struct

def parse_network_packet(packet_buffer: bytearray):
    # Create a memoryview over the raw byte buffer to prevent copying
    view = memoryview(packet_buffer)
    
    # Read the header fields without slicing the buffer
    # Header: 2-byte packet ID (unsigned short), 4-byte payload length (unsigned int)
    packet_id, payload_len = struct.unpack_from(">HI", view, 0)
    
    # Slice the payload as a zero-copy sub-view
    payload_view = view[6:6 + payload_len]
    
    # Cast the payload directly to 32-bit single-precision floats (C-type 'f')
    # This exposes the underlying bytes as floats with zero allocation
    float_values = payload_view.cast('f')
    
    return packet_id, float_values

# Simulate receiving a binary packet: Type 42, 12 bytes of payload (3 floats)
raw_packet = bytearray(struct.pack(">HIfff", 42, 12, 1.1, 2.2, 3.3))

packet_id, float_data = parse_network_packet(raw_packet)

print(f"Packet ID: {packet_id}")
print(f"Decoded Floats: {list(float_data)}")

# Because it is zero-copy, mutating the cast view updates the original buffer in-place
float_data[0] = 99.9
print(f"Mutated raw buffer payload (first 4 bytes of float): {raw_packet[6:10]}")
```

---
*Logged on 2024-06-03 14:15:22 (UTC)*
