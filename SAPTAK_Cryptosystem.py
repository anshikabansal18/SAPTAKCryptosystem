
import random
import itertools
import joblib
import math
import pandas as pd
from collections import Counter

key_strength_model = joblib.load("saptak_key_strength_model.pkl")

# 4-bit S-box (bijective, reversible)
SBOX = {
    "0000": "1110", "0001": "0100", "0010": "1101", "0011": "0001",
    "0100": "0010", "0101": "1111", "0110": "1011", "0111": "1000",
    "1000": "0011", "1001": "1010", "1010": "0110", "1011": "1100",
    "1100": "0101", "1101": "1001", "1110": "0000", "1111": "0111"
}

INV_SBOX = {v: k for k, v in SBOX.items()}

def apply_sbox(bits):
    out = []
    for i in range(0, len(bits), 4):
        block = ''.join(str(b) for b in bits[i:i+4])
        if len(block) < 4:
            block = block.ljust(4, "0")
        out.extend(int(b) for b in SBOX[block])
    return out


def reverse_sbox(bits):
    out = []
    for i in range(0, len(bits), 4):
        block = ''.join(str(b) for b in bits[i:i+4])
        out.extend(int(b) for b in INV_SBOX[block])
    return out

def select4bases() -> list:
    SWARAS = ['S', 'R', 'G', 'M', 'P', 'D', 'N']
    main_base = []
    # randomly selecting 4 bases from SWARAS
    for i in range(4):
        main_base.append(random.choice(SWARAS))
        SWARAS.remove(main_base[i])
    return(SWARAS,main_base)

def generate_SAPTAK_sequence(plaintext: str, main_base: list) -> list:
    # generating SAPTAK sequence (random character table)
    SAPTAK_sequence = []
    list_comb = [list(comb) for comb in itertools.product(main_base, repeat = 4)]
    for letter in plaintext:
        SAPTAK_sequence.append(list_comb[ord(letter)])

    # list of list to list
    SAPTAK_sequence = [item for sublist in SAPTAK_sequence for item in sublist]
    return SAPTAK_sequence, list_comb

def index_sequence_encryption(plaintext: str) -> list:
    # randomly generating indexes
    index_sequence = []
    for i in range(len(plaintext)*4):
        index_sequence.append(random.randint(0,((len(plaintext)*4)*2)-1))
    index_sequence = sorted(index_sequence)
    return index_sequence

def merge3bases(plaintext: str, SWARAS: list, SAPTAK_sequence: list, index_sequence: list) -> list:
    # merging 3 letters to SAPTAK sequence
    for i in range(len(plaintext)*4):
        SAPTAK_sequence.insert(index_sequence[i], random.choice(SWARAS))
    return SAPTAK_sequence

def coding_table_3bit() -> dict:
    # coding table generation
    bits3 = ['000','001','010','011','100','101','110'] 
    swaras = ['S', 'R', 'G', 'M', 'P', 'D', 'N']
    binary_conversion3bit = {}
    for i in range(7):
        binary_conversion3bit[bits3[i]] = random.choice(swaras)
        swaras.remove(binary_conversion3bit[bits3[i]])
    binary_conversion3bit['111'] = 'E'
    return binary_conversion3bit

def dict_swap(dictionary: dict) -> dict:
    dict_swapped = {v: k for k, v in dictionary.items()}
    return dict_swapped

def toBinary(SAPTAK_sequence: list,binary_conversionNbit: dict) -> list:
    #conversion to binary
    binary_conversionNbit_swap = dict_swap(binary_conversionNbit)
    S2B = []
    for letter in SAPTAK_sequence:
        S2B.append(binary_conversionNbit_swap[letter])

    #conversion of string to int
    S2B_listoflist = []
    for i in range(len(S2B)):
        S2B_listoflist.append(list(S2B[i]))
    S2B_list = list(itertools.chain.from_iterable(S2B_listoflist))
    intS2B = [int(ele) for ele in S2B_list]
    return intS2B

def coding_table_2bit(main_base: list) -> dict:
    # coding table generation
    bits2 = ['00','01','10','11'] 
    main_base2 = main_base.copy()
    binary_conversion2bit = {}
    for i in range(4):
        binary_conversion2bit[bits2[i]] = random.choice(main_base2)
        main_base2.remove(binary_conversion2bit[bits2[i]])
    return binary_conversion2bit

def complementary_codingRule(binary_conversion2bit: dict) -> dict:
    # generating complementary dictionary
    complementary_list = []
    for values in binary_conversion2bit.values():
        complementary_list.append(values)
    complementary_list_reverse = complementary_list[::-1]
    complementary_dict = {}
    for i in range(4):
        complementary_dict[complementary_list[i]] = complementary_list_reverse[i]
    return complementary_dict

def password_complement(key_password: list,complementary_dict: dict) -> list:
    # complementary password
    for i in range(len(key_password)):
        key_password[i] = complementary_dict[key_password[i]]
    return key_password

def index_sequence_key(intP2B: list) -> list:
    # randomly generating indexes
    index_sequence = []
    for i in range(len(intP2B)//2):
        index_sequence.append(random.randint(0,(len(intP2B)-1)))
    return index_sequence

def divide_merge(intP2B: list, index_sequence: list) -> list:
    # dividing and merging 2 list randomly
    intP2B_1 = intP2B[:len(intP2B)//2]
    intP2B_2 = intP2B[len(intP2B)//2:]

    for i in range(len(intP2B_1)):
        intP2B_2.insert(index_sequence[i], intP2B_1[i])
    return intP2B_2

def rotate_bits(bits, shift=3):
    shift = shift % len(bits)
    return bits[shift:] + bits[:shift]

def xor(intP2B_2: list, intS2B: list) -> list:
    xor_list = []
    if len(intS2B) > 256:
        x = [intS2B[i:i + 256] for i in range(0, len(intS2B), 256)]
        for block in x:
            for i in range(len(block)):
                xor_list.append(block[i] ^ intP2B_2[i])
    else:
        for i in range(len(intS2B)):
            xor_list.append(intS2B[i] ^ intP2B_2[i])
    return xor_list

def permute_key(key, shift):
    shift = shift % len(key)
    return key[shift:] + key[:shift]

def xor_multi_round(key, data, rounds=3):
    result = data.copy()

    for r in range(rounds):
        round_key = permute_key(key, r * 7)  # deterministic
        result = xor(round_key, result)

    return result

def binary_to_SAPTAK_e(plaintext: str, binary_conversion3bit: dict, xor_list: list) -> list:
    xor_str = [str(x) for x in xor_list]
    grouped_bin = []
    for i in range(len(plaintext)*8):
        grouped_bin.append(''.join(xor_str[0:3]))
        xor_str = xor_str[3:]

    B2S = []
    for group in grouped_bin:
        B2S.append(binary_conversion3bit[group])
    return B2S

def binary_to_SAPTAK_d(ciphertext: str, binary_conversion3bit: dict, xor_list: list) -> list:
    xor_str = [str(x) for x in xor_list]
    grouped_bin = []
    for i in range(len(ciphertext)):
        grouped_bin.append(''.join(xor_str[0:3]))
        xor_str = xor_str[3:]

    B2S = []
    for group in grouped_bin:
        B2S.append(binary_conversion3bit[group])
    return B2S

def remove3bases(main_base: list, B2S: list) -> list:
    B2Sd = [i for i in B2S if i in main_base]
    return B2Sd

def toPlaintext(B2S: list, main_base: list) -> list:
    # grouping in four
    plaintext = []
    grouped_cipher = []
    for i in range(len(B2S)//4):
        grouped_cipher.append(''.join(B2S[0:4]))
        B2S = B2S[4:]
    #string to list
    grouped_cipher_list = []
    for string in grouped_cipher:
        grouped_cipher_list.append([i for i in string])
    #character table to plaintext]
    list_comb = [list(comb) for comb in itertools.product(main_base, repeat = 4)]
    for lis in grouped_cipher_list:
        index = list_comb.index(lis)
        plaintext.append(chr(index))
    plaintext_str = "".join(plaintext)
    return plaintext_str

def extract_key_features(key_bits):
    counts = Counter(key_bits)
    p0 = counts.get(0, 0) / len(key_bits)
    p1 = counts.get(1, 0) / len(key_bits)

    entropy = 0
    for p in [p0, p1]:
        if p > 0:
            entropy -= p * math.log2(p)

    longest_run = max(len(list(g)) for _, g in itertools.groupby(key_bits))

    return [
        entropy,
        p1,
        longest_run,
        sum(key_bits) / len(key_bits)
    ]

def key_generation() -> list:
    password = '1234567890123456'
    user_code = '0987654321098765'
    key_password = password + user_code

    SWARAS, main_base = select4bases()
    key_password, _ = generate_SAPTAK_sequence(key_password, main_base)
    binary_conversion2bit = coding_table_2bit(main_base)
    complementary_dict = complementary_codingRule(binary_conversion2bit)
    key_password = password_complement(key_password, complementary_dict)

    # Try multiple times to get an ML-approved strong key
    for _ in range(10):   # bounded loop for safety
        intP2B = toBinary(key_password, binary_conversion2bit)
        index_sequence = index_sequence_key(intP2B)
        key_256bits = divide_merge(intP2B, index_sequence)

        # --- ML feature extraction ---
        features = extract_key_features(key_256bits)

        # --- IMPORTANT: use DataFrame to match training ---
        features_df = pd.DataFrame(
            [features],
            columns=["entropy", "one_ratio", "longest_run", "mean"]
        )

        prediction = key_strength_model.predict(features_df)[0]

        if prediction == 1:   # 1 = Strong key
            return key_256bits

    # Fallback: return the last generated key (guaranteed non-None)
    return key_256bits

def encryption(plaintext: str, return_bits=False):
    # --- base selection ---
    SWARAS, main_base = select4bases()
    SAPTAK_sequence, _ = generate_SAPTAK_sequence(plaintext, main_base)
    index_sequence = index_sequence_encryption(plaintext)
    SAPTAK_sequence_new = merge3bases(
        plaintext, SWARAS, SAPTAK_sequence, index_sequence
    )
    binary_conversion3bit = coding_table_3bit()
    intS2B = toBinary(SAPTAK_sequence_new, binary_conversion3bit)
    key_256bits = key_generation()
    xor_bits = xor(key_256bits, intS2B)
    sbox_bits = apply_sbox(xor_bits)
    ciphertext = binary_to_SAPTAK_e(
        plaintext, binary_conversion3bit, sbox_bits
    )
    ciphertext_str = "".join(ciphertext)
    if return_bits:
        return ciphertext_str, sbox_bits
    return ciphertext_str, main_base, binary_conversion3bit, key_256bits

def decryption(ciphertext: list, main_base: list, binary_conversion3bit: dict, key_256bits: list) -> list:
    intS2B = toBinary(ciphertext, binary_conversion3bit)
    unsboxed = reverse_sbox(intS2B)
    xor_list = xor(key_256bits, unsboxed)
    B2S = binary_to_SAPTAK_d(ciphertext, binary_conversion3bit, xor_list)
    B2Sd = remove3bases(main_base, B2S)
    plaintext = toPlaintext(B2Sd, main_base)
    return plaintext

# python module to create GUI
from tkinter import *

root = Tk()
root.title("SAPTAK CRYPTOGRAPHY")
root.geometry("800x250")

def xyz():
    def encryptMessage():
        pt = e1.get()
        ct, main_base, coding_rule, key = encryption(pt)
        e2.insert(0, ct)
        return ct, main_base, coding_rule, key
    global y, z, w
    x, y, z, w = encryptMessage()

def decryptMessage():
    ct1 = list(e3.get())
    pt1 = decryption(ct1, y, z, w)
    e4.insert(0, pt1)

def clearFields():
    e1.delete(0, END)
    e2.delete(0, END)
    e3.delete(0, END)
    e4.delete(0, END)

# Creating labels and positioning them on the grid
Label(root, text='Plaintext').grid(row=0, column=0, sticky=W, padx=10, pady=5)
Label(root, text='Encrypted text').grid(row=1, column=0, sticky=W, padx=10, pady=5)
Label(root, text='Ciphertext').grid(row=3, column=0, sticky=W, padx=10, pady=5)
Label(root, text='Decrypted text').grid(row=4, column=0, sticky=W, padx=10, pady=5)

# Creating entries and positioning them on the grid
e1 = Entry(root, width=100)
e1.grid(row=0, column=1, padx=10, pady=5)
e2 = Entry(root, width=100)
e2.grid(row=1, column=1, padx=10, pady=5)
e3 = Entry(root, width=100)
e3.grid(row=3, column=1, padx=10, pady=5)
e4 = Entry(root, width=100)
e4.grid(row=4, column=1, padx=10, pady=5)

# Creating buttons
Button(root, text="Encrypt", bg="green", fg="white", command=xyz).grid(row=2, column=1, pady=5)
Button(root, text="Decrypt", bg="red", fg="white", command=decryptMessage).grid(row=5, column=1, pady=5)
Button(root, text="Clear", bg="blue", fg="white", command=clearFields).grid(row=5, column=2, pady=5)

root.mainloop()


