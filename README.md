# Length Extension Attack Demo (MAC Forgery)

This project demonstrates how a naive MAC construction  
```python
MAC = MD5(secret || message)

---

## Project Files

- `server.py`: Simulates an insecure MAC using `MD5(secret || message)`
- `client.py`: Performs a length extension attack on the MAC
- `secure_server.py`: Simulates a secure server using `HMAC(secret, message)` with SHA256
- `README.md`: Instructions to run the project
- `MAC and LEA (1.Background Study)` : 
- `MAC and LEA (2.Mitigation Write-Up)`:


---

## Steps to Run
- pip install -r requirements.txt
- python Client.py


---

## Expected Output
===Length Extension Attack Simulation ===
Original message: b'amount=100&to=alice'
Original MAC:
614d28d808af46d3702 fe35fae67267c
Data to append: b'&admin=true'
Assumed key len: 14

=== Insecure MD5 Server ===
Message: in=true' MAC:
b'amount=100&to=alice\x80\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x08\x01\x00\x00\x00\x00\x00\x00&adm
97312a73075b6e1589117ce55e0a3ca6
MAC verified. Message is authentic.

Secure Server Verification (HMAC-SHA256)
=== Secure HMAC-SHA256 Server ===
Message: in=true' HMAC:
b'amount=100&to=alice\x80\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x08\x01\x00\x00\x00\x00\x00\x00&adm
97312a73075b6e1589117ce55e0a3ca6
HMAC verification failed.

---
