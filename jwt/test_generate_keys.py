import unittest
from unittest.mock import patch, Mock, call
import os

from jwt.generate_keys import generateKeyPair


class TestGenerateKeys (unittest.TestCase):
  @patch('builtins.open')
  @patch('cryptography.hazmat.backends')
  @patch('cryptography.hazmat.primitives.asymmetric.rsa.generate_private_key')
  def testIfPairExistsNotGenerate (self, backendsm, generatem, openm):
    os.path.isfile = Mock(return_value=True)

    generateKeyPair()

    backendsm.assert_not_called()
    generatem.assert_not_called()
    openm.assert_not_called()

  @patch('builtins.open')
  @patch('cryptography.hazmat.backends')
  @patch('cryptography.hazmat.primitives.asymmetric.rsa.generate_private_key')
  def testIfPrivateKeyPresentCleanup (self, generatem, backendsm, openm):
    os.path.isfile = Mock(side_effect=[True, False])
    os.remove = Mock()
    os.chmod = Mock()

    path = 'my-keys-folder'
    fileName = 'my-key-file'

    generateKeyPair(path, fileName)

    os.remove.assert_called_once()
    os.remove.assert_called_with(os.path.join(path, fileName))

  @patch('builtins.open')
  @patch('cryptography.hazmat.backends')
  @patch('cryptography.hazmat.primitives.asymmetric.rsa.generate_private_key')
  def testIfPublicKeyPresentCleanup (self, generatem, backendsm, openm):
    os.path.isfile = Mock(side_effect=[False, True])
    os.remove = Mock()
    os.chmod = Mock()

    path = 'my-keys-folder'
    fileName = 'my-key-file'

    generateKeyPair(path, fileName)

    os.remove.assert_called_once()
    os.remove.assert_called_with(os.path.join(path, fileName + '.pub'))

  @patch('builtins.open')
  @patch('cryptography.hazmat.backends')
  @patch('cryptography.hazmat.primitives.asymmetric.rsa.generate_private_key')
  def testGenerateMethodActuallyCalled (self, generatem, backendsm, openm):
    os.path.isfile = Mock(return_value=False)
    os.chmod = Mock()

    generateKeyPair()

    generatem.assert_called_once()

  @patch('builtins.open')
  @patch('cryptography.hazmat.backends')
  @patch('cryptography.hazmat.primitives.asymmetric.rsa.generate_private_key')
  def testUpdatePermissionsOnPrivateKeyFile (self, generatem, backendsm, openm):
    os.path.isfile = Mock(return_value=False)
    os.chmod = Mock()

    path = 'my-key-folder'
    fileName = 'my-key-file'

    generateKeyPair(path, fileName)

    os.chmod.ayn_call([call(os.path.join(path, fileName), 0o644)])

  @patch('builtins.open')
  @patch('cryptography.hazmat.backends')
  @patch('cryptography.hazmat.primitives.asymmetric.rsa.generate_private_key')
  def testUpdatePermissionsOnPublicKeyFile (self, generatem, backendsm, openm):
    os.path.isfile = Mock(return_value=False)
    os.chmod = Mock()

    path = 'my-key-folder'
    fileName = 'my-key-file'

    generateKeyPair(path, fileName)

    os.chmod.ayn_call([call(os.path.join(path, fileName + '.pub'), 0o644)])

if __name__ == '__main__':
  unittest.main()
