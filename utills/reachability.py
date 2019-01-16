#
#  reachability.py
#  ATOM
#
#  Created by Karthik V.
#  Updated copyright on 16/1/19 5:55 PM.
#
#  Copyright © 2019 Karthik Venkatesh. All rights reserved.
#

import socket

REMOTE_SERVER = "www.google.com"


def is_connected():
    try:
        host = socket.gethostbyname(REMOTE_SERVER)
        _ = socket.create_connection((host, 80), 2)
        return True
    except Exception as e:
        print("Reachability Exception: ", e)
        return False
