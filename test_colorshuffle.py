import sys
sys.path.insert(0, 'MainCode')

from encryption import colorShuffle, key
import encryption as enc

# Test input: 4 character values (simulating "test")
# t=19, e=4, s=18, t=19
test_input = [19, 4, 18, 19]

print("=== Testing colorShuffle ===")
print(f"Input array: {test_input}")
print(f"Input length: {len(test_input)}")

# Reset key
enc.key = ""

# Run colorShuffle
result = colorShuffle(test_input)

print(f"\nOutput pixels: {result}")
print(f"Number of pixels: {len(result)}")
print(f"Key generated: {enc.key}")

# Parse the key
key_str = enc.key
length = int(key_str[0])
cmd_type = key_str[1]
channels_used = [int(ch) for ch in key_str[2:]]

print(f"\nKey analysis:")
print(f"  Command length: {length}")
print(f"  Command type: {cmd_type}")
print(f"  Channels used: {channels_used}")
print(f"  Number of channels: {len(channels_used)}")

# Verify data integrity
print(f"\n=== Verification ===")
print(f"Expected pixels needed: {len(test_input)} chars / {len(channels_used)} channels = {len(test_input) / len(channels_used):.2f} pixels")
print(f"Actual pixels created: {len(result)}")

# Extract data back
extracted = []
for pixel in result:
    for ch in channels_used:
        extracted.append(pixel[ch])

print(f"\nExtracted values: {extracted}")
print(f"Original values:  {test_input}")

# Remove padding (values of 85)
extracted_no_padding = [v for v in extracted if v != 85]
print(f"Extracted (no padding): {extracted_no_padding}")

if extracted_no_padding == test_input:
    print("\n✓ SUCCESS: colorShuffle preserves data correctly!")
else:
    print("\n✗ FAILURE: Data mismatch!")
    print(f"  Expected: {test_input}")
    print(f"  Got: {extracted_no_padding}")
