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
