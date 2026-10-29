"""Exercise the production flow method without a live inverter or HA instance."""
import ast
from pathlib import Path
from types import SimpleNamespace as NS
import unittest
from unittest.mock import AsyncMock, Mock

class PortUpdateTests(unittest.IsolatedAsyncioTestCase):
    async def test_existing_inverter_updates_host_and_port(self):
        path=Path(__file__).resolve().parents[1]/'custom_components/sunways_local/config_flow.py'
        tree=ast.parse(path.read_text())
        owner=next(n for n in tree.body if isinstance(n,ast.ClassDef) and n.name=='SunwaysLocalConfigFlow')
        method=next(n for n in owner.body if isinstance(n,ast.AsyncFunctionDef) and n.name=='async_step_user')
        module=ast.Module(body=[ast.ImportFrom(module='__future__',names=[ast.alias(name='annotations')],level=0),method],type_ignores=[])
        ast.fix_missing_locations(module)
        class AlreadyConfigured(Exception): pass
        context=dict(CONF_HOST='host',CONF_PORT='port',DEFAULT_PORT=5488,InverterError=OSError,
                     async_connect_inverter=AsyncMock(return_value=NS(serial_number='synthetic')))
        exec(compile(module,str(path),'exec'),context)
        for data,port in [({'host':'same.invalid','port':6000},6000),({'host':'new.invalid'},5488)]:
            flow=NS(async_set_unique_id=AsyncMock(),_abort_if_unique_id_configured=Mock(side_effect=AlreadyConfigured),async_create_entry=Mock())
            with self.assertRaises(AlreadyConfigured):
                await context['async_step_user'](flow,data)
            flow._abort_if_unique_id_configured.assert_called_once_with(updates={'host':data['host'],'port':port})
            flow.async_create_entry.assert_not_called()
