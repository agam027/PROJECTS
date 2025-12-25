# SecureTool — Python Security Utility (CLI)

SecureTool is a Python-based command-line utility designed to analyze password strength, perform secure password hashing and verification, and audit password lists for weak credentials.  
It demonstrates correct password-handling practices and clean CLI tool design.

---

## Features

- **Password Strength Analysis**
  - Entropy-based scoring
  - Checks for length, character variety, and complexity
  - Estimates time required to crack the password

- **Secure Password Hashing**
  - Hash passwords using industry-standard algorithms (default: SHA-256)
  - Supports algorithm selection via CLI flags

- **Password Verification**
  - Verifies passwords by re-hashing and comparing against stored hashes
  - Demonstrates real-world password validation logic

- **Password Audit Mode**
  - Audits a file of passwords in bulk
  - Flags weak passwords using a configurable minimum score
  - Prints a clear summary report

---

## Installation

Clone the repository:

```bash
git clone https://github.com/agam027/securetool.git
cd securetool
```
---

## Usage:

```bash
Check password strength
python securetool.py check "MyStrongPass123!"

Hash a password
python securetool.py hash "MyStrongPass123!" --algo sha256

Verify a password against a hash
python securetool.py verify "MyStrongPass123!" --hash <hash-value>

Audit a file of passwords
python securetool.py audit passwords.txt --min-score 3

Example Output
Password Strength SCORE: 9
Password Entropy: 71.45 bits
Estimated Crack Time: Thousands of years

Auditing file: passwords.txt
--------------------------------
Total passwords checked: 13
Weak passwords: 10
Strong passwords: 3

Project Structure
securetool/
├── main.py
├── password_strength.py
├── util.py
├── top30.json
└── README.md


Security Note ⚠️

This project is intended for educational and demonstration purposes only.
All passwords used are test data. The tool does not store real credentials or user information.

```