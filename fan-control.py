#!/usr/bin/python3

import time
import argparse
import logging
import logging.handlers

from controller import PID
from element import Thermometer
from driver import Fan
from system import ClosedLoop

parser = argparse.ArgumentParser()
parser.add_argument('-T', '--update-delay', dest='update_delay', 
	help='Update delay in seconds', type=int, default = 1)
parser.add_argument('-p', '--proportional', dest='proportional', 
	help='Proportional constant', type=float, default = 1.0)
parser.add_argument('-i', '--integrative', dest='integrative', 
	help='Integrative constant', type=float, default = 0.2)
parser.add_argument('-d', '--derivative', dest='derivative', 
	help='Derivative constant', type=float, default = 0.0)
parser.add_argument('-l', '--minimal', dest='minimal_temperature', 
	help='Temperature with maximal control (with P = 1)', type=float, default = 52.0)
parser.add_argument('-u', '--maximal', dest='maximal_temperature', 
	help='Temperature with zero control', type=float, default = 75.0)
parser.add_argument('--integral-minimum', dest='integral_minimum', 
	help='Integral component minimum internal value', type=float)
parser.add_argument('--integral-maximum', dest='integral_maximum', 
	help='Integral component maximum internal value', type=float)

verbosity_group = parser.add_mutually_exclusive_group()
verbosity_group.add_argument('-v', '--verbose', dest='verbose',
	help='Print control state', action='store_true')
verbosity_group.add_argument('-q', '--quiet', dest='quiet',
	help='Print only warnings', action='store_true')

parser.add_argument('--syslog', dest='syslog',
	help='Use syslog for logging', action='store_true')
args = parser.parse_args()

TEMPERATURE_FILE = "/sys/devices/10060000.tmu/temp"
FAN_MODE_FILE = "/sys/devices/odroid_fan.14/fan_mode"
FAN_SPEED_FILE = "/sys/devices/odroid_fan.14/pwm_duty"

root_logger = logging.getLogger()
if args.quiet:
	root_logger.setLevel(logging.WARNING)
elif args.verbose:
	root_logger.setLevel(logging.DEBUG)
else:
	root_logger.setLevel(logging.INFO)

if args.syslog:
	root_logger.addHandler(logging.handlers.SysLogHandler())
else:
	root_logger.addHandler(logging.StreamHandler())

with PID(proportional = args.proportional, integrative = args.integrative, derivative = args.derivative,
			integral_minimum = args.integral_minimum, integral_maximum = args.integral_maximum) as controller:
	with Thermometer(source_path = TEMPERATURE_FILE, minimal = args.minimal_temperature, maximal = args.maximal_temperature) as element:
		with Fan(mode_path = FAN_MODE_FILE, speed_path = FAN_SPEED_FILE) as driver:
			with ClosedLoop(controller = controller, element = element, driver = driver) as system:
				while True:
					try:
						system.step()
						time.sleep(args.update_delay)
					except KeyboardInterrupt:
						break

logging.shutdown()

