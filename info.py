from datetime import datetime

capacity_path = "/sys/class/power_supply/axp2202-battery/capacity"
status_path = "/sys/class/power_supply/axp2202-battery/status"

def formatted_time():
	return datetime.now().strftime("%H:%M") 

def battery_status():
	return read_file(status_path)

def battery_capacity():
	return read_file(capacity_path)

def read_file(file_path):
	try:
		with open(file_path, "r") as f:
			return f.read().strip()
	except FileNotFoundError:
		print("File not found " + file_path)
		return "err"
	except IOError:
		print("I/O error" + file_path)
		return "err"