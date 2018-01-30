"""Jinja2 filter functions."""	
	
def GetProgressBarColour(percentage):
  result = int(percentage.split('.')[0])
  if result < 25:
    return 'danger'
  elif result < 50:
    return 'warning'
  elif result < 100:
    return 'success'
  else:
    return 'info'