import asyncio
import inspect
import threading
import types

# Older pysnmp releases still reference asyncio.coroutine, which was
# removed from Python's public asyncio namespace in newer interpreters.
if not hasattr(asyncio, 'coroutine'):
    asyncio.coroutine = types.coroutine

from pysnmp.hlapi import asyncio as pysnmp_asyncio

CommunityData = pysnmp_asyncio.CommunityData
ContextData = pysnmp_asyncio.ContextData
ObjectIdentity = pysnmp_asyncio.ObjectIdentity
ObjectType = pysnmp_asyncio.ObjectType
SnmpEngine = pysnmp_asyncio.SnmpEngine
UdpTransportTarget = pysnmp_asyncio.UdpTransportTarget
get_cmd = getattr(pysnmp_asyncio, 'get_cmd', None) or getattr(pysnmp_asyncio, 'getCmd')

from .scanner import Scanner


class SNMP(Scanner):
    def __init__(self, cred, target, username, password, config):
        super(SNMP, self).__init__(cred, target, config, username, password)

    def fingerprint(self):
        # Don't fingerprint since it's UDP
        return True

    def _check(self):
        return self._run_async_check()

    def _run_async_check(self):
        try:
            asyncio.get_running_loop()
        except RuntimeError:
            return asyncio.run(self._async_check())

        result = {}

        def run_in_thread():
            try:
                result['value'] = asyncio.run(self._async_check())
            except Exception as exc:
                result['exception'] = exc

        thread = threading.Thread(target=run_in_thread)
        thread.start()
        thread.join()

        if 'exception' in result:
            raise result['exception']

        return result['value']


    async def _make_transport_target(self):
        address = (str(self.target.host), int(self.target.port))
        if hasattr(UdpTransportTarget, 'create'):
            return await UdpTransportTarget.create(address)

        transport = UdpTransportTarget(address)
        if inspect.isawaitable(transport):
            return await transport
        return transport

    async def _get_sysdescr(self, transport):
        result = get_cmd(
            SnmpEngine(),
            CommunityData(self.password),
            transport,
            ContextData(),
            ObjectType(ObjectIdentity('SNMPv2-MIB', 'sysDescr', 0)),
        )
        if inspect.isawaitable(result):
            result = await result
        return result

    async def _async_check(self):
        transport = await self._make_transport_target()
        errorIndication, errorStatus, errorIndex, varBinds = await self._get_sysdescr(transport)

        evidence = ""
        if errorIndication:
            self.logger.debug(errorIndication)
        elif errorStatus:
            self.logger.debug('%s at %s' % (errorStatus.prettyPrint(),
                                errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))
        else:
            for varBind in varBinds:
                evidence += ' = '.join([x.prettyPrint() for x in varBind])

        if evidence == "":
            raise Exception

        return evidence

    def _mkscanner(self, cred, target, u, p, config):
        return SNMP(cred, target, u, p, config)
