#! /bin/bash

##########################################################
## Bash script to run on each core
## 
## @author: Wei Xu
## @affiliation: CSC@BNL
## @date create: Jun. 30, 2013
## @date last modified: Jun. 30, 2013
##########################################################

echo start of DPC.sh

PATH=$PBS_O_PATH
#./a.out < mydata.$PBS_VNODENUM

cd $PBS_O_HOME/WorkflowPrototype/Parallel_Packages/DPC

./single_dpc.py ${PBS_VNODENUM} $1 $2

echo end of DPC.sh
