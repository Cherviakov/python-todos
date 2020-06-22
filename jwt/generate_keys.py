import os

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.serialization import Encoding, PrivateFormat, PublicFormat, NoEncryption

def generateKeyPair (path = os.path.abspath(os.getcwd()), fileName = "key"):
  privatePath = os.path.join(path, fileName)
  publicPath = os.path.join(path, fileName + '.pub')
  isPrivateKeyExists = os.path.isfile(privatePath)
  isPublicKeyExists = os.path.isfile(publicPath)
  if (isPrivateKeyExists == False or isPublicKeyExists == False):
    if (isPrivateKeyExists == True):
      os.remove(privatePath)
    if (isPublicKeyExists == True):
      os.remove(publicPath)
    try:
      private_key_instance = rsa.generate_private_key(
        public_exponent=65537,
        key_size=4096,
        backend=default_backend(),
      )
      private_key = private_key_instance.private_bytes(
        encoding=Encoding.PEM,
        format=PrivateFormat.PKCS8,
        encryption_algorithm=NoEncryption(),
      )
      public_key = private_key_instance.public_key().public_bytes(
        encoding=Encoding.PEM,
        format=PublicFormat.SubjectPublicKeyInfo,
      )
    except Exception as err:
      print("generate keys error", type(err), err)
    try:
      privateFile = open(privatePath, "w")
      privateFile.write(private_key.decode())
      privateFile.close()
      publicFile = open(publicPath, "w")
      publicFile.write(public_key.decode())
      publicFile.close()
      os.chmod(privatePath, 0o644)
      os.chmod(publicPath, 0o644)
    except Exception as err:
      print("writing keys to file error", type(err), err)
