import base64

def encrypt(text, key):
    result = ""

    for i in range(len(text)):
        result += chr(ord(text[i]) ^ ord(key[i % len(key)]))

    return base64.b64encode(result.encode()).decode()


def decrypt(ciphertext, key):
    data = base64.b64decode(ciphertext).decode()
    result = ""

    for i in range(len(data)):
        result += chr(ord(data[i]) ^ ord(key[i % len(key)]))

    return result


# Main program
message = input("Enter message: ")
key = input("Enter key: ")

encrypted = encrypt(message, key)

print("\nEncrypted message:", encrypted)

decrypted = decrypt(encrypted, key)

print("Decrypted message:", decrypted)