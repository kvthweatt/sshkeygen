from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
import sys

def generate_ssh_keys(key_size=2048, pv_keyfile=None, pb_keyfile=None):
    """
    Generate an RSA SSH key pair and display or save them.
    
    Args:
        key_size: Size of the RSA key in bits (default: 2048)
        pv_keyfile: Path to save private key file (optional)
        pb_keyfile: Path to save public key file (optional)
    """
    # Generate private key
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=key_size,
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
    
    # Save or display the keys
    if pv_keyfile and pb_keyfile:
        # Save to files
        with open(pv_keyfile, 'wb') as f:
            f.write(private_pem)
        print(f"Private key saved to: {pv_keyfile}")
        
        with open(pb_keyfile, 'wb') as f:
            f.write(public_pem)
        print(f"Public key saved to: {pb_keyfile}")
    else:
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
    sys.argv.pop(0)
    pv_keyfile = None
    pb_keyfile = None
    key_size = 2048
    
    if "-h" in sys.argv:
        print("Usage: python ssh_keygen.py [options]")
        print("\nOptions:")
        print("  -pvk=<file>    Specify private key output file")
        print("  -pbk=<file>    Specify public key output file")
        print("  -kl=<size>     Specify key size in bits (default: 2048, min: 1024)")
        print("  -h             Show this help menu")
        exit()
    else:
        args = ' '.join(sys.argv)
        if args.find("-h") != -1:
            args = args.replace("-h", "")
            args = args.split(" ")
            if "" in args:
                args.remove("")
        else:
            args = args.split(" ")
        
        nargs = []
        for arg in args:
            if "=" in arg:
                nargs.append(arg.split("="))
        
        for narg in nargs:
            lv = narg[0]
            rv = narg[1]
            if lv == "-pvk":
                pv_keyfile = rv
                continue
            if lv == "-pbk":
                pb_keyfile = rv
                continue
            if lv == "-kl":
                key_size = int(rv)
                if key_size < 1024:
                    print("Weak key size. Must be >= 1024.")
                    exit()
        
        # Check if only one key file is specified
        if (pv_keyfile is None) != (pb_keyfile is None):
            print("If one key file is specified, so must the other!")
            if pv_keyfile is None:
                print("Private key: File not specified.")
            elif pb_keyfile is None:
                print("Public key: File not specified.")
            exit()
    
    generate_ssh_keys(key_size=key_size, pv_keyfile=pv_keyfile, pb_keyfile=pb_keyfile)