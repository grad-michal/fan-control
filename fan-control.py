#/usr/bin/python3
import time
from controller import PID
from element import Thermometer
from driver import Fan
from system import ClosedLoop

TEMPERATURE_FILE = "/sys/devices/10060000.tmu/temp"
FAN_MODE_FILE = "/sys/devices/odroid_fan.14/fan_mode"
FAN_SPEED_FILE = "/sys/devices/odroid_fan.14/pwm_duty"
SLEEP_TIME = 1

with PID(proportional = 1.0, integrative = 0.2, derivative = 0.0) as controller:
	with Thermometer(source_path = TEMPERATURE_FILE) as element:
		with Fan(mode_path = FAN_MODE_FILE, speed_path = FAN_SPEED_FILE) as driver:
			with ClosedLoop(controller = controller, element = element, driver = driver) as system:
				while True:
					try:
						system.step()
						time.sleep(SLEEP_TIME)
					except KeyboardInterrupt:
						break
