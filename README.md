# QuantFabric测试系统部署
# 一、XTest简介
- XTest是QuantFabric量化交易系统的测试用例集合，可以作为QuantFabric开发和学习过程中测试使用，所使用测试环境为不同柜台厂商提供的仿真测试环境，可以直接运行。主要组件如下：
    - XServer：QuantFabric交易系统中间件，部署在用户侧、公司侧。
    - XWatcher：交易监控组件，部署在交易服务器，监控交易服务器的交易组件和交易服务器性能指标。
    - XRiskJudge：交易风控系统，提供防自成交、流速、撤单限制等风控功能。
    - XMarketCenter：行情网关，采用插件架构，通过加载不同插件适配不同柜台的行情API。
    - XTrader：交易网关，采用插件架构，通过加载不同插件适配不同柜台的交易API。
    - QuantServer：策略进程，通过内存通道读取行情数据出发交易信号，将报单、撤单请求通过内存通过发送到XTrader交易网关，并读取从XTrader交易网关返回的订单状态、仓位信息、资金信息。
    - XDataPalyer：行情数据转发组件，用于将XServer收到的行情数据分发到不能获取行情的交易服务器。
    - HFTrader：高频交易组件，将行情、交易、策略整合到一个进程，提供ns级别的系统内部延迟。


## 二、QuantFabric交易系统部署
### 1、XTest下载
- 在Linux服务器创建xtrader用户，并在xtrader主目录下执行：

```bash
git clone https://github.com/QuantFabric/XTest.git XTest
```

### 2、基础组件部署
- 启动XServer中间件：
    ```bash
    sh /home/xtrader/XTest/XServer/run.sh
    ```
- XMonitor监控客户端启动：
    ```bash
    # 打包依赖库到当前目录Lib目录下，执行一次即可
    /home/xtrader/XTest/XMonitor/DeployApp.sh XMonitor_0.9.0
    sh /home/xtrader/XTest/XMonitor/run.sh
    ```


### 3、交易组件部署
- XWatcher、XRiskJudge、XTrader、XMarketCenter为交易相关组件，需要部署在交易服务器上。
- 启动XWatcher监控组件：
    ```bash
    sudo sh /home/xtrader/XTest/XWatcher/run.sh
    ```

- 启动XRiskJudge风控系统：
    ```bash
    sh /home/xtrader/XTest/XRiskJudge/run.sh
    ```

- 启动CTP行情网关：
    ```bash
    sh /home/xtrader/XTest/CTPMarket/run.sh
    ```

- 启动CTP交易网关：
    ```bash
    sudo sh /home/xtrader/XTest/CTPTrader/run.sh
    ```

- 启动宽睿OES交易网关：
    ```bash
    sudo sh /home/xtrader/XTest/OESTrader/run.sh
    ```

- 启动盛立REM行情网关：
    ```bash
    sh /home/xtrader/XTest/REMMarket/run.sh
    ```

- 启动盛立REM交易网关：
    ```bash
    sudo sh /home/xtrader/XTest/REMTrader/tool/run.sh  # 启动盛立采集信息工具
    sudo sh /home/xtrader/XTest/REMTrader/run.sh
    ```

- 启动易达YD交易网关：
    ```bash
    sudo sh /home/xtrader/XTest/YDTrader/run.sh
    ```
- Quant虚拟环境准备：
    ```bash
    conda create -n Quant Python=3.9
    conda activate Quant
    pip3 install HPSocket -i https://pypi.tuna.tsinghua.edu.cn/simple/
    pip3 install loguru
    ```

- 启动QuantServer策略交易：
    ```bash
    sudo sh /home/xtrader/XTest/QuantServer/run.sh
    ```


### 4、高频交易组件部署
- 启动CTP HFTrader：
    ```bash
    sudo sh /home/xtrader/XTest/HFTraderCTP/run.sh
    ```

- 启动盛立REM HFTrader：
    ```bash
    sudo sh /home/xtrader/XTest/HFTraderREM/tool/run.sh  # 启动盛立采集信息工具
    sudo sh /home/xtrader/XTest/HFTraderREM/run.sh
    ```

- 启动易达YD HFTrader：
    ```bash
    sudo sh /home/xtrader/XTest/HFTraderTYD/run.sh
    ```

- 启动华鑫Tora HFTrader：
    ```bash
    sudo sh /home/xtrader/XTest/HFTraderTora/run.sh
    ```

- 启动中泰XTP HFTrader：
    ```bash
    sudo sh /home/xtrader/XTest/HFTraderXTP/run.sh
    ```


### 5、工具使用
- Capture是一个抓包工具。
- MarketReader是一个行情消费者，从行情队列读取行情数据。
- SHMClient是一个共享内存队列消费者。
- XDataPlayer行情数据转发组件，可以根据需求部署：
    ```bash
    sh /home/xtrader/XTest/XDataPlayer/run.sh
    ```