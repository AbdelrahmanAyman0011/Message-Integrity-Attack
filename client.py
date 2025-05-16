# client.py (Length-Extension Attack Simulation using hashpumpy & Base64)
import subprocess
import sys
import base64

# Import the hashpump function for MD5 length extension attacks
try:
    from hashpumpy import hashpump
except ImportError:
    print("Error: hashpumpy not installed. Run 'pip install hashpumpy'")
    sys.exit(1)

# --- Configuration ---
original_message = b"amount=100&to=alice"  # The message we intercepted
data_to_append   = b"&admin=true"          # The new data we want to append
key_length_guess = 14                      # Attacker's guess for the secret key length

# --- Step 1: Retrieve the original MAC from the insecure server ---
# We send the Base64-encoded original_message to server.py to get its MAC
b64_orig = base64.b64encode(original_message).decode('ascii')
output = subprocess.check_output([
    sys.executable, 'server.py',
    '--message', b64_orig
]).decode().splitlines()
original_mac = output[1].split()[-1]  # Parse "MAC: <value>" line

print("=== Length Extension Attack Simulation ===")
print(f"Original message: {original_message}")
print(f"Original MAC:     {original_mac}")
print(f"Data to append:   {data_to_append}")
print(f"Assumed key len:  {key_length_guess}\n")

# --- Step 2: Perform the length extension attack ---
# hashpump returns (new_mac, forged_message_str)
new_mac, forged_message_str = hashpump(
    original_mac,
    original_message.decode('ascii'),
    data_to_append.decode('ascii'),
    key_length_guess
)
# Convert the returned forged message (latin1-encoded) back to bytes
forged_message = forged_message_str.encode('latin1')

print(f"Forged message: {forged_message}")
print(f"Forged MAC:     {new_mac}\n")

# --- Step 3: Verify the forged pair against both servers ---
# Base64-encode the forged message so we can send it as a CLI argument
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
