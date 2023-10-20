#!/bin/bash
ulimit -c unlimited
WORK_PATH=$(cd $(dirname $0); pwd)
export APP_LOG_PATH=$WORK_PATH/log
mkdir -p $APP_LOG_PATH
cd $WORK_PATH
export LD_LIBRARY_PATH=$WORK_PATH/Lib:$LD_LIBRARY_PATH
#nohup  $WORK_PATH/HFTrader_0.6.7 -d -a 215010093 -f $WORK_PATH/Config/HFTrader215010093.yml > $APP_LOG_PATH/run.log 2>&1 &
nohup  $WORK_PATH/HFTrader_0.6.7 -d -a 53392900673 -f $WORK_PATH/Config/HFTrader53392900673.yml > $APP_LOG_PATH/run.log 2>&1 &
echo $! > pid.txt
