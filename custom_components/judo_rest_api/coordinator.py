"""The Update Coordinator for the RestItems."""

import asyncio
import logging
from datetime import timedelta

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from .configentry import MyConfigEntry
from .const import CONF, FORMATS, TYPES
from .items import RestItem
from .restobject import RestAPI, RestObject

logging.basicConfig()
log = logging.getLogger(__name__)


class MyCoordinator(DataUpdateCoordinator):
    """My custom coordinator."""

    def __init__(
        self,
        hass: HomeAssistant,
        my_api: RestAPI,
        api_items: RestItem,
        p_config_entry: MyConfigEntry,
    ) -> None:
        """Initialize my coordinator."""
        super().__init__(
            hass,
            log,
            # Name of the data. For logging purposes.
            name="judo_rest_api-coordinator",
            # Polling interval. Will only be polled if there are subscribers.
            # update_interval=CONST.SCAN_INTERVAL,
            update_interval=timedelta(
                seconds=int(p_config_entry.data[CONF.SCAN_INTERVAL])
            ),
            # Set always_update to `False` if the data returned from the
            # api can be compared via `__eq__` to avoid duplicate updates
            # being dispatched to listeners
            always_update=True,
        )
        self._rest_api = my_api
        self._device = None
        self._restitems = api_items
        self._number_of_items = len(api_items)
        self._config_entry = p_config_entry

    async def get_value(self, rest_item: RestItem):
        """Read a value from the rest API"""

        if rest_item.type in (TYPES.SELECT_NOIF, TYPES.BUTTON):
            return None
        ro = RestObject(self._rest_api, rest_item)
        if ro is None:
            log.warning("RestObject is None for Item %s", rest_item.translation_key)
            # rest_item.state = None
        else:
            val = await ro.value
            if val is not None:
                log.debug(
                    "Set Value %s for Item %s", str(val), rest_item.translation_key
                )
                rest_item.state = val
            else:
                log.warning("None value for Item %s ignored", rest_item.translation_key)
        return rest_item.state

    def get_value_from_item(self, translation_key: str) -> int:
        """Read a value from another rest item"""
        for _useless, item in enumerate(self._restitems):
            if item.translation_key == translation_key:
                return item.state
        return None

    async def _async_setup(self):
        """Set up the coordinator.

        This is the place to set up your coordinator,
        or to load data, that only needs to be loaded once.

        This method will be called automatically during
        coordinator.async_config_entry_first_refresh.
        """
        # await self._rest_api.login()
        await self._rest_api.connect()

    async def fetch_data(self, idx=None):
        """Fetch all values from the REST."""
        # if idx is not None:
        if idx is None:
            # first run: Update all entitiies
            to_update = tuple(range(len(self._restitems)))
        elif len(idx) == 0:
            # idx exists but is not yet filled up: Update all entitiys.
            to_update = tuple(range(len(self._restitems)))
        else:
            # idx exists and is filled up: Update only entitys requested by the coordinator.
            to_update = idx

        # log.info("Start Scan")
        for index in to_update:
            item = self._restitems[index]
            try:
                await self.get_value(item)
            except Exception:
                log.warning(
                    "connection to Judo Water treatment failed for %s",
                    item.translation_key,
                )

    async def _async_update_data(self):
        """Fetch data from API endpoint.

        This is the place to pre-process the data to lookup tables
        so entities can quickly look up their data.
        """
        try:
            # Note: asyncio.TimeoutError and aiohttp.ClientError are already
            # handled by the data update coordinator.
            async with asyncio.timeout(60):
                # Grab active context variables to limit data required to be fetched from API
                # Note: using context is not required if there is no need or ability to limit
                # data retrieved from API.
                # listening_idx = set(self.async_contexts())
                return await self.fetch_data()  # !!!!!using listening_idx will result in some entities nevwer updated !!!!!
        except Exception:
            log.warning("Error fetching Judo Water treatment data")

    @property
    def rest_api(self):
        """Return rest_api."""
        return self._rest_api
