import unittest
import fakeredis

import data

class DataTest(unittest.TestCase):

  def setUp(self):
    self.db = fakeredis.FakeStrictRedis()

  def test_increments_visits(self):
    data.increment_visits(self.db)
    data.increment_visits(self.db)
    v = data.increment_visits(self.db)
    self.assertEqual(3, v)

  def test_returns_no_redirect(self):
    v = data.get_redirect(self.db, 'none_existant')
    self.assertIsNone(v)

  def test_returns_existing_redirect(self):
    data.set_redirect(self.db, 'path', 'http://value.com')
    v = data.get_redirect(self.db, 'path')
    self.assertEqual(v, 'http://value.com')

  def test_deletes_existing_redirect(self):
    data.set_redirect(self.db, 'path', 'http://value.com')
    data.remove_redirect(self.db, 'path')
    v = data.get_redirect(self.db, 'path')
    self.assertIsNone(v)

if __name__ == '__main__':
  unittest.main()

