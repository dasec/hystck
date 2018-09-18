from hystck.botnet.bots.mariposa.mariposa import MariposaBot

__author__ = 'Sascha Kopp'

b = MariposaBot()
b.start()
raw_input("Press enter to quit")
b.stop()
