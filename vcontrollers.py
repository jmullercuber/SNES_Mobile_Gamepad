import time
import uinput

# general class to represent gamepads and video game controllers
class Controller(uinput.Device):
    # class variable to count number of instances
    n = 0

    # mapping from button names to uinput event values
    # empty gamepad
    btn_map = {}

    valid_btns = btn_map.keys()

    # constructor function
    def __init__(self, name, id):
        # events our controller can generate
        events = self.btn_map.values()
        # set up device and initialize
        uinput.Device.__init__(self, events, name=name+' '+str(id))
        # set controller id and increment counter
        self.id = id
        Controller.n += 1

    def press_button(self, btn):
        # if this isn't a valid button, don't press it
        if not btn in self.valid_btns:
            return False
        self.emit(self.btn_map[btn], 1)
        return True

    def release_button(self, btn):
        if not btn in self.valid_btns:
            return False
        self.emit(self.btn_map[btn], 0)
        return True

    def click_button(self, btn):
        if not btn in self.valid_btns:
            return False
        self.emit_click(self.btn_map[btn])
        return True

    def timed_click(self, btn, length, delay=0):
        ''' Times are in seconds '''
        time.sleep(delay)
        self.press_button(btn)
        time.sleep(length)
        self.release_button(btn)

    def combo(self, btns):
        for b,v in btns.items():
            if b in self.valid_btns:
                self.emit(self.btn_map[b], int(v), syn=False)
        self.syn()

#
class SNESController(Controller):
    # override class variable to count number of instances
    # counting SNESControllers specifically
    n = 0

    # mapping from button names to uinput event values
    # A,B,X,Y, L,R, START,SELECT, UP,DOWN,LEFT,RIGHT
    btn_map = {
        'A':    uinput.BTN_A,
        'B':    uinput.BTN_B,
        'X':    uinput.BTN_X,
        'Y':    uinput.BTN_Y,
        'L':    uinput.BTN_TL,
        'R':    uinput.BTN_TR,
        'START':    uinput.BTN_START,
        'SELECT':   uinput.BTN_SELECT,
        'UP':       uinput.BTN_DPAD_UP,
        'DOWN':     uinput.BTN_DPAD_DOWN,
        'LEFT':     uinput.BTN_DPAD_LEFT,
        'RIGHT':    uinput.BTN_DPAD_RIGHT,
    }

    valid_btns = btn_map.keys()

    # constructor function
    def __init__(self):
        # inherit some stuff
        Controller.__init__(self, 'Custom SNES Controller', SNESController.n)
        # controller counter
        SNESController.n += 1

class LameController(Controller):
    # it's lame because it's got no buttons
    def __init__(self):
        # inherit some stuff
        Controller.__init__(self, 'Lame Controller', Controller.n)
