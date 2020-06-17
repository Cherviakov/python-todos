import unittest

from jwt.helpers import (
  encodingToBase64, 
  base64ToEncoding,
  constructSigningInput,
  serialize,
  deserialize,
)

class TestHelper (unittest.TestCase):
  def testUTF8ToBase64 (self):
    string = "Hello World!"
    encoded = "SGVsbG8gV29ybGQh"
    self.assertEqual(encodingToBase64(string), encoded)

  def testBase64ToUTF8 (self):
    string = "SGVsbG8gV29ybGQh"
    decoded = "Hello World!"
    self.assertEqual(base64ToEncoding(string), decoded)

  def testAsciiToBase64 (self):
    string = ascii("HËllo world")
    encoded = "J0hceGNibGxvIHdvcmxkJw=="
    self.assertEqual(encodingToBase64(string, 'ascii'), encoded)

  def testBase64ToAscii (self):
    string = "J0hceGNibGxvIHdvcmxkJw=="
    decoded = ascii("HËllo world")
    self.assertEqual(base64ToEncoding(string, 'ascii'), decoded)

  def testConstructSigningInput (self):
    headers = encodingToBase64("Hello world")
    message = encodingToBase64("Some message")
    result = "Hello world.U29tZSBtZXNzYWdl"
    self.assertEqual(constructSigningInput(headers, message), result)

  def testSerialize (self):
    json = { "a": "te st", "b": 2, "c": True }
    result = "JTdCJTIyYSUyMiUzQSUyMCUyMnRlJTIwc3QlMjIlMkMlMjAlMjJiJTIyJTNBJTIwMiUyQyUyMCUyMmMlMjIlM0ElMjB0cnVlJTdE"
    self.assertEqual(serialize(json), result)

  def testDeserialize (self):
    string = "JTdCJTIyYSUyMiUzQSUyMCUyMnRlJTIwc3QlMjIlMkMlMjAlMjJiJTIyJTNBJTIwMiUyQyUyMCUyMmMlMjIlM0ElMjB0cnVlJTdE"
    result = { "a": "te st", "b": 2, "c": True }
    self.assertEqual(deserialize(string), result)

if __name__ == '__main__':
  unittest.main()
