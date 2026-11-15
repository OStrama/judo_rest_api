"""Config flow."""

from typing import Any
import voluptuous as vol
from homeassistant import config_entries, exceptions
import homeassistant.helpers.config_validation as cv
from .const import CONF, CONST


async def validate_input(data: dict) -> dict[str, Any]:
    """Validate the input."""
    # Validate the data can be used to set up a connection.

    # This is a simple example to show an error in the UI for a short hostname
    # The exceptions are defined at the end of this file, and are used in the
    # `async_step_user` method below.
    if len(data["host"]) < 3:
        raise InvalidHost

    # If your PyPI package is not built with async, pass your methods
    # to the executor:
    # await hass.async_add_executor_job(
    #     your_validate_func, data["username"], data["password"]
    # )

    # If you cannot connect:
    # throw CannotConnect
    # If the authentication is wrong:
    # InvalidAuth

    # Return info that you want to store in the config entry.
    # "Title" is what is displayed to the user for this hub device
    # It is stored internally in HA as part of the device config.
    # See `async_step_user` below for how this is used
    return {"title": data["host"]}


class ConfigFlow(config_entries.ConfigFlow, domain=CONST.DOMAIN):  # pylint: disable=W0223
    """Class config flow."""

    VERSION = 2

    async def async_step_user(self, user_input=None) -> config_entries.ConfigFlowResult:
        """Step for setup process."""
        # This goes through the steps to take the user through the setup process.
        # Using this it is possible to update the UI and prompt for additional
        # information. This example provides a single form (built from `DATA_SCHEMA`),
        # and when that has some validated input, it calls `async_create_entry` to
        # actually create the HA config entry. Note the "title" value is returned by
        # `validate_input` above.

        # DATA_SCHEMA = vol.Schema({("host"): str, ("port"): cv.port})
        # The caption comes from strings.json / translations/en.json.
        # strings.json can be processed into en.json with some HA commands.
        # did not find out how this works yet.
        data_schema = vol.Schema(
            schema={
                vol.Required(schema=CONF.HOST): str,
                vol.Optional(schema=CONF.PORT, default="80"): cv.port,
                vol.Optional(schema=CONF.USERNAME, default="admin"): str,
                vol.Optional(schema=CONF.PASSWORD, default="Connectivity"): str,
                vol.Optional(schema=CONF.DEVICE_POSTFIX, default=""): str,
                vol.Optional(schema=CONF.SCAN_INTERVAL, default="60"): str,
            }
        )

        errors = {}
        info = None
        if user_input is not None:
            try:
                info = await validate_input(data=user_input)

                return self.async_create_entry(title=info["title"], data=user_input)

            except Exception:  # noqa: BLE001
                errors["base"] = "unknown error"

        # If there is no user input or there were errors, show the form again,
        # #including any errors that were found with the input.
        return self.async_show_form(
            step_id="user",
            data_schema=data_schema,
            errors=errors,
            description_placeholders={
                CONF.HOST: "host",
                CONF.PORT: "port",
                CONF.USERNAME: "username",
                CONF.PASSWORD: "password",
                CONF.DEVICE_POSTFIX: "Device-Postfix",
                CONF.SCAN_INTERVAL: "scan_interval",
            },
        )

    async def async_step_reconfigure(
        self, user_input: dict[str, Any] | None = None
    ) -> config_entries.ConfigFlowResult:
        """Trigger a reconfiguration flow."""
        errors: dict[str, str] = {}
        reconfigure_entry: config_entries.ConfigEntry[Any] = (
            self._get_reconfigure_entry()
        )

        if user_input:
            return self.async_update_reload_and_abort(
                entry=reconfigure_entry, data_updates=user_input
            )

        schema_reconfigure = vol.Schema(
            schema={
                vol.Required(
                    schema=CONF.HOST, default=reconfigure_entry.data[CONF.HOST]
                ): str,
                vol.Optional(
                    schema=CONF.PORT, default=reconfigure_entry.data[CONF.PORT]
                ): cv.port,
                vol.Optional(
                    schema=CONF.USERNAME, default=reconfigure_entry.data[CONF.USERNAME]
                ): str,
                vol.Optional(
                    schema=CONF.PASSWORD, default=reconfigure_entry.data[CONF.PASSWORD]
                ): str,
                # reconfigure of device postfix leads to duplicated devices
                vol.Optional(
                    schema=CONF.DEVICE_POSTFIX,
                    default=reconfigure_entry.data[CONF.DEVICE_POSTFIX],
                ): str,
                vol.Optional(
                    schema=CONF.SCAN_INTERVAL,
                    default=reconfigure_entry.data[CONF.SCAN_INTERVAL],
                ): str,
            }
        )

        return self.async_show_form(
            step_id="reconfigure",
            data_schema=schema_reconfigure,
            errors=errors,
            description_placeholders={
                CONF.HOST: "host",
                CONF.PORT: "port",
                CONF.USERNAME: "username",
                CONF.PASSWORD: "password",
                CONF.DEVICE_POSTFIX: "Device-Postfix",
                CONF.SCAN_INTERVAL: "scan_interval",
            },
        )


class InvalidHost(exceptions.HomeAssistantError):
    """Error to indicate there is an invalid hostname."""


class ConnectionFailed(exceptions.HomeAssistantError):
    """Error to indicate there is an invalid hostname."""
