#!/bin/python2.7

import argparse
import copy
import datetime
import glob
import os
import time
import signal


#datetime formats
DTFMT = '%Y-%m-%dT%H:%M:%S' # YYYY-mm-ddTHH:MM:SS datetime parse format

description = """
Monitor directories for log files and echo them to STDOUT
"""
arg_parser = argparse.ArgumentParser( description=description, 
    formatter_class=argparse.ArgumentDefaultsHelpFormatter )

arg_parser.add_argument('--glob', action='store'     
    , default='*'
    , type=str
    , help="Path (glob) of log files to echo"
    )

arg_parser.add_argument('--no-time-stamp', '-NTS', action='store_true'     
    , dest='no_time_stamp'
    , help="Suppress time-stamp output."
    )

arg_parser.add_argument('--no-file-name', '-NFN', action='store_true'     
    , dest='no_file_name'
    , help="Suppress file name in the output."
    )

args = arg_parser.parse_args()


def try_and_open(files_orig, fps_orig=[]):
    files = copy.copy(files_orig)
    fps   = copy.copy(fps_orig)
    
    for fp in fps:
        if fp.name not in files:
            fp.close()
        else:
            files.remove(fp.name)

    for file in files:
        try:
            new_fp = open(file, 'r')
            fps.append(new_fp)
        except Exception as e:
            print "Could not open {} because of {}".format(file, e)

    return fps


SIGNAL_STOP = False
def main( globstr       = '*' 
        , no_time_stamp = False
        , no_file_name  = False
        ):
    global SIGNAL_STOP
    files = filter(os.path.isfile, glob.glob(globstr))
    fps   = try_and_open(files)

    try:
        while not SIGNAL_STOP:
            now = '' if no_time_stamp else datetime.datetime.now().strftime(DTFMT)
            for fp in fps:
                for line in fp.readlines():
                    fp_name = '' if no_file_name else fp.name
                    print now,fp_name,line ,

            time.sleep(1)

            if files != filter(os.path.isfile, glob.glob(globstr)):
                files = filter(os.path.isfile, glob.glob(globstr))
                fps   = try_and_open(files)
    
        print "Closing open files."
        for fp in fps:
            fp.close()

    except KeyboardInterrupt as e:
        print "Keyboard interrupt. Closing open files."
        for fp in fps:
            fp.close()

    print "Done. Exiting"
    return

def sigterm_handler(_signo, _stack_frame):
    global SIGNAL_STOP
    print "SIGTERM detected. Attempting to stop echo_logs.py."
    SIGNAL_STOP = True
    return


if __name__=="__main__":
    signal.signal(signal.SIGTERM, sigterm_handler)
    print "Starting echo_logs.py on {}".format(args.glob)
    main( globstr       = args.glob 
        , no_time_stamp = args.no_time_stamp
        , no_file_name  = args.no_file_name
        )
    print "bye."


