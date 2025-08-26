"""Item classes."""

from .const import DeviceConstants, FormatConstants, TypeConstants


class StatusItem:
    """An item of a status, e.g. error code and error text along with a precise description.

    A class is intentionally defined here because the assignment via dictionaries would not work so elegantly in the end,
    especially when searching backwards. (At least I don't know how...)
    """

    def __init__(
        self,
        number: int,
        translation_key: str | None = None,
    ) -> None:
        """Initialise StatusItem."""
        self._number = number
        self._translation_key = translation_key

    @property
    def number(self) -> int:
        """Return number."""
        return self._number

    @number.setter
    def number(self, value: int) -> None:
        """Set number."""
        self._number = value

    @property
    def translation_key(self) -> str:
        """Return translation_key."""
        return self._translation_key

    @translation_key.setter
    def translation_key(self, val: str) -> None:
        """Set translation_key."""
        self._translation_key = val


class RestItem:
    """Class ApiIem item.

    This can either be a RestItem or a WebifItem
    """

    def __init__(
        self,
        translation_key: str,
        mformat: FormatConstants,
        mtype: TypeConstants,
        device: DeviceConstants,
        address_read: int = None,
        read_index=0,
        read_bytes=1,
        address_write: int = None,
        write_index=0,
        write_bytes=1,
        resultlist=None,
        params: dict = None,
    ) -> None:
        """Initialise RestItem."""
        self._translation_key = translation_key
        self._address_read = address_read
        self._read_index = read_index
        self._read_bytes = read_bytes
        self._address_write = address_write
        self._write_index = write_index
        self._write_bytes = write_bytes
        self._format = mformat
        self._type = mtype
        self._device = device
        self._resultlist = resultlist
        self._params = params
        self._state = None
        self._raw_value = None

    @property
    def params(self) -> dict:
        """Return state."""
        return self._params

    @params.setter
    def params(self, val: dict):
        self._params = val

    @property
    def state(self):
        """Return the state of the item set by restobject."""
        return self._state

    @state.setter
    def state(self, val):
        """Set the state of the item from rest."""
        self._state = val

    @property
    def format(self) -> FormatConstants:
        """Return format."""
        return self._format

    @property
    def type(self):
        """Return type."""
        return self._type

    @property
    def device(self) -> DeviceConstants:
        """Return device."""
        return self._device

    @device.setter
    def device(self, val: DeviceConstants):
        """Return device."""
        self._device = val

    @property
    def raw_value(self):
        """Return the raw value from REST API."""
        return self._raw_value

    @raw_value.setter
    def raw_value(self, val):
        """Set the raw value from REST API."""
        self._raw_value = val

    @property
    def translation_key(self) -> str:
        """Return translation_key."""
        return self._translation_key

    @translation_key.setter
    def translation_key(self, val: str) -> None:
        """Set translation_key."""
        self._translation_key = val

    @property
    def resultlist(self):
        """Return resultlist."""
        return self._resultlist

    def get_translation_key_from_number(self, val: int) -> str:
        """Get errortext from coresponding number."""
        if val is None:
            return None
        if self._resultlist is None:
            return None
        for _useless, item in enumerate(self._resultlist):
            if val == item.number:
                return item.translation_key
        return "unbekannt <" + str(val) + ">"

    def get_number_from_translation_key(self, val: str) -> int:
        """Get number of coresponding errortext."""
        if val is None:
            return None
        if self._resultlist is None:
            return None
        for _useless, item in enumerate(self._resultlist):
            if val == item.translation_key:
                return item.number
        return -1

    @property
    def address_read(self) -> int:
        """Return address."""
        return self._address_read

    @address_read.setter
    def address_read(self, val: int):
        """Set address."""
        self._address_read = val

    @property
    def read_index(self) -> int:
        """Return address."""
        return self._read_index

    @read_index.setter
    def read_index(self, val: int):
        """Set address."""
        self._read_index = val

    @property
    def read_bytes(self) -> int:
        """Return address."""
        return self._read_bytes

    @read_bytes.setter
    def read_bytes(self, val: int):
        """Set address."""
        self._read_bytes = val

    @property
    def address_write(self) -> int:
        """Return address."""
        return self._address_write

    @address_write.setter
    def address_write(self, val: int):
        """Set address."""
        self._address_write = val

    @property
    def write_index(self) -> int:
        """Return address."""
        return self._write_index

    @write_index.setter
    def write_index(self, val: int):
        """Set address."""
        self._write_index = val

    @property
    def write_bytes(self) -> int:
        """Return address."""
        return self._write_bytes

    @write_bytes.setter
    def write_bytes(self, val: int):
        """Set address."""
        self._write_bytes = val
