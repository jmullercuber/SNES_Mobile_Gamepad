from vcontrollers import SNESController

# instantiate the device
c = SNESController()

# press and release the A button 20 times, in 0.5 second intervals
for i in range(20):
    button = 'A'
    print(button)
    c.timed_click(button, length=0.5, delay=0.5)

# clean up when done
c.destroy()
