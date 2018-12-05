import sys

if len(sys.argv) != 2:
    print("Usage : {} <flag>".format(sys.argv[0]))
    sys.exit()
if len(sys.argv[1]) != 18:
    print("Flag length must be 18 chars long !")
    sys.exit()

alphabet = " _0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz.,:;?!'\"-=+*(){}"
flag = sys.argv[1]
rnd = [[1, 3, 3, 7][i % 4] for i in range(18)]
mov = [0x55 + ((i % 2) * 2 - 1) for i in range(18)]

for c in flag[::-1]:
    value = alphabet.index(c) + 0x27
    value ^= rnd.pop() ^ mov.pop()
    print("ld a,${:02X}\npush af".format(value))
