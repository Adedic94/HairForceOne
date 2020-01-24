import logging

logformat="%(levelname)s:%(filename)s:%(lineno)d:%(asctime)s:%(message)s"
logfilename = 'mylogging.log'
loglevel = logging.DEBUG

formatterDEBUG = logging.Formatter(logformat)

handlerDEBUG = logging.FileHandler(logfilename)
handlerDEBUG.setFormatter(formatterDEBUG)

loggerDEBUG = logging.getLogger('root_name')
loggerDEBUG.addHandler(handlerDEBUG)
loggerDEBUG.setLevel(loglevel)

# loggerDEBUG.debug("We're on!")

# logging.basicConfig(filename='./mylogging.log',level=logging.DEBUG,format=logformat)
# logging.info("Logging is initialized")
