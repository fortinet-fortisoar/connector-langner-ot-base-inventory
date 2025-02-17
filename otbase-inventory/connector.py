"""
Copyright start
MIT License
Copyright (c) 2024 Fortinet Inc
Copyright end
"""

from connectors.core.connector import Connector, get_logger, ConnectorError

from .operations import operations, _check_health

logger = get_logger("otbase-inventory")


class OTBaseInventory(Connector):
    def execute(self, config, operation, params, **kwargs):
        logger.debug("Invoking {0} Operation".format(operation))
        try:
            action = operations.get(operation)
            logger.info('Executing action {0}'.format)
            return action(config, params)
        except Exception as Err:
            logger.exception("Exception in execute function: {0} ".format(str(Err)))
            raise ConnectorError(str(Err))

    def check_health(self, config):
        _check_health(config)