from datetime import datetime

dt = datetime.fromtimestamp(1596229437)

dt_format = "%%m/%%d/%%Y".replace("%%", "%")

formatted = dt.strftime(dt_format)
print(formatted)