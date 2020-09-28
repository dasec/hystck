from hystck.botnet.bots.zeus.zeus import ZeusBot

b = ZeusBot(True)  # use False if you want ip.php based nat detection (currently only static config supported)
b.start()
raw_input("press enter to exit:\n")
b.stop()
