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



def print_msg(func:str, msg):
    logger.debug(f"{func} MessageType {msg.MessageType:#X}")
    if msg.MessageType == pack_message.EMessageType.EFutureMarketData:
        logger.debug("Colo:{} Broker:{} ExchangeID:{} TradingDay:{} ActionDay:{} UpdateTime:{} MillSec:{} LastPrice:{} "
                     "Volume:{} Turnover:{} OpenPrice:{} ClosePrice:{} PreClosePrice:{} SettlementPrice:{} PreSettlementPrice:{} "
                     "OpenInterest:{} PreOpenInterest:{} HighestPrice:{} LowestPrice:{} UpperLimitPrice:{} LowerLimitPrice:{} "
                     "BidPrice1:{} BidVolume1:{} AskPrice1:{} AskVolume1:{} RecvLocalTime:{} CurrentTime:{}", 
                    msg.FutureMarketData.Colo, msg.FutureMarketData.Broker, msg.FutureMarketData.ExchangeID, msg.FutureMarketData.TradingDay, 
                    msg.FutureMarketData.ActionDay, msg.FutureMarketData.UpdateTime, msg.FutureMarketData.MillSec, msg.FutureMarketData.LastPrice,
                    msg.FutureMarketData.Volume, msg.FutureMarketData.Turnover, msg.FutureMarketData.OpenPrice, msg.FutureMarketData.ClosePrice,
                    msg.FutureMarketData.PreClosePrice, msg.FutureMarketData.SettlementPrice, msg.FutureMarketData.PreSettlementPrice,
                    msg.FutureMarketData.OpenInterest, msg.FutureMarketData.PreOpenInterest, msg.FutureMarketData.HighestPrice, 
                    msg.FutureMarketData.LowestPrice, msg.FutureMarketData.UpperLimitPrice, msg.FutureMarketData.LowerLimitPrice,
                    msg.FutureMarketData.BidPrice1, msg.FutureMarketData.BidVolume1, msg.FutureMarketData.AskPrice1, 
                    msg.FutureMarketData.AskVolume1, msg.FutureMarketData.RecvLocalTime, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"))
    elif msg.MessageType == pack_message.EMessageType.EOrderStatus:
        logger.debug("Colo:{} Broker:{} Product:{} Account:{} Ticker:{} ExchangeID:{} BusinessType:{} OrderRef:{} "
                     "OrderSysID:{} OrderLocalID:{} OrderToken:{} EngineID:{} UserReserved1:{} UserReserved2:{} "
                     "OrderType:{} OrderSide:{} OrderStatus:{} SendPrice:{} SendVolume:{} TotalTradedVolume:{} "
                     "TradedAvgPrice:{} TradedVolume:{} TradedPrice:{} CanceledVolume:{} Commission:{} RecvMarketTime:{} "
                     "SendTime:{} InsertTime:{} BrokerACKTime:{} ExchangeACKTime:{} RiskID:{} Trader:{} ErrorID:{} "
                     "ErrorMsg:{} UpdateTime:{}", 
                    msg.OrderStatus.Colo, msg.OrderStatus.Broker, msg.OrderStatus.Product, msg.OrderStatus.Account,
                    msg.OrderStatus.Ticker, msg.OrderStatus.ExchangeID, msg.OrderStatus.BusinessType, msg.OrderStatus.OrderRef,
                    msg.OrderStatus.OrderSysID, msg.OrderStatus.OrderLocalID, msg.OrderStatus.OrderToken, msg.OrderStatus.EngineID,
                    msg.OrderStatus.UserReserved1, msg.OrderStatus.UserReserved2, msg.OrderStatus.OrderType, msg.OrderStatus.OrderSide,
                    msg.OrderStatus.OrderStatus, msg.OrderStatus.SendPrice, msg.OrderStatus.SendVolume, msg.OrderStatus.TotalTradedVolume,
                    msg.OrderStatus.TradedAvgPrice, msg.OrderStatus.TradedVolume, msg.OrderStatus.TradedPrice, msg.OrderStatus.CanceledVolume,
                    msg.OrderStatus.Commission, msg.OrderStatus.RecvMarketTime, msg.OrderStatus.SendTime, msg.OrderStatus.InsertTime,
                    msg.OrderStatus.BrokerACKTime, msg.OrderStatus.ExchangeACKTime, msg.OrderStatus.RiskID, msg.OrderStatus.Trader,
                    msg.OrderStatus.ErrorID, msg.OrderStatus.ErrorMsg, msg.OrderStatus.UpdateTime)
    elif msg.MessageType == pack_message.EMessageType.EAccountFund:
        logger.debug("Colo:{} Broker:{} Product:{} Account:{} BusinessType:{} Deposit:{} Withdraw:{} CurrMargin:{} "
                     "Commission:{} CloseProfit:{} PositionProfit:{} Available:{} WithdrawQuota:{} ExchangeMargin:{} "
                     "Balance:{} PreBalance:{} UpdateTime:{}", 
                    msg.AccountFund.Colo, msg.AccountFund.Broker, msg.AccountFund.Product, msg.AccountFund.Account,
                    msg.AccountFund.BusinessType, msg.AccountFund.Deposit, msg.AccountFund.Withdraw, msg.AccountFund.CurrMargin,
                    msg.AccountFund.Commission, msg.AccountFund.CloseProfit, msg.AccountFund.PositionProfit, 
                    msg.AccountFund.Available, msg.AccountFund.WithdrawQuota, msg.AccountFund.ExchangeMargin,
                    msg.AccountFund.Balance, msg.AccountFund.PreBalance, msg.AccountFund.UpdateTime)
    elif msg.MessageType == pack_message.EMessageType.EAccountPosition:
        if msg.AccountPosition.BusinessType == pack_message.EBusinessType.EFUTURE:
            logger.debug("Colo:{} Broker:{} Product:{} Account:{} Ticker:{} ExchangeID:{} BusinessType:{} "
                        "LongTdVolume:{} LongYdVolume:{} LongOpenVolume:{} LongOpeningVolume:{} "
                        "LongClosingTdVolume:{} LongClosingYdVolume:{} ShortTdVolume:{} ShortYdVolume:{} "
                        "ShortOpenVolume:{} ShortOpeningVolume:{} ShortClosingTdVolume:{} "
                        "ShortClosingYdVolume:{} UpdateTime:{}", 
                        msg.AccountPosition.Colo, msg.AccountPosition.Broker, msg.AccountPosition.Product, 
                        msg.AccountPosition.Account, msg.AccountPosition.Ticker, msg.AccountPosition.ExchangeID,
                        msg.AccountPosition.BusinessType, msg.AccountPosition.FuturePosition.LongTdVolume,
                        msg.AccountPosition.FuturePosition.LongYdVolume, msg.AccountPosition.FuturePosition.LongOpenVolume,
                        msg.AccountPosition.FuturePosition.LongOpeningVolume, msg.AccountPosition.FuturePosition.LongClosingTdVolume,
                        msg.AccountPosition.FuturePosition.LongClosingYdVolume, msg.AccountPosition.FuturePosition.ShortTdVolume,
                        msg.AccountPosition.FuturePosition.ShortYdVolume, msg.AccountPosition.FuturePosition.ShortOpenVolume,
                        msg.AccountPosition.FuturePosition.ShortOpeningVolume, msg.AccountPosition.FuturePosition.ShortClosingTdVolume,
                        msg.AccountPosition.FuturePosition.ShortClosingYdVolume, msg.AccountPosition.UpdateTime)
        elif msg.AccountPosition.BusinessType == pack_message.EBusinessType.ESTOCK:
            logger.debug("Colo:{} Broker:{} Product:{} Account:{} Ticker:{} ExchangeID:{} BusinessType:{} "
                        "LongYdPosition:{} LongPosition:{} LongTdBuy:{} LongTdSell:{} "
                        "MarginYdPosition:{} MarginPosition:{} MarginTdBuy:{} MarginTdSell:{} "
                        "ShortYdPosition:{} ShortPosition:{} ShortTdBuy:{} ShortTdSell:{} "
                        "ShortDirectRepaid:{} SpecialPositionAvl:{} UpdateTime:{}", 
                        msg.AccountPosition.Colo, msg.AccountPosition.Broker, msg.AccountPosition.Product, 
                        msg.AccountPosition.Account, msg.AccountPosition.Ticker, msg.AccountPosition.ExchangeID,
                        msg.AccountPosition.BusinessType, msg.AccountPosition.StockPosition.LongYdPosition, 
                        msg.AccountPosition.StockPosition.LongPosition, msg.AccountPosition.StockPosition.LongTdBuy,
                        msg.AccountPosition.StockPosition.LongTdSell, msg.AccountPosition.StockPosition.MarginYdPosition,
                        msg.AccountPosition.StockPosition.MarginPosition, msg.AccountPosition.StockPosition.MarginTdBuy,
                        msg.AccountPosition.StockPosition.MarginTdSell, msg.AccountPosition.StockPosition.ShortYdPosition,
                        msg.AccountPosition.StockPosition.ShortPosition, msg.AccountPosition.StockPosition.ShortTdBuy,
                        msg.AccountPosition.StockPosition.ShortTdSell, msg.AccountPosition.StockPosition.ShortDirectRepaid,
                        msg.AccountPosition.StockPosition.SpecialPositionAvl, msg.AccountPosition.UpdateTime)


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


def signal_handler(sig, frame):
    if sig == signal.SIGINT:
        logger.info("收到SIGINT信号,正在退出...")
    elif sig == signal.SIGTERM:
        logger.info("收到SIGTERM信号,正在退出...")
    
    sys.exit(0)


class BaseEngine(object):
    def __init__(self, strategy_name:str, strategy_id:int):
        self.strategy_name = strategy_name
        self.program_name = ""
        self.strategy_id = strategy_id
        self.data_connection = None
        self.hp_pack_client = None
        self.msg = pack_message.PackMessage()
        self.account_info_dict = dict()
        self.position_info_dict = dict()
        self.order_connection_dict = dict()
        self.order_id = 1

        self.start_time = datetime.datetime.now().time()
        self.end_time = None
        target_time1 = datetime.time(15, 30, 0)
        target_time2 = datetime.time(23, 30, 0)
        if self.start_time < target_time1:
            self.end_time = target_time1
        elif self.start_time < target_time2:
            self.end_time = target_time2

    def connect_to_xwatcher(self, ip:str, port:int):
        # 启动客户端连接XWatcher
        self.hp_pack_client = HPPackClient()
        self.hp_pack_client.Start(host=ip, port=port, head_flag=0x169, size=0XFFFF)
        logger.info(f"Connect to XWatcher:{ip}:{port}")

        # 发送登录请求
        msg = pack_message.PackMessage()
        msg.MessageType = pack_message.EMessageType.ELoginRequest
        msg.LoginRequest.ClientType = pack_message.EClientType.EXQUANT
        msg.LoginRequest.Account = self.strategy_name
        self.hp_pack_client.SendData(msg.to_bytes())

    def init_app_status(self, app_name:str, app_log_path:str):
        # 发送进程初始化状态
        cmd = sys.executable + " " + " ".join(sys.argv)
        self.program_name = app_name
        scripts = "nohup {} > {}/{}_run_{}.log 2>&1 &".format(cmd, app_log_path, self.program_name, datetime.datetime.now().strftime('%Y%m%d%H%M%S'))
        logger.info(f"{self.program_name} start:{scripts}")

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

    def connect_to_marketserver(self, market_server_name:str):
        # 连接MarketServer
        self.data_connection = shm_connection.SHMDataConnection(self.strategy_name)
        self.data_connection.Start(market_server_name)
        logger.info(f"{self.strategy_name} Connect to MarketServer:{market_server_name}")

    def connect_to_orderserver(self, order_server_name:str, account_list:list):
        # 连接XTrader
        for account in account_list:
            order_connection = shm_connection.SHMConnection(self.strategy_name + account)
            self.order_connection_dict[account] = order_connection
            order_connection.Start(order_server_name + account)
            logger.info(f"{account} Connect to XTrader:{order_server_name + account}")

    def update_tick(self, msg: pack_message.PackMessage):
        print_msg("update_tick", msg)

    def notify_orderstatus(self, msg:pack_message.PackMessage):
        print_msg("notify_orderstatus", msg)

    def notify_fund(self, msg:pack_message.PackMessage):
        print_msg("notify_fund", msg)

    def notify_position(self, msg: pack_message.PackMessage):
        print_msg("notify_position", msg)
            
    def run(self):
        # 注册中断信号
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)
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
        # 主要处理逻辑
        while True:
            # 收取行情数据
            self.data_connection.HandleMsg()
            ret = self.data_connection.Pop(self.msg)
            if ret:
                if self.msg.MessageType == pack_message.EMessageType.EFutureMarketData:
                    print_msg("", self.msg)
                    self.update_tick(self.msg)

                elif self.msg.MessageType == pack_message.EMessageType.EStockMarketData:
                    print_msg("", self.msg)
                    self.update_tick(self.msg)
                    
            # 回报数据处理
            for account, order_connection in self.order_connection_dict.items():
                while True:
                    # 收取交易回报信息
                    order_connection.HandleMsg()
                    ret = order_connection.Pop(self.msg)
                    if ret:
                        if self.msg.MessageType == pack_message.EMessageType.EAccountFund:
                            account_info_dict = dict()
                            account_info_dict["Colo"] = self.msg.AccountFund.Colo
                            account_info_dict["Broker"] = self.msg.AccountFund.Broker
                            account_info_dict["Product"] = self.msg.AccountFund.Product
                            account_info_dict["Account"] = self.msg.AccountFund.Account
                            account_info_dict["Balance"] = self.msg.AccountFund.Balance
                            account_info_dict["Avaliable"] = self.msg.AccountFund.Avaliable
                            account_info_dict["ChannelID"] = self.msg.ChannelID
                            self.account_info_dict[self.msg.AccountFund.Account] = account_info_dict

                            self.notify_fund(self.msg)

                        elif self.msg.MessageType == pack_message.EMessageType.EAccountPosition:
                            position_dict = dict()
                            position_dict["Colo"] = self.msg.AccountPosition.Colo
                            position_dict["Broker"] = self.msg.AccountPosition.Broker
                            position_dict["Product"] = self.msg.AccountPosition.Product
                            position_dict["Account"] = self.msg.AccountPosition.Account
                            position_dict["ChannelID"] = self.msg.ChannelID
                            key = self.msg.AccountPosition.Account + ":" + self.msg.AccountPosition.Ticker
                            self.position_info_dict[key] = position_dict

                            self.notify_position(self.msg)

                        elif self.msg.MessageType == pack_message.EMessageType.EOrderStatus:
                            self.notify_orderstatus(self.msg)
                    else:
                        break
            # 获取当前时间
            now = datetime.datetime.now().time()  # 获取当前时间部分
            # 比较时间
            if now > self.end_time:
                logger.info(f"当前时间:{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}，已经收盘，退出程序")
                break
        sys.stdout.flush()


