from MainCode.decryption import parseKey

key = '5s20124M-3,-5,-5,3,2,-2,2,1,-43d3m171,1'
print(f"Key: {key}")
print(f"\nParsed commands:")

commands = parseKey(key)
for cmd in commands:
    print(f"  Type: '{cmd['type']}', Data: '{cmd['data']}'")
