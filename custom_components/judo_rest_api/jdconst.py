"""Heatpump constants."""

from homeassistant.components.sensor import SensorStateClass, SensorDeviceClass
from homeassistant.const import (
    UnitOfVolumeFlowRate,
    UnitOfMass,
    UnitOfVolume,
    UnitOfTime,
)

from .const import DEVICES, FORMATS, TYPES
from .items import RestItem, StatusItem

reverse_device_list: dict[str, str] = {
    "dev_system": "SYS",
#    "dev_statistik": "ST",
}

################################################################################
# Listen mit Fehlermeldungen, Warnmeldungen und Statustexte
# Beschreibungstext ist ebenfalls möglich
# class StatusItem(): def __init__(self, number, text, description = None):
################################################################################

# fmt: off

UNIT_STATUS: list[StatusItem] = [
    StatusItem(number=0, translation_key="ge_hardness"),
    StatusItem(number=1, translation_key="en_hardness"),
    StatusItem(number=2, translation_key="fr_hardness"),
    StatusItem(number=3, translation_key="ppm"),
    StatusItem(number=4, translation_key="mmol"),
    StatusItem(number=5, translation_key="mval"),
]

UNIT_TYPE: list[StatusItem] = [
    StatusItem(number=0x32, translation_key="i_soft"),
    StatusItem(number=0x33, translation_key="i_soft_safe_plus"),
    StatusItem(number=0x34, translation_key="softwell_p"),
    StatusItem(number=0x35, translation_key="softwell_s"),
    StatusItem(number=0x36, translation_key="softwell_k"),
    StatusItem(number=0x37, translation_key="i_soft_tga"),
    StatusItem(number=0x38, translation_key="quicksoft_m"),
    StatusItem(number=0x39, translation_key="quicksoft_p"),
    StatusItem(number=0x3C, translation_key="i_fill"),
    StatusItem(number=0x3D, translation_key="i_dos_eco"),
    StatusItem(number=0x41, translation_key="i_dos_eco"),
    StatusItem(number=0x42, translation_key="i_soft_k_safe_plus"),
    StatusItem(number=0x43, translation_key="i_soft_k"),
    StatusItem(number=0x44, translation_key="zewa_prom_i_safe"),
    StatusItem(number=0x46, translation_key="quicksoft_cd"),
    StatusItem(number=0x47, translation_key="softwell_kp"),
    StatusItem(number=0x48, translation_key="softwell_ks"),
    StatusItem(number=0x49, translation_key="optiline_z"),
    StatusItem(number=0x4A, translation_key="optiline_e"),
    StatusItem(number=0x4B, translation_key="i_soft_pro_s"),
    StatusItem(number=0x4C, translation_key="i_soft_pro_l"),
    StatusItem(number=0x4D, translation_key="quicksoft_mp"),
    StatusItem(number=0x4E, translation_key="i_soft_c_safe"),
    StatusItem(number=0x4F, translation_key="i_soft_c"),
    StatusItem(number=0x50, translation_key="i_soft_k"),
    StatusItem(number=0x51, translation_key="i_soft_k_safe_plus"),
    StatusItem(number=0x52, translation_key="softwell_kp"),
    StatusItem(number=0x53, translation_key="i_soft"),
    StatusItem(number=0x54, translation_key="i_soft_k"),
    StatusItem(number=0x55, translation_key="i_soft_tga"),
    StatusItem(number=0x56, translation_key="i_soft_safe"),
    StatusItem(number=0x57, translation_key="i_soft_safe_plus"),
    StatusItem(number=0x58, translation_key="i_soft_pro"),
    StatusItem(number=0x59, translation_key="softwell_p"),
    StatusItem(number=0x5A, translation_key="softwell_k"),
    StatusItem(number=0x5B, translation_key="quicksoft_m"),
    StatusItem(number=0x5C, translation_key="quicksoft_p"),
    StatusItem(number=0x5D, translation_key="scansoft_m"),
    StatusItem(number=0x5E, translation_key="scansoft_p"),
    StatusItem(number=0x5F, translation_key="finesky_whs_c"),
    StatusItem(number=0x60, translation_key="finesky_whs_p"),
    StatusItem(number=0x61, translation_key="quicksoft_cd"),
    StatusItem(number=0x62, translation_key="softwell_kp"),
    StatusItem(number=0x63, translation_key="softwell_s"),
    StatusItem(number=0x64, translation_key="softwell_ks"),
    StatusItem(number=0x65, translation_key="optiline_z"),
    StatusItem(number=0x66, translation_key="optiline_e"),
    StatusItem(number=0x67, translation_key="i_soft_k_safe_plus"),
    StatusItem(number=0x68, translation_key="zewa_prom_i_safe"),
    StatusItem(number=0x6A, translation_key="aqua_tenera_e"),
    StatusItem(number=0x6B, translation_key="aqua_tenera_d"),
]

