"""Tests for classes from ingestion_utils module."""

from f8a_utils.ingestion_utils import unknown_package_flow
import unittest
from unittest import mock
from collections import namedtuple

# Input data
data_v1 = set()
Package1 = namedtuple("Package", ["name", "version"])
data_v1.add(Package1(name='pkg', version='ver'))


class MyTestCase(unittest.TestCase):
    """Test class for unknown_package_flow."""

    @mock.patch('requests_futures.sessions.FuturesSession.post')
    def test_ingest_epv(self, _session):
        """Test unknown_package_flow positive."""
        unknown_package_flow('dummy_eco', data_v1)

    @mock.patch('requests_futures.sessions.FuturesSession.post')
    def test_ingest_epv_failed(self, _session):
        """Test unknown_package_flow negative."""
        _session.side_effect = Exception(mock.Mock(return_value={'status': 404}), 'not found')
        with self.assertRaises(Exception):
            unknown_package_flow('dummy_eco', data_v1)