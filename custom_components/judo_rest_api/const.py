"""Constants."""

from dataclasses import dataclass

from homeassistant.const import (
    CONF_HOST,
    CONF_PORT,
    CONF_PASSWORD,
    CONF_USERNAME,
    CONF_SCAN_INTERVAL,
)


@dataclass(frozen=True)
class ConfConstants:
    """Constants used for configurastion"""

    HOST = CONF_HOST
    PORT = CONF_PORT
    PASSWORD = CONF_PASSWORD
    USERNAME = CONF_USERNAME
    DEVICE_POSTFIX = "Device-Postfix"
    SCAN_INTERVAL = CONF_SCAN_INTERVAL


CONF = ConfConstants()


@dataclass(frozen=True)
class MainConstants:
    """Main constants."""

    DOMAIN = "judo_rest_api"
    SCAN_INTERVAL = "60"  # timedelta(seconds=60))
    UNIQUE_ID = "unique_id"
    APPID = 100


CONST = MainConstants()


@dataclass(frozen=True)
class FormatConstants:
    """Format constants."""

    NUMBER = "number"
    TEXT = "text"
    STATUS = "status"
    UNKNOWN = "unknown"
    SWITCH = "Switch"
    BUTTON = "Button"
    TIMESTAMP = "Timestamp"
    SW_VERSION = "SW_Version"


FORMATS = FormatConstants()


@dataclass(frozen=True)
class TypeConstants:
    """Type constants."""

    SENSOR = "Sensor"
    SENSOR_CALC = "Sensor_Calc"
    SELECT = "Select"
    SELECT_NOIF = "Select_noif"
    NUMBER = "Number"
    NUMBER_RO = "Number_RO"
    SWITCH = "Switch"
    BUTTON = "Button"


TYPES = TypeConstants()


@dataclass(frozen=True)
class DeviceConstants:
    """Device constants."""

    SYS = "dev_system"
    ST = "dev_statistics"
    UK = "dev_unknown"


DEVICES = DeviceConstants()

COMMANDS = {
    "Geraetetyp": "FF00",
    "Geraetenummer": "0600",
    "SW-Version": "0100",
    "Inbetriebnahmedatum": "0E00",
    "Betriebsstundenzaehler": "2500",
    "Kundendienst-Serviceadresse": "5800",
    "Wunschwasserhaerte": "5100",
    "Salzvorrat": "5600",
    "Salzreichweite": "5700",
    "Gesamtwassermenge": "2800",
    "Weichwassermenge": "2900",
    "Tagesstatistik": "FB00",
    "Wochenstatistik": "FC00",
    "Monatsstatistik": "FD00",
    "Jahresstatistik": "FE00",
}


DEVICETYPES = {
    "32": "i-soft",
    "33": "i-soft SAFE+",
    "34": "SOFTwell P",
    "35": "SOFTwell S",
    "36": "SOFTwell K",
    "37": "i-soft TGA",
    "38": "QUICKSOFT-M",
    "39": "QUICKSOFT-P",
    "3C": "i-fill",
    "3D": "i-dos eco",
    "41": "i-dos eco",
    "42": "i-soft K SAFE+",
    "43": "i-soft K",
    "44": "ZEWA/PROM i-SAFE",
    "46": "QUICKSOFT CD",
    "47": "SOFTwell KP",
    "48": "SOFTwell KS",
    "49": "optiline Z",
    "4A": "optiline E",
    "4B": "i-soft PRO-S",
    "4C": "i-soft PRO L",
    "4D": "QUICKSOFT MP",
    "4E": "i-soft C SAFE",
    "4F": "i-soft C",
    "50": "i-soft K",
    "51": "i-soft K SAFE+",
    "52": "SOFTwell KP",
    "53": "i-soft",
    "54": "i-soft K",
    "55": "i-soft TGA",
    "56": "i-soft safe",
    "57": "i-soft SAFE+",
    "58": "i-soft PRO",
    "59": "SOFTwell P",
    "5A": "SOFTwell K",
    "5B": "Quicksoft M",
    "5C": "Quicksoft P",
    "5D": "Scansoft-M",
    "5E": "Scansoft-P",
    "5F": "Finesky WHS-C",
    "60": "Finesky WHS-P",
    "61": "QUICKSOFT CD",
    "62": "SOFTwell KP",
    "63": "SOFTwell S",
    "64": "SOFTwell KS",
    "65": "optiline Z",
    "66": "optiline E",
    "67": "i-soft K SAFE+",
    "68": "ZEWA/PROM i-SAFE",
    "6A": "Aqua Tenera E",
    "6B": "Aqua Tenera D",
}
