from hystck.botnet.bots.mariposa.mariposa import MariposaBotMaster

__author__ = 'Sascha Kopp'

b = MariposaBotMaster()
b.start()
raw_input("Press enter to quit")
b.stop()
