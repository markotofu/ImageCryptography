# ImageCryptography Project Guide

## Overview
A multi-layered image-based cryptography system that encrypts text into PNG images using advanced obfuscation techniques including color channel manipulation, matrix transformations, dummy pixel injection, and cascading determinant-based transformations. The system uses a 64-character alphabet optimized for efficient encoding and provides reversible encryption with key-based decryption.

### ⚠️ Obfuscation vs. Encryption: Understanding the Difference

**This project is primarily OBFUSCATION, not cryptographic ENCRYPTION.**

#### What is Obfuscation?
**Obfuscation** makes data hard to understand by making it look random or meaningless, but it's not mathematically proven to be secure.

- **Goal:** Hide information by making it confusing
- **Security:** "Security through obscurity" - relies on keeping the method secret
- **Strength:** Can be broken with enough time, effort, and knowledge of the method
- **Standards:** No official standards or peer review
- **Example:** Scrambling text, encoding in images, custom ciphers

#### What is Encryption?
**Encryption** uses mathematically proven algorithms that are secure even when the method is publicly known.

- **Goal:** Make data mathematically impossible to decode without the key
- **Security:** Security through cryptographic strength - the algorithm is public!
- **Strength:** Would take millions of years to break with current computers (e.g., AES-256)
- **Standards:** Rigorously tested, peer-reviewed, government-approved (NIST, etc.)
- **Example:** AES, RSA, ChaCha20

#### This Project's Classification

| Aspect | This System | True Encryption (AES-256) |
|--------|-------------|---------------------------|
| **Type** | Advanced Obfuscation | Cryptographic Encryption |
| **Security Basis** | Complexity of method | Mathematical proof |
| **If Method Known** | Can be broken | Still secure with key |
| **Key Space** | ~40-80 bits | 256 bits (2²⁵⁶ possibilities) |
| **Attack Resistance** | Moderate | Extremely High |
| **Standardized** | No | Yes (NIST approved) |
| **Best For** | Fun, learning, puzzles | Sensitive data, real security |

#### Why This Matters

**What this system CAN protect against:**
- ✅ Casual observers (looks like random image)
- ✅ Basic automated scanning tools
- ✅ People without cryptography knowledge
- ✅ Quick manual inspection

**What this system CANNOT protect against:**
- ❌ Professional cryptanalysts
- ❌ Determined attackers with resources
- ❌ Known-plaintext attacks (if attacker has text-image pairs)
- ❌ Legal/government surveillance with warrants
- ❌ Advanced pattern recognition tools

#### When to Use This Project
- 🎓 **Learning:** Understand cryptography concepts
- 🧩 **Puzzles:** Create fun challenges for friends
- 🎨 **Art Projects:** Hide messages in images creatively
- 🔬 **Experimentation:** Test ideas and algorithms
- 💬 **Casual Privacy:** Hide non-critical personal notes

#### When NOT to Use This Project
- 🚫 **Banking/Financial Data**
- 🚫 **Passwords or Authentication**
- 🚫 **Legal Documents**
- 🚫 **Medical Records**
- 🚫 **Any data where security truly matters**

**For real security, use established libraries:**
- Python: `cryptography`, `PyCryptodome` (with AES-256)
- JavaScript: `crypto` module (with AES-GCM)
- Industry standard: TLS/SSL for communication

---

**Bottom Line:** This is a sophisticated obfuscation system that's great for learning and fun, but it's NOT a replacement for real encryption. Think of it as a really good puzzle lock vs. a bank vault.

## Setup Instructions

1. **Clone the repository:**
   ```sh
   git clone <your-repo-url>
   cd ImageCryptography
   ```

2. **Create a virtual environment (recommended):**
   ```sh
   python -m venv .venv
   ```

3. **Activate the virtual environment:**
   - **Windows PowerShell:**
     ```powershell
     . .\.venv\Scripts\Activate.ps1
     ```
   - **macOS/Linux:**
     ```sh
     source .venv/bin/activate
     ```

4. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```

5. **Run the code:**
   ```sh
   python MainCode/main.py
   ```

## Features

### Core Encryption Capabilities
- **64-Character Alphabet:** Optimized character set (a-z, 0-9, punctuation, special chars) perfectly aligned for 6-bit encoding
- **Multi-Layer Obfuscation:** 4+ independent obfuscation techniques applied in sequence
- **Key-Based Decryption:** Generates unique decryption keys for each encryption
- **Lossless Compression:** All text is perfectly recoverable with the correct key
- **Case-Insensitive:** Automatically converts uppercase to lowercase for consistent encoding

### Encryption Layers

#### 1. **Color Shuffle**
- Randomly shuffles RGB channel order (R→G→B, B→R→G, etc.)
- Can use 1, 2, or 3 color channels (randomly selected)
- Unused channels filled with random noise
- **Purpose:** Spreads character data across color channels unpredictably

#### 2. **Dummy Pixel Generator**
- Injects 2-7 random dummy pixels before each real pixel
- Dummy pixels are indistinguishable from real data
- **Purpose:** Increases image size and hides real data density

#### 3. **Matrix Obfuscation (per round)**
- Applies 3×3 matrix multiplication to pixel RGB values using modular arithmetic (mod 256)
- Each matrix has an odd determinant (coprime with 256) ensuring invertibility
- Uses Extended Euclidean Algorithm for modular inverse calculation
- **Purpose:** Non-linear transformation that spreads each input bit across all output bits

#### 4. **Randomized Manipulation (2-6 rounds)**
- Randomly applies either Matrix Obfuscation OR Determinant Cascading per round
- Number of rounds: 2-6 (randomly chosen each encryption)
- Commands stored in array, then reversed when building key
- Both transformations operate on the full grid
- **Purpose:** Unpredictable layering increases security, each round compounds previous transformations

#### 5. **Random Top Row**
- Adds a random pixel row at the top of the image
- Used as reference data for determinant calculations
- **Purpose:** Provides unpredictable seed data for cascading transformations

#### 6. **Determinant-Based Cascading (Working!)**
- Uses sliding 3-pixel windows to calculate determinants from first row reference pixels
- Each pixel transformation depends on three reference pixels
- Includes value modification: adds (det mod 4) × 64, giving offsets of 0, 64, 128, or 192
- **Cascading effect:** Each encrypted pixel becomes a reference for the next encryption
  - Reference window shifts: left ← picked, picked ← right, right ← newly encrypted
  - Creates dependency chain where each pixel affects all subsequent pixels
  - Must decrypt in FORWARD order (same as encryption) because each decrypted pixel is needed as reference
- Randomly interleaved with Matrix Obfuscation (2-6 total rounds)
- **Purpose:** Creates context-dependent encryption where identical characters produce different outputs based on position

### Security Features
- **~40 bits of entropy** (without random dictionary)
- **~474 bits of entropy** (with randomized dictionary - not yet implemented)
- Resistant to casual reverse-engineering
- Multiple independent obfuscation layers
- Deterministic but key-dependent transformations

## Usage Guide

### Running the Program
When you run `main.py`, you'll see a menu:
- **Option 1:** Text to Image Generation
- **Option 2:** Image Decryption

### Text to Image Mode
1. Select option `1`
2. Choose input method:
   - `1` for direct text input
   - `2` to read from `MainCode/testText` file
3. The program generates `output_image.png` in the project root

### Image to Text Mode
1. Select option `2`
2. The program reads `output_image.png` and prints the decrypted text

## How It Works

### 📊 Complete Encryption Flow Diagram

```
INPUT TEXT: "hello"
    ↓
