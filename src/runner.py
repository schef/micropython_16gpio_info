import uasyncio as asyncio
import common_pins
import common
import leds

blink_status_active = False

async def process_time_measure(timeout=20):
    print("[RUNNER]: start process_time_measure")
    timestamp = common.get_millis()
    bigest = 0
    while True:
        await asyncio.sleep(0)
        timepassed = common.millis_passed(timestamp)
        if timepassed >= timeout:
            if timepassed > bigest:
                bigest = timepassed
            print("[RUNNER]: timeout warning %d ms with bigest %d" % (timepassed, bigest))
        timestamp = common.get_millis()

def set_blink_status(active):
    global blink_status_active
    print(f"[RUNNER]: set_blink_status[{active}]")
    blink_status_active = active

async def blink_status_task():
    while True:
        last_state = leds.get_state_by_name(common_pins.ONBOARD_LED.name)
        leds.set_state_by_name(common_pins.ONBOARD_LED.name, int(not last_state))
        if blink_status_active:
            await asyncio.sleep_ms(500)
        else:
            await asyncio.sleep_ms(200)

async def main_logic_task():
    while True:

        set_blink_status(False)
        await asyncio.sleep_ms(1*30*1000)

        set_blink_status(True)
        for i in leds.leds[1:]:
            leds.set_state_by_name(i.name, 1)
            await asyncio.sleep_ms(500)
            leds.set_state_by_name(i.name, 0)
            await asyncio.sleep_ms(500)
            await asyncio.sleep_ms(29*1000)

def init():
    print("[RUNNER]: init")
    leds.init()

async def add_tasks():
    print("[RUNNER]: add_tasks")
    tasks = []
    tasks.append(asyncio.create_task(blink_status_task()))
    tasks.append(asyncio.create_task(main_logic_task()))
    tasks.append(asyncio.create_task(process_time_measure()))
    for task in tasks:
        await task
    print("[RUNNER]: Error: loop task finished!")


def run():
    print("[RUNNER]: run")
    init()
    asyncio.run(add_tasks())
