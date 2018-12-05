import sys

if len(sys.argv) != 2:
    print("Usage : {} <text>".format(sys.argv[0]))
    sys.exit()

alphabet = " _0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz.,:;?!'\"-=+*(){}"
text = sys.argv[1]

print("ld a,{}\nldi (hl),a".format(len(text)))
lc = ''
for c in text[::-1]:
    if c != lc:
        print("ld a,${:02X}".format(alphabet.index(c) + 0x27))
    print("ldi (hl),a")
    lc = c
