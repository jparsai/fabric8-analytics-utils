"""Utility file to trigger unknown package ingestion."""

import logging
import os
from collections import namedtuple
from typing import Set
from requests_futures.sessions import FuturesSession

logger = logging.getLogger(__name__)

_APP_SECRET_KEY = os.getenv('APP_SECRET_KEY', 'not-set')
_INGESTION_API_URL = "http://{host}:{port}/{endpoint}".format(
    host=os.environ.get("INGESTION_SERVICE_HOST", "bayesian-jobs"),
    port=os.environ.get("INGESTION_SERVICE_PORT", "34000"),
    endpoint='ingestions/epv')
_session = FuturesSession()


def unknown_package_flow(ecosystem: str, unknown_pkgs: Set[namedtuple]):
    """Unknown Package flow utility function.

    :param ecosystem: Ecosystem
    :param unknown_pkgs: Set of tuple having packages name and version
    """
    logger.debug('Triggered Unknown Package Flow for ecosystem: {} and Package: {}'
                 .format(ecosystem, unknown_pkgs))

    # Create payload to be passed to ingestion API
    payload = {
        "ecosystem": ecosystem,
        "packages": [],
        "force": False,
        "force_graph_sync": True
    }

    # Set the unknown packages and versions
    logger.info('===========================================')
    for pkg in unknown_pkgs:
        if hasattr(pkg, 'name'):
            logger.info('name is present')
            payload['packages'].append({'package': pkg.name, 'version': pkg.version})
        else:
            logger.info('name is not present')
            logger.info('----------------------')
            logger.info('name' in pkg)
            logger.info('++++++++++++++++++++++')
            logger.info('package' in pkg)
            logger.info('**********************')


    # If package list is not empty then call ingestion API
    if payload['packages']:
        try:
            _session.post(url=_INGESTION_API_URL,
                          json=payload,
                          headers={'auth_token': _APP_SECRET_KEY})
        except Exception as e:
            logger.error('Failed to trigger unknown flow for payload %s with error %s',
                         payload, e)
            raise Exception('Ingestion failed') from e
        else:
            logger.info('Ingestion call being executed')
