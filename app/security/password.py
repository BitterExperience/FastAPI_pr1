from pwdlib import PasswordHash

pwd_context = PasswordHash.recommended()



def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain: str, hashed: str) -> bool:
    return "Good" if pwd_context.verify(plain, hashed) else "bad"