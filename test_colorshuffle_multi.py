import sys
sys.path.insert(0, 'MainCode')

from encryption import colorShuffle
import encryption as enc
import random

# Set seed to force using only 1 channel
random.seed(42)

# Test multiple times to see different channel configurations
for test_num in range(10):
    random.seed(test_num)
    enc.key = ""
    
    test_input = [19, 4, 18, 19]  # "test"
    result = colorShuffle(test_input)
    
    key_str = enc.key
    channels_used = [int(ch) for ch in key_str[2:]]
    
    # Extract data
    extracted = []
    for pixel in result:
        for ch in channels_used:
            extracted.append(pixel[ch])
    
    extracted_no_padding = [v for v in extracted if v != 85]
    
    status = "✓" if extracted_no_padding == test_input else "✗"
    print(f"Test {test_num}: {status} Key={key_str}, Channels={len(channels_used)}, Pixels={len(result)}, Match={extracted_no_padding == test_input}")
    
    if extracted_no_padding != test_input:
        print(f"  Expected: {test_input}")
        print(f"  Got: {extracted_no_padding}")
