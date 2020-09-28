from hystck.botnet.bots.hellobot.hello_bot import HelloBotMaster

__author__ = 'Sascha Kopp'

b = HelloBotMaster()
b.start()
raw_input("press enter to exit:\n")
b.stop()
