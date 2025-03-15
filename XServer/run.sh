#!/bin/bash
ulimit -c unlimited
WORK_PATH=$(cd $(dirname $0); pwd)
export APP_LOG_PATH=$WORK_PATH/log
mkdir -p $APP_LOG_PATH
mkdir -p $WORK_PATH/Bin
cd $WORK_PATH
sleep 2
export LD_LIBRARY_PATH=$WORK_PATH/Lib:$LD_LIBRARY_PATH
nohup $WORK_PATH/XServer_0.9.0 -d -a XServer -f $WORK_PATH/XServer.yml > $APP_LOG_PATH/XServer_1.0.0_run.log 2>&1 &
echo $! > pid.txt
