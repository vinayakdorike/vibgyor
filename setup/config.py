from configparser import ConfigParser
import logging

logger = logging.getLogger('MainAPI')
def config(filename='../configurations.ini', section='config_data'):
    '''
    filename='../configurations.ini', section='config_data'
    '''
    logger.debug("Reading Configuration File")
    # create a parser
    parser = ConfigParser()
    # read config file
    try:
        parser.read(filename)
    except Exception as e:
        logger.error("-----------------------Stopping Execution: Exception occurred 'Config' File Not Found",exc_info=True)
        exit()
    # get section, default to postgresql
    config_vars = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            config_vars[param[0]] = param[1]
    else:
        logger.error("-----------------------Stopping Execution: 'Section' not found in config file: %s",section)
        exit()
    return config_vars