SALT_MASS: list[StatusItem] = [
    StatusItem(number=0, translation_key="mass_0kg"),
    StatusItem(number=1, translation_key="mass_1kg"),
    StatusItem(number=5, translation_key="mass_5kg"),
    StatusItem(number=10, translation_key="mass_10kg"),
    StatusItem(number=15, translation_key="mass_15kg"),
    StatusItem(number=20, translation_key="mass_20kg"),
    StatusItem(number=25, translation_key="mass_25kg"),
    StatusItem(number=50, translation_key="mass_50kg"),
]
#####################################################
# Description of physical units via the status list #
#####################################################

PARAMS_FLOWRATE: dict = {
    "min": 0,
    "max": 5,
    "step": 0.1,
    "divider": 100,
    "precision": 2,
    "unit": UnitOfVolumeFlowRate.LITERS_PER_MINUTE,
    "stateclass": SensorStateClass.MEASUREMENT,
}

PARAMS_MASS: dict = {
    "min": 0,
    "max": 100,
    "step": 1,
    "divider": 1000,
    "preciosion": 2,
    "unit": UnitOfMass.KILOGRAMS,
    "stateclass": SensorStateClass.MEASUREMENT,
    "icon": "mdi:weight-kilogram"
}

PARAMS_DAYS: dict = {
    "min": 1,
    "max": 255,
    "step": 1,
    "preciosion": 0,
    "unit": UnitOfTime.DAYS,
    "stateclass": SensorStateClass.MEASUREMENT,
    "icon": "mdi:timelapse"
}

PARAMS_MINUTES: dict = {
    "step": 1,
    "preciosion": 0,
    "unit": UnitOfTime.MINUTES,
    "stateclass": SensorStateClass.MEASUREMENT,
    "icon": "mdi:timelapse"
}

PARAMS_HOURS: dict = {
    "step": 1,
    "preciosion": 0,
    "unit": UnitOfTime.HOURS,
    "stateclass": SensorStateClass.MEASUREMENT,
    "icon": "mdi:timelapse"
}

PARAMS_GDH: dict = {
    "min": 1,
    "max": 18,
    "step": 1,
    "preciosion": 1,
    "unit": "°dH",
    "divider": 1,
    "stateclass": SensorStateClass.MEASUREMENT,
    "icon": "mdi:water-opacity"
}

PARAMS_QBM_H: dict = {
    "min": 0,
    "max": 100,
    "step": 1,
    "divider": 1000,
    "preciosion": 3,
    "unit": UnitOfVolume.CUBIC_METERS,
    "stateclass": SensorStateClass.TOTAL_INCREASING,
    "deviceclass": SensorDeviceClass.WATER,
    "icon": "mdi:water"
}

PARAMS_QBM_W: dict = {
    "min": 0,
    "max": 100,
    "step": 1,
    "divider": 1000,
    "preciosion": 3,
    "unit": UnitOfVolume.CUBIC_METERS,
    "stateclass": SensorStateClass.TOTAL_INCREASING,
    "deviceclass": SensorDeviceClass.WATER,
    "icon": "mdi:water-outline"
}


PARAMS_CONTACT: dict = {
    "icon": "mdi:phone"
}

PARAMS_CLOSE: dict = {
    "icon": "mdi:water-pump-off"
}
PARAMS_OPEN: dict = {
    "icon": "mdi:water-pump"
}

PARAMS_REG: dict = {
    "icon": "mdi:water-check-outline"
}

PARAMS_INFO: dict = {
    "icon": "mdi:information-box-outline"
}

PARAMS_MASS_REFILL: dict = {
    "icon": "mdi:weight-kilogram",
    "min": 0,
    "max": 50,
    "step": 0.05,
    "divider": 1000,
    "preciosion": 3,
    "unit": UnitOfMass.KILOGRAMS,
    "stateclass": SensorStateClass.MEASUREMENT
}
# pylint: disable=line-too-long

