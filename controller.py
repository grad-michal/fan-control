import logging

class Controller(object):
	def update(self, error):
		raise NotImplementedError

class PID(Controller):
	LOGGER = logging.getLogger('PID')

	def __init__(self, proportional, integrative, derivative, integral_minimum = None, integral_maximum = None, minimal_control = None, force_shutdown_error = None):
		self._proportional = proportional
		self._integrative = integrative
		self._derivative = derivative

		self._force_shutdown_error = force_shutdown_error
		self._ignore_minimal_control = False
		
		if minimal_control is None:
			self._minimal_control = 0.0
		else:
			self._minimal_control = minimal_control
		
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
		
		if error > 0:
			self._ignore_minimal_control = False
		
		if not self._force_shutdown_error is None and error <= self._force_shutdown_error:
			control = 0.0
			self._ignore_minimal_control = True
			PID.LOGGER.debug("Force shutdown error reached (%.02f) and control set to 0.0", self._force_shutdown_error)					
		
		if not self._ignore_minimal_control  and control < self._minimal_control:
			control = self._minimal_control						
			PID.LOGGER.debug("Control set to minimal control: %.02f", control)					
		
		return control

