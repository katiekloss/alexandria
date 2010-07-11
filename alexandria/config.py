import ConfigParser
import logging

config = ConfigParser.ConfigParser()

def get(*args, **kwargs):
    """Convenience function for retrieving values from the config."""

    return config.get(*args, **kwargs)

def loadConfig(filename):
    """Loads a ConfigParser instance to the config global."""
    global config
    config.read(filename)
    logging.info("Loaded configuration from %s" % filename)
