import hmac
import hashlib

SECRET_KEY = b'supersecretkey'  # Still unknown to attacker

def generate_hmac(message: bytes) -> str:
    return hmac.new(SECRET_KEY, message, hashlib.sha256).hexdigest()

def verify(message: bytes, mac: str) -> bool:
    expected_mac = generate_hmac(message)
    return hmac.compare_digest(mac, expected_mac)

def main():
    message = b"amount=100&to=alice"
    mac = generate_hmac(message)

    print("=== Secure Server Simulation ===")
    print(f"Original message: {message.decode()}")
    print(f"HMAC: {mac}")
    print("\\n--- Verifying legitimate message ---")
    if verify(message, mac):
        print("HMAC verified successfully. Message is authentic.\\n")

    forged_message = b"amount=100&to=alice&admin=true"
    forged_mac = mac  # attacker reuses original HMAC

    print("--- Verifying forged message ---")
    if verify(forged_message, forged_mac):
        print("HMAC verified (unexpected).")
    else:
        print("HMAC verification failed (as expected).")

if __name__ == "__main__":
    main()