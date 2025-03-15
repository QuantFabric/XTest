from multiprocessing import Process, Queue, Manager, Event
import shm_connection
import pack_message
import time
import signal
import sys
import datetime
import os
from loguru import logger # type: ignore
from HPSocket import TcpPack
from HPSocket import helper
import HPSocket.pyhpsocket as HPSocket

class HPPackClient(TcpPack.HP_TcpPackClient):
    EventDescription = TcpPack.HP_TcpPackServer.EventDescription

    @EventDescription
    def OnSend(self, Sender, ConnID, Data):
        logger.info('[%d, OnSend] data len=%d' % (ConnID, len(Data)))

    @EventDescription
    def OnConnect(self, Sender, ConnID):
        logger.info('[%d, OnConnect] Success.' % ConnID)

    @EventDescription
    def OnReceive(self, Sender, ConnID, Data):
        logger.info('[%d, OnReceive] data len=%d' % (ConnID, len(Data)))

    def SendData(self, msg):
        self.Send(self.Client, msg)

            
def print_msg(msg):
    print(f"MessageType {msg.MessageType:#X}")
    if msg.MessageType == pack_message.EMessageType.EFutureMarketData:
        print("Colo", msg.FutureMarketData.Colo)
        print("Broker", msg.FutureMarketData.Broker)
        print("ExchangeID", msg.FutureMarketData.ExchangeID)
        print("TradingDay", msg.FutureMarketData.TradingDay)
        print("ActionDay", msg.FutureMarketData.ActionDay)
        print("UpdateTime", msg.FutureMarketData.UpdateTime)
        print("MillSec", msg.FutureMarketData.MillSec)
        print("LastPrice", msg.FutureMarketData.LastPrice)
        print("Volume", msg.FutureMarketData.Volume)
        print("Turnover", msg.FutureMarketData.Turnover)
        print("OpenPrice", msg.FutureMarketData.OpenPrice)
        print("ClosePrice", msg.FutureMarketData.ClosePrice)
        print("PreClosePrice", msg.FutureMarketData.PreClosePrice)
        print("SettlementPrice", msg.FutureMarketData.SettlementPrice)
        print("PreSettlementPrice", msg.FutureMarketData.PreSettlementPrice)
        print("OpenInterest", msg.FutureMarketData.OpenInterest)
        print("PreOpenInterest", msg.FutureMarketData.PreOpenInterest)
        print("HighestPrice", msg.FutureMarketData.HighestPrice)
        print("LowestPrice", msg.FutureMarketData.LowestPrice)
        print("UpperLimitPrice", msg.FutureMarketData.UpperLimitPrice)
        print("LowerLimitPrice", msg.FutureMarketData.LowerLimitPrice)
        print("BidPrice1", msg.FutureMarketData.BidPrice1)
        print("BidVolume1", msg.FutureMarketData.BidVolume1)
        print("AskPrice1", msg.FutureMarketData.AskPrice1)
        print("AskVolume1", msg.FutureMarketData.AskVolume1)
        print("RecvLocalTime", msg.FutureMarketData.RecvLocalTime)
        print("CurrentTime", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"))
    elif msg.MessageType == pack_message.EMessageType.EOrderStatus:
        print("Colo", msg.OrderStatus.Colo)
        print("Broker", msg.OrderStatus.Broker)
        print("Product", msg.OrderStatus.Product)
        print("Account", msg.OrderStatus.Account)
        print("Ticker", msg.OrderStatus.Ticker)
        print("ExchangeID", msg.OrderStatus.ExchangeID)
        print("BusinessType", msg.OrderStatus.BusinessType)
        print("OrderRef", msg.OrderStatus.OrderRef)
        print("OrderSysID", msg.OrderStatus.OrderSysID)
        print("OrderLocalID", msg.OrderStatus.OrderLocalID)
        print("OrderToken", msg.OrderStatus.OrderToken)
        print("EngineID", msg.OrderStatus.EngineID)
        print("UserReserved1", msg.OrderStatus.UserReserved1)
        print("UserReserved2", msg.OrderStatus.UserReserved2)
        print("OrderType", msg.OrderStatus.OrderType)
        print("OrderSide", msg.OrderStatus.OrderSide)
        print("OrderStatus", msg.OrderStatus.OrderStatus)
        print("SendPrice", msg.OrderStatus.SendPrice)
        print("SendVolume", msg.OrderStatus.SendVolume)
        print("TotalTradedVolume", msg.OrderStatus.TotalTradedVolume)
        print("TradedAvgPrice", msg.OrderStatus.TradedAvgPrice)
        print("TradedVolume", msg.OrderStatus.TradedVolume)
        print("TradedPrice", msg.OrderStatus.TradedPrice)
        print("CanceledVolume", msg.OrderStatus.CanceledVolume)
        print("Commission", msg.OrderStatus.Commission)
        print("RecvMarketTime", msg.OrderStatus.RecvMarketTime)
        print("SendTime", msg.OrderStatus.SendTime)
        print("InsertTime", msg.OrderStatus.InsertTime)
        print("BrokerACKTime", msg.OrderStatus.BrokerACKTime)
        print("ExchangeACKTime", msg.OrderStatus.ExchangeACKTime)
        print("RiskID", msg.OrderStatus.RiskID)
        print("Trader", msg.OrderStatus.Trader)
        print("ErrorID", msg.OrderStatus.ErrorID)
        print("ErrorMsg", msg.OrderStatus.ErrorMsg)
        print("UpdateTime", msg.OrderStatus.UpdateTime)
    elif msg.MessageType == pack_message.EMessageType.EAccountFund:
        print("Colo", msg.AccountFund.Colo)
        print("Broker", msg.AccountFund.Broker)
        print("Product", msg.AccountFund.Product)
        print("Account", msg.AccountFund.Account)
        print("BusinessType", msg.AccountFund.BusinessType)
        print("Deposit", msg.AccountFund.Deposit)
        print("Withdraw", msg.AccountFund.Withdraw)
        print("CurrMargin", msg.AccountFund.CurrMargin)
        print("Commission", msg.AccountFund.Commission)
        print("CloseProfit", msg.AccountFund.CloseProfit)
        print("PositionProfit", msg.AccountFund.PositionProfit)
        print("Available", msg.AccountFund.Available)
        print("WithdrawQuota", msg.AccountFund.WithdrawQuota)
        print("ExchangeMargin", msg.AccountFund.ExchangeMargin)
        print("Balance", msg.AccountFund.Balance)
        print("PreBalance", msg.AccountFund.PreBalance)
        print("UpdateTime", msg.AccountFund.UpdateTime)
    elif msg.MessageType == pack_message.EMessageType.EAccountPosition:
        print("Colo", msg.AccountPosition.Colo)
        print("Broker", msg.AccountPosition.Broker)
        print("Product", msg.AccountPosition.Product)
        print("Account", msg.AccountPosition.Account)
        print("Ticker", msg.AccountPosition.Ticker)
        print("ExchangeID", msg.AccountPosition.ExchangeID)
        print("BusinessType", msg.AccountPosition.BusinessType)
        if msg.AccountPosition.BusinessType == pack_message.EBusinessType.EFUTURE:
            print("LongTdVolume", msg.AccountPosition.FuturePosition.LongTdVolume)
            print("LongYdVolume", msg.AccountPosition.FuturePosition.LongYdVolume)
            print("LongOpenVolume", msg.AccountPosition.FuturePosition.LongOpenVolume)
            print("LongOpeningVolume", msg.AccountPosition.FuturePosition.LongOpeningVolume)
            print("LongClosingTdVolume", msg.AccountPosition.FuturePosition.LongClosingTdVolume)
            print("LongClosingYdVolume", msg.AccountPosition.FuturePosition.LongClosingYdVolume)
            print("ShortTdVolume", msg.AccountPosition.FuturePosition.ShortTdVolume)
            print("ShortYdVolume", msg.AccountPosition.FuturePosition.ShortYdVolume)
            print("ShortOpenVolume", msg.AccountPosition.FuturePosition.ShortOpenVolume)
            print("ShortOpeningVolume", msg.AccountPosition.FuturePosition.ShortOpeningVolume)
            print("ShortClosingTdVolume", msg.AccountPosition.FuturePosition.ShortClosingTdVolume)
            print("ShortClosingYdVolume", msg.AccountPosition.FuturePosition.ShortClosingYdVolume)
        elif msg.AccountPosition.BusinessType == pack_message.EBusinessType.ESTOCK:
            print("LongYdPosition", msg.AccountPosition.StockPosition.LongYdPosition)
            print("LongPosition", msg.AccountPosition.StockPosition.LongPosition)
            print("LongTdBuy", msg.AccountPosition.StockPosition.LongTdBuy)
            print("LongTdSell", msg.AccountPosition.StockPosition.LongTdSell)
            print("MarginYdPosition", msg.AccountPosition.StockPosition.MarginYdPosition)
            print("MarginPosition", msg.AccountPosition.StockPosition.MarginPosition)
            print("MarginTdBuy", msg.AccountPosition.StockPosition.MarginTdBuy)
            print("MarginTdSell", msg.AccountPosition.StockPosition.MarginTdSell)
            print("ShortYdPosition", msg.AccountPosition.StockPosition.ShortYdPosition)
            print("ShortPosition", msg.AccountPosition.StockPosition.ShortPosition)
            print("ShortTdBuy", msg.AccountPosition.StockPosition.ShortTdBuy)
            print("ShortTdSell", msg.AccountPosition.StockPosition.ShortTdSell)
            print("ShortDirectRepaid", msg.AccountPosition.StockPosition.ShortDirectRepaid)
            print("SpecialPositionAvl", msg.AccountPosition.StockPosition.SpecialPositionAvl)
           
        print("UpdateTime", msg.AccountPosition.UpdateTime)


def signal_handler(sig, frame):
    if sig == signal.SIGINT:
        logger.info("收到SIGINT信号,正在退出...")
    elif sig == signal.SIGTERM:
        logger.info("收到SIGTERM信号,正在退出...")
    
    sys.exit(0)


class QuantServer(object):
    def __init__(self, strategy_name:str):
        self.strategy_name = strategy_name
        self.program_name = ""
        self.strategy_id = 1
        self.data_connection = None
        self.hp_pack_client = None
        self.msg = pack_message.PackMessage()
        self.account_info_dict = dict()
        self.order_connection_dict = dict()

    def ConnectToXWatcher(self, ip:str, port:int):
        cmd = sys.executable + " " + " ".join(sys.argv)
        app_log_path = os.environ.get('APP_LOG_PATH')
        if app_log_path is None:
            app_log_path = "./log/"
        self.program_name = os.path.basename(os.path.realpath(__file__))
        scripts = "nohup {} > {}/{}_run_{}.log 2>&1 &".format(cmd, app_log_path, self.program_name, datetime.datetime.now().strftime('%Y%m%d%H%M%S'))
        logger.info(f"{self.program_name} start:{scripts}")
        self.hp_pack_client = HPPackClient()
        self.hp_pack_client.Start(host=ip, port=port, head_flag=0x169, size=0XFFFF)
        logger.info(f"Connect to XWatcher:{ip}:{port}")
        msg = pack_message.PackMessage()
        msg.MessageType = pack_message.EMessageType.ELoginRequest
        msg.LoginRequest.ClientType = pack_message.EClientType.EXQUANT
        msg.LoginRequest.Account = self.strategy_name
        self.hp_pack_client.SendData(msg.to_bytes())

        msg = pack_message.PackMessage()
        msg.MessageType = pack_message.EMessageType.EAppStatus
        msg.AppStatus.Colo = ""
        msg.AppStatus.Account = self.strategy_name
        msg.AppStatus.AppName = self.program_name
        msg.AppStatus.PID = os.getpid()
        msg.AppStatus.Status = "Start"
        msg.AppStatus.UsedCPURate = 0.50
        msg.AppStatus.UsedMemSize = 500.0
        msg.AppStatus.StartTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
        msg.AppStatus.LastStartTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
        msg.AppStatus.APIVersion = "1.0"
        msg.AppStatus.StartScript = scripts
        msg.AppStatus.UpdateTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
        self.hp_pack_client.SendData(msg.to_bytes())

    def ConnectToMarketServer(self, market_server_name:str):
        # 连接MarketServer
        self.data_connection = shm_connection.SHMDataConnection(self.strategy_name)
        self.data_connection.Start(market_server_name)
        logger.info(f"{self.strategy_name} Connect to MarketServer:{market_server_name}")

    def ConnectToOrderServer(self, order_server_name:str, account_list:list):
        # 连接XTrader
        for account in account_list:
            order_connection = shm_connection.SHMConnection(account)
            self.order_connection_dict[account] = order_connection
            order_connection.Start(order_server_name + account)
            logger.info(f"{account} Connect to XTrader:{order_server_name + account}")
            
    def Run(self):
        # 发送EventLog
        msg = pack_message.PackMessage()
        msg.MessageType = pack_message.EMessageType.EEventLog
        msg.EventLog.Colo = ""
        msg.EventLog.Account = self.strategy_name
        msg.EventLog.App = self.program_name
        msg.EventLog.Event = f"{self.strategy_name} Start, accounts:{','.join(self.order_connection_dict.keys())}"
        msg.EventLog.Level = pack_message.EEventLogLevel.EINFO
        msg.EventLog.UpdateTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
        self.hp_pack_client.SendData(msg.to_bytes())
        
        order_id = 1
        while True:
            # 收取行情数据
            self.data_connection.HandleMsg()
            ret = self.data_connection.Pop(self.msg)
            if ret and self.msg.MessageType == pack_message.EMessageType.EFutureMarketData:
                logger.info(f"recv market data Ticker:{self.msg.FutureMarketData.Ticker} LastPrice:{self.msg.FutureMarketData.LastPrice}")
                # print_msg(self.msg)
                # 策略信号
                if self.msg.FutureMarketData.BidVolume1 > 100 and self.msg.FutureMarketData.AskVolume1 < 10:
                    order = pack_message.PackMessage()
                    order.MessageType = pack_message.EMessageType.EOrderRequest
                    order.OrderRequest.ExchangeID = self.msg.FutureMarketData.ExchangeID
                    order.OrderRequest.Ticker = self.msg.FutureMarketData.Ticker
                    order.OrderRequest.BusinessType = pack_message.EBusinessType.EFUTURE
                    order.OrderRequest.OrderType = pack_message.EOrderType.ELIMIT
                    order.OrderRequest.Price = self.msg.FutureMarketData.AskPrice1
                    order.OrderRequest.Volume = 1
                    order.OrderRequest.OrderToken = order_id
                    order_id += 1
                    order.OrderRequest.Direction = pack_message.EOrderDirection.EBUY
                    # order.OrderRequest.Offset = pack_message.EOrderOffset.EOPEN
                    order.OrderRequest.Offset = 0
                    order.OrderRequest.EngineID = self.strategy_id
                    order.OrderRequest.RiskStatus = pack_message.ERiskStatusType.EPREPARE_CHECKED
                    order.OrderRequest.RecvMarketTime = self.msg.FutureMarketData.RecvLocalTime
                    order.OrderRequest.SendTime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
                    for account, order_connection in self.order_connection_dict.items():
                        order.OrderRequest.Account = account
                        order_connection.Push(order)
                        order_connection.HandleMsg()  # 发送订单到XTrader
                        logger.info(f"send buy order to {account} ChannelID:{order.ChannelID} {order.OrderRequest.Ticker} price:{order.OrderRequest.Price} orderid:{order.OrderRequest.OrderToken} Direction:{order.OrderRequest.Direction} Offset:{order.OrderRequest.Offset}")
                elif self.msg.FutureMarketData.AskVolume1 > 100 and self.msg.FutureMarketData.BidVolume1 < 10:
                    order = pack_message.PackMessage()
                    order.MessageType = pack_message.EMessageType.EOrderRequest
                    order.OrderRequest.ExchangeID = self.msg.FutureMarketData.ExchangeID
                    order.OrderRequest.Ticker = self.msg.FutureMarketData.Ticker
                    order.OrderRequest.BusinessType = pack_message.EBusinessType.EFUTURE
                    order.OrderRequest.OrderType = pack_message.EOrderType.ELIMIT
                    order.OrderRequest.Price = self.msg.FutureMarketData.BidPrice1
                    order.OrderRequest.Volume = 1
                    order.OrderRequest.OrderToken = order_id
                    order_id += 1
                    order.OrderRequest.Direction = pack_message.EOrderDirection.ESELL
                    # order.OrderRequest.Offset = pack_message.EOrderOffset.EOPEN
                    order.OrderRequest.Offset = 0
                    order.OrderRequest.EngineID = self.strategy_id
                    order.OrderRequest.RiskStatus = pack_message.ERiskStatusType.EPREPARE_CHECKED
                    order.OrderRequest.RecvMarketTime = self.msg.FutureMarketData.RecvLocalTime
                    order.OrderRequest.SendTime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
                    for account, order_connection in self.order_connection_dict.items():
                        order.OrderRequest.Account = account
                        order_connection.Push(order)
                        order_connection.HandleMsg() # 发送订单到XTrader
                        logger.info(f"send sell order to {account} ChannelID:{order.ChannelID} {order.OrderRequest.Ticker} price:{order.OrderRequest.Price} orderid:{order.OrderRequest.OrderToken} Direction:{order.OrderRequest.Direction} Offset:{order.OrderRequest.Offset}")

            # 回报数据处理
            for account, order_connection in self.order_connection_dict.items():
                while True:
                    # 收取交易回报信息
                    order_connection.HandleMsg()
                    ret = order_connection.Pop(self.msg)
                    if ret:
                        print_msg(self.msg)
                        if self.msg.MessageType == pack_message.EMessageType.EAccountFund:
                            account_info_dict = dict()
                            account_info_dict["Colo"] = self.msg.AccountFund.Colo
                            account_info_dict["Broker"] = self.msg.AccountFund.Broker
                            account_info_dict["Product"] = self.msg.AccountFund.Product
                            account_info_dict["Account"] = self.msg.AccountFund.Account
                            account_info_dict["ChannelID"] = self.msg.ChannelID
                            self.account_info_dict[self.msg.AccountFund.Account] = account_info_dict
                        elif self.msg.MessageType == pack_message.EMessageType.EAccountPosition:
                            account_info_dict = dict()
                            account_info_dict["Colo"] = self.msg.AccountPosition.Colo
                            account_info_dict["Broker"] = self.msg.AccountPosition.Broker
                            account_info_dict["Product"] = self.msg.AccountPosition.Product
                            account_info_dict["Account"] = self.msg.AccountPosition.Account
                            account_info_dict["ChannelID"] = self.msg.ChannelID
                            self.account_info_dict[self.msg.AccountPosition.Account] = account_info_dict
                        elif self.msg.MessageType == pack_message.EMessageType.EOrderStatus:
                            pass
                    else:
                        break
            
            # 定义目标时间
            target_time = datetime.time(15, 30, 0)  # 15:30:00
            # 获取当前时间
            now = datetime.datetime.now().time()  # 获取当前时间部分
            # 比较时间
            if now > target_time:
                logger.info(f"当前时间:{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}，已经收盘，退出程序")
                break
        sys.stdout.flush()


if __name__ == "__main__":
    output_path = os.path.join(os.getcwd(), 'output')
    strategy_name = "SMAStrategy"
    logger.remove()
    # 输出至标准输出
    logger.add(sys.stdout, level="DEBUG")
    # 输出至日志文件
    logger.add(f"{output_path}/{strategy_name}_{datetime.datetime.now().strftime('%Y%m%d')}.log", level="DEBUG", rotation="500 MB")
    
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    account_list = ["188795"]
    market_server_name = "MarketServer"
    order_server_name = "OrderServer"
    server = QuantServer(strategy_name=strategy_name)
    server.ConnectToXWatcher(ip="127.0.0.1", port=8001)
    server.ConnectToMarketServer(market_server_name=market_server_name)
    server.ConnectToOrderServer(order_server_name=order_server_name, account_list=account_list)
    server.Run()
