from logging import DEBUG, Formatter, getLogger, handlers


def configure_logger():
    """Configure logger to write messages to console.

    The admin service writes all STDOUT to /var/log/mycroft_admin_service.log.
    So writing logs to STDOUT will result in log messages being written there.
    """
    logger = getLogger('adapt')
    if not logger.hasHandlers():
        logger.setLevel(DEBUG)
        log_msg_formatter = Formatter(
            '{asctime} | {levelname:8} | {process:5} | {name} | {message}',
            style='{'
        )
        log_handler = handlers.TimedRotatingFileHandler(
            filename='/var/log/mycroft/adapt.log',
            when='midnight',
            utc=True
        )
        log_handler.setLevel(DEBUG)
        log_handler.setFormatter(log_msg_formatter)
        logger.addHandler(log_handler)

    return logger


def log_parse_tag(log, tag, confidence=None):
    log.info('*** \tSTART INDEX: ' + str(tag['start_token']))
    if len(tag["entities"]) > 1:
        log.info(
            "ALERT!!!! Multiple entities found in tag!!!!")
    else:
        entity = tag["entities"][0]
        log.info(f'*** \tENTITY')
        log.info(f'*** \t\tconfidence: {entity["confidence"]}')
        log.info(f'*** \t\tword(s): {entity["key"]}')
        log.info(f'*** \t\tskill vocabulary matches: ')
        for item in entity['data']:
            log.info("*** \t\t\t" + str(item[1]))
        log.info(f'***')
        log.info(f'*** \tTAG CONFIDENCE: {confidence}')
        log.info(f'***')
