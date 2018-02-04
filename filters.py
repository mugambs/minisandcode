"""Jinja2 filter functions."""	
	
def GetProgressBarColour(percentage):
  if percentage < 25:
    return 'danger'
  elif percentage < 50:
    return 'warning'
  elif percentage < 100:
    return 'success'
  else:
    return 'info'