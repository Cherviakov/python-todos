from datetime import * 

from dateutil.relativedelta  import *
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding 

from jwt.helpers import (
  constructSigningInput,
  serialize,
)

class Generator:
  def __init__ (self, privateKey, config = { 'iss': 'server', 'accessExpires': { 'hours': +1 }, 'refreshExpires': { 'months': +1 } }):
    self._key = privateKey
    self._iss = config['iss']
    self._aexp = config['accessExpires']
    self._rexp = config['refreshExpires']

  def generateAccessToken (self, aud, userId):
    headers = serialize({ 'type': 'JWS', 'alg': 'PS512' })
    exp = datetime.now() + relativedelta(**self._aexp)
    message = serialize({
      'iss': self._iss,
      'aud': aud,
      'exp': exp,
      'iat': datetime.now(),
      'sub': userId,
    })
    signature = self._sign(headers, message) 
    accessToken = headers + '.' + message + '.' + signature
    return [accessToken, exp]

  def generateRefreshToken (self, aud, userId):
    headers = serialize({ 'type': 'JWS', 'alg': 'PS512' })
    message = serialize({
      'iss': self._iss,
      'aud': aud,
      'exp': datetime.now() + relativedelta(**self._rexp),
      'iat': datetime.now(),
      'sub': userId,
    })
    signature = self._sign(headers, message)
    return (headers + '.' + message + '.' + signature).encode('utf-8').hex()

  def _sign (self, headers, message):
    signingInput = constructSigningInput(headers, message)
    return self._key.sign(
      signingInput, 
      padding.PSS(
        mgf=padding.MGF1(hashes.SHA256()),
        salt_length=padding.PSS.MAX_LENGTH
      ),
      hashes.SHA256(),
    ) 
