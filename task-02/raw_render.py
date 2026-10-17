import struct
import zlib
from PIL import Image

# 1. Read and clean the 12 corrupted bytes
with open("challenge.png", "rb") as f:
    data = bytearray(f.read())
clean_data = data[:0x30045] + data[0x30051:]

# 2. Extract IDAT chunks
idat_stream = b""
pos = 8
while pos < len(clean_data):
    length = struct.unpack(">I", clean_data[pos : pos + 4])[0]
    chunk_type = clean_data[pos + 4 : pos + 8]
    if chunk_type == b"IDAT":
        idat_stream += clean_data[pos + 8 : pos + 8 + length]
    pos += 12 + length

# 3. Decompress raw stream
decompressor = zlib.decompressobj(-15)
raw = decompressor.decompress(idat_stream[2:])

print(f"Total decompressed bytes: {len(raw)}")
print(f"First 32 bytes (hex): {raw[:32].hex()}")
print(f"First 32 bytes (repr): {raw[:32]!r}\n")


# 4. Try rendering as raw RGB (ignoring filter bytes entirely)
# 724 * 850 * 3 = 1,846,200 bytes
try:
    img_raw = Image.frombytes("RGB", (724, 850), raw[: 724 * 850 * 3])
    img_raw.save("raw_render.png")
    print("[+] Saved raw_render.png (rendered as pure RGB without filter bytes)")
except Exception as e:
    print(f"[-] Raw RGB render failed: {e}")
