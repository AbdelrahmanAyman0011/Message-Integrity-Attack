## Steps

1. Run `server.py` to get original MAC and message.
2. Run `client.py` to forge a new message and MAC.
3. Use `verify()` in `server.py` to test the forged MAC.
4. Run `secure_server.py` to see the attack fail with HMAC.
   '''

# Save files

files_to_create = {
"server.py": server_code,
"client.py": client_code,
"secure_server.py": secure_server_code,
"README.md": readme_content
}

for filename, content in files_to_create.items():
with open(os.path.join(base_dir, filename), "w") as f:
f.write(content)

base_dir # Return the base directory path
