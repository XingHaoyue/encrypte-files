from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import hashes
import cryptography.hazmat.primitives.asymmetric.padding as pad
from cryptography.hazmat.primitives import serialization

private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048,
    backend=default_backend()
)
public_key = private_key.public_key()


# pem = private_key.private_bytes(
#     encoding=serialization.Encoding.PEM,
#     format=serialization.PrivateFormat.PKCS8,
#     encryption_algorithm=serialization.NoEncryption()
# )
# with open('private_key.pem', 'wb') as f:
#     f.write(pem)

# pem = public_key.public_bytes(
#     encoding=serialization.Encoding.PEM,
#     format=serialization.PublicFormat.SubjectPublicKeyInfo
# )
# with open('public_key.pem', 'wb') as f:
#     f.write(pem)


# raw_message = str(input(">>> "))
# message = raw_message.encode("utf-8")
# print(message)
with open('test.txt', 'rb') as f:
    message = f.read()
# print(pem)
print(public_key)
print(message)
encrypted = public_key.encrypt(
    message,
    pad.OAEP(
        mgf=pad.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    )
)


print(encrypted)