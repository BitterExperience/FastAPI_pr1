from app.security.password import hash_password, verify_password




from app.security.jwt import create_access_token, decode_access_token

token = create_access_token({"sub": "123"})
print("Token:", token[:50] + "...")
print("Length:", len(token))
print("____")
token_decode = decode_access_token(token)
print(token_decode.get('sub'))

#
# res = hash_password("secret123")
# print("Hash:", res)
# print(verify_password("secret123", res))