import sys
sys.path.append(".")
import shm_connection
import pack_message
import time
import signal
import datetime
import os
from loguru import logger # type: ignore
from HPSocket import TcpPack
from HPSocket import helper
import HPSocket.pyhpsocket as HPSocket
from kline import KLineGenerator, BarData


def print_msg(func:str, msg):
    logger.debug(f"{func} MessageType {msg.MessageType:#X}")
    if msg.MessageType == pack_message.EMessageType.EFutureMarketData:
        logger.debug("Colo:{} Ticker:{} ExchangeID:{} TradingDay:{} ActionDay:{} UpdateTime:{} MillSec:{} LastPrice:{} "
                     "Volume:{} Turnover:{} OpenPrice:{} ClosePrice:{} PreClosePrice:{} SettlementPrice:{} PreSettlementPrice:{} "
                     "OpenInterest:{} PreOpenInterest:{} HighestPrice:{} LowestPrice:{} UpperLimitPrice:{} LowerLimitPrice:{} "
                     "BidPrice1:{} BidVolume1:{} AskPrice1:{} AskVolume1:{} RecvLocalTime:{} CurrentTime:{}", 
                    msg.FutureMarketData.Colo, msg.FutureMarketData.Ticker, msg.FutureMarketData.ExchangeID, msg.FutureMarketData.TradingDay, 
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
    def __init__(self, strategy_name:str, strategy_id:int, snapshot_interval, slice_per_sec, intervals:list, trading_sections:list):
        self.strategy_name = strategy_name
        self.program_name = ""
        self.strategy_id = strategy_id
        self.snapshot_interval = snapshot_interval
        self.slice_per_sec = slice_per_sec
        self.intervals = intervals
        self.trading_sections = list()
        self.section_start = 0
        self.section_end = 0
        timestamp:int = int(time.time())
        struct_time = time.strptime(f"{datetime.datetime.now().strftime('%Y-%m-%d')} 17:00:00", "%Y-%m-%d %H:%M:%S")
        compare_time = int(time.mktime(struct_time))
        for (start_time, end_time) in trading_sections:
            struct_time = time.strptime(f"{datetime.datetime.now().strftime('%Y-%m-%d')} {start_time}", "%Y-%m-%d %H:%M:%S")
            _start_time = int(time.mktime(struct_time))
            struct_time = time.strptime(f"{datetime.datetime.now().strftime('%Y-%m-%d')} {end_time}", "%Y-%m-%d %H:%M:%S")
            _end_time = int(time.mktime(struct_time))
            if timestamp > compare_time:
                if _end_time < _start_time:
                    _end_time = _end_time + 24 * 60 * 60
                self.trading_sections.append((_start_time, _end_time))
                logger.info(f"BaseEngine TradingSection:{start_time}-{end_time} {_start_time}-{_end_time}")
                break
            else:
                # 过滤夜盘时间
                if compare_time < _start_time:
                    continue
                # 日盘盘中启动时过滤已经执行交易小节
                if timestamp > _end_time:
                    continue
                self.trading_sections.append((_start_time, _end_time))
                logger.info(f"BaseEngine TradingSection:{start_time}-{end_time} {_start_time}-{_end_time}")

        self.data_connection = None
        self.hp_pack_client = None
        self.msg = pack_message.PackMessage()
        self.account_info_dict = dict()
        self.position_info_dict = dict()
        self.order_connection_dict = dict()
        self.order_id = 1
        self.klines = dict()
        self.timestamp_sec = 0
        self.new_order:bool = False
        self.order_request:pack_message.PackMessage = pack_message.PackMessage()

        self.start_time = int(time.time())
        self.end_time = self.trading_sections[-1][1] + 10 * 60

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

    def on_window_bar(self, bar: BarData):
        raise NotImplementedError("BaseEngine基类中on_window_bar方法必须在子类重新实现")

    def notify_orderstatus(self, msg:pack_message.PackMessage):
        print_msg("notify_orderstatus", msg)

    def notify_fund(self, msg:pack_message.PackMessage):
        print_msg("notify_fund", msg)

    def notify_position(self, msg: pack_message.PackMessage):
        print_msg("notify_position", msg)

    def check_trading(self, timestamp:int):
        ret : bool = False
        for (start_time, end_time) in self.trading_sections:
            if start_time <= timestamp and timestamp < end_time:
                self.section_start = start_time * 1000
                self.section_end = end_time * 1000
                ret = True
                break
        return ret

    def cancel_order(self, action_order: pack_message.PackMessage):
        if action_order.MessageType == pack_message.EMessageType.EActionRequest:
            account = action_order.ActionRequest.Account
            order_connection = self.order_connection_dict.get(account, None)
            if order_connection:
                order_connection.Push(action_order)
                order_connection.HandleMsg() # 发送订单到XTrader

    def close_all_order(self, section_start:int, section_end:int, timestamp:int):
        pass

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
            # 
            timestamp_sec:int = int(time.time())
            is_trading: bool = self.check_trading(timestamp=timestamp_sec)
            # 收取行情数据
            self.data_connection.HandleMsg()
            ret = self.data_connection.Pop(self.msg)
            if ret:
                if is_trading:
                    self.new_order = False
                    if self.msg.MessageType == pack_message.EMessageType.EFutureMarketData:
                        print_msg("run", self.msg)
                        struct_time = time.strptime(f"{self.msg.FutureMarketData.ActionDay} {self.msg.FutureMarketData.UpdateTime}", "%Y%m%d %H:%M:%S")
                        timestamp = time.mktime(struct_time) * 1000 + int(self.msg.FutureMarketData.MillSec)
                        if self.msg.FutureMarketData.Ticker not in self.klines:
                            kline_generator = KLineGenerator(ticker=self.msg.FutureMarketData.Ticker, snapshot_interval=self.snapshot_interval, 
                                                            slice_per_sec=self.slice_per_sec, intervals=self.intervals)
                            kline_generator.set_call_back(self.on_window_bar)
                            kline_generator.process_tick(section_start=self.section_start, section_end=self.section_end, timestamp=timestamp, 
                                                        price=self.msg.FutureMarketData.LastPrice, volume=self.msg.FutureMarketData.Volume)
                            self.klines[self.msg.FutureMarketData.Ticker] = kline_generator
                        else:
                            kline_generator = self.klines[self.msg.FutureMarketData.Ticker]
                            kline_generator.process_tick(section_start=self.section_start, section_end=self.section_end, timestamp=timestamp, 
                                                        price=self.msg.FutureMarketData.LastPrice, volume=self.msg.FutureMarketData.Volume)
                        if timestamp + 10 * 1000 < self.section_end:
                            self.update_tick(self.msg)

                    elif self.msg.MessageType == pack_message.EMessageType.EStockMarketData:
                        print_msg("run", self.msg)
                        struct_time = time.strptime(f"{datetime.datetime.now().strftime('%Y%m%d')} {self.msg.StockMarketData.UpdateTime}", "%Y%m%d %H:%M:%S")
                        timestamp = time.mktime(struct_time) * 1000 + int(self.msg.StockMarketData.MillSec)
                        if self.msg.StockMarketData.Ticker not in self.klines:
                            kline_generator = KLineGenerator(ticker=self.msg.StockMarketData.Ticker, snapshot_interval=self.snapshot_interval, 
                                                            slice_per_sec=self.slice_per_sec, intervals=self.intervals)
                            kline_generator.set_call_back(self.on_window_bar)
                            kline_generator.process_tick(section_start=self.section_start, section_end=self.section_end, timestamp=timestamp, 
                                                        price=self.msg.StockMarketData.LastPrice, volume=self.msg.StockMarketData.Volume)
                            self.klines[self.msg.StockMarketData.Ticker] = kline_generator
                        else:
                            kline_generator = self.klines[self.msg.StockMarketData.Ticker]
                            kline_generator.process_tick(section_start=self.section_start, section_end=self.section_end, timestamp=timestamp, 
                                                        price=self.msg.StockMarketData.LastPrice, volume=self.msg.StockMarketData.Volume)
                        if timestamp + 10 * 1000 < self.section_end:
                            self.update_tick(self.msg)
                    
                    if self.new_order:
                        if self.order_request.MessageType == pack_message.EMessageType.EOrderRequest:
                            for account, order_connection in self.order_connection_dict.items():
                                self.order_request.OrderRequest.Account = account
                                order_connection.Push(self.order_request)
                                order_connection.HandleMsg() # 发送订单到XTrader
                                if self.order_request.OrderRequest.Direction == pack_message.EOrderDirection.EBUY:
                                    logger.info(f"send buy order to {account} ChannelID:{self.order_request.ChannelID} {self.order_request.OrderRequest.Ticker} price:{self.order_request.OrderRequest.Price} orderid:{self.order_request.OrderRequest.OrderToken} Direction:{self.order_request.OrderRequest.Direction} Offset:{self.order_request.OrderRequest.Offset}")
                                else:
                                    logger.info(f"send sell order to {account} ChannelID:{self.order_request.ChannelID} {self.order_request.OrderRequest.Ticker} price:{self.order_request.OrderRequest.Price} orderid:{self.order_request.OrderRequest.OrderToken} Direction:{self.order_request.OrderRequest.Direction} Offset:{self.order_request.OrderRequest.Offset}")


            # 检查K线闭合
            if self.timestamp_sec < timestamp_sec:
                self.timestamp_sec = timestamp_sec
            if self.timestamp_sec % 60 == 5:
                if self.section_start + 59 * 1000 <= timestamp_sec * 1000 and timestamp_sec * 1000  < self.section_end + 59 * 1000:
                    self.timestamp_sec = self.timestamp_sec + 1
                    for ticker, current_kline in self.klines.items():
                        current_kline.close_kline(section_start=self.section_end, section_end=self.section_end, timestamp=timestamp_sec * 1000)
                    logger.info(f"当前时间:{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}超时闭合K线")
                    
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
                            account_info_dict["Available"] = self.msg.AccountFund.Available
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
                        
            # 比较时间
            if timestamp_sec > self.end_time:
                logger.info(f"当前时间:{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}，已经收盘，退出程序")
                break
        sys.stdout.flush()


