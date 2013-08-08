#! usr/bin/env python

"""
    Workflow cluster manager manages clusters
    @author: Wei Xu
    @affiliation: CSC @ BNL
    @date created: May 1, 2013
    @data last modified: Jul. 8, 2013
"""

import os
import sys
import stomp
import time
import json
import random
import Image
import logging
from workflow_listener import Listener
from workflow_setting import system_log_file, result_path

class Workflow_cluster(Listener):
    def __init__(self, brokers, user='cluster', passcode='cluster', ssqueues=['/queue/cluster'], smqueue='/queue/cluster-completed'):
        """
            initialization
            @param _brokers: broker host and port
            @param _user: listener's username
            @param _passcode: listener's passcode
            @param _connection: current stomp connection
            @param _connected: connection status
            @param _subs_queues: subscribed queues
            @param _subm_queue: submit queue
            @param _listen: listen and wait controller
            """
        
        self._brokers = brokers
        self._user = user
        self._passcode = passcode
        self._connection = None
        self._connected = False
        self._subs_queues = ssqueues
        self._subm_queue = smqueue
        self._jobs_count = 0 #num of submitted jobs
        self._jobs_queue = [] #temp test purpose
        #self._jobs_dict = {} #submitted job message dictionary
    
        logging.basicConfig(filename = system_log_file, format = '%(asctime)s %(message)s', level = logging.INFO)
    
    def __del__(self):
        self.disconnect()
        #self._jobs_queue = []
        logging.info("Cluster disconnected.")
    
    def on_message(self, headers, message):
        msg = json.loads(message)
        #print "qsub", msg['job'], "for user", msg['user']
        ##index = random.randrange(0,10001) #qsub index
        self._jobs_count += 1
        ##self._jobs_dict[index] = message
        self._jobs_queue.append(message)
        comm = ''
        if msg['mode'] == 'local':
            comm = 'python '+msg['method']+' '+msg['output_data_file']+' '+msg['information']
            print comm
            os.system(comm)
        elif msg['mode'] == 'cluster':
            #comm = "qsub -l nodes=9:ppn=12 -v numnode=9,numproc=12,namephi='"+msg['output_data_file']+"',namea='a.tif',namegx='gx.tif',namegy='gy.tif' "+msg['method']
            if msg['job'] == 'DPC' or 'X8C':            
                comm = "qsub -v outfile='"+msg['output_data_file']+"' "+msg['method']
            elif msg['job'] == 'FBP':
                # use information field to put input .h5 filename
                comm = "qsub -v file='"+msg['information']+"',outfile='"+msg['output_data_file']+"' "+msg['method'] 
            print comm
            os.system(comm)

        logging.info("Run job on %s machine" % msg['mode'])

    def checkupdate(self):
        """
            check qstat to gather result
        """
        for i in range(len(self._jobs_queue)):
            msg = json.loads(self._jobs_queue[i])
            if os.path.isfile(result_path+msg['output_data_file']) is True:
                return i
                    
        return False #"/Users/weixu/Desktop/BNL/MyProjects/WorkflowPrototype/" folder)
    
    def listen_and_wait(self, waiting_period=2.0):
        if self._connected is False:
            self.connect()

        update = False
        index = ''
        message = ""
        while(self._connected and update is not True):
            time.sleep(waiting_period) #wait for on_message
            if self._jobs_count > 0:
                update = self.checkupdate()
                if update is not False:
                    index = update #the index of the queue is done
                    update = True

        return index
        
    def start(self):
        self.connect()
        
        listen = True
        while(listen):
            try:
                index = self.listen_and_wait()
                self.send(self._subm_queue, self._jobs_queue[index])
                self._jobs_count -= 1
                self._jobs_queue.pop(index) #pop the item with the index
                logging.info("complete one job")
            except KeyboardInterrupt:
                print "\nStopping"
                listen = False
            finally: #every time after try, execute finally part.
                print "Idle, start waiting"
                print "-------------------------------"

        print "Bye bye"
