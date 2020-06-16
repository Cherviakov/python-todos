from base64 import b64encode, b64decode

def UTF8ToBase64 (string):
  return b64encode(string.encode("UTF-8")).decode("UTF-8")

def base64ToUTF8 (string):
  return b64decode(string.encode("UTF-8")).decode("UTF-8")
