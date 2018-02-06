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

def GetProgressCircleColour(percentage):
  if percentage < 10:
    return '#F44336'  # red
  elif percentage < 20:
    return '#FF5722'  # deeporange
  elif percentage < 30:
    return '#FF9800'  # orange
  elif percentage < 40:
    return '#FFC107'  # amber
  elif percentage < 50:
    return '#FFEB3B'  # yellow
  elif percentage < 60:
    return '#CDDC39'  # lime
  elif percentage < 70:
    return '#8BC34A'  # lightgreen
  elif percentage < 80:
    return '#4CAF50'  # green
  elif percentage < 90:
    return '#009688'  # teal
  elif percentage < 100:
    return '#00BCD4'  # cyan
  else:
    return '#03A9F4' # lightblue
