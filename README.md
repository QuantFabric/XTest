# QuantFabric测试系统部署

- 在Linux服务器创建xtrader用户，并在xtrader主目录下执行：

```bash
git clone https://github.com/QuantFabric/XTest.git Test
```

- 按顺序启动XServer、XWatcher、XRiskJudge、XMarketCenter、XTrader等组件。

```bash
sh /home/xtrader/Test/XServer/run.sh
sudo sh /home/xtrader/Test/XWatcher/run.sh
sh /home/xtrader/Test/XRiskJudge/run.sh
sh /home/xtrader/Test/CTPMarket/run.sh
sudo sh /home/xtrader/Test/CTPTrader/run.sh
# 可以进入相应组件目录后执行run.sh
# 关闭相应组件时执行stop.sh
```

- XMonitor监控客户端启动：

```bash
# 打包依赖库到当前目录Lib目录下，执行一次即可
/home/xtrader/Test/XMonitor/DeployApp.sh XMonitor_0.9.0
sh /home/xtrader/Test/XMonitor/run.sh
```

