"""Helpers for working with redis."""

def _path_key(path):
  return 'REDIRECT:' + path

def get_redirect(db, path):
  path, visits = db.hmget(_path_key(path), 'redirect_to', 'visits')
  if not path:
    return None, 0
  return path.decode('utf-8'), int(visits)

def list_redirects(db, cursor=None, count=50):
  if not cursor:
    cursor = 0
  cursor, keys = db.scan(match=_path_key('*'), cursor=cursor, count=count)
  if not keys:
    return (None, [])

  paths = (k.decode('utf-8').partition(':')[2] for k in keys)
  p = db.pipeline(transaction=False)
  for k in keys:
    p.hmget(k, ['redirect_to', 'visits'])
  values = ((v[0].decode('utf-8'), int(v[1])) for v in p.execute())
  if len(keys) < count:
    cursor = None
  return (cursor, list(zip(paths, values)))

def set_redirect(db, path, value):
  db.hmset(_path_key(path), {'redirect_to': value, 'visits': 0})

def remove_redirect(db, path):
  db.delete(_path_key(path))

def get_visits(db):
  v = db.get('GLOBAL:visits')
  if not v:
    return 0
  return int(v)

def increment_visits(db, path=None):
  p = db.pipeline(transaction=False)
  p.incr('GLOBAL:visits')
  if path:
    p.hincrby(_path_key(path), 'visits')
  result = p.execute()
  if len(result) > 1:
    return tuple(result)
  return result[0]