# fmt: off
REST_SYS_ITEMS: list[RestItem] = [
    RestItem( address_read="FF00", read_bytes = 2, read_index=0, mformat=FORMATS.STATUS, mtype=TYPES.SENSOR, device=DEVICES.SYS, resultlist=UNIT_TYPE, params= PARAMS_INFO, translation_key="device_type"),
    RestItem( address_read="0600", read_bytes = 4, read_index=0, mformat=FORMATS.NUMBER, mtype=TYPES.SENSOR, device=DEVICES.SYS, params= PARAMS_INFO, translation_key="device_number"),
    RestItem( address_read="0100", read_bytes = 3, read_index=0, mformat=FORMATS.SW_VERSION, mtype=TYPES.SENSOR, device=DEVICES.SYS, params= PARAMS_INFO, translation_key="software_version"),

    RestItem( address_read="5100", read_bytes = 2, read_index=0, address_write="3000", write_bytes = 1, write_index=0, mformat=FORMATS.NUMBER, mtype=TYPES.NUMBER, device=DEVICES.SYS, params= PARAMS_GDH,translation_key="water_hardeness"),
    RestItem( address_read="5700", read_bytes = 1, read_index=0, address_write="5700", write_bytes = 1, write_index=0, mformat=FORMATS.NUMBER, mtype=TYPES.NUMBER, device=DEVICES.SYS, params= PARAMS_DAYS,translation_key="salt_warning"),

#   RestItem( address_read="5600", read_bytes = 2, read_index=0, mformat=FORMATS.NUMBER, mtype=TYPES.SENSOR, device=DEVICES.SYS, params= PARAMS_MASS, translation_key="salt_storage_mass"),
    RestItem( address_read="5600", read_bytes = 2, read_index=0, address_write="5600", write_bytes = 2, write_index=0, mformat=FORMATS.NUMBER, mtype=TYPES.NUMBER, device=DEVICES.SYS, params= PARAMS_MASS_REFILL, translation_key="salt_storage_mass"),

    RestItem( address_read="5600", read_bytes = 2, read_index=2, mformat=FORMATS.NUMBER, mtype=TYPES.SENSOR, device=DEVICES.SYS, params= PARAMS_DAYS,translation_key="salt_storage_days"),

    RestItem( address_read="2800", read_bytes = 4, read_index=0, mformat=FORMATS.NUMBER, mtype=TYPES.SENSOR, device=DEVICES.SYS, params= PARAMS_QBM_H, translation_key="water_total"),
    RestItem( address_read="2900", read_bytes = 4, read_index=0, mformat=FORMATS.NUMBER, mtype=TYPES.SENSOR, device=DEVICES.SYS, params= PARAMS_QBM_W, translation_key="water_treated"),
    RestItem( address_read="5800", read_bytes = 16, read_index=0, mformat=FORMATS.TEXT, mtype=TYPES.SENSOR, device=DEVICES.SYS, params= PARAMS_CONTACT,translation_key="service_contact"),
    RestItem( address_read="2500", read_bytes = 1, read_index=0, mformat=FORMATS.NUMBER, mtype=TYPES.SENSOR, device=DEVICES.SYS, params= PARAMS_MINUTES,translation_key="operating_minutes"),
    RestItem( address_read="2500", read_bytes = 1, read_index=1, mformat=FORMATS.NUMBER, mtype=TYPES.SENSOR, device=DEVICES.SYS, params= PARAMS_HOURS,translation_key="operating_hours"),
    RestItem( address_read="2500", read_bytes = 2, read_index=2, mformat=FORMATS.NUMBER, mtype=TYPES.SENSOR, device=DEVICES.SYS, params= PARAMS_DAYS,translation_key="operating_days"),
    RestItem( address_read="0E00", read_bytes = 4, read_index=0, mformat=FORMATS.TIMESTAMP, mtype=TYPES.SENSOR, device=DEVICES.SYS,params= PARAMS_INFO, translation_key="install_date"),

    RestItem(address_write="3C00", write_bytes = 0, write_index=0, mformat=FORMATS.BUTTON, mtype=TYPES.BUTTON, device=DEVICES.SYS, params= PARAMS_CLOSE, translation_key="leakage_protection_close"),
    RestItem(address_write="3D00", write_bytes = 0, write_index=0, mformat=FORMATS.BUTTON, mtype=TYPES.BUTTON, device=DEVICES.SYS, params= PARAMS_OPEN, translation_key="leakage_protection_open"),
    RestItem(address_write="350000", write_bytes = 0, write_index=0, mformat=FORMATS.BUTTON, mtype=TYPES.BUTTON, device=DEVICES.SYS, params= PARAMS_REG, translation_key="start_regeneration"),

#    RestItem(address_read="5600", read_bytes = 2, read_index=0,address_write="5600", write_bytes = 2, write_index=0, mformat=FORMATS.STATUS, mtype=TYPES.SELECT_NOIF, device=DEVICES.SYS, params= PARAMS_MASS_REFILL, resultlist=SALT_MASS, translation_key="salt_refill_mass"),
]

#REST_ST_ITEMS: list[RestItem] = [
    #RestItem( address_read="FB00", mformat=FORMATS.NUMBER, mtype=TYPES.SENSOR, device=DEVICES.ST, params=PARAMS_QBM_H, translation_key="day_statistics"),
#]

DEVICELISTS: list = [
    REST_SYS_ITEMS,
    #REST_ST_ITEMS,
]

# fmt: on
