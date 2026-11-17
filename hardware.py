import RPi.GPIO as GPIO
import time
import threading
import app
 
FEEDBTN, TOUCHBTN, TRIG, ECHO, WASHBTN = 8, 10, 23, 24, 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(FEEDBTN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(TOUCHBTN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(WASHBTN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(TRIG, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(ECHO, GPIO.IN)

def trigger():
    GPIO.output(TRIG, GPIO.HIGH)
    time.sleep(0.00001)
    GPIO.output(TRIG, GPIO.LOW)

def feed(channel):
    app.input_data["feedBtn"] = True

def touch(channel):
    app.input_data["touchBtn"] = True

def wash(channel):
    app.input_data["washBtn"] = True
 
GPIO.add_event_detect(FEEDBTN, GPIO.FALLING, callback=feed, bouncetime=300)
GPIO.add_event_detect(TOUCHBTN, GPIO.FALLING, callback=touch, bouncetime=300)
GPIO.add_event_detect(WASHBTN, GPIO.FALLING, callback=wash, bouncetime=300)

def get_distance_cm(timeout_s=0.03):
    trigger()
    deadline = time.monotonic() + timeout_s
    while GPIO.input(ECHO) == 0:
        if time.monotonic() > deadline:
            return None
    start = time.monotonic()
    while GPIO.input(ECHO) == 1:
        if time.monotonic() > deadline:
            return None
    end = time.monotonic()
    return (end - start) * 34300 / 2

def update(distance):
    if distance is None: return
    if distance < 10:
        app.input_data["isNear"] = True
    else:
        app.input_data["isNear"] = False

def sensor_loop():
    try:
        while True:
            distance = get_distance_cm()
            update(distance) 
            time.sleep(0.1)
    finally:
        GPIO.cleanup()

if __name__ == "__main__":
    sensor_thread = threading.Thread(target=sensor_loop, daemon=True)
    sensor_thread.start()
    app.app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=False)
