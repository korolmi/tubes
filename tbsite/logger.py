import time

def DoLog(msg, mod="common"):
	""" логгирует сообщение  """

	logger = open("/tmp/tubes.log",encoding="utf-8", mode="a")
	ts = time.strftime("%d %b %Y %H:%M:%S",time.gmtime())
	logger.write("{0}\t{1}\t{2}\n".format(ts,mod,msg))
	logger.close()