┌─────────────────────────────────────────────────────────────┐
│ STEP 1: Character to Index Mapping                         │
│ Function: textToArray() → encryption()                     │
│                                                             │
│ "hello" → [7, 4, 11, 11, 14]                              │
│ (converts each char to its index in numToLetter array)    │
│                                                             │
│ Key Generated: (none yet)                                  │
└─────────────────────────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────────────────────────┐
│ STEP 2: Color Shuffle                                      │
│ Function: colorShuffle()                                    │
│                                                             │
│ Input:  [7, 4, 11, 11, 14]                                │
│ Action: Distribute across 1-3 RGB channels randomly        │
│         Unused channels filled with random noise           │
│ Output: [[7,R,R], [4,R,11], [11,R,14]]                    │
│         (R = random noise, example: 3 channels used)       │
│                                                             │
│ Key Generated: "5s012" (5 chars total, 's', channels 0,1,2)│
└─────────────────────────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────────────────────────┐
│ STEP 3: Dummy Pixel Injection                              │
│ Function: dummyPixelGenerator()                             │
│                                                             │
│ Input:  [[7,R,R], [4,R,11], [11,R,14]]                    │
│ Action: Insert 2-7 random pixels before EACH real pixel    │
│ Output: [[R,R,R], [R,R,R], [7,R,R],                       │
│          [R,R,R], [R,R,R], [4,R,11], ...]                 │
│         (example: 2 dummy pixels per real pixel)           │
│                                                             │
│ Key Generated: "3d2" (3 chars total, 'd', multiplier 2)   │
└─────────────────────────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────────────────────────┐
│ STEP 4: Grid Arrangement                                   │
│ Function: arrayToGrid()                                     │
│                                                             │
│ Input:  1D array of pixels                                 │
│ Action: Arrange into ~square grid + add random top row     │
│ Output: Grid structure:                                     │
│         Row 0: [R,R,R] [R,R,R] [R,R,R] [R,R,R] ← RANDOM   │
│         Row 1: [7,R,R] [R,R,R] [R,R,R] [4,R,11] ← DATA    │
│         Row 2: [R,R,R] [R,R,R] [11,R,14] [R,R,R] ← DATA   │
│                                                             │
│ Key Generated: (none)                                      │
└─────────────────────────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────────────────────────┐
│ STEP 5: Randomized Manipulation Loop (2-6 rounds)          │
│ Function: randomizedEncryption()                            │
│                                                             │
│ Randomly applies either:                                    │
│   • Matrix Obfuscation (M) OR                              │
│   • Determinant Cascading (m)                              │
│                                                             │
│ Example sequence: M → m → M → m                            │
│                                                             │
│ Commands stored in array: ["...M...", "3m2", "...M...", "3m1"]│
│ (will be reversed when added to key)                       │
└─────────────────────────────────────────────────────────────┘
    ↓
    ├─── OPTION A: Matrix Obfuscation ───┐
    │                                     │
