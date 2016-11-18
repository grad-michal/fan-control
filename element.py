import os
import sys

class Element(object):
	def measure(self):
		raise NotImplementedError

class Thermometer(Element):
	def __init__(self, source_path, minimal = 52.0, maximal = 75.0):
		self._source_path = source_path
		self._zero_point = minimal
		self._scale = maximal - minimal
	
	def __enter__(self):
		self._source_file = os.open(self._source_path, os.O_RDONLY)
		return self
		
	def __exit__(self, exc_type, exc_value, traceback):
		os.close(self._source_file)

	def measure(self):
		read = os.pread(self._source_file, 100, 0)
		sensors = []
		for sensor_line in read.decode().split('\n'):
			if not sensor_line:
				continue
			sensor_name, sensor_value = sensor_line.split(' : ')
			sensors.append(int(sensor_value))
		average_sensor = sum(sensors) / len(sensors)
		current = average_sensor / 1000.0
		print("Current Temperature: ", current)
		input = (current - self._zero_point) / self._scale
		return input
