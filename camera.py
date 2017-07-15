#!/usr/bin/env python

import picamera
import time
import RPi.GPIO as GPIO
import settings

from datetime import datetime

from debounce import Debounce


def get_timestamp():
    return datetime.now().isoformat()


def get_filename(prefix='IMG', ext='jpg', output_dir=settings.PHOTO_OUTPUT_DIRECTORY):
    return '%s/%s_%s.%s' % (output_dir, prefix, get_timestamp(), ext)


@Debounce
def take_photo(pin):
    print 'take_photo'
    with picamera.PiCamera() as camera:
        print 'starting up camera'
        time.sleep(settings.CAMERA_WARMUP_TIME)  # The camera needs to warm up
        print 'capturing photo'
        filename = get_filename()
        camera.capture(filename)
        print 'captured image: %s' % filename


@Debounce
def take_video(pin):
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

    GPIO.add_event_detect(settings.CAMERA_GPIO_PIN, GPIO.RISING, take_photo, bouncetime=250)
    GPIO.add_event_detect(settings.VIDEO_GPIO_PIN, GPIO.RISING, take_video, bouncetime=250)
    print 'setup complete'


setup_button()

# This is a really hacky way to run forever
while True:
    time.sleep(1e6)
