from gpiozero import OutputDevice

devices = [OutputDevice(pin) for pin in [1, 7, 8, 24]]
