# An example client - LINUX ONLY! (Relies on iwlist and iwconfig)

from wifi import Cell, Scheme
import sys

from twisted.internet import reactor
from twisted.internet.protocol import Protocol, ClientFactory
from twisted.protocols.basic import LineReceiver

class Main(Protocol):
    def dataReceived(self,data):
        print data
        self.transport.write(data)

class MainFactory(ClientFactory):
    def buildProtocol(self,addr):
        print 'Connected'
        return Main()

    def clientConnectionLost(self,connector,reason):
        print 'Connection lost'

    def clientConnectionFailed(self,connector,reason):
        print 'connection failed'

device = sys.argv[0]

ssids = Cell.all(device)
for ssid in ssids:
    print str(ssid)

HOST_PORT = 65060

reactor.connectTCP('172.24.72.1', HOST_PORT, MainFactory())
reactor.run()

'''''
schemes = list(Scheme.all())

scheme.for_cell(device, 'home', )

for scheme in schemes:
    ssid = scheme.options.get('wpa-ssid', scheme.options.get('wireless-essid'))
    if ssid in ssids:
        print('Connecting to %s' % ssid)
        scheme.activate()
        break
'''''
