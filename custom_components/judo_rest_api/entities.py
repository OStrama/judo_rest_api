"""Entity classes used in this integration."""

import logging

from homeassistant.components.sensor import SensorEntity, SensorStateClass
from homeassistant.components.number import NumberEntity
from homeassistant.components.switch import SwitchEntity
from homeassistant.components.button import ButtonEntity
from homeassistant.components.select import SelectEntity
from homeassistant.core import callback
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity import Entity
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .configentry import MyConfigEntry
from .const import CONF, CONST, FORMATS, TYPES
from .coordinator import MyCoordinator
from .items import RestItem
from .restobject import RestAPI, RestObject

logging.basicConfig()
log = logging.getLogger(__name__)


class MyEntity(Entity):
    """An entity using CoordinatorEntity.

    The CoordinatorEntity class provides:
    should_poll
    async_update
    async_added_to_hass
    available

    The base class for entities that hold general parameters
    """

    _attr_should_poll = True
    _attr_has_entity_name = True
    _attr_entity_name = None
    _divider = 1

    def __init__(
        self,
        config_entry: MyConfigEntry,
        rest_item: RestItem,
        coordinator: MyCoordinator = None,
    ) -> None:
        """Initialize the entity."""
        self._config_entry = config_entry
        self._rest_item = rest_item
        self._coordinator = coordinator
        self._rest_api = self._coordinator.rest_api

        dev_postfix = "_" + self._config_entry.data[CONF.DEVICE_POSTFIX]

        if dev_postfix == "_":
            dev_postfix = ""

        self._dev_device = self._rest_item.device + dev_postfix

        self._attr_translation_key = self._rest_item.translation_key
        self._dev_translation_placeholders = {"postfix": dev_postfix}

        dev_postfix = "_" + config_entry.data[CONF.DEVICE_POSTFIX]
        if dev_postfix == "_":
            dev_postfix = ""

        # self._dev_device = self._rest_api.get_devicetype()
        self._dev_device = self._rest_item.device

        self._attr_entity_category = self._rest_item.entity_category

        self._attr_unique_id = (
            CONST.DOMAIN
            + "_"
            + self._dev_device
            + "_"
            + self._rest_item.translation_key
        )

        match self._rest_item.format:
            case FORMATS.STATUS | FORMATS.TEXT | FORMATS.TIMESTAMP | FORMATS.SW_VERSION:
                self._divider = 1
            case _:
                # default state class to record all entities by default
                self._attr_state_class = SensorStateClass.MEASUREMENT
                if self._rest_item.params is not None:
                    self._attr_state_class = self._rest_item.params.get(
                        "stateclass", SensorStateClass.MEASUREMENT
                    )
                    self._attr_native_unit_of_measurement = self._rest_item.params.get(
                        "unit", ""
                    )
                    self._attr_native_step = self._rest_item.params.get("step", 1)
                    self._divider = self._rest_item.params.get("divider", 1)
                    self._attr_device_class = self._rest_item.params.get(
                        "deviceclass", None
                    )
                    self._attr_suggested_display_precision = self._rest_item.params.get(
                        "precision", 2
                    )
                    self._attr_native_min_value = self._rest_item.params.get(
                        "min", -999999
                    )
                    self._attr_native_max_value = self._rest_item.params.get(
                        "max", 999999
                    )

        if self._rest_item.params is not None:
            icon = self._rest_item.params.get("icon", None)
            if icon is not None:
                self._attr_icon = icon

    def my_device_info(self) -> DeviceInfo:
        """Build the device info with dynamic values."""
        # Default fallback values
        sw_version = "unknown"
        model = "Judo Device"
        serial_number = "unknown"

        # Try to get real values from coordinator
        if self._coordinator is not None:
            device_info_values = self._coordinator.get_device_info_values()

            if device_info_values["sw_version"]:
                sw_version = str(device_info_values["sw_version"])

            if device_info_values["model"]:
                model = str(device_info_values["model"])

            if device_info_values["serial_number"]:
                serial_number = str(int(device_info_values["serial_number"]))

        return {
            "identifiers": {(CONST.DOMAIN, self._dev_device)},
            "translation_key": self._dev_device,
            "translation_placeholders": self._dev_translation_placeholders,
            "sw_version": sw_version,
            "serial_number": serial_number,
            "model": model,
            "manufacturer": "Judo",
            "suggested_area": "Utility room",
        }

    @property
    def device_info(self) -> DeviceInfo:
        """Return device info."""
        return self.my_device_info()

    @property
    def extra_state_attributes(self):
        """Return the state attributes."""
        attrs = {}

        # Add raw REST API response if available
        if (
            hasattr(self, "_rest_item")
            and self._rest_item
            and self._rest_item.raw_value is not None
        ):
            attrs["raw_value"] = self._rest_item.raw_value

        attrs["address_read"] = self._rest_item.address_read

        return attrs


