# Length Extension Attack Demo (MAC Forgery)

This project demonstrates a length extension attack on insecure MAC implementations using MD5, and shows how switching to HMAC mitigates the attack.

---

## Project Files

- `server.py`: Simulates an insecure MAC using `MD5(secret || message)`
- `client.py`: Performs a length extension attack on the MAC
- `secure_server.py`: Simulates a secure server using `HMAC(secret, message)` with SHA256
- `README.md`: Instructions to run the project

---

## Steps to Run

### 1. Run the insecure server to get original MAC:
```bash
python server.py
