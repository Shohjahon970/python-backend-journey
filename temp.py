from pwdlib import PasswordHash

pwdHasher = PasswordHash.recommended()
password = "test123"
pasword_hash=pwdHasher.hash(password)
print(pwdHasher.verify("test456",pasword_hash))
