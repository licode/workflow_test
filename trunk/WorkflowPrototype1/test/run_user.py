#! /usr/bin/env python

"""
    perform as user 
    example for FBP:
    $> python run_user.py xuw FBP "" "local" "output_1.png" 0 180 1
    stands for:        userID job script outputfile related parameters
    example for FFT:
    $> python run_user.py xuw FFT "" "local" "output_fft.png"
    example for DPC:
    $> python run_user.py xuw DPC "" "cluster" "phi_test.tif"
    example for Spectroscopy:
    $> python run_user.py xuw X8C "" "cluster" "fitted.tif"

"""

import time
import stomp
import sys
import json
from workflow.workflow_user import Workflow_user
from workflow.workflow_setting import brokers

if __name__ == '__main__':
    user = "test_user"
    passcode = "test_user"
    job = ""
    method = ""
    info = ""
    outfile = ""
    mode = ""

    if len(sys.argv) >= 6: #DPC
        user = str(sys.argv[1])
        passcode = str(sys.argv[1])
        job = str(sys.argv[2])
        method = str(sys.argv[3])
        mode = str(sys.argv[4])
        outfile = str(sys.argv[5])
    else:
        raise "No enough parameters!"
        exit()

    if len(sys.argv) == 9: #FBP
        info = str(sys.argv[6])+' '+str(sys.argv[7])+' '+str(sys.argv[8])

    wu = Workflow_user(brokers, user, passcode)
    message = {"instrument": "HXN",
        "job": job,
        "user": user,
        "passcode": passcode,
        "input_data_file": "",
        "output_data_file": outfile,
        "information": info,
        "method": method,
        "mode": mode
    }
    msg = json.dumps(message)
    wu.submit(msg)
