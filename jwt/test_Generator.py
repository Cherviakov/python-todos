import unittest
from unittest.mock import patch, Mock, call
from datetime import * 

from jwt.Generator import Generator 

class PrivateKey:
  pass

class Matcher:
  def __init__ (self, values):
    self.values = values

  def __eq__ (self, other):
    arg = other
    if isinstance(other, dict):
      arg = other.values()
    if isinstance(self.values, list):
      isPresentList = [] 
      for v in self.values:
        isPresentList.append(v in arg)
      return all(isPresentList)
    else:
      value = self.values
      return value in arg 

class TestGenerator(unittest.TestCase):
  def setUp (self):
    privateKey = PrivateKey()
    privateKey.sign = Mock(return_value='signature')
    self.Gen = Generator(privateKey)

  @patch('jwt.Generator.serialize', return_value = '')
  @patch('cryptography.hazmat.primitives.hashes')
  @patch('cryptography.hazmat.primitives.asymmetric.padding')
  def testGenerateAccessToken(self, paddingm, hashesm, serializem):
    aud = 'http://localhost:3000'
    userId = '1'

    [accessToken, expires] = self.Gen.generateAccessToken(aud, userId)

    self.assertEqual(serializem.call_count, 2) 
    serializem.assert_called_with(Matcher([self.Gen._iss, aud, userId]))
    self.assertEqual(self.Gen._key.sign.call_count, 1) 
    self.assertEqual(type(accessToken) is str, True)
    self.assertEqual(type(expires) is datetime, True)

  @patch('jwt.Generator.serialize', return_value = '')
  @patch('cryptography.hazmat.primitives.hashes')
  @patch('cryptography.hazmat.primitives.asymmetric.padding')
  def testGenerateRefreshToken(self, paddingm, hashesm, serializem):
    aud = 'http://localhost:3000'
    userId = '1'

    refreshToken = self.Gen.generateRefreshToken(aud, userId)

    self.assertEqual(serializem.call_count, 2) 
    serializem.assert_called_with(Matcher([self.Gen._iss, aud, userId]))
    self.assertEqual(self.Gen._key.sign.call_count, 1) 
    self.assertEqual(type(refreshToken) is str, True)
    
  @patch('jwt.Generator.constructSigningInput', return_value = '')
  @patch('cryptography.hazmat.primitives.hashes')
  @patch('cryptography.hazmat.primitives.asymmetric.padding')
  def testSign(self, paddingm, hashesm, constructSigningInputm):
    headers = 'headers'
    message = 'message'

    self.Gen._sign(headers, message)

    constructSigningInputm.assert_called_with(headers, message)
    self.assertEqual(self.Gen._key.sign.call_count, 1)
