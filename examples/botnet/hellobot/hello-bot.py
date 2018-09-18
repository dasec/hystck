from hystck.botnet.bots.hellobot.hello_bot import HelloBot

__author__ = 'Sascha Kopp'

b = HelloBot()
b.start()
raw_input("press enter to exit:\n")
b.stop()
