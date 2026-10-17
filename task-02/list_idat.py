with open("challenge.png", "rb") as f:
    data = f.read()

pos = 8
while pos < len(data):
    length = int.from_bytes(data[pos:pos+4], "big")
    name = data[pos+4:pos+8]
    print(f"Offset 0x{pos:06x} | Chunk: {name} | Length: {length}")
    pos += 12 + length
