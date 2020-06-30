from json import dumps, loads
from urllib.parse import quote, unquote
from base64 import b64encode, b64decode

def encodingToBase64 (string, encoding = "UTF-8"):
  return b64encode(string.encode(encoding, 'backslashreplace')).decode(encoding, 'backslashreplace')

def base64ToEncoding (string, encoding = "UTF-8"):
  return b64decode(string.encode(encoding, 'backslashreplace')).decode(encoding, 'backslashreplace')

def constructSigningInput (headers, message):
  return base64ToEncoding(headers, 'ascii') + "." + message

def serialize (json):
  return encodingToBase64(quote(dumps(json, indent=2, default=str)))

def deserialize (string):
  return loads(unquote(base64ToEncoding(string)))
