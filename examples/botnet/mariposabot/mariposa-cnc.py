from hystck.botnet.bots.mariposa.mariposa import MariposaCnC

__author__ = 'Sascha Kopp'

b = MariposaCnC()
b.start()
raw_input("Press enter to quit")
b.stop()
