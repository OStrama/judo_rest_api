"""RESTobject.

A REST object that contains a REST item and communicates with the REST-API.
It contains a REST Client for setting and getting REST response values
"""

import asyncio
import requests
import logging

from .configentry import MyConfigEntry
from .const import DEVICETYPES, FORMATS, TYPES, CONF
from .items import ModbusItem

logging.basicConfig()
log = logging.getLogger(__name__)


class RestAPI:
    """
    RestAPI class that provides a connection to the modbus,
    which is used by the ModbusItems.
    """

    def __init__(self, config_entry: MyConfigEntry) -> None:
        """Construct ModbusAPI.

        :param config_entry: HASS config entry
        :type config_entry: MyConfigEntry
        """
        self._ip = config_entry.data[CONF.HOST]
        self._port = config_entry.data[CONF.PORT]
        self._user = config_entry.data[CONF.USER]
        self._password = config_entry.data[CONF.PASSWORD]
        self._rest_client = None
        self._api_url = "http://"+self._user+":"+self._password+"@"+self._ip+":"+self_port+"/api/rest/"
        self._devicetype = None


    async def get_rest(self, command: str):
        try:
            url = self._api_url + command
            response = requests.get(url)
            res response.json()
            return res["data"]
        except Exception:
            log.warning("Connection to Judo Water Treatment failed")
            return None

    async def connect(self):
        """Open REST connection to test if available."""
        res = self.get_rest("FF00")
        if res is None:
            return None
        if res in DEVICETYPES:
            self._devicetype = res["data"]
            log.info("Connected to "+self._devicetype)
            return True
        else:
            log.warning("Unknown Device detected, ID="+res["data"])
            return None

    def close(self):
        """Close REST connection."""
        log.info("Connection to heatpump closed")
        return True

    def get_devicetype(self):
        """Return device type."""
        return self._devicetype


class RestObject:
    """RestObject.

    A REST object that contains a REST item and communicates with the REST.
    It contains a REST Client for setting and getting REST register values
    """

    def __init__(self, rest_api: RestAPI, rest_item: RestItem) -> None:
        """Construct RestObject.

        :param rest_api: The REST API
        :type rest_api: RestAPI
        :param rest_item: definition of rest item
        :type rest_item: RestItem
        """
        self._rest_item = rest_item
        self._rest_client = rest_api.get_device()

    def check_valid_result(self, val) -> int:
        """Check if item is available and valid."""
        match self._modbus_item.format:
            case FORMATS.TEMPERATUR:
                return self.check_temperature(val)
            case FORMATS.PERCENTAGE:
                return self.check_percentage(val)
            case FORMATS.STATUS:
                return self.check_status(val)
            case _:
                self._modbus_item.is_invalid = False
                return val

    def check_temperature(self, val) -> int:
        """Check availability of temperature item and translate
        return value to valid int

        :param val: The value from the modbus
        :type val: int"""
        match val:
            case -32768:
                # No Sensor installed, remove it from the list
                self._modbus_item.is_invalid = True
                return None
            case 32768:
                # This seems to be zero, should be allowed
                self._modbus_item.is_invalid = True
                return None
            case -32767:
                # Sensor broken set return value to -99.9 to inform user
                self._modbus_item.is_invalid = False
                return -999
            case _:
                # Temperature Sensor seems to be Einerkomplement
                if val > 32768:
                    val = val - 65536
                self._modbus_item.is_invalid = False
                return val

    def check_percentage(self, val) -> int:
        """Check availability of percentage item and translate
        return value to valid int

        :param val: The value from the modbus
        :type val: int"""
        if val == 65535:
            self._modbus_item.is_invalid = True
            return None
        else:
            self._modbus_item.is_invalid = False
            return val

    def check_status(self, val) -> int:
        """Check general availability of item."""
        self._modbus_item.is_invalid = False
        return val

    def check_valid_response(self, val) -> int:
        """Check if item is valid to write."""
        match self._modbus_item.format:
            case FORMATS.TEMPERATUR:
                if val < 0:
                    val = val + 65536
                return val
            case _:
                return val

    def validate_modbus_answer(self, mbr) -> int:
        """Check if there's a valid answer from modbus and
        translate it to a valid int depending from type

        :param mbr: The modbus response
        :type mbr: modbus response"""
        val = None
        if mbr.isError():
            myexception_code: ExceptionResponse = mbr
            if myexception_code.exception_code == 2:
                self._modbus_item.is_invalid = True
            else:
                log.warning(
                    "Received Modbus library error: %s in item: %s",
                    str(mbr),
                    str(self._modbus_item.name),
                )
            return None
        if isinstance(mbr, ExceptionResponse):
            log.warning(
                "Received ModbusException: %s from library in item: %s",
                str(mbr),
                str(self._modbus_item.name),
            )
            return None
            # THIS IS NOT A PYTHON EXCEPTION, but a valid modbus message
        if len(mbr.registers) > 0:
            val = self.check_valid_result(mbr.registers[0])
            return val

    @property
    async def value(self):
        """Returns the value from the modbus register."""
        if self._modbus_client is None:
            return None

        if not self._modbus_item.is_invalid:
            try:
                match self._modbus_item.type:
                    case TYPES.SENSOR | TYPES.SENSOR_CALC:
                        # Sensor entities are read-only
                        mbr = await self._modbus_client.read_input_registers(
                            self._modbus_item.address, slave=1
                        )
                        return self.validate_modbus_answer(mbr)
                    case TYPES.SELECT | TYPES.NUMBER | TYPES.NUMBER_RO:
                        mbr = await self._modbus_client.read_holding_registers(
                            self._modbus_item.address, slave=1
                        )
                        return self.validate_modbus_answer(mbr)
                    case _:
                        log.warning(
                            "Unknown Sensor type: %s in %s",
                            str(self._modbus_item.type),
                            str(self._modbus_item.name),
                        )
                        return None
            except ModbusException as exc:
                log.warning(
                    "ModbusException: Reading %s in item: %s failed",
                    str(exc),
                    str(self._modbus_item.name),
                )
                return None

    # @value.setter
    async def setvalue(self, value) -> None:
        """Set the value of the modbus register, does nothing when not R/W.

        :param val: The value to write to the modbus
        :type val: int"""
        if self._modbus_client is None:
            return
        try:
            match self._modbus_item.type:
                case TYPES.SENSOR | TYPES.NUMBER_RO | TYPES.SENSOR_CALC:
                    # Sensor entities are read-only
                    return
                case _:
                    await self._modbus_client.write_register(
                        self._modbus_item.address,
                        self.check_valid_response(value),
                        slave=1,
                    )
        except ModbusException:
            log.warning(
                "ModbusException: Writing %s to %s (%s) failed",
                str(value),
                str(self._modbus_item.name),
                str(self._modbus_item.address),
            )
            return