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

def nl_listed(iterable: Iterable[str], style=", ", use_and=True):
    listed = [*iterable]
    if len(listed) == 0:
        return ""
    if len(listed) == 1:
        return listed[0]
    final_str = ""
    for word in listed[:-2]:
        final_str += word+style
    if use_and:
        final_str += f"{listed[-2]} and {listed[-1]}"
    else:
        final_str += listed[-2]+style+listed[-1]
        
    return final_str