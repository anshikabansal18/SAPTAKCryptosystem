import math
import itertools
import random
import csv
from collections import Counter

def select4bases() -> list:
    SWARAS = ['S', 'R', 'G', 'M', 'P', 'D', 'N']
    main_base = []
    # randomly selecting 4 bases from SWARAS
    for i in range(4):
        main_base.append(random.choice(SWARAS))
        SWARAS.remove(main_base[i])
    return(SWARAS,main_base)

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

def dict_swap(dictionary: dict) -> dict:
    return {v: k for k, v in dictionary.items()}

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

def generate_SAPTAK_sequence(plaintext: str, main_base: list) -> list:
    SAPTAK_sequence = []
    list_comb = [list(comb) for comb in itertools.product(main_base, repeat=4)]
    for letter in plaintext:
        SAPTAK_sequence.append(list_comb[ord(letter)])

    SAPTAK_sequence = [item for sublist in SAPTAK_sequence for item in sublist]
    return SAPTAK_sequence, list_comb

def key_generation() -> list:
    # 16 alphanumeric input + 16 from user's profile
    password = '1234567890123456'    #input("Enter 16 characters password: ")
    user_code = '0987654321098765'   #input("Enter 16 characters user_code: ")
    key_password = password + user_code
    SWARAS, main_base = select4bases()
    key_password, list_comb = generate_SAPTAK_sequence(key_password, main_base)
    binary_conversion2bit = coding_table_2bit(main_base)
    complementary_dict = complementary_codingRule(binary_conversion2bit)
    key_password = password_complement(key_password, complementary_dict)
    intP2B = toBinary(key_password, binary_conversion2bit)
    index_sequence = index_sequence_key(intP2B)
    key_256bits = divide_merge(intP2B, index_sequence)
    return key_256bits

def extract_features(key_bits):
    counts = Counter(key_bits)
    p0 = counts.get(0, 0) / len(key_bits)
    p1 = counts.get(1, 0) / len(key_bits)

    entropy = 0
    for p in [p0, p1]:
        if p > 0:
            entropy -= p * math.log2(p)

    longest_run = max(len(list(g)) for _, g in itertools.groupby(key_bits))

    return [
        entropy,        # randomness
        p1,             # ratio of 1s
        longest_run,    # repetition
        sum(key_bits) / len(key_bits),  # mean
    ]

def label_key(entropy):
    return 1 if entropy >= 0.95 else 0   # 1 = Strong, 0 = Weak

with open("saptak_key_dataset.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["entropy", "one_ratio", "longest_run", "mean", "label"])

    for _ in range(2000):   # 2000 keys is enough
        key = key_generation()
        features = extract_features(key)
        label = label_key(features[0])
        writer.writerow(features + [label])

print("Dataset generated successfully.")
