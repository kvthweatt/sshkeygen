from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend

def generate_ssh_keys():
    """
    Generate a 2048-bit RSA SSH key pair and display them.
    """
    # Generate private key
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )
    
    # Serialize private key in PEM format
    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption()
    )
    
    # Get public key
    public_key = private_key.public_key()
    
    # Serialize public key in PEM format
    public_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    
    # Display the keys
    print("=" * 60)
    print("PRIVATE KEY:")
    print("=" * 60)
    print(private_pem.decode('utf-8'))
    print()
    print("=" * 60)
    print("PUBLIC KEY:")
    print("=" * 60)
    print(public_pem.decode('utf-8'))
    print("=" * 60)
    
    return private_pem, public_pem

if __name__ == "__main__":
    generate_ssh_keys()