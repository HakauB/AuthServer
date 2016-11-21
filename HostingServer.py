from twisted.protocols import basic
from twisted.internet import reactor, protocol
from twisted.internet.protocol import Factory, Protocol
from twisted.internet.endpoints import TCP4ServerEndpoint
from twisted.protocols.basic import LineReceiver

import sys, traceback

from datetime import datetime, timedelta
import time
import sqlite3

# TABLBE : PACKET_TYPE
PACKET_TABLE_LOOKUP = {
    'LUX':'LUX',
    'MOT':'MOTION'
}

PACKET_LENGTH_LOOKUP = {
    'LUX':'1',
    'MOT':'9'
}

class DataLogger(LineReceiver):

    def __init__(self):
        self.id = None
        self.state = 'RECEIVING'

    def connectionMade(self):
        self.id = self.transport.getPeer()
        print(self.id, " connected")

    def connectionLost(self, reason):
        print(self.id, " disconnected via: ", reason, " at state: ", self.state)

    def lineReceived(self, line):
        if self.state == 'RECEIVING':
            self.handle_RECEIVING(line)

    def handle_RECEIVING(self, line):
        splits = line.split(' ')
        packet_type = splits[0]

        devId = splits[1]
        timeStamp = splits[2]
        data = splits[3:]
        now = time.time() * 1000

        conn = sqlite3.connect('headserver.db', detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)

        if packet_type == 'LUX':
            self.enter_LUX(conn, devId, timeStamp, now, data)
        elif packet_type == 'MOT':
            self.enter_MOT(conn, devId, timeStamp, now, data)
        else:
            print("Unknow packet_type: ", packet_type)
        conn.close()

    def enter_MOT(self, conn, devId, timeStamp, now, data):
        c = conn.cursor()
        if len(data) == 9:
            c.execute('pragma foreign_keys')
            c.execute('begin')
            try:
                c.execute('INSERT INTO entry VALUES(',timeStamp,', ',now,', ',devId,', (select max(seq) from entry) + 1)')
                c.execute('INSERT INTO motion VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, (select max(seq) from entry))', data)
                conn.commit()
            except:
                try:
                    c.execute('INSERT INTO entry VALUES(',timeStamp,', ',now,', ',devId,', 0)')
                    c.execute('INSERT INTO motion VALUES($?, ?, ?, ?, ?, ?, ?, ?, ?, (select max(seq) from entry))', data)
                    conn.commit()
                except:
                    print('INSERT failed')
        else:
            print("Wrong data count: ", len(data))

    def enter_LUX(self, conn, devId, timeStamp, now, data):
        c = conn.cursor()
        entryTuple = (timeStamp, now, devId)
        print entryTuple
        print data[0]
        if len(data) == 1:
            c.execute('pragma foreign_keys')
            c.execute('begin')
            try:
                c.execute('INSERT INTO entry VALUES(?, ?, ?, (select max(seq) from entry) + 1)', entryTuple)
                c.execute('INSERT INTO lux VALUES(?, (select max(seq) from entry))', (data[0],))
                conn.commit()
                print("L0")
            except:
                try:
                    try:
                        c.execute('INSERT INTO entry VALUES(?, ?, ?, 0)', entryTuple)
                        c.execute('INSERT INTO lux VALUES(?, (select max(seq) from entry))', (data[0],))
                        conn.commit()
                        print("L1")
                    finally:
                        a=1 # Do Nothing
                except:
                    print '-'*60
                    traceback.print_exc(file=sys.stdout)
                    print '-'*60
                    print('INSERT failed')
        else:
            print("Wrong data count: ", len(data))

class ReceiverFactory(Factory):

    def __init__(self):
        users = {}

    def buildProtocol(self, addr):
        return DataLogger()

HOST_PORT = 65060

reactor.listenTCP(HOST_PORT, ReceiverFactory())
reactor.run()
