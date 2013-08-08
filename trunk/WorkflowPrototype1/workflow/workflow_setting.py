#! usr/bin/ python
"""
    workflow system setting file
    @author: Wei Xu
    @affiliation: CSC @ BNL
    @date created: May 1, 2013
    @data last modified: Jul. 8, 2013
"""

home_path = '/kbase/home/wxu/WorkflowPrototype/'

brokers = [('localhost', 61613)]

module_dict = {
    'FBP':home_path+'Packages/Tomo/FBP.py',
    'FFT':home_path+'Packages/Basic/FFT.py',
    'DPC':home_path+'Packages/DPC/DPC.py',
    'X8C':home_path+'Packages/X8C/X8C.py'
}

cluster_module_dict = {
    'FBP':home_path+'Parallel_Packages/Tomo/fbp_mpi.pbs',
    'DPC':home_path+'Parallel_Packages/DPC/dpc_mpi.pbs',
    'X8C':home_path+'Parallel_Packages/X8C/x8c_mpi.pbs'
}

data_path = home_path+'Data/'
result_path = home_path+'Results/'

message_format = {
    "instrument": "HXN",
    "job": "", #FBP, FFT
    "user": "", #user name
    "passcode": "", #user passcode
    "input_data_file": "filename.png", #input filename
    "output_data_file": "ofilename.png", #output filename
    "information": "info msg",
    "method": "", #empty string means use system module instead of self-defined module
    "mode": "local" #processing mode: local vs. cluster
}

system_log_file = 'workflow_manager.log'
