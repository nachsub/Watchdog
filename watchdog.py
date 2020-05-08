import datetime as dt
from time import sleep
import os
import tempfile
import time


def write_now(filep, msg):
    """Write msg to the file given by filep, forcing the msg to be written to the filesystem immediately (now).

    Without this, if you write to files, and then execute programs
    that should read them, the files will not show up in the program
    on disk.
    """
    filep.write(msg)
    filep.flush()
    # The above call to flush is not enough to write it to disk *now*;
    # according to https://stackoverflow.com/a/41506739/257924 we must
    # also call fsync:
    os.fsync(filep)


def print_now(filep, msg):
    """Call write_now with msg plus a newline."""
    write_now(filep, msg)

def deleteContent(pfile):
    pfile.seek(0)
    pfile.truncate()

file = open("watchdog.txt", "w+")
init = dt.datetime.now()
seconds_count = 30
while True:
    delta_seconds = (dt.datetime.now() - init).seconds
    if delta_seconds and delta_seconds == seconds_count:
        init = dt.datetime.now()
        print("30 seconds has passed")
        s = init.strftime('%m/%d/%Y %I:%M:%S')
        deleteContent(file)
        print_now(file, s)
    sleep(1)
file.close()
