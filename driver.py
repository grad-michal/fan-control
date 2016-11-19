import os

import logging

class Driver(object):
	LOGGER = logging.getLogger('Driver')
	
	def __init__(self):		
		self._last_write = -1

	def update(self, control):
		if control >= 1.0:
			control = 1.0
		elif control <= 0.0:
			control = 0.0
		target = self._calculate_target(control)
		if target == self._last_write:
			return
			
		spinning_up = False
		if self._last_write <= 0 and target > 0:
			spin_up_target = self._spin_up_target()
			if spin_up_target > target:				
				target = spin_up_target
				spinning_up = True
		
		if spinning_up:
			Driver.LOGGER.info("Fan set to %i (spinning up)", target)
		else:
			Driver.LOGGER.info("Fan set to %i (%.0f%%)", target, control*100.0)
			
		self._write_speed(target)
		self._last_write = target
		
	def _calculate_target(self, control):
		raise NotImplementedError
		
	def _write_speed(self, target):
		raise NotImplementedError
		
	def _spin_up_target(self):
		raise NotImplementedError
		
class DriverXU4(Driver):
	FAN_MODE_FILE = "/sys/devices/odroid_fan.14/fan_mode"
	FAN_SPEED_FILE = "/sys/devices/odroid_fan.14/pwm_duty"

	def __init__(self):		
		super(DriverXU4, self).__init__()
	
	def __enter__(self):
		self._mode_file = os.open(FAN_MODE_FILE, os.O_WRONLY)
		self._speed_file = os.open(FAN_SPEED_FILE, os.O_WRONLY)
		os.write(self._mode_file, b"0")
		return self
		
	def __exit__(self, exc_type, exc_value, traceback):
		os.write(self._mode_file, b"1")
		os.close(self._speed_file)
		os.close(self._mode_file)

	def _calculate_target(self, control):
		return int(control * 251) + 3
		
	def _write_speed(self, target):
		written = str(target).encode()
		os.write(self._speed_file, written)		
		
	def _spin_up_target(self):
		return 200

class DriverC2(Driver):
	PWM_STATE_FILE = "/sys/devices/platform/pwm-ctrl/enable0"
	PWM_DUTY_FILE = "/sys/devices/platform/pwm-ctrl/duty0"
	PWM_FREQ_FILE = "/sys/devices/platform/pwm-ctrl/freq0"

	def __init__(self):		
		super(DriverC2, self).__init__()
	
	def __enter__(self):
		self._state_file = os.open(DriverC2.PWM_STATE_FILE, os.O_WRONLY)
		self._speed_file = os.open(DriverC2.PWM_DUTY_FILE, os.O_WRONLY)
		self._freq_file = os.open(DriverC2.PWM_FREQ_FILE, os.O_WRONLY)
		os.write(self._state_file, b"1")
		os.write(self._freq_file, b"100000")
		os.write(self._freq_file, b"0")
		return self
		
	def __exit__(self, exc_type, exc_value, traceback):
		os.write(self._state_file, b"0")
		os.write(self._freq_file, b"0")
		os.close(self._speed_file)
		os.close(self._state_file)
		os.close(self._freq_file)

	def _calculate_target(self, control):
		if control == 0:
			return 0
			
		return int(control * 523) + 500
		
	def _write_speed(self, target):
		written = str(target).encode()
		os.write(self._speed_file, written)	

	def _spin_up_target(self):
		return 1000
