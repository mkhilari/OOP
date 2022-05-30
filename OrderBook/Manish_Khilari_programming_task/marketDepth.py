

from posixpath import split
import sys


class MessageReader: 

    def __init__(self): 
        
        self.bytes = self.read() 
        self.messages = self.getMessages() 

    def read(self): 

        """Returns a list of bytes read from a standard input stream """ 

        bytes = [] 

        for byte in sys.stdin.buffer.read(): 

            bytes.append(byte) 

        return bytes 

    def getMessages(self): 

        """Returns a list of messages given an input list of bytes """ 

        messages = [] 
        i = 0 

        while (i < len(self.bytes)): 

            # Read message 
            sequenceNumber \
                = int.from_bytes(
                    bytes = self.bytes[i : 
                    i + Message.SEQUENCE_NUMBER_LENGTH], 
                    byteorder = "little", signed = False) 
            i += Message.SEQUENCE_NUMBER_LENGTH 

            messageSize \
                = int.from_bytes(
                    bytes = self.bytes[i : 
                    i + Message.MESSAGE_SIZE_LENGTH], 
                    byteorder = "little", signed = False) 
            i += Message.MESSAGE_SIZE_LENGTH 

            messageType = chr(self.bytes[i]) 

            message = self.bytes[i : i + messageSize] 
            i += messageSize 

            messages.append(Message(sequenceNumber, messageSize, 
            messageType, message)) 

        return messages 


class Message: 

    SEQUENCE_NUMBER_LENGTH = 4 
    MESSAGE_SIZE_LENGTH = 4 

    SYMBOL_LENGTH = 3 
    ORDER_ID_LENGTH = 8 
    RESERVED1_LENGTH = 3 
    VOLUME_LENGTH = 8 
    PRICE_LENGTH = 4 
    RESERVED2_LENGTH = 4 

    ADD = "A" 
    UPDATE = "U" 
    DELETE = "D" 
    EXECUTE = "E" 

    def __init__(self, sequenceNumber, messageSize, messageType, 
    message = []): 
        
        self.sequenceNumber = sequenceNumber 
        self.messageSize = messageSize 
        self.messageType = messageType 

        self.message = message 
    
    def __str__(self): 

        s = "" 
        
        s += f"sequenceNumber = {self.sequenceNumber} \n" 
        s += f"messageSize = {self.messageSize} \n" 
        s += f"messageType = {self.messageType} \n" 
        s += f"message = {self.message} \n" 

        return s 


class OrderSide: 

    BUY = "B" 
    SELL = "S" 


class Order: 

    def __init__(self, orderID, symbol, orderSide, 
    volume, price): 
        
        self.orderID = orderID 
        self.symbol = symbol 
        self.orderSide = orderSide 
        self.volume = volume 
        self.price = price 
    
    def getOrderName(orderID, symbol, orderSide): 

        return f"{orderID} {symbol} {orderSide}" 
    
    def getName(self): 

        return Order.getOrderName(self.orderID, self.symbol, 
        self.orderSide) 
    
    def __str__(self): 
        
        s = "" 
        
        s += f"orderName = {self.getName()} \n" 
        s += f"volume = {self.volume} \n" 
        s += f"price = {self.price} \n" 

        return s 


