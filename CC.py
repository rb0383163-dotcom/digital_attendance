text = "Hello, World 2026!"
shift = 4
mode = "encrypt"  # Change to "decrypt" to reverse it

if mode == "decrypt":
    shift = -shift

result = ""

for char in text:
    if char.isupper():
        result += chr((ord(char) + shift - 65) % 26 + 65)
    elif char.islower():
        result += chr((ord(char) + shift - 97) % 26 + 97)
    # Check for digits 0-9
    elif char.isdigit():
        # Subtract 48 (ASCII for '0') and wrap around using modulo 10
        result += chr((ord(char) + shift - 48) % 10 + 48)
    else:
        result += char

print(f"Result ({mode}ed): {result}")