# 🎵 SAPTAK Cryptosystem

SAPTAK Cryptosystem is a novel cryptographic system inspired by DNA cryptography but rooted in the rich structure of Indian classical music. Unlike traditional DNA cryptography which uses 4 bases (A, T, G, C), SAPTAK uses 8 symbolic bases – the 7 Indian musical notes (S, R, G, M, P, D, N) and an additional character E – to introduce more randomness, uniqueness, and cultural integration into data encryption.

## 🔐 Core Features

- **Musical Note-Based Encoding:** Uses the 7 Swaras (Sa, Re, Ga, Ma, Pa, Dha, Ni) as the foundational elements for encryption.

- **Randomized Key Generation:** Generates a 256-bit key using 2-bit encoding, complementary rules, and random swara sequences.

- **Multi-Layered Encryption:** Employs randomly generated index sequences, character tables, and XOR operations to transform plaintext securely.

- **Decryption:** Reverses the encryption process using the same key and swara mappings to retrieve the original plaintext.

## 🧠 Algorithms Used

- **key_generation()** – Builds a secure key from a password and user profile using swara transformations and 2-bit encoding.

- **encryption() –** Converts input text to a SAPTAK sequence using 3-bit mappings and injects additional randomness.

- **decryption() –** Restores plaintext by reversing the transformations and decoding the SAPTAK sequence.

## 🧠 ML Approach

- **ML-Assisted Key Validation:** SAPTAK integrates a supervised Machine Learning model to evaluate the statistical strength of generated cryptographic keys at runtime.

- **Feature-Driven Analysis:** Keys are analyzed using entropy and bit-level statistical features (e.g., Shannon entropy, bit balance, run-length patterns).

- **Strong-Key Enforcement:** Weak keys are automatically rejected, ensuring only high-quality 256-bit keys are used for encryption.

- **Security-First Design:** Machine learning acts as a validation and decision layer, complementing cryptographic logic without replacing it.

## 🛡️ Security Highlights

- Utilizes complementary base pairing logic for additional protection.

- Adds extra entropy with 8 symbolic bases instead of 4.

- Each encryption is unique due to randomized index and base generation.

## 📸 Screenshots


![image](https://github.com/user-attachments/assets/a9f77890-7751-4be7-a770-62617c18c750)

![image](https://github.com/user-attachments/assets/fc1c13eb-15ca-435d-aa0e-29d07dc6a632)

SAPTAK generates different ciphertexts for the same input using randomized base selection and key sequences, ensuring greater security through unpredictability.

![image](https://github.com/user-attachments/assets/d3ab19d1-aa04-4ffa-80c6-3548dc75f148)





