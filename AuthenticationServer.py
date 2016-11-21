from twisted.protocols import basic
from twisted.internet import reactor, protocol
from twisted.internet.protocol import Factory, Protocol
from twisted.internet.endpoints import TCP4ServerEndpoint
from twisted.protocols.basic import LineReceiver
from twisted.python import log

from datetime import datetime, timedelta
import time
import sqlite3

class ReverseChallengeAuthenticator(LineReceiver):

    # Model for users = {id, key, state}
    def __init__(self):
        self.id = None
        self.key = None
        self.state = 'TO_AUTH'

    # On connection store id as ip_addr
    # TODO: Log connections with time stamps
    def connectionMade(self):
        self.id = self.transport.getPeer()
        print(self.id, " connected")

    # On disconnect show disconnect reason and state
    def connectionLost(self, reason):
        print(str(self.id), " disconnected via: ", reason, " at state: ", self.state)

    def lineReceived(self, line):
        if self.state == 'TO_AUTH':
            self.handle_TO_AUTH(line)
        elif self.state == 'AUTHING':
            self.handle_AUTHING(line)
        else:
            self.handle_AUTHED(line)

    def handle_TO_AUTH(self, key):
        reversedKey = key[::-1]
        self.sendLine(reversedKey)
        self.key = key
        self.state = 'AUTHING'

    def handle_AUTHING(self, key):
        if self.key == key:

            HOST_PORT = "65060"
            self.sendLine(HOST_PORT)

            now = time.time() * 1000

            row = (str(self.id), now)
            conn = sqlite3.connect('headserver.db', detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
            c = conn.cursor()
            c.execute('begin')
            c.execute('INSERT INTO authenticated VALUES(?,?)', row)
            conn.commit()
            conn.close()

            print(str(self.id), " authenticated")

            self.state = 'AUTHED'

        else:
            print("AUTH_FAILED: Wrong key from client")
            self.sendLine("AUTH_FAILED")
            self.state = 'TO_AUTH'

    def handle_AUTHED(self, line):
        print("Already AUTHED!")

class AuthenticationFactory(Factory):

    def __init__(self):
        users = {}

    def buildProtocol(self, addr):
        return ReverseChallengeAuthenticator()


AUTH_PORT = 65055

reactor.listenTCP(AUTH_PORT, AuthenticationFactory())
reactor.run()
