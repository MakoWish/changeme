import asyncio
import threading

from pysnmp.hlapi.asyncio import (
    CommunityData,
    ContextData,
    ObjectIdentity,
    ObjectType,
    SnmpEngine,
    UdpTransportTarget,
    get_cmd,
)

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

    async def _async_check(self):
        transport = await UdpTransportTarget.create((str(self.target.host), int(self.target.port)))
        errorIndication, errorStatus, errorIndex, varBinds = await get_cmd(
            SnmpEngine(),
            CommunityData(self.password),
            transport,
            ContextData(),
            ObjectType(ObjectIdentity('SNMPv2-MIB', 'sysDescr', 0)),
        )

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
