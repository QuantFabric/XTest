#!/bin/bash
ulimit -c unlimited
WORK_PATH=$(cd $(dirname $0); pwd)
export APP_LOG_PATH=$WORK_PATH/log
mkdir -p $APP_LOG_PATH
cd $WORK_PATH
export LD_LIBRARY_PATH=$WORK_PATH/Lib:$LD_LIBRARY_PATH
nohup $WORK_PATH/XTrader_0.9.3 -d -a 3866259 -f $WORK_PATH/Config/XTrader.yml -L $WORK_PATH/Lib/libREMTrader_0.4.0.so > $APP_LOG_PATH/XTrader_3866259_run.log 2>&1 &
echo $! > pid.txt
