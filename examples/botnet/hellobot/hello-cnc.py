from hystck.botnet.bots.hellobot.hello_bot import HelloCnC

__author__ = 'Sascha Kopp'

b = HelloCnC()
b.start()
raw_input("press enter to exit:\n")
b.stop()
