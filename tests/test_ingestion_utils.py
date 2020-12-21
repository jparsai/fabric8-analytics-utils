"""Tests for classes from ingestion_utils module."""

from f8a_utils.ingestion_utils import unknown_package_flow
from unittest import mock
from collections import namedtuple

# Valid input data
data_v1 = set()
Package1 = namedtuple("Package", ["name", "version"])
data_v1.add(Package1(name='pkg', version='ver'))

# Invalid input data
data_v2 = set()
Package2 = namedtuple("Package", ["pkg", "ver"])
data_v2.add(Package2(pkg='pkg', ver='ver'))


@mock.patch('requests_futures.sessions.FuturesSession.post')
def test_ingest_epv(_session):
    """Test unknown_package_flow positive."""
    res = unknown_package_flow('dummy_eco', data_v1)
    assert res is True


@mock.patch('requests_futures.sessions.FuturesSession.post')
def test_ingest_epv_failed(_session):
    """Test unknown_package_flow negative."""
    res = unknown_package_flow('dummy_eco', data_v2)
    assert res is False
