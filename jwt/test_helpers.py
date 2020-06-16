import unittest

from jwt.helpers import UTF8ToBase64, base64ToUTF8

class TestHelper (unittest.TestCase):
  def testUTF8ToBase64 (self):
    string = "Hello World!"
    encoded = "SGVsbG8gV29ybGQh"
    self.assertEqual(UTF8ToBase64(string), encoded)

  # @unittest.skip("skip")
  def testBase64ToUTF8 (self):
    string = "SGVsbG8gV29ybGQh"
    decoded = "Hello World!"
    self.assertEqual(base64ToUTF8(string), decoded)

if __name__ == '__main__':
  unittest.main()
