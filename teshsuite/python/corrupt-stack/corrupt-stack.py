# Copyright (c) 2019-2020. The SimGrid Team. All rights reserved.
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the license (GNU LGPL) which comes with this package.

# Second failing example for bug #9 on Framagit (Python bindings crashing)
#
# An intricate recursion is used to make the crash happen.

import sys
from simgrid import *

def do_sleep1(i, len):
    if i > 0:
        this_actor.info("Iter {:d}".format(i))
        do_sleep3(i - 1, len)
        this_actor.sleep_for(len)
        this_actor.info("Mid ({:d})".format(i))
        do_sleep3(int(i / 2), len)
        this_actor.info("Done ({:d})".format(i))

def do_sleep3(i, len):
    if i > 0:
        this_actor.info("Iter {:d}".format(i))
        do_sleep5(i - 1, len)
        this_actor.sleep_for(len)
        this_actor.info("Mid ({:d})".format(i))
        do_sleep5(int(i / 2), len)
        this_actor.info("Done ({:d})".format(i))

def do_sleep5(i, len):
    if i > 0:
        this_actor.info("Iter {:d}".format(i))
        do_sleep1(i - 1, len)
        this_actor.sleep_for(len)
        this_actor.info("Mid ({:d})".format(i))
        do_sleep1(int(i / 2), len)
        this_actor.info("Done ({:d})".format(i))

def Sleeper1():
    do_sleep1(16, 1)

def Sleeper3():
    do_sleep3(6, 3)

def Sleeper5():
    do_sleep5(4, 5)

if __name__ == '__main__':
    e = Engine(sys.argv)

    e.load_platform(sys.argv[1])             # Load the platform description

    # Register the classes representing the actors
    e.register_actor("sleeper1", Sleeper1)
    e.register_actor("sleeper3", Sleeper3)
    e.register_actor("sleeper5", Sleeper5)

    e.load_deployment(sys.argv[2])

    e.run()
    this_actor.info("Finalize!")