# secureserver.py (Secure HMAC-SHA256 Server)
import argparse
import base64
import hmac
import hashlib

SECRET_KEY = b'supersecretkey'  # Unknown to attacker

def generate_hmac(message: bytes) -> str:
    return hmac.new(SECRET_KEY, message, hashlib.sha256).hexdigest()

def verify(message: bytes, mac: str) -> bool:
    return hmac.compare_digest(generate_hmac(message), mac)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Secure HMAC-SHA256 server simulation")
    parser.add_argument('--message', type=str, default="", help="Base64-encoded message")
    parser.add_argument('--mac',     type=str, default=None, help="Hex HMAC")
    args = parser.parse_args()

    # Decode the Base64 message
    message = base64.b64decode(args.message.encode('ascii'))
    mac     = args.mac or generate_hmac(message)

    print("=== Secure HMAC-SHA256 Server ===")
    print(f"Message: {message}")
    print(f"HMAC:    {mac}\n")

    if verify(message, mac):
        print("HMAC verified. Message is authentic.")
    else:
        print("HMAC verification failed.")
