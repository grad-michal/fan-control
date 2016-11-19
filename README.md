# fan-control

Software fan control with PID controller for ODroid XU4 and Odroid C2.

This python script replaces native fan control for Odroid XU4 with software-controlled one or starts control for 
custom-built Odroid C2 fan which uses GPIO PWM as control.

Implementated controller is standard discrete PID with integration boundaries.

By default it uses zero derivative constant (which is fine for thermal control) and will try to keep average temperature
below 52°C. However, most of the constants can be changed by program arguments.

# running

For defaults run either:

```shell
./fan-control.py --device XU4
```

or

```shell
./fan-control.py --device C2
```

# Help

```shell
./fan-control.py --help
```
