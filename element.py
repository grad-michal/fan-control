import os
import sys

import logging

class Element(object):
	def measure(self):
		raise NotImplementedError

class Thermometer(Element):
	LOGGER = logging.getLogger('Thermometer')

	def __init__(self, minimal, maximal, source_path):
		self._source_path = source_path
		self._zero_point = minimal
		self._scale = maximal - minimal
		self._warn_level = (maximal + minimal) / 2.0
		
	def __enter__(self):
		self._source_file = os.open(self._source_path, os.O_RDONLY)
		return self
		
	def __exit__(self, exc_type, exc_value, traceback):
		os.close(self._source_file)	
		
	def measure(self):		
		current = self._current()
		if current >= self._warn_level:
			level = logging.WARNING
		else:
			level = logging.INFO
		Thermometer.LOGGER.log(level, "Current temperature is %.1f°C", current)
		input = (current - self._zero_point) / self._scale
		return input
		
	def _current(self):
		raise NotImplementedError

class ThermometerXU4(Thermometer):	
	SENSOR_FILE_PATH = "/sys/devices/10060000.tmu/temp"

	def __init__(self, minimal, maximal):
		super(ThermometerXU4, self). __init__(minimal, maximal, ThermometerXU4.SENSOR_FILE_PATH)
	
	def _current(self):
		read = os.pread(self._source_file, 100, 0)
		sensors = []
		for sensor_line in read.decode().split('\n'):
			if not sensor_line:
				continue
			sensor_name, sensor_value = sensor_line.split(' : ')
			sensors.append(int(sensor_value))
		average_sensor = sum(sensors) / len(sensors)
		return average_sensor / 1000.0
		
class ThermometerC2(Thermometer):
	SENSOR_FILE_PATH = "/sys/devices/virtual/thermal/thermal_zone0/temp"

	def __init__(self, minimal, maximal):
		super(ThermometerC2, self). __init__(minimal, maximal, ThermometerC2.SENSOR_FILE_PATH)
	
	def _current(self):
		read = os.pread(self._source_file, 100, 0)		
		return int(read.decode()) / 1000.0
