#!/bin/bash
ulimit -c unlimited
WORK_PATH=$(cd $(dirname $0); pwd)
export APP_LOG_PATH=$WORK_PATH/log
mkdir -p $APP_LOG_PATH
cd $WORK_PATH
export LD_LIBRARY_PATH=$WORK_PATH/Lib:$LD_LIBRARY_PATH
nohup /home/xtrader/.conda/envs/Quant/bin/python  /home/xtrader/XTest/QuantServer/quant_server_test.py  > $APP_LOG_PATH/quant_server_run_`date +%Y%m%d%H%M%S`.log 2>&1 &
echo $! > pid.txt
