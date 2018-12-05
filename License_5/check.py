import hashlib

KEY = 0x57616e6e6120726561647a203f203e626574612e6861636b6e646f2e636f6d3c
def encrypt(license):
    hashes = []
    with open(license) as f:
        for line in f:
            hashes.append(int(hashlib.sha256(line).hexdigest(), 16))
    return reduce((lambda x, y: x^y), hashes)

if encrypt('license.txt') == KEY:
    print('Registered !')
else:
    print('Wrong license file.')
