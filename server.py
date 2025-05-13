# server.py (Insecure MD5 Server)
import argparse
import base64
import hashlib

SECRET_KEY = b'supersecretkey'  # Unknown to attacker

def generate_mac(message: bytes) -> str:
    return hashlib.md5(SECRET_KEY + message).hexdigest()

def verify(message: bytes, mac: str) -> bool:
    return generate_mac(message) == mac

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Insecure MD5 server simulation")
    parser.add_argument('--message', type=str, default="", help="Base64-encoded message")
    parser.add_argument('--mac',     type=str, default=None, help="Hex MAC")
    args = parser.parse_args()

    # Decode the Base64 message
    message = base64.b64decode(args.message.encode('ascii'))
    mac     = args.mac or generate_mac(message)

    print("=== Insecure MD5 Server ===")
    print(f"Message: {message}")
    print(f"MAC:     {mac}\n")

    if verify(message, mac):
        print("MAC verified. Message is authentic.")
    else:
        print("MAC verification failed.")
