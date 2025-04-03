import engine
import pack_message
import os
from loguru import logger
import sys
import datetime
from kline import BarData


class StrategyTest(engine.BaseEngine):
    
    def __init__(self, strategy_name:str, snapshot_interval, slice_per_sec, intervals:list, trading_sections):
        self.strategy_id = 1
        super().__init__(strategy_name=strategy_name, strategy_id=self.strategy_id, snapshot_interval=snapshot_interval, 
                            slice_per_sec=slice_per_sec, intervals=intervals, trading_sections=trading_sections)

    def update_tick(self, msg: pack_message.PackMessage):
        if msg.MessageType == pack_message.EMessageType.EFutureMarketData:
            # 策略信号
            if msg.FutureMarketData.BidVolume1 > 100 and msg.FutureMarketData.AskVolume1 < 10:
                order = pack_message.PackMessage()
                order.MessageType = pack_message.EMessageType.EOrderRequest
                order.OrderRequest.ExchangeID = msg.FutureMarketData.ExchangeID
                order.OrderRequest.Ticker = msg.FutureMarketData.Ticker
                order.OrderRequest.BusinessType = pack_message.EBusinessType.EFUTURE
                order.OrderRequest.OrderType = pack_message.EOrderType.ELIMIT
                order.OrderRequest.Price = msg.FutureMarketData.AskPrice1
                order.OrderRequest.Volume = 1
                order.OrderRequest.OrderToken = self.order_id
                self.order_id +=  1
                order.OrderRequest.Direction = pack_message.EOrderDirection.EBUY
                # order.OrderRequest.Offset = pack_message.EOrderOffset.EOPEN
                order.OrderRequest.Offset = 0
                order.OrderRequest.EngineID = self.strategy_id
                order.OrderRequest.RiskStatus = pack_message.ERiskStatusType.EPREPARE_CHECKED
                order.OrderRequest.RecvMarketTime = msg.FutureMarketData.RecvLocalTime
                order.OrderRequest.SendTime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")

                self.order_request = order
                self.new_order = True
            elif msg.FutureMarketData.AskVolume1 > 100 and msg.FutureMarketData.BidVolume1 < 10:
                order = pack_message.PackMessage()
                order.MessageType = pack_message.EMessageType.EOrderRequest
                order.OrderRequest.ExchangeID = msg.FutureMarketData.ExchangeID
                order.OrderRequest.Ticker = msg.FutureMarketData.Ticker
                order.OrderRequest.BusinessType = pack_message.EBusinessType.EFUTURE
                order.OrderRequest.OrderType = pack_message.EOrderType.ELIMIT
                order.OrderRequest.Price = msg.FutureMarketData.BidPrice1
                order.OrderRequest.Volume = 1
                order.OrderRequest.OrderToken = self.order_id
                self.order_id +=  1
                order.OrderRequest.Direction = pack_message.EOrderDirection.ESELL
                # order.OrderRequest.Offset = pack_message.EOrderOffset.EOPEN
                order.OrderRequest.Offset = 0
                order.OrderRequest.EngineID = self.strategy_id
                order.OrderRequest.RiskStatus = pack_message.ERiskStatusType.EPREPARE_CHECKED
                order.OrderRequest.RecvMarketTime = msg.FutureMarketData.RecvLocalTime
                order.OrderRequest.SendTime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")

                self.order_request = order
                self.new_order = True

    def on_window_bar(self, bar: BarData):
        logger.info(f"StrategyTest::on_window_bar ticker:{bar.ticker} {bar.interval // 60}min close:{bar.close} start_time:{bar.start_time} end_time:{bar.end_time}")



if __name__ == "__main__":
    output_path = os.path.join(os.getcwd(), 'output')
    strategy_name = "StrategyTest"
    logger.remove()
    # 输出至标准输出
    logger.add(sys.stdout, level="DEBUG")
    # 输出至日志文件
    logger.add(f"{output_path}/{strategy_name}_{datetime.datetime.now().strftime('%Y%m%d')}.log", level="DEBUG", rotation="500 MB")

    account_list = ["188795"]
    market_server_name = "MarketServer"
    order_server_name = "OrderServer"
    xwatcher_ip = "127.0.0.1"
    xwatcher_port = 8001
    snapshot_interval = 0
    slice_per_sec = 2
    intervals = [60, 300, 900, 1800]
    trading_sections = [("21:00:00", "23:30:00"), ("09:00:00", "10:15:00"), ("10:30:00", "11:30:00"), ("13:30:00", "15:00:00")]

    strategy_engine = StrategyTest(strategy_name=strategy_name, snapshot_interval=snapshot_interval, slice_per_sec=slice_per_sec, intervals=intervals, trading_sections=trading_sections)
    strategy_engine.connect_to_xwatcher(ip=xwatcher_ip, port=xwatcher_port)
    strategy_engine.init_app_status(app_name=os.path.basename(os.path.realpath(__file__)), app_log_path=output_path)
    strategy_engine.connect_to_marketserver(market_server_name=market_server_name)
    strategy_engine.connect_to_orderserver(order_server_name=order_server_name, account_list=account_list)
    strategy_engine.run()
