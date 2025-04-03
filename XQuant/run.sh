#!/bin/bash
ulimit -c unlimited
WORK_PATH=$(cd $(dirname $0); pwd)
export APP_LOG_PATH=$WORK_PATH/log
mkdir -p $APP_LOG_PATH
cd $WORK_PATH
export APP_LOG_PATH=/home/Deploy/Log/`date +%Y%m%d`
export LD_LIBRARY_PATH=/home/Deploy/Lib:$LD_LIBRARY_PATH
nohup /home/Deploy/Release/XQuant_0.1.0 -d -a TestStrategy -f /home/Deploy/Config/XQuant.yml  > $APP_LOG_PATH/XQuant_run_`date +%Y%m%d%H%M%S`.log 2>&1 &
sleep 1
nohup /home/xtrader/.conda/envs/Quant/bin/python /home/xtrader/XQuant/SMAStrategy.py > $APP_LOG_PATH/XQuant_pyrun_`date +%Y%m%d%H%M%S`.log 2>&1 &
