from pwdlib import PasswordHash
pasword_hasher = PasswordHash.recommended()
def hash_password(password):
    result = pasword_hasher.hash(password)
    return result
def verify_password(password,hashed_password):
    return pasword_hasher.verify(password,hashed_password)



