import zlib
import struct

with open("challenge.png", "rb") as f:
    data = bytearray(f.read())

expected_crc = 0xcad1ced6

found = False
for h in range(1, 4096):
    height = struct.pack(">I", h)
    calculated_crc = zlib.crc32(data[12:20] + height + data[24:29])
    
    if calculated_crc == expected_crc:
        print(f"[+] Found original height: {h} (0x{height.hex()})")
        data[20:24] = height
        with open("fixed.png", "wb") as out:
            out.write(data)
        print("[+] Wrote repaired file to fixed.png")
        found = True
        break

if not found:
    print("[-] Height brute-force failed. Both width and height might be altered.")
