import base64
import math

# Helper function to perform XOR operation
def xor(a, b):
    return bytes([x ^ y for x, y in zip(a, b)])

# Linear Congruential Generator class
class LCG:
    def __init__(self, a, b, mod=2**16, state=0):
        self.a = a
        self.b = b
        self.mod = mod
        self.state = state

    def next(self):
        self.state = (self.a * self.state + self.b) % self.mod
        return self.state

# Function to try decrypting the message with given LCG parameters
def decrypt_message(encrypted_message, a, b):
    encrypted_bytes = base64.b64decode(encrypted_message)
    lcg = LCG(a, b)
    states = [lcg.next() for _ in range(math.ceil(len(encrypted_bytes) / 2))]
    key = b"".join([state.to_bytes(2, 'little') for state in states])
    decrypted = xor(encrypted_bytes, key)
    try:
        return decrypted.decode('ASCII')
    except UnicodeDecodeError:
        return None  # In case the decryption doesn't result in valid ASCII

# Encoded message from the server
encrypted_message = ""

# Example of brute-forcing parameters
for a in range(1337, 10000):
    for b in range(1337, 10000):
        result = decrypt_message(encrypted_message, a, b)
        if result and "SpeishFlag" in result:
            print(f"Decrypted message with a={a}, b={b}: {result}")
            break
