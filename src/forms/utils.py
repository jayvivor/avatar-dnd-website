from collections.abc import Iterable

def to_iter(obj, blacklist=[str]):
  '''
  Returns an iterable version of whatever object it is being passed.
  '''

  for t in blacklist:
    if isinstance(obj, t):
      return [obj]
  
  if isinstance(obj, Iterable):
    return obj
  
  return [obj]