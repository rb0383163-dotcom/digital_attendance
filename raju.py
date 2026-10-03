#import math
def gcd(a,b):
    #""" calculate the greatest common divisor."""
    while b:
        a,b=b,a%b
        return a
def generate_keypair(p,q):
    #"""generate public and private keys from two prime numbers"""
    n=p*q
    phi=(p-1)*(q-1)
    e=17
    while gcd(e,phi)!=1:
        e+=2
        d=pow(e,-1,phi)
        return (e,n),(d,n)
    def encrypt(public_key,plaintext_msg):
        e,n=public_key
        ciphertext=pow(plaintext_msg,e,n)
        return ciphertext
    def decrypt(private_key,ciphertext_msg):
        #"""decrypt a numerical message using a privatekey."""
        d,n=private_key
        plaintext=pow(ciphertext_msg,d,n)
        return plaintext
if __name__=="__main__":
        prime1=61
        prime2=53
        public,private=generate_keypair(prime1,prime2)
        print(f"publickey(e,n):{public}")
        print(f"privatekey(d,n):{private}")
        secret_message=42
        print(f"original message:{secret_message}")
        encrypted_msg=encrypt(public,secret_message)
        print(f"encrypted ciphertext:{encrypted_msg}")
        decrypted_msg=decrypt(private,secret_msg)
        print(f"decrypted plaintext:{decrypted_msg}")
        
        
        
        