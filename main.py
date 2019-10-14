#!/usr/bin/python3

import os

VOLUME_SCALE = os.getenv('VOLUME_SCALE', 1.5)
TIME_MARGIN  = os.getenv('TIME_MARGIN',  5)

from flask import Flask, abort, request, Response
import pychromecast, time

app = Flask(__name__)

@app.route('/<host>')
def play_mp3(host):
    try:
        c = pychromecast.Chromecast(host)
        c.wait()

    except:
        abort(404)

    mp3 = request.args.get('mp3')

    if mp3 is None:
        abort(404)

    volume = c.status.volume_level

    try:
        c.set_volume(volume * VOLUME_SCALE)

        mc = c.media_controller
        mc.play_media(mp3, 'audio/mpeg')
        mc.block_until_active()

        time.sleep(TIME_MARGIN)

        while mc.status.player_is_playing:
            time.sleep(TIME_MARGIN)

    finally:
        c.set_volume(volume)

        return Response()

if __name__ == '__main__':
    app.run('0.0.0.0', 80, True)
