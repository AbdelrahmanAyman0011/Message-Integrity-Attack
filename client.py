# client.py
import subprocess
import sys
import base64

# Import hashpump from hashpumpy to perform length extension attack
try:
    from hashpumpy import hashpump
except ImportError:
    print("Error: hashpumpy not installed. Run 'pip install hashpumpy'")
    sys.exit(1)

# Attacker’s known intercepted message and MAC pair from the insecure server
original_message = b"amount=100&to=alice"
data_to_append = b"&admin=true"
key_length_guess = 14  # Attacker guesses the length of the secret key

# Step 1: Request original MAC from the insecure server (base64 encode the message)
b64_orig = base64.b64encode(original_message).decode('ascii')
output = subprocess.check_output([
    sys.executable, 'server.py',
    '--message', b64_orig
]).decode().splitlines()

# Parse the MAC from the server response
original_mac = None
for line in output:
    if "MAC:" in line:
        original_mac = line.split()[-1]
        break

if not original_mac:
    print("Error: Couldn't find MAC in server response.")
    sys.exit(1)

print("=== Length Extension Attack Simulation ===")
print(f"Original message: {original_message}")
print(f"Original MAC:     {original_mac}")
print(f"Data to append:   {data_to_append}")
print(f"Assumed key len:  {key_length_guess}\n")

# Step 2: Perform the length extension attack with hashpump
new_mac, forged_message_str = hashpump(
    original_mac,
    original_message.decode('ascii'),
    data_to_append.decode('ascii'),
    key_length_guess
)

# hashpump returns forged_message as bytes already in recent versions
forged_message = forged_message_str

print(f"Forged message: {forged_message}")
print(f"Forged MAC:     {new_mac}\n")

# Step 3: Verify forged pair against insecure and secure servers

# Base64 encode forged message for transmission
b64_forged = base64.b64encode(forged_message).decode('ascii')

print("--- Insecure Server Verification (MD5) ---")
print(subprocess.check_output([
    sys.executable, 'server.py',
    '--message', b64_forged,
    '--mac', new_mac
]).decode())

print("--- Secure Server Verification (HMAC-SHA256) ---")
print(subprocess.check_output([
    sys.executable, 'secureserver.py',
    '--message', b64_forged,
    '--mac', new_mac
]).decode())
