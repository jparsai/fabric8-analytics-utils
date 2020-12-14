
import logging
import os
import time
from collections import namedtuple
from typing import Set
from requests_futures.sessions import FuturesSession

logger = logging.getLogger(__name__)

_APP_SECRET_KEY = os.getenv('APP_SECRET_KEY', 'not')
_INGESTION_API_URL = "http://{host}:{port}/{endpoint}".format(
    host=os.environ.get("INGESTION_SERVICE_HOST", "bayesian-jobs"),
    port=os.environ.get("INGESTION_SERVICE_PORT", "34000"),
    endpoint='ingestions/epv')
_session = FuturesSession()


def unknown_package_flow(ecosystem: str, unknown_pkgs: Set[namedtuple]) -> bool:
    """Unknown Package flow. Trigger bayesianApiFlow."""
    logger.debug('Triggered Unknown Package Flow for ecosystem: {} and Package: {}'
                 .format(ecosystem, unknown_pkgs))
    started_at = time.time()
    # Create payload to be passed to ingestion API
    payload = {
        "ecosystem": ecosystem,
        "packages": [],
        "force": False,
        "force_graph_sync": True
    }

    # Set the unknown packages and versions
    for pkg in unknown_pkgs:
        payload['packages'].append({'package': pkg.name, 'version': pkg.version})

    if payload['packages']:
        logger.info('Invoking Ingestion URL for payload = {}'.format(payload))
        logger.info('_APP_SECRET_KEY = {}'.format(_APP_SECRET_KEY))
        _session.post(url=_INGESTION_API_URL,
                      json=payload,
                      headers={'auth_token': _APP_SECRET_KEY})

    elapsed_time = time.time() - started_at
    logger.info('Unknown flow for %f packages took %f seconds', len(unknown_pkgs), elapsed_time)
    return True
