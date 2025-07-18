import random
import socket
import string
import subprocess
import tempfile

import requests

from . import const
from .logger import logger


def str2byte(content):
    """compile str to byte"""
    return content.encode(const.DEFAULT_CHARSET)


def download_file(target_url):
    """download file to temp path, and return its file path for further usage"""
    resp = requests.get(target_url)
    with tempfile.NamedTemporaryFile("wb+", delete=False) as f:
        file_name = f.name
        f.write(resp.content)
    return file_name


def is_port_using(port_num):
    """if port is using by others, return True. else return False"""
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(const.PORT_TIMEOUT)

    try:
        result = s.connect_ex((const.DEFAULT_HOST, port_num))
        # if port is using, return code should be 0. (can be connected)
        return result == 0
    finally:
        s.close()


def is_device_connected(device_id, adb_executor):
    """return True if device connected, else return False"""
    _ADB = adb_executor
    try:
        device_name = subprocess.check_output(
            [_ADB, "-s", device_id, "shell", "getprop", "ro.product.model"]
        )
        device_name = (
            device_name.decode(const.DEFAULT_CHARSET)
            .replace("\n", "")
            .replace("\r", "")
        )
        logger.info("device {} online".format(device_name))
    except subprocess.CalledProcessError:
        return False
    return True


def generate_random_string(length=7):
    return "".join(random.choices(string.ascii_letters + string.digits, k=length))
