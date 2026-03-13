# TryHackMe – Flip  
## AES-CBC Bit Flipping Attack

This repository documents the exploitation of a vulnerable authentication service that incorrectly used **AES encryption in CBC mode** without integrity protection.

The goal of the challenge was to authenticate as an **administrator** by manipulating encrypted data returned by the server.

---

# Challenge Summary

The service accepts:

- a username
- a password

It then:

1. encrypts the data using AES-CBC
2. leaks the ciphertext
3. asks the user to submit ciphertext back
4. decrypts the provided ciphertext
5. checks if the decrypted message contains admin credentials

Because CBC encryption **does not guarantee integrity**, attackers can modify ciphertext and control parts of the decrypted plaintext.

This allows bypassing authentication.

---

# Vulnerable Logic

The server decrypts attacker-supplied ciphertext and checks for the presence of a specific credential string.

Example logic:

```python
if b'admin&password=...' in decrypted_data:
    grant_access()
