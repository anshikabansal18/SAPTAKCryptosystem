import random
import csv

from SAPTAK_Cryptosystem import encryption

def mutate_plaintext(pt):
    if len(pt) == 0:
        return pt
    i = random.randint(0, len(pt) - 1)
    return pt[:i] + chr((ord(pt[i]) + 1) % 128) + pt[i+1:]


with open("crypto_eval_dataset.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["plaintext_len", "bit_diff_ratio"])

    for _ in range(1000):
        # original plaintext
        pt = ''.join(chr(random.randint(32, 126)) for _ in range(16))

        # encrypt original
        _, bits1 = encryption(pt, return_bits=True)

        # mutate plaintext
        pt2 = mutate_plaintext(pt)

        # encrypt mutated
        _, bits2 = encryption(pt2, return_bits=True)

        # --- TRUE bit-level avalanche measurement ---
        min_len = min(len(bits1), len(bits2))
        diff = sum(1 for i in range(min_len) if bits1[i] != bits2[i])
        diff_ratio = diff / min_len

        writer.writerow([len(pt), round(diff_ratio, 3)])

print("Cryptographic evaluation dataset created.")

