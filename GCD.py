def find_gcd(a, b):
  while b != 0:
    a, b = b, a % b
  return a


# Example usage:
print(find_gcd(60, 36))  