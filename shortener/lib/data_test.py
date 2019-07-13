import unittest
import fakeredis

import data

class DataTest(unittest.TestCase):

  def setUp(self):
    self.db = fakeredis.FakeStrictRedis()

  def test_increment_and_get_global_visits(self):
    data.increment_visits(self.db)
    data.increment_visits(self.db)
    v = data.get_visits(self.db)
    self.assertEqual(2, v)

  def test_increments_global_and_path_visits(self):
    data.increment_visits(self.db)
    data.increment_visits(self.db, path='test')
    v = data.increment_visits(self.db, path='test')
    self.assertEqual((3, 2), v)

  def test_returns_no_redirect(self):
    v = data.get_redirect(self.db, 'none_existant')
    self.assertEqual((None, 0), v)

  def test_returns_existing_redirect(self):
    data.set_redirect(self.db, 'path', 'http://value.com')
    v, visits = data.get_redirect(self.db, 'path')
    self.assertEqual(v, 'http://value.com')
    self.assertEqual(0, visits)

  def test_deletes_existing_redirect(self):
    data.set_redirect(self.db, 'path', 'http://value.com')
    data.remove_redirect(self.db, 'path')
    v = data.get_redirect(self.db, 'path')
    self.assertEqual((None, 0), v)

  def test_lists_redirects_when_none(self):
    cursor, results = data.list_redirects(self.db)
    self.assertIsNone(cursor)
    self.assertEqual(0, len(results))

  def test_lists_has_no_cursor_if_no_more_results(self):
    expected = [('t1', ('v1', 0)), ('t2', ('v2', 0))]
    for key, (path, _) in expected:
      data.set_redirect(self.db, key, path)

    # Should return no cursor since we only had 2 results and count is 50
    cursor, results = data.list_redirects(self.db, count=50)
    self.assertIsNone(cursor)
    self.assertSequenceEqual(expected, results)

  def test_lists_has_no_cursor_if_more_results(self):
    expected = [('t1', ('v1', 0)), ('t2', ('v2', 0))]
    for key, (path, _) in expected:
      data.set_redirect(self.db, key, path)

    # Should return a cursor then no cursor
    cursor, results = data.list_redirects(self.db, count=1)
    self.assertIsNotNone(cursor)
    self.assertSequenceEqual(expected[:1], results)
    cursor, results = data.list_redirects(self.db, cursor=cursor, count=2)
    self.assertIsNone(cursor)
    self.assertSequenceEqual(expected[1:], results)

if __name__ == '__main__':
  unittest.main()