┌───┴─────────────────────────────────────┴───────────────────┐
│ STEP 5A: Matrix Obfuscation (if chosen)                    │
│ Function: matrixObfuscation()                               │
│                                                             │
│ Input:  Grid of pixels [[R,G,B], [R,G,B], ...]            │
│ Action: For EACH pixel:                                     │
│         1. Create random 3×3 matrix M (odd determinant)     │
│         2. Multiply: [R',G',B'] = M × [R,G,B] mod 256      │
│                                                             │
│ Example:                                                    │
│   M = [[ 2, -1,  3],     [120]       [calculated]          │
│        [-1,  4,  0],  ×  [130]  =    [values]     mod 256  │
│        [ 1, -2,  1]]     [140]       [0-255]               │
│                                                             │
│ Output: Transformed grid (all pixels modified)             │
│                                                             │
│ Key Command: "25M2,-1,3,-1,4,0,1,-2,1"                    │
│             (length 25, 'M', matrix values)                │
└─────────────────────────────────────────────────────────────┘
    │
    └─── OPTION B: Determinant Cascading ──┐
                                            │
┌───────────────────────────────────────────┴─────────────────┐
│ STEP 5B: Determinant Cascading (if chosen)                 │
│ Function: detMultiplier()                                   │
│                                                             │
│ Input:  Grid of pixels (first row unchanged)               │
│ Action: For EACH data pixel (row 2+):                      │
│   1. Pick random pixel from row 0: pickedIndex = 2         │
│   2. Get 3 reference pixels: [left, picked, right]         │
│   3. Calculate determinant of 3×3 matrix from refs         │
│   4. Modify pixel: P' = (P + (det%4)×64) mod 256           │
│   5. CASCADE: Update refs for next pixel                   │
│      • left ← picked                                        │
│      • picked ← right                                       │
│      • right ← newly encrypted pixel                        │
│                                                             │
│ Example:                                                    │
│   Refs: [[100,150,200], [50,75,100], [25,30,35]]          │
│   det = 0, mod = (0%4)×64 = 0                              │
│   Pixel [120,130,140] → [(120+0)%256, ...] = [120,130,140]│
│                                                             │
│ Output: Modified grid (data rows transformed)              │
│                                                             │
│ Key Command: "3m2" (length 3, 'm', picked index 2)        │
└─────────────────────────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────────────────────────┐
│ STEP 6: Key Assembly                                       │
│ Function: encryption()                                      │
│                                                             │
│ Manipulation commands stored in array during loop:         │
│   ["25M2,-1,3,...", "3m2", "24M1,0,-2,...", "3m1"]        │
│                                                             │
│ Key assembly (commands REVERSED for decryption):           │
│   "5s012" + "3d2" + "3m1" + "24M1,0,-2,..." + "3m2" + ... │
│    ↑       ↑       ↑                                        │
│    │       │       └─ Manipulation commands (reversed!)    │
│    │       └───────── Dummy pixel multiplier               │
│    └───────────────── Color shuffle channels               │
│                                                             │
│ Final Key: "5s0123d23m124M1,0,-2,4,-5,1,0,3,-13m225M..." │
└─────────────────────────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────────────────────────┐
│ STEP 7: Image Generation                                   │
│ Function: textToArray()                                     │
│                                                             │
│ Action: Convert grid to PNG image                          │
│         Each pixel → RGB value at (x,y) coordinate         │
│                                                             │
│ Output: output_image.png                                   │
│         Appears as random colored noise                     │
└─────────────────────────────────────────────────────────────┘

OUTPUT: PNG Image + Decryption Key
```

### 📊 Complete Decryption Flow Diagram

```
INPUT: PNG Image + Decryption Key
    ↓
┌─────────────────────────────────────────────────────────────┐
│ STEP 1: Load Image & Parse Key                             │
│ Function: decryption()                                      │
│                                                             │
│ Actions:                                                    │
│   1. Load output_image.png                                 │
│   2. Convert to pixel grid using imgToGrid()               │
│   3. Parse key string into command array                   │
│                                                             │
│ Key: "5s0123d23m124M...3m225M..."                         │
│ Parsed Commands:                                            │
│   [{'type':'s', 'data':'012'},                             │
│    {'type':'d', 'data':'2'},                               │
│    {'type':'m', 'data':'1'},                               │
│    {'type':'M', 'data':'2,-1,3,...'},                      │
│    {'type':'m', 'data':'2'},                               │
│    {'type':'M', 'data':'...'}]                             │
└─────────────────────────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────────────────────────┐
│ STEP 2: Reverse Manipulation Commands (IN ORDER)           │
│ Function: decryption() loop                                 │
│                                                             │
│ Process manipulation commands ('M' and 'm') sequentially:   │
│ Commands already in CORRECT reverse order from encryption  │
│                                                             │
│ For each command:                                           │
│   if type == 'm': reverseDetMultiplier()                   │
│   if type == 'M': reverseMatrixObfuscation()               │
└─────────────────────────────────────────────────────────────┘
    ↓
    ├─── Process 'm' commands ────┐
    │                              │
┌───┴──────────────────────────────┴──────────────────────────┐
│ STEP 2A: Reverse Determinant Cascading                     │
│ Function: reverseDetMultiplier()                            │
│                                                             │
│ Input:  Encrypted grid                                      │
│ Action: FORWARD decryption (same order as encryption):      │
│   1. Get pickedIndex from command data                      │
│   2. Initialize refs: [left, picked, right] from row 0     │
│   3. For EACH data pixel (row 2+):                         │
│      a. Calculate SAME determinant as encryption            │
│      b. Reverse: P = (P' - (det%4)×64) mod 256             │
│      c. CASCADE: Update refs with DECRYPTED pixel           │
│         • left ← picked                                     │
│         • picked ← right                                    │
│         • right ← decrypted pixel                           │
│                                                             │
│ Key Insight: Must process FORWARD because each decrypted   │
│              pixel is needed as reference for the next!     │
│                                                             │
│ Output: Partially decrypted grid                           │
└─────────────────────────────────────────────────────────────┘
    │
    └─── Process 'M' commands ────┐
                                   │
┌──────────────────────────────────┴──────────────────────────┐
│ STEP 2B: Reverse Matrix Obfuscation                        │
│ Function: reverseMatrixObfuscation()                        │
│                                                             │
│ Input:  Encrypted grid (flattened to 1D for processing)    │
│ Action: For EACH pixel:                                     │
│   1. Parse matrix M from command data                       │
│   2. Calculate M⁻¹ using matrix_inverse_mod()              │
│      • Compute determinant: det(M)                          │
│      • Find det⁻¹ mod 256 using Extended Euclidean Alg     │
│      • Calculate adjugate matrix (cofactor transpose)       │
│      • M⁻¹ = det⁻¹ × adjugate mod 256                      │
│   3. Multiply: [R,G,B] = M⁻¹ × [R',G',B'] mod 256         │
│                                                             │
│ Example:                                                    │
│   M⁻¹ = [[calculated],     [encrypted]     [original]      │
│          [inverse     ],  ×  [pixel   ]  =  [pixel  ] mod 256│
│          [matrix      ]]     [values  ]     [values ]       │
│                                                             │
│ Output: Decrypted grid (converted back to 2D)              │
└─────────────────────────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────────────────────────┐
│ STEP 3: Remove Random Top Row                              │
│ Function: reverseGrid()                                     │
│                                                             │
│ Input:  Grid with random top row                           │
│ Action: Remove first row (row 0)                           │
│         Flatten remaining rows to 1D pixel array            │
│                                                             │
│ Output: 1D array of pixels (still with dummy pixels)       │
└─────────────────────────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────────────────────────┐
│ STEP 4: Remove Dummy Pixels                                │
│ Function: reverseDummyPixels()                              │
│                                                             │
│ Input:  Pixel array with pattern: [D,D,R,D,D,R,D,D,R,...]  │
│         (D=dummy, R=real, multiplier=2)                     │
│ Action: Extract every (multiplier+1)th pixel               │
│         Skip first 'multiplier' pixels, take next pixel     │
│                                                             │
│ Example (multiplier=2):                                     │
│   Input:  [[D],[D],[R],[D],[D],[R],[D],[D],[R]]           │
│   Output: [[R],[R],[R]]                                    │
│                                                             │
│ Output: 1D array of real data pixels only                  │
└─────────────────────────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────────────────────────┐
│ STEP 5: Extract Character Indices                          │
│ Function: reverseColorShuffle()                             │
│                                                             │
│ Input:  Real pixels [[R,G,B], [R,G,B], ...]               │
│ Action: Extract data from correct RGB channels             │
│         Use channel info from 's' command: "012"            │
│                                                             │
│ Example (channels [0,1,2]):                                │
│   Pixel [7,4,11] → extract [7, 4, 11]                     │
│   Pixel [11,14,R] → extract [11, 14]                      │
│                                                             │
│ Output: Array of character indices [7,4,11,11,14]          │
└─────────────────────────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────────────────────────┐
│ STEP 6: Convert Indices to Characters                      │
│ Function: decryption() final loop                           │
│                                                             │
│ Input:  [7, 4, 11, 11, 14]                                │
│ Action: Map each index to character in numToLetter array   │
│         Skip NULL_CHAR_INDEX (63) used for padding         │
│                                                             │
│ Mapping:                                                    │
│   7 → 'h', 4 → 'e', 11 → 'l', 11 → 'l', 14 → 'o'         │
│                                                             │
│ Output: "hello"                                            │
└─────────────────────────────────────────────────────────────┘

OUTPUT: Original Text
```

### 🔄 Key Reversal Strategy

**During Encryption:**
```
Commands applied in order: colorShuffle → dummyPixels → M₁ → m₁ → M₂ → m₂
Commands stored in array: [M₁, m₁, M₂, m₂]
Key assembled: "s..." + "d..." + [m₂, M₂, m₁, M₁] ← REVERSED!
```

**During Decryption:**
```
Key parsed: "s...", "d...", m₂, M₂, m₁, M₁ ← Read in order
Apply: m₂ → M₂ → m₁ → M₁ ← Automatically correct reverse order!
Then: removeDummyPixels → reverseColorShuffle
```

**Why This Works:**
- Encryption stores manipulation commands in application order
- Then reverses them when appending to key
- Decryption simply reads and applies commands in order from key
- No need for complex parsing or reversal logic during decryption!

### Mathematical Foundation
- **Modular Arithmetic:** All operations use mod 256 to keep values in 0-255 range
- **Invertible Matrices:** Only matrices with odd determinants (coprime with 256) are used
- **Extended Euclidean Algorithm:** Computes modular multiplicative inverse for decryption
- **Adjugate Matrix Method:** Calculates 3×3 matrix inverse in modular arithmetic
- **Determinant Cascading:** Uses 3×3 determinant calculation from reference pixels, applies (det mod 4) × 64 transformation

### Implementation Details

#### Key Format Structure
The encryption key uses a length-prefixed format:
```
<total_length><command_type><command_data>
```

**Examples:**
- `5s012` = Length 5, type 's' (color shuffle), channels 0,1,2
- `3d6` = Length 3, type 'd' (dummy pixels), multiplier 6
- `25M1,-2,3,4,0,-1,2,5,-3` = Length 25, type 'M' (matrix), 9 matrix values
- `3m2` = Length 3, type 'm' (determinant), picked index 2

**Key Assembly Order:**
1. Color shuffle command (s)
2. Dummy pixel command (d)
3. Manipulation commands (M and m) in REVERSE order of application

This allows decryption to read commands sequentially and apply them in correct reverse order.

#### Function Call Flow

**Encryption Path:**
```
encryption(text)
  └─> textToArray(size, text)
      ├─> char → index mapping
      └─> randomizedEncryption(indices)
          ├─> colorShuffle(indices) → generates 's' command
          ├─> dummyPixelGenerator(pixels) → generates 'd' command
          ├─> arrayToGrid(pixels) → adds random top row
          └─> loop (2-6 times):
              ├─> matrixObfuscation(grid) → appends 'M' command
              └─> detMultiplier(grid) → appends 'm' command
  └─> Reverse manipulation commands and assemble key
  └─> Save PNG image
```

**Decryption Path:**
```
decryption(key)
  ├─> Load PNG image
  ├─> imgToGrid(image) → convert to 2D pixel array
  ├─> parseKey(key) → extract commands
  ├─> Process manipulation commands in order:
  │   ├─> reverseDetMultiplier(grid, index) for 'm' commands
  │   └─> reverseMatrixObfuscation(pixels, matrix) for 'M' commands
  ├─> reverseGrid(grid) → remove top row, flatten
  ├─> reverseDummyPixels(pixels, multiplier)
  ├─> reverseColorShuffle(pixels, channels)
  └─> indices → characters → text
```

#### Critical Implementation Notes

1. **Matrix Inverse Calculation:**
   - Requires determinant to be odd (coprime with 256)
   - Uses cofactor expansion for 3×3 matrices
   - Applies modular inverse to determinant
   - Formula: M⁻¹ = (det⁻¹ × adjugate) mod 256

2. **Determinant Cascading:**
   - References MUST come from unchanged first row
   - Decryption MUST proceed forward (not backward)
   - Each decrypted pixel becomes reference for next
   - Cascading: left ← picked, picked ← right, right ← new_pixel

3. **Command Reversal:**
   - Manipulation commands stored in application order during encryption
   - Reversed when appending to final key
   - Decryption reads and applies in key order (automatically reversed)
   - This eliminates complex parsing logic

4. **Pixel Data Structure:**
   - Characters → 1D index array
   - After colorShuffle → 2D pixel array [[R,G,B], ...]
   - After dummyPixels → expanded 2D pixel array
   - After arrayToGrid → 2D grid [rows[pixels]]
   - Manipulations operate on grid structure

## Capabilities & Limitations

### What It Can Do ✅
- Encrypt any text containing the 64 supported characters
- Generate unique encryption keys for each encryption
- Decrypt images perfectly with correct key
- Handle texts of arbitrary length (limited only by memory)
- Produce images that look like random noise
- Protect against casual inspection and basic reverse-engineering
- Work without the code (increased security through obscurity)
- Use multiple independent obfuscation layers simultaneously

### What It Cannot Do ❌
- **Not cryptographically secure** against professional cryptanalysis
- Does not support characters outside the 64-character alphabet
- Cannot decrypt without the original key
- Does not provide key exchange or key management
- Not resistant to known-plaintext attacks (if attacker has plaintext-image pairs)
- Uses pseudo-random number generator (not cryptographically secure)
- Limited key space compared to modern encryption (AES-256)

### Character Set (64 Characters)
- **Lowercase letters:** a-z (26 chars)
- **Digits:** 0-9 (10 chars)
- **Punctuation:** space, . , ! ? ; : " - ( ) < > { } @ # $ & * + = _ % newline (27 chars)
- **Null character:** þ (thorn) - used for padding only (1 char)
- **Note:** Uppercase letters are automatically converted to lowercase

### Security Level
- **Against casual observers:** Very effective - appears as random image
- **Against hobbyists:** Strong - would take weeks/months to break
- **Against security researchers:** Moderate - could break in days with code
- **Against professionals:** Weak - vulnerable to sophisticated attacks
- **Best use cases:** Fun projects, puzzles, non-critical data, learning cryptography

## Troubleshooting
- **Unexpected characters in output?** Your input contains unsupported characters (e.g., uppercase, symbols). They are converted to `'a'`.
- **Import errors?** Run `pip install -r requirements.txt` in your activated virtual environment.
- **File not found?** Ensure you're running from the project root directory.

## Customization

### Easy Modifications
- **Change Manipulation Round Count:** 
  - In `encryption.py` line ~95, modify: `num_manipulationround = random.randint(2, 6)`
  - Higher = more secure but slower and larger key
- **Force Only Matrix or Only Determinant:** 
  - In `encryption.py` line ~97-100, remove the random choice:
  - For matrix only: `inputArray= matrixObfuscation(inputArray)`
  - For determinant only: `inputArray = detMultiplier(inputArray)`
- **Adjust Dummy Pixel Ratio:** 
  - In `encryption.py` line ~160, modify: `dummyMultiplier = random.randint(2, 7)`
  - Higher = larger images, more obfuscation
- **Change Output Filename:** 
  - In `encryption.py` line ~345, modify: `img.save("output_image.png")`

### Advanced Modifications
- **Add/Remove Characters:** 
  - Update `numToLetter` list in both `encryption.py` and `decryption.py` (must match!)
  - Keep total at 64 characters for optimal performance (power of 2)
- **Implement Random Dictionary:** 
  - Would increase security to ~474 bits of entropy
  - Requires storing dictionary permutation in key (adds ~86 characters to key)
- **Change Matrix Range:** 
  - In `matrixObfuscation()`, modify: `M = np.random.randint(-5, 6, (3, 3))`
  - Larger range = more variation but potential overflow issues

## Project Structure
```
ImageCryptography/
├── MainCode/
│   ├── main.py          # Main program entry point
│   ├── encryption.py    # Text-to-image conversion
│   ├── decryption.py    # Image-to-text conversion
│   └── testText         # Sample text file for testing
├── .venv/               # Virtual environment (not in git)
├── .gitignore           # Git ignore rules
├── requirements.txt     # Python dependencies
└── README.md            # This file
```

## Notes
- **Python version:** Tested on Python 3.14
- **Git:** Do NOT commit `.venv` to git (it's in `.gitignore`)
- **Dependencies:** If you add new packages, run `pip freeze > requirements.txt`
- **Beginner project:** This is a learning project; bugs and improvements are expected!

## Technical Details

### Key Format
The encryption key encodes all transformation parameters:
```
Example: 4s10323M1,-1,4,1,-2,3,3,-5,526M1,-2,-4,-5,-1,1,-2,-5,423M-1,0,-1,0,1,5,-2,4,122M3,1,3,0,-5,0,-3,4,4
```

Key structure:
- `<length><type><data>` format for each command
- **s:** Color shuffle (e.g., `4s103` = use channels 1,0,3)
- **d:** Dummy pixel multiplier (e.g., `3d3` = 3 dummy pixels per real pixel)
- **M:** Matrix transformation (e.g., `26M1,-1,4,...` = 3×3 matrix values)
- **m:** Determinant position (optional, e.g., `4m12` = start at position 12)

### Image Properties
- **Format:** PNG (lossless compression)
- **Dimensions:** Approximately square (width ≈ height)
- **Color Depth:** 24-bit RGB (8 bits per channel)
- **Size:** Varies based on text length and dummy pixel ratio
  - Formula: `num_pixels ≈ (text_length / channels_used) * (dummy_multiplier + 1)`
- **Appearance:** Random noise pattern (no visible structure)

### Performance
- **Encryption Speed:** ~0.1-0.5 seconds for typical messages
- **Decryption Speed:** ~0.1-0.5 seconds (slightly slower due to matrix inverse)
- **Memory Usage:** Minimal (entire image kept in RAM)
- **Image Size:** ~1-10 KB for typical messages (depends on dummy pixel ratio)

## Future Improvements
- ✅ Fixed determinant-based cascading transformation (now working!)
- ✅ Implemented randomized interleaving of Matrix and Determinant operations
- ⬜ Implement randomized dictionary shuffling (+434 bits entropy)
- ⬜ Add AES-256 encryption layer for true cryptographic security
- ⬜ Implement secure key exchange mechanism (Diffie-Hellman)
- ⬜ Add HMAC for integrity verification
- ⬜ Support full Unicode character set
- ⬜ Add GUI for easier interaction
- ⬜ Implement steganography (hide in existing images)
- ⬜ Add compression for large texts
- ⬜ Create mobile app version 




## Detailed Comparison: Obfuscation vs. Encryption

| Feature | This System (Obfuscation) | AES-256 (Encryption) |
|---------|---------------------------|----------------------|
| **Security Type** | Obfuscation | Cryptographic Encryption |
| **Key Size** | ~40-80 bits | 256 bits |
| **Possible Keys** | ~10¹² to 10²⁴ | 2²⁵⁶ (≈10⁷⁷) |
| **Break Time (Brute Force)** | Hours to months | Billions of years |
| **Method Public?** | No (security relies on secrecy) | Yes (publicly documented) |
| **Peer Reviewed?** | No | Yes (extensively) |
| **Security Level** | Moderate complexity | Military-grade |
| **Speed** | Moderate (~0.1-0.5s) | Very Fast (<0.01s) |
| **Key Length** | 50-200 characters | 32 bytes (fixed) |
| **Standardized** | No | Yes (NIST FIPS 197) |
| **Hardware Support** | No | Yes (AES-NI instructions) |
| **Patent Free** | Yes | Yes |
| **Quantum Resistant** | No | Partially (Grover's algorithm) |
| **Known Attacks** | Pattern analysis, statistical | None practical |
| **Best Use Case** | Learning, fun, art | Real security needs |

### Real-World Security Levels

**This System:**
- **Against your friend:** 🟢🟢🟢🟢🟢 (Excellent - they'll never guess)
- **Against a hobbyist:** 🟢🟢🟢⚪⚪ (Good - would take significant effort)
- **Against a CS student:** 🟢🟢⚪⚪⚪ (Fair - could break with analysis)
- **Against a security researcher:** 🟢⚪⚪⚪⚪ (Weak - would break in days/weeks)
- **Against a professional:** ⚪⚪⚪⚪⚪ (Minimal - would break in hours/days)

**AES-256:**
- **Against anyone:** 🟢🟢🟢🟢🟢 (Excellent - effectively unbreakable)

### Why Obfuscation Can Be Useful

Despite not being "true encryption," obfuscation has legitimate uses:

1. **Learning Tool:** Excellent for understanding cryptographic concepts
2. **Layered Security:** Can be combined with real encryption for extra protection
3. **Low Stakes:** Perfect when absolute security isn't critical
4. **Creativity:** Allows for custom, artistic approaches to hiding data
5. **No Export Restrictions:** Often easier to deploy internationally than strong encryption
6. **Performance:** Can be faster for specific use cases
7. **Fun:** More engaging than just using a library function!

### The "Security Through Obscurity" Debate

**Security through obscurity** means relying on keeping your method secret. This project uses it.

**Problems with this approach:**
- Once someone figures out the method, ALL messages encrypted with it are vulnerable
- Can't share the code publicly without reducing security
- No peer review means bugs/weaknesses might exist
- Reverse engineering is possible

**Why real encryption is better:**
- The algorithm is public (AES source code is freely available)
- Security comes from the key, not the algorithm
- Thousands of experts have tried to break it (and failed)
- You can share the code without compromising security

**Analogy:**
- **Obfuscation:** Hiding your key under a rock (works until someone watches where you put it)
- **Encryption:** Using a bank vault (everyone knows how vaults work, but they still can't open yours without the combination)

## Credits & Acknowledgments
- **Cryptographic Concepts:** Based on classical cipher techniques (Hill cipher, substitution ciphers)
- **Modern Touches:** Matrix multiplication, modular arithmetic, cascading transformations
- **Educational Purpose:** Designed for learning cryptography fundamentals
- **Not For Production:** Use established libraries (cryptography, PyCryptodome) for real security needs

## License
This is an educational project. Use at your own risk. Not recommended for protecting sensitive data.

---

**Remember:** This is obfuscation, not encryption. For real security, use industry-standard libraries like `cryptography` or `PyCryptodome` with AES-256!