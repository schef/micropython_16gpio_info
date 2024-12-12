import time
import common
import common_pins

leds = []

led_pins = [
    common_pins.ONBOARD_LED,
    common_pins.B_LED1,
    common_pins.B_LED2,
    common_pins.B_LED3,
    common_pins.B_LED4,
    common_pins.B_LED5,
    common_pins.B_LED6,
    #common_pins.B_LED7,
    #common_pins.B_LED8,
    #common_pins.B_LED9,
    #common_pins.B_LED10,
    #common_pins.B_LED11,
    #common_pins.B_LED12,
    #common_pins.B_LED13,
    #common_pins.B_LED14,
    #common_pins.B_LED15,
    #common_pins.B_LED16,
]

class Led:
    def __init__(self, id, name, active_high=False):
        self.output = common.create_output(id)
        self.active_high = active_high
        self.state = None
        self.set_state(0)
        self.name = name

    def set_state(self, state):
        if self.active_high:
            if state:
                self.output.off()
            else:
                self.output.on()
        else:
            if state:
                self.output.on()
            else:
                self.output.off()
        self.state = state

def set_state_by_name(name, state):
    print("[LEDS]: set_state_by_name(%s, %s)" % (name, state))
    for led in leds:
        if led.name == name:
            led.set_state(state)

def get_state_by_name(name):
    for led in leds:
        if led.name == name:
            return led.state
    return None

def test_leds():
    global leds
    leds = []
    init_leds()
    for led in leds:
        print("[LEDS]: testing %s" % (led.name))
        led.set_state(1)
        time.sleep_ms(1000)
        led.set_state(0)
        time.sleep_ms(1000)

def init_leds():
    for pin in led_pins:
        leds.append(Led(pin.id, pin.name))

def init():
    print("[LEDS]: init")
    init_leds()
