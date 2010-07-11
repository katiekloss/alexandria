import ConfigParser
import logging

config = ConfigParser.ConfigParser()

def loadConfig(filename):
    """Loads a ConfigParser instance to the config global."""
    global config
    config.read(filename)
    logging.info("Loaded configuration from %s" % filename)