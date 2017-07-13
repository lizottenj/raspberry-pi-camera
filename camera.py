import picamera
import time
import RPi.GPIO as GPIO
import settings

from datetime import datetime


def get_timestamp():
    return datetime.now().isoformat()


def get_filename(prefix='IMG', ext='jpg', output_dir=settings.PHOTO_OUTPUT_DIRECTORY):
    return '%s/%s_%s.%s' % (output_dir, prefix, get_timestamp(), ext)


def take_photo():
    print 'take_photo'
    with picamera.PiCamera() as camera:
        print 'starting up camera'
        time.sleep(settings.CAMERA_WARMUP_TIME)  # The camera needs to warm up
        print 'capturing photo'
        filename = get_filename()
        camera.capture(filename)
        print 'captured image: %s' % filename


def take_video():
    print 'take_video'
    with picamera.PiCamera() as camera:
        print 'starting up camera'
        time.sleep(settings.CAMERA_WARMUP_TIME)  # The camera needs to warm up
        print 'capturing video'
        filename = get_filename(prefix='VID', ext='h264', output_dir=settings.VIDEO_OUTPUT_DIRECTORY)
        camera.start_recording(filename)
        camera.wait_recording(settings.VIDEO_RECORDING_TIME)
        camera.stop_recording()
        print 'captured video: %s' % filename


def setup_button():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(settings.CAMERA_GPIO_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(settings.VIDEO_GPIO_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    print 'setup complete'


setup_button()

while True:
    camera_input_state = GPIO.input(settings.CAMERA_GPIO_PIN)
    video_input_state = GPIO.input(settings.VIDEO_GPIO_PIN)

    if not camera_input_state:
        take_photo()
    elif not video_input_state:
        take_video()

    time.sleep(.2)

