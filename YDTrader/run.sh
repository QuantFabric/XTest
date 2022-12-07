#!/bin/bash
ulimit -c unlimited
WORK_PATH=$(cd $(dirname $0); pwd)
export APP_LOG_PATH=$WORK_PATH/log
mkdir -p $APP_LOG_PATH
cd $WORK_PATH
export LD_LIBRARY_PATH=$WORK_PATH/Lib:$LD_LIBRARY_PATH
nohup $WORK_PATH/XTrader_0.8.0 -d -a 100 -f $WORK_PATH/Config/XTrader.yml -L $WORK_PATH/Lib/libYDTrader_0.2.0.so > $APP_LOG_PATH/XTrader_100_run.log 2>&1 &
echo $! > pid.txt
