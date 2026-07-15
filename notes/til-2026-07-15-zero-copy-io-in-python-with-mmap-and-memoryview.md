# Zero-Copy I/O in Python with mmap and memoryview

When processing massive files, traditional I/O operations copy data multiple times between kernel space, user space, and Python's runtime memory, leading to high CPU overhead and memory thrashing. By pairing memory-mapped files (`mmap`) with Python's built-in `memoryview`, we can slice and manipulate binary data directly from the OS page cache without duplicating bytes in memory. This "zero-copy" approach dramatically reduces memory consumption and speeds up large-scale file parsing.

## Key Takeaways
- `mmap` maps a file directly into the process's virtual address space, allowing file access to behave like reading an in-memory array while letting the OS handle demand-paging and caching.
- `memoryview` allows safe, zero-copy slicing of objects supporting the buffer protocol (like `mmap` or `bytes`), avoiding the creation of new string/bytes objects in Python's heap.
- This pattern is highly effective for writing high-performance parsers (e.g., binary protocols, CSVs, or custom log formats) where you need to scan and extract subsets of data from multi-gigabyte files.

## Code Example

```python
import mmap
import os

# Create a dummy binary file representing structured log packets
# Format: [4-byte ID] [Payload] [Newline Delimiter]
filename = "telemetry_data.bin"
with open(filename, "wb") as f:
    f.write(b"\x00\x00\x00\x01" + b"METRIC_CPU: 92%" + b"\n")
    f.write(b"\x00\x00\x00\x02" + b"METRIC_MEM: 45%" + b"\n")
    f.write(b"\x00\x00\x00\x01" + b"METRIC_CPU: 95%" + b"\n")

def parse_metrics(file_path: str, target_id: bytes):
    with open(file_path, "r+b") as f:
        # Memory-map the file (read-only to prevent accidental writes)
        with mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ) as mm:
            # Create a memoryview over the mapped file buffer
            mv = memoryview(mm)
            
            offset = 0
            file_size = len(mm)
            
            while offset < file_size:
                # Scan for the newline delimiter
                next_newline = mm.find(b"\n", offset)
                if next_newline == -1:
                    break
                
                # Zero-Copy slice: Creates a subview without copying the underlying bytes
                line_view = mv[offset:next_newline]
                
                # Extract header and payload using slice notation on the view
                packet_id = line_view[0:4]
                if packet_id.tobytes() == target_id:
                    payload_view = line_view[4:]
                    # Only allocate memory for string instantiation when we find a match
                    print(f"Match found at offset {offset}: {payload_view.tobytes().decode('utf-8')}")
                    
                offset = next_newline + 1

# Extract all payloads belonging to packet ID: \x00\x00\x00\x01
parse_metrics(filename, b"\x00\x00\x00\x01")

# Clean up
os.remove(filename)
```

---
*Logged on 2024-11-14 16:45:00 (UTC)*
