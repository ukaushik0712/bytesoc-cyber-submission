import zlib
from PIL import Image

with open("challenge.png", "rb") as f:
    data = f.read()

# 1. Remove the 12 injected bytes after the 3rd IDAT chunk
clean_data = data[:0x30045] + data[0x30051:]

# 2. Extract and concatenate all IDAT chunk payloads
pos = 8
idat_stream = bytearray()

while pos < len(clean_data):
    length = int.from_bytes(clean_data[pos : pos + 4], "big")
    chunk_type = clean_data[pos + 4 : pos + 8]
    chunk_data = clean_data[pos + 8 : pos + 8 + length]

    if chunk_type == b"IDAT":
        idat_stream.extend(chunk_data)
    elif chunk_type == b"IEND":
        break

    pos += 12 + length

# 3. Decompress using raw deflate (skipping 2-byte header and ignoring Adler-32 checksum)
decompressor = zlib.decompressobj(-15)
raw_pixels = decompressor.decompress(bytes(idat_stream[2:]))

# 4. Re-align scanlines, reverse PNG filters, and crop the flag area
width, height = 724, 850
bpp = 3  # 3 bytes per pixel (RGB)
stride = 1 + width * bpp  # 2173 bytes per scanline

recon_all = bytearray()
prev_row = bytearray(width * bpp)

for y in range(height):
    row = raw_pixels[y * stride : (y + 1) * stride]
    ftype = row[0]
    scanline = row[1:]  # Strip the 1-byte filter header
    recon = bytearray(len(scanline))

    for i in range(len(scanline)):
        left = recon[i - bpp] if i >= bpp else 0
        up = prev_row[i]

        if ftype == 1:    # Sub
            recon[i] = (scanline[i] + left) & 0xFF
        elif ftype == 2:  # Up
            recon[i] = (scanline[i] + up) & 0xFF
        else:             # None (0) or corrupted filter byte fallback
            recon[i] = scanline[i]

    recon_all.extend(recon)
    prev_row = recon


img_final = Image.frombytes("RGB", (width, height), bytes(recon_all))
img_cropped = img_final.crop((0, 780, width, height))
img_cropped.save("flag_cropped.png")
