# Diffie-Hellman Key Exchange

p = 23
g = 5

# Private keys
a = 6
b = 15

# Public keys
A = pow(g, a, p)
B = pow(g, b, p)

# Shared secret keys
key_A = pow(B, a, p)
key_B = pow(A, b, p)

print("Public Prime (p):", p)
print("Primitive Root (g):", g)

print("Alice Public Key:", A)
print("Bob Public Key:", B)

print("Alice Shared Key:", key_A)
print("Bob Shared Key:", key_B)

if key_A == key_B:
    print("Key Exchange Successful!")
else:
    print("Key Exchange Failed!")