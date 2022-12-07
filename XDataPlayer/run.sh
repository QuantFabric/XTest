#!/bin/bash
ulimit -c unlimited
WORK_PATH=$(cd $(dirname $0); pwd)
export APP_LOG_PATH=$WORK_PATH/log
mkdir -p $APP_LOG_PATH
sleep 2
export LD_LIBRARY_PATH=$WORK_PATH/Lib:$LD_LIBRARY_PATH
nohup $WORK_PATH/XDataPlayer_0.2.0 -d -a XDataPalyer -f $WORK_PATH/XDataPlayer.yml > $APP_LOG_PATH/run.log 2>&1 &
echo $! > pid.txt
