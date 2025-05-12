import hashlib
import struct
import binascii
from server import verify as insecure_verify
from secure_server import verify as secure_verify

# Simulate the original server's MAC generation (insecure)
SECRET_KEY = b'supersecretkey'  # Normally unknown to attacker
original_message = b"amount=100&to=alice"
original_mac = hashlib.md5(SECRET_KEY + original_message).hexdigest()

def md5_padding(message_length):
    """Calculate MD5 padding for a given message length."""
    padding = b'\x80'
    padding_len = 56 - (message_length % 64)
    if padding_len <= 0:
        padding_len += 64
    padding += b'\x00' * (padding_len - 1)
    padding += struct.pack('<Q', message_length * 8)
    return padding

def perform_attack():
    data_to_append = b"&admin=true"
    
    print("=== Length Extension Attack Demo ===")
    print(f"Original message: {original_message}")
    print(f"Original MAC (MD5): {original_mac}")
    print(f"Data to append: {data_to_append}\n")

    # Try with known key length (14) for demo purposes
    key_length = len(SECRET_KEY)
    print(f"Attempting with key length: {key_length}")

    # Calculate padding and forge message
    padded_length = key_length + len(original_message)
    padding = md5_padding(padded_length)
    forged_message = original_message + padding + data_to_append

    # Generate forged MAC (simulates attacker's prediction)
    h = hashlib.md5()
    h.update(SECRET_KEY + original_message + padding + data_to_append)
    forged_mac = h.hexdigest()

    print(f"\nForged message (hex): {binascii.hexlify(forged_message)}")
    print(f"Forged message: {forged_message}")
    print(f"Forged MAC: {forged_mac}")

    # Test against both servers
    print("\n=== Verification Results ===")
    
    # 1. Test against INSECURE server
    print("\n[Insecure Server (MD5)]")
    if insecure_verify(forged_message, forged_mac):
        print("✅ SUCCESS! Insecure server accepted the forgery (VULNERABLE)")
    else:
        print("❌ FAILED: Insecure server rejected the forgery")

    # 2. Test against SECURE HMAC server
    print("\n[Secure Server (HMAC-SHA256)]")
    if secure_verify(forged_message, forged_mac):
        print("❌ CRITICAL ERROR: Secure server accepted the forgery")
    else:
        print("✅ SECURE: HMAC server correctly rejected the forgery")

if __name__ == "__main__":
    perform_attack()