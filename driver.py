import os

import logging

class Driver(object):
	def update(self, control):
		raise NotImplementedError

class Fan(Driver):
	LOGGER = logging.getLogger('Fan')

	def __init__(self, mode_path, speed_path):
		self._mode_path = mode_path
		self._speed_path = speed_path
	
	def __enter__(self):
		self._mode_file = os.open(self._mode_path, os.O_WRONLY)
		self._speed_file = os.open(self._speed_path, os.O_WRONLY)
		os.write(self._mode_file, b"0")
		return self
		
	def __exit__(self, exc_type, exc_value, traceback):
		os.write(self._mode_file, b"1")
		os.close(self._speed_file)
		os.close(self._mode_file)

	def update(self, control):
		target = int(control * 255)
		if target >= 255:
			target = 254
		elif target <= 3:
			target = 2
		written = str(target).encode()
		Fan.LOGGER.debug("Fan set to %i", target)
		os.write(self._speed_file, written)
