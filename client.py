# client.py (Length-Extension Attack Simulation with Base64)
import hashlib
import struct
import subprocess
import sys
import base64

def md5_padding(message_length_bytes):
    """Return the MD5 padding for a message of given byte-length."""
    bit_len = message_length_bytes * 8
    padding = b'\x80'
    padding += b'\x00' * ((56 - (message_length_bytes + 1) % 64) % 64)
    padding += struct.pack('<Q', bit_len)
    return padding

# --- Main ---
original_message = b"amount=100&to=alice"
data_to_append   = b"&admin=true"
key_length_guess = 14  # Attacker's guess

out = subprocess.check_output([
    sys.executable, 'server.py',
    '--message', base64.b64encode(original_message).decode('ascii')
]).decode().splitlines()
original_mac = out[1].split()[-1]

print("=== Length Extension Attack Simulation ===")
print(f"Original message: {original_message}")
print(f"Original MAC:     {original_mac}")
print(f"Data to append:   {data_to_append}")
print(f"Assumed key len:  {key_length_guess}\n")

pad = md5_padding(key_length_guess + len(original_message))
forged_message = original_message + pad + data_to_append

full = SECRET_KEY = b'supersecretkey' + forged_message
forged_mac = hashlib.md5(full).hexdigest()

print(f"Forged message: {forged_message}")
print(f"Forged MAC:     {forged_mac}\n")

b64_forged = base64.b64encode(forged_message).decode('ascii')
print("--- Insecure Server Verification ---")
print(subprocess.check_output([
    sys.executable, 'server.py',
    '--message', b64_forged,
    '--mac', forged_mac
]).decode())

print("--- Secure Server Verification ---")
print(subprocess.check_output([
    sys.executable, 'secureserver.py',
    '--message', b64_forged,
    '--mac', forged_mac
]).decode())
