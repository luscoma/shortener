"""Helpers for working with redis."""

def get_redirect(db, path):
  v = db.get('REDIRECT:' + path)
  if not v:
    return v
  return v.decode('utf-8')

def list_redirects(db, cursor=None, count=50):
  if not cursor:
    cursor = 0
  cursor, keys = db.scan(match='REDIRECT:*', cursor=cursor, count=count)
  if not keys:
    return (None, [])

  paths = (k.decode('utf-8').partition(':')[2] for k in keys)
  values = (v.decode('utf-8') for v in db.mget(keys))
  if len(keys) < count:
    cursor = None
  return (cursor, zip(paths, values))

def set_redirect(db, path, value):
  db.set('REDIRECT:' + path, value)

def remove_redirect(db, path):
  db.delete('REDIRECT:' + path)

def increment_visits(db):
  return db.incr('GLOBAL:visits')

