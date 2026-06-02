import asyncio
from types import SimpleNamespace
from unittest import mock

from changeme.scanners.snmp import SNMP
from changeme.target import Target


class FakePretty:
    def __init__(self, value):
        self.value = value

    def prettyPrint(self):
        return self.value


class FakeUdpTransportTarget:
    requested = None

    @classmethod
    async def create(cls, address):
        cls.requested = address
        return cls()


async def fake_get_cmd(*args, **kwargs):
    return None, None, None, ((FakePretty('SNMPv2-MIB::sysDescr.0'), FakePretty('test device')),)


def build_scanner():
    cred = {'default_port': 1161, 'name': 'publicprivate'}
    target = Target(host='127.0.0.1')
    return SNMP(cred, target, '', 'public', SimpleNamespace())


def test_snmp_check_uses_asyncio_transport():
    scanner = build_scanner()
    with mock.patch('changeme.scanners.snmp.UdpTransportTarget', FakeUdpTransportTarget), \
         mock.patch('changeme.scanners.snmp.get_cmd', fake_get_cmd):
        assert scanner._check() == 'SNMPv2-MIB::sysDescr.0 = test device'

    assert FakeUdpTransportTarget.requested == ('127.0.0.1', 1161)


def test_snmp_check_can_run_when_event_loop_exists():
    scanner = build_scanner()

    async def run_check():
        with mock.patch('changeme.scanners.snmp.UdpTransportTarget', FakeUdpTransportTarget), \
             mock.patch('changeme.scanners.snmp.get_cmd', fake_get_cmd):
            return scanner._check()

    assert asyncio.run(run_check()) == 'SNMPv2-MIB::sysDescr.0 = test device'
