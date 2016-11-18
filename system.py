class System(object):
	def step(self):
		raise NotImplementedError

class ClosedLoop(System):
	def __init__(self, controller, element, driver, set_point = 0.0):
		self._controller = controller
		self._element = element
		self._driver = driver
		self._set_point = set_point
	
	def __enter__(self):
		return self
		
	def __exit__(self, exc_type, exc_value, traceback):
		pass

	def step(self):
		input = self._element.measure()
		error = input - self._set_point
		output = self._controller.update(error)
		self._driver.update(output)
