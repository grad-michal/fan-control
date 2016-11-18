class Controller(object):
	def update(self, error):
		raise NotImplementedError

class PID(Controller):
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
		print("Error: ", error)
		self._integral += error
		if self._integral > self._integral_maximum:
			self._integral = self._integral_maximum
		if self._integral < self._integral_minimum:
			self._integral = self._integral_minimum
		print("Integral: ", self._integral)
	
		proportional_part = self._proportional * error
		integrative_part = self._integrative * self._integral
		derivative_part = self._derivative * (error - self._last_error)
		
		print("PID: ", proportional_part, integrative_part, derivative_part)
		print("Control: ", proportional_part + integrative_part + derivative_part)
		return proportional_part + integrative_part + derivative_part