class OrderBook: 

    def __init__(self, messages, topN): 
        
        self.topN = topN 
        
        # orders is a map with (key, value) pairs of 
        # (orderName, order) 
        self.orders = {} 

        self.symbolSnapshot = {} 
        self.snapshots = [] 

        self.executeOrders(messages) 
    
    def executeOrders(self, messages): 

        """Executes orders given a list of messages """ 

        for message in messages: 

            messageType = message.messageType 
            symbol = "" 

            if (messageType == Message.ADD): 

                symbol = self.addOrder(message) 
            elif (messageType == Message.UPDATE): 

                symbol = self.updateOrder(message) 
            elif (messageType == Message.DELETE): 

                symbol = self.deleteOrder(message) 
            elif (messageType == Message.EXECUTE): 

                symbol = self.executeOrder(message) 

            # Create snapshot 
            buyOrders = [] 
            sellOrders = [] 

            for orderName in self.orders: 
                
                order = self.orders[orderName] 
                orderSide = order.orderSide 

                if (orderSide == OrderSide.BUY): 

                    buyOrders.append(order) 
                elif (orderSide == OrderSide.SELL): 

                    sellOrders.append(order) 
            
            # Get the top N buy and sell orders 
            buyOrders.sort(key = lambda order : order.price, reverse = True) 
            sellOrders.sort(key = lambda order : order.price) 

            buyOrders = buyOrders[: self.topN] 
            sellOrders = sellOrders[: self.topN] 

            # Get buyOrderList 
            buyOrderList = "[" 

            for i in range(len(buyOrders)): 

                buyOrder = buyOrders[i] 

                buyOrderList += f"({buyOrder.price}, {buyOrder.volume})" 

                if (i < len(buyOrders) - 1): 

                    buyOrderList += ", " 

            buyOrderList += "]" 

            # Get sellOrderList 
            sellOrderList = "[" 

            for i in range(len(sellOrders)): 

                sellOrder = sellOrders[i] 

                sellOrderList += f"({sellOrder.price}, {sellOrder.volume})" 

                if (i < len(sellOrders) - 1): 

                    sellOrderList += ", " 

            sellOrderList += "]" 

            # Get snapshot 
            snapshot = f"{message.sequenceNumber}, {symbol}, " 
            snapshot += f"{buyOrderList}, {sellOrderList}" 

            # Exclude sequenceNumber when comparing snapshots 
            if (symbol not in self.symbolSnapshot 
            or str(snapshot.split(" ")[1 :]) 
            != str(self.symbolSnapshot[symbol].split(" ")[1 :])): 

                # New topN snapshot for the current symbol 
                self.symbolSnapshot[symbol] = snapshot 
                
                print(snapshot) 

                self.snapshots.append(snapshot) 
            
    def addOrder(self, message): 
        
        # Read message 
        messageBytes = message.message 

        i = 1 

        # Read symbol 
        symbol = "" 

        for c in range(i, i + Message.SYMBOL_LENGTH): 

            symbol += chr(messageBytes[c]) 
        
        i += Message.SYMBOL_LENGTH 

        # Read orderID 
        orderID \
            = int.from_bytes(
                bytes = messageBytes[i : 
                i + Message.ORDER_ID_LENGTH], 
                byteorder = "little", signed = False) 
        i += Message.ORDER_ID_LENGTH 

        # Read orderSide 
        orderSide = chr(messageBytes[i]) 
        i += 1 

        i += Message.RESERVED1_LENGTH 

        # Read volume 
        volume \
            = int.from_bytes(
                bytes = messageBytes[i : 
                i + Message.VOLUME_LENGTH], 
                byteorder = "little", signed = False) 
        i += Message.VOLUME_LENGTH 

        # Read price 
        price \
            = int.from_bytes(
                bytes = messageBytes[i : 
                i + Message.PRICE_LENGTH], 
                byteorder = "little", signed = False) 
        i += Message.PRICE_LENGTH 

        i += Message.RESERVED2_LENGTH 

        # Add new order 
        newOrder = Order(orderID, symbol, orderSide, volume, price) 
        newOrderName = newOrder.getName() 

        self.orders[newOrderName] = newOrder 

        return symbol 

    def updateOrder(self, message): 

        # Read message 
        messageBytes = message.message 

        i = 1 

        # Read symbol 
        symbol = "" 

        for c in range(i, i + Message.SYMBOL_LENGTH): 

            symbol += chr(messageBytes[c]) 
        
        i += Message.SYMBOL_LENGTH 

        # Read orderID 
        orderID \
            = int.from_bytes(
                bytes = messageBytes[i : 
                i + Message.ORDER_ID_LENGTH], 
                byteorder = "little", signed = False) 
        i += Message.ORDER_ID_LENGTH 

        # Read orderSide 
        orderSide = chr(messageBytes[i]) 
        i += 1 

        i += Message.RESERVED1_LENGTH 

        # Read volume 
        volume \
            = int.from_bytes(
                bytes = messageBytes[i : 
                i + Message.VOLUME_LENGTH], 
                byteorder = "little", signed = False) 
        i += Message.VOLUME_LENGTH 

        # Read price 
        price \
            = int.from_bytes(
                bytes = messageBytes[i : 
                i + Message.PRICE_LENGTH], 
                byteorder = "little", signed = False) 
        i += Message.PRICE_LENGTH 

        i += Message.RESERVED2_LENGTH 

        # Update order with new volume and price 
        orderName = Order.getOrderName(orderID, symbol, orderSide) 

        self.orders[orderName].volume = volume 
        self.orders[orderName].price = price 

        return symbol 

    def deleteOrder(self, message): 

        # Read message 
        messageBytes = message.message 

        i = 1 

        # Read symbol 
        symbol = "" 

        for c in range(i, i + Message.SYMBOL_LENGTH): 

            symbol += chr(messageBytes[c]) 
        
        i += Message.SYMBOL_LENGTH 

        # Read orderID 
        orderID \
            = int.from_bytes(
                bytes = messageBytes[i : 
                i + Message.ORDER_ID_LENGTH], 
                byteorder = "little", signed = False) 
        i += Message.ORDER_ID_LENGTH 

        # Read orderSide 
        orderSide = chr(messageBytes[i]) 
        i += 1 

        i += Message.RESERVED1_LENGTH 

        # Delete order 
        orderName = Order.getOrderName(orderID, symbol, orderSide) 

        self.orders.pop(orderName) 

        return symbol 

    def executeOrder(self, message): 

        # Read message 
        messageBytes = message.message 

        i = 1 

        # Read symbol 
        symbol = "" 

        for c in range(i, i + Message.SYMBOL_LENGTH): 

            symbol += chr(messageBytes[c]) 
        
        i += Message.SYMBOL_LENGTH 

        # Read orderID 
        orderID \
            = int.from_bytes(
                bytes = messageBytes[i : 
                i + Message.ORDER_ID_LENGTH], 
                byteorder = "little", signed = False) 
        i += Message.ORDER_ID_LENGTH 

        # Read orderSide 
        orderSide = chr(messageBytes[i]) 
        i += 1 

        i += Message.RESERVED1_LENGTH 

        # Read tradedVolume 
        tradedVolume \
            = int.from_bytes(
                bytes = messageBytes[i : 
                i + Message.VOLUME_LENGTH], 
                byteorder = "little", signed = False) 
        i += Message.VOLUME_LENGTH 

        # Update order with new volume 
        orderName = Order.getOrderName(orderID, symbol, orderSide) 

        self.orders[orderName].volume += -tradedVolume 

        if (self.orders[orderName].volume <= 0): 

            # Order fully traded 
            self.orders.pop(orderName) 

        return symbol 





def main(): 

    # Get command line arguments 
    DEFAULT_TOP_N = 5 

    topN = DEFAULT_TOP_N 

    if (len(sys.argv) >= 2): 

        topN = int(sys.argv[1]) 

    aMessageReader = MessageReader() 

    messages = aMessageReader.messages 

    for message in messages: 

        print(message) 
    
    anOrderBook = OrderBook(messages, topN) 

    # Output snapshots to file 
    fileOutput = open(file = "output2.log", mode = "w") 

    for snapshot in anOrderBook.snapshots: 

        fileOutput.write(f"{snapshot}\n") 

main() 