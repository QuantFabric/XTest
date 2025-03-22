import engine
import pack_message
import os
from loguru import logger
import sys
import datetime



class StrategyTest(engine.BaseEngine):
    
    def __init__(self, strategy_name:str):
        self.strategy_id = 2
        super().__init__(strategy_name, self.strategy_id)


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
                for account, order_connection in self.order_connection_dict.items():
                    order.OrderRequest.Account = account
                    order_connection.Push(order)
                    order_connection.HandleMsg()  # 发送订单到XTrader
                    logger.info(f"send buy order to {account} ChannelID:{order.ChannelID} {order.OrderRequest.Ticker} price:{order.OrderRequest.Price} orderid:{order.OrderRequest.OrderToken} Direction:{order.OrderRequest.Direction} Offset:{order.OrderRequest.Offset}")
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
                for account, order_connection in self.order_connection_dict.items():
                    order.OrderRequest.Account = account
                    order_connection.Push(order)
                    order_connection.HandleMsg() # 发送订单到XTrader
                    logger.info(f"send sell order to {account} ChannelID:{order.ChannelID} {order.OrderRequest.Ticker} price:{order.OrderRequest.Price} orderid:{order.OrderRequest.OrderToken} Direction:{order.OrderRequest.Direction} Offset:{order.OrderRequest.Offset}")




if __name__ == "__main__":
    output_path = os.path.join(os.getcwd(), 'output')
    strategy_name = "StrategyTest"
    logger.remove()
    # 输出至标准输出
    logger.add(sys.stdout, level="DEBUG")
    # 输出至日志文件
    logger.add(f"{output_path}/{strategy_name}_{datetime.datetime.now().strftime('%Y%m%d')}.log", level="DEBUG", rotation="500 MB")

    account_list = ["188795", "237477"]
    market_server_name = "MarketServer"
    order_server_name = "OrderServer"
    xwatcher_ip = "192.168.1.168"
    xwatcher_port = 8001

    strategy_engine = StrategyTest(strategy_name=strategy_name)
    strategy_engine.connect_to_xwatcher(ip=xwatcher_ip, port=xwatcher_port)
    strategy_engine.init_app_status(app_name=os.path.basename(os.path.realpath(__file__)), app_log_path=output_path)
    strategy_engine.connect_to_marketserver(market_server_name=market_server_name)
    strategy_engine.connect_to_orderserver(order_server_name=order_server_name, account_list=account_list)
    strategy_engine.run()
