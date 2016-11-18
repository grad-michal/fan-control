import logging

class Controller(object):
	def update(self, error):
		raise NotImplementedError

class PID(Controller):
	LOGGER = logging.getLogger('PID')

	def __init__(self, proportional, integrative, derivative, integral_minimum = None, integral_maximum = None):
		self._proportional = proportional
		self._integrative = integrative
		self._derivative = derivative
		
		if integral_maximum is None:
			self._integral_minimum = 0.0
		else:
			self._integral_minimum = integral_minimum
		if integral_maximum is None:
			self._integral_maximum = 1.0 / integrative
		else:
			self._integral_maximum = integral_maximum
		self._integral = 0.0
		self._last_error = 0.0
	
	def __enter__(self):
		return self
		
	def __exit__(self, exc_type, exc_value, traceback):
		pass

	def update(self, error):
		PID.LOGGER.debug("Error: %f", error)
		self._integral += error
		if self._integral > self._integral_maximum:
			self._integral = self._integral_maximum
		if self._integral < self._integral_minimum:
			self._integral = self._integral_minimum
		PID.LOGGER.debug("Integral: %f", self._integral)
	
		proportional_part = self._proportional * error
		integrative_part = self._integrative * self._integral
		derivative_part = self._derivative * (error - self._last_error)
		
		control = proportional_part + integrative_part + derivative_part
		PID.LOGGER.debug("Control: %.03f + %.03f + %.03f = %.03f", proportional_part, integrative_part, derivative_part, control)
		return control