class MySensorEntity(CoordinatorEntity, SensorEntity, MyEntity):
    """Class that represents a sensor entity.

    Derived from Sensorentity
    and decorated with general parameters from MyEntity
    """

    def __init__(
        self,
        config_entry: MyConfigEntry,
        rest_item: RestItem,
        coordinator: MyCoordinator,
        idx,
    ) -> None:
        """Initialize of MySensorEntity."""
        super().__init__(coordinator, context=idx)
        self.idx = idx
        MyEntity.__init__(self, config_entry, rest_item, coordinator)

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self._attr_native_value = self._rest_item.state
        self.async_write_ha_state()


class MyNumberEntity(CoordinatorEntity, NumberEntity, MyEntity):  # pylint: disable=W0223
    """Represent a Number Entity.

    Class that represents a number entity derived from NumberEntity
    and decorated with general parameters from MyEntity
    """

    def __init__(
        self,
        config_entry: MyConfigEntry,
        rest_item: RestItem,
        coordinator: MyCoordinator,
        idx,
    ) -> None:
        """Initialize NyNumberEntity."""
        super().__init__(coordinator, context=idx)
        self._idx = idx
        MyEntity.__init__(self, config_entry, rest_item, coordinator)

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self._attr_native_value = self._rest_item.state
        self.async_write_ha_state()

    async def async_set_native_value(self, value: float) -> None:
        """Send value over modbus and refresh HA."""
        ro = RestObject(self._rest_api, self._rest_item)
        await ro.setvalue(value)  # rest_item.state will be set inside ro.setvalue
        #        await self._coordinator.get_value(self._rest_item)
        self._attr_native_value = self._rest_item.state
        self.async_write_ha_state()


class MySwitchEntity(CoordinatorEntity, SwitchEntity, MyEntity):  # pylint: disable=W0223
    """Represent a Number Entity.

    Class that represents a number entity derived from NumberEntity
    and decorated with general parameters from MyEntity
    """

    def __init__(
        self,
        config_entry: MyConfigEntry,
        rest_item: RestItem,
        coordinator: MyCoordinator,
        idx,
    ) -> None:
        """Initialize NyNumberEntity."""
        super().__init__(coordinator, context=idx)
        self._idx = idx
        MyEntity.__init__(self, config_entry, rest_item, coordinator)

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self._attr_is_on = self._rest_item.state
        self.async_write_ha_state()

    async def async_turn_on(self, **kwargs):
        """Turn the entity on."""
        ro = RestObject(self._rest_api, self._rest_item)
        await ro.setvalue(1)  # rest_item.state will be set inside ro.setvalue
        self._attr_is_on = self._rest_item.state
        self.async_write_ha_state()

    async def async_turn_off(self, **kwargs):
        """Turn the entity off."""
        ro = RestObject(self._rest_api, self._rest_item)
        await ro.setvalue(0)  # rest_item.state will be set inside ro.setvalue
        self._attr_is_on = self._rest_item.state
        self.async_write_ha_state()


class MyButtonEntity(CoordinatorEntity, ButtonEntity, MyEntity):  # pylint: disable=W0223
    """Represent a Number Entity.

    Class that represents a number entity derived from NumberEntity
    and decorated with general parameters from MyEntity
    """

    def __init__(
        self,
        config_entry: MyConfigEntry,
        rest_item: RestItem,
        coordinator: MyCoordinator,
        idx,
    ) -> None:
        """Initialize NyNumberEntity."""
        super().__init__(coordinator, context=idx)
        self._idx = idx
        MyEntity.__init__(self, config_entry, rest_item, coordinator)

    async def async_press(self):
        """Turn the entity on."""
        ro = RestObject(self._rest_api, self._rest_item)
        await ro.setvalue()  # rest_item.state will be set inside ro.setvalue


class MySelectEntity(CoordinatorEntity, SelectEntity, MyEntity):  # pylint: disable=W0223
    """Class that represents a sensor entity.

    Class that represents a sensor entity derived from Sensorentity
    and decorated with general parameters from MyEntity
    """

    def __init__(
        self,
        config_entry: MyConfigEntry,
        rest_item: RestItem,
        coordinator: MyCoordinator,
        idx,
    ) -> None:
        """Initialze MySelectEntity."""
        super().__init__(coordinator, context=idx)
        self._idx = idx
        MyEntity.__init__(self, config_entry, rest_item, coordinator)

        # option list build from the status list of the ModbusItem
        self.options = []
        for _useless, item in enumerate(self._rest_item.resultlist):
            self.options.append(item.translation_key)

        if self._rest_item.type == TYPES.SELECT_NOIF:
            self._rest_item.state = self.options[0]
            self._attr_current_option = self._rest_item.state
        else:
            self._attr_current_option = "FEHLER"

    async def async_select_option(self, option: str) -> None:
        """Write the selected option to modbus and refresh HA."""
        ro = RestObject(self._rest_api, self._rest_item)
        await ro.addvalue(option)  # rest_item.state will be set inside ro.setvalue
        if self._rest_item.type == TYPES.SELECT_NOIF:
            self._rest_item.state = self.options[0]
            self._attr_current_option = self._rest_item.state
        else:
            self._rest_item.state = option
            self._attr_current_option = self._rest_item.state
        self.async_write_ha_state()

    @callback
    def _handle_coordinator_update(self) -> None:
        """Handle updated data from the coordinator."""
        self._attr_current_option = self._rest_item.state
        self.async_write_ha_state()
