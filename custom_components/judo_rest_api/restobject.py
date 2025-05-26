"""RESTobject.

A REST object that contains a REST item and communicates with the REST-API.
It contains a REST Client for setting and getting REST response values
"""

import logging
from datetime import datetime
from functools import partial
import requests
from homeassistant.core import HomeAssistant

from .configentry import MyConfigEntry
from .const import DEVICETYPES, FORMATS, CONF, TYPES
from .items import RestItem

logging.basicConfig()
log = logging.getLogger(__name__)


class RestAPI:
    """
    RestAPI class that provides a connection to the rest api,
    which is used by the RestItems.
    """

    def __init__(self, config_entry: MyConfigEntry, hass: HomeAssistant) -> None:
        """Construct RestAPI.

        :param config_entry: HASS config entry
        :type config_entry: MyConfigEntry
        """
        self._ip = config_entry.data[CONF.HOST]
        self._port = config_entry.data[CONF.PORT]
        self._username = config_entry.data[CONF.USERNAME]
        self._password = config_entry.data[CONF.PASSWORD]
        self._hass = hass
        self._rest_client = None
        self._base_url = (
            "http://"
            # + str(self._user)
            # + ":"
            # + str(self._password)
            # + "@"
            + str(self._ip)
            + ":"
            + str(self._port)
        )
        self._api_url = self._base_url + "/api/rest/"
        self._devicetype = None
        self._session = None
        self._connected = False

    async def login(self) -> None:
        """Log into the portal. Create cookie to stay logged in for the session."""

        _useless = await self._hass.async_add_executor_job(
            partial(
                requests.get,
                url=self._base_url,
                auth=(self._username, self._password),
                timeout=10,
            )
        )

        # r = requests.get(self._base_url, auth=(self._username, self._password), timeout=10 )
        # log.warning(r.text)

    async def get_rest(self, command: str):
        """get raw response from REST api"""
        if command is None:
            return None

        response = None
        try:
            log.debug("Send command %s", command)
            url = self._api_url + command
            response = await self._hass.async_add_executor_job(
                partial(
                    requests.get,
                    url=url,
                    auth=(self._username, self._password),
                    timeout=10,
                )
            )
            log.debug("Response %s", response.status_code)
            status = response.status_code
            if status == 200:
                res = await self._hass.async_add_executor_job(response.json)
                log.debug("Content %s", str(res["data"]))
                return res["data"]
            else:
                log.warning("Content ignored for API return status %s", str(status))
                return None
        except Exception:
            if response is not None:
                status = str(response.status_code)
            else:
                status = "unknown status"
            log.warning("Judo REST API call failed with %s", status)
            return None

    async def set_rest(self, command: str, towrite: str):
        """write raw response to REST api"""
        if command is None:
            return None
        if towrite is None:
            return None

        try:
            url = self._api_url + command + towrite
            response = await self._hass.async_add_executor_job(
                partial(
                    requests.get,
                    url=url,
                    auth=(self._username, self._password),
                    timeout=2,
                )
            )
            res = await self._hass.async_add_executor_job(response.json)
            return res["data"]
        except Exception:
            log.warning("Connection to Judo Water Treatment failed")
            return None

    async def connect(self):
        """Open REST connection to test if available."""
        res = await self.get_rest("FF00")
        if res is None:
            return None
        if res in DEVICETYPES:
            self._devicetype = res
            log.info("Connected to %s", self._devicetype)
            return True

        log.warning("Unknown Device detected, ID=%s", res)
        return None

    def close(self):
        """Close REST connection."""
        log.info("Connection to judo closed")
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
        self._rest_api = rest_api
        self._divider = 1
        if self._rest_item.params is not None:
            self._divider = self._rest_item.params.get("divider", 1)

    def order_hex_buffer(self, buffer: str, flip) -> str:
        """brings a hex buffer in the right order"""
        if flip is True:
            little_endian = bytes.fromhex(buffer)[::-1].hex()
            return little_endian
        big_endian = bytes.fromhex(buffer)[::1].hex()
        return big_endian

    def format_int_message(self, number: int, flip) -> str:
        """format int message as hex buffer to be sent to REST APPI"""
        numbytes = str(self._rest_item.write_bytes * 2)
        mask = "%0." + numbytes + "X"
        return self.order_hex_buffer(mask % number, flip)

    def format_str_message(self, text: str, flip) -> str:
        """format str message as hex buffer to be sent to REST APPI"""
        return self.order_hex_buffer(text.encode("utf-8").hex(), flip)

    @property
    async def value(self):
        """Returns the value from the REST API."""
        if self._rest_api is None:
            return None
        if self._rest_item.format is FORMATS.BUTTON:
            return None

        res = await self._rest_api.get_rest(self._rest_item.address_read)

        if res is None:
            return None

        index = self._rest_item.read_index * 2
        big_endian = res[index : index + self._rest_item.read_bytes * 2]
        little_endian = bytes.fromhex(big_endian)[::-1].hex()
        big_endian = bytes.fromhex(big_endian)[::1].hex()

        if big_endian is None:
            return None
        if little_endian is None:
            return None
        if big_endian == "":
            return None
        if little_endian == "":
            return None
        match self._rest_item.format:
            case FORMATS.SWITCH:
                return None
            case FORMATS.NUMBER:
                return float(int(little_endian, 16) / self._divider)
            case FORMATS.SW_VERSION:
                major = str(int(little_endian[0:2], 16))
                minor = str(int(little_endian[2:4], 16)).zfill(2)
                letter = str(bytearray.fromhex(little_endian[4:6]).decode())
                return str(major + "." + minor + letter)
            case FORMATS.TIMESTAMP:
                return str(datetime.fromtimestamp(int(big_endian, 16)))
            case FORMATS.TEXT:
                return bytearray.fromhex(big_endian).decode()
            case FORMATS.STATUS:
                return self._rest_item.get_translation_key_from_number(
                    int(little_endian, 16)
                )
            case _:
                log.warning(
                    "Unknown format: %s in %s",
                    str(self._rest_item.type),
                    str(self._rest_item.translation_key),
                )
                return None
        return None

    # @value.setter
    async def setvalue(self, value=None) -> None:
        """Set the value of the rest register, does nothing when not R/W."""
        """:param val: The value to write to the rest"""
        """:type val: any"""
        towrite = None
        if self._rest_api is None:
            return

        if self._rest_item.type == TYPES.SENSOR:
            return
        if self._rest_item.format is FORMATS.BUTTON:
            await self._rest_api.set_rest(self._rest_item.address_write, "")
            return
        if value is None:
            return
        self._rest_item.state = value
        match self._rest_item.format:
            case FORMATS.SWITCH:
                if value == 0:
                    await self._rest_api.set_rest(self._rest_item.address_read, "")
                if value == 1:
                    await self._rest_api.set_rest(self._rest_item.address_write, "")
                return
            case FORMATS.NUMBER:
                towrite = self.format_int_message(
                    int(float(value) * self._divider), True
                )
            case FORMATS.TEXT:
                towrite = self.format_str_message((value), True)
            case FORMATS.STATUS:
                towrite = self.format_int_message(
                    (self._rest_item.get_number_from_translation_key(value))
                    * self._divider,
                    True,
                )
            case _:
                log.warning(
                    "Unknown format: %s in %s",
                    str(self._rest_item.type),
                    str(self._rest_item.translation_key),
                )
                return
        if towrite is not None:
            await self._rest_api.set_rest(self._rest_item.address_write, towrite)
        return

    async def addvalue(self, value=None) -> None:
        """Set the value of the rest register, does nothing when not R/W."""
        """:param val: The value to write to the rest"""
        """:type val: any"""
        towrite = None
        if self._rest_api is None:
            return None

        if self._rest_item.type == TYPES.SENSOR:
            return None
        if self._rest_item.format is FORMATS.BUTTON:
            return None
        if value is None:
            return None

        res = await self._rest_api.get_rest(self._rest_item.address_read)

        if res is None:
            return None

        index = self._rest_item.read_index * 2
        big_endian = res[index : index + self._rest_item.read_bytes * 2]
        little_endian = bytes.fromhex(big_endian)[::-1].hex()
        big_endian = bytes.fromhex(big_endian)[::1].hex()

        if big_endian is None:
            return None
        if little_endian is None:
            return None
        if big_endian == "":
            return None
        if little_endian == "":
            return None
        offset = float(int(little_endian, 16) / self._divider)

        #        self._rest_item.state = value + offset
        match self._rest_item.format:
            case FORMATS.NUMBER:
                self._rest_item.state = value + offset
                towrite = self.format_int_message(
                    int((float(value) + float(offset)) * self._divider), True
                )
            case FORMATS.TEXT:
                self._rest_item.state = value + offset
                towrite = self.format_str_message((value + offset), True)
            case FORMATS.STATUS:
                self._rest_item.state = (
                    self._rest_item.get_number_from_translation_key(value) + offset
                )
                towrite = self.format_int_message(
                    int(
                        (
                            float(
                                self._rest_item.get_number_from_translation_key(value)
                            )
                            + float(offset)
                        )
                        * self._divider
                    ),
                    True,
                )
            case _:
                log.warning(
                    "Unknown format: %s in %s",
                    str(self._rest_item.type),
                    str(self._rest_item.translation_key),
                )
                return
        if towrite is not None:
            await self._rest_api.set_rest(self._rest_item.address_write, towrite)
        return
