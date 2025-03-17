#!/bin/bash
ulimit -c unlimited
WORK_PATH=$(cd $(dirname $0); pwd)
export APP_LOG_PATH=$WORK_PATH/log
mkdir -p $APP_LOG_PATH
cd $WORK_PATH
sleep 2
export QT_QPA_PLATFORM_PLUGIN_PATH=/opt/Qt5.12.12/5.12.12/gcc_64/plugins/platforms
export LD_LIBRARY_PATH=$WORK_PATH/Lib:$LD_LIBRARY_PATH
nohup $WORK_PATH/XMonitor_0.9.2 -d -a admin -f $WORK_PATH/XMonitor.yml > $APP_LOG_PATH/run.log 2>&1 &
echo $! > pid.txt
