#! /usr/bin/env python
# -*- encoding: UTF-8 -*-

"""Example: Use run Method"""

import qi
from naoqi import ALProxy
import argparse
import sys
import pdb


def main(session):
    """
    This example uses the run method.
    """
    # Get the service ALAnimationPlayer.

    animation_player_service = session.service("ALAnimationPlayer")

    # play an animation, this will return when the animation is finished
    # animation_player_service.run("animations/Stand/Gestures/Hey_1")

    # pdb.set_trace()
    # play an animation, this will return right away
    future = animation_player_service.run("animations/Stand/Gestures/No_3", _async=True)
    IP = "192.168.86.55"
    tts = ALProxy("ALTextToSpeech", IP, 9559)
    tts.say("Wrong")
    # wait the end of the animation
    future.value()

    # play an animation, this will return right away
    # future = animation_player_service.run("animations/Stand/Gestures/Hey_1", _async=True)
    # stop the animation
    # future.cancel()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", type=str, default="192.168.86.55",
                        help="Robot IP address. On robot or Local Naoqi: use '127.0.0.1'.")
    parser.add_argument("--port", type=int, default=9559,
                        help="Naoqi port number")

    args = parser.parse_args()
    session = qi.Session()
    try:
        session.connect("tcp://" + args.ip + ":" + str(args.port))
    except RuntimeError:
        print ("Can't connect to Naoqi at ip \"" + args.ip + "\" on port " + str(args.port) +".\n"
               "Please check your script arguments. Run with -h option for help.")
        sys.exit(1)
    main(session)