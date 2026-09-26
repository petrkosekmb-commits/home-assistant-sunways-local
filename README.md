# Sunways Local for Home Assistant

[Česky](README.cs.md) | English

Community Home Assistant integration for reading Sunways inverter data directly over the local network, without a Sunways cloud account.

## What it does

- connects directly to a supported inverter or communication dongle;
- automatically discovers the device capabilities exposed by the underlying library;
- creates Home Assistant sensors dynamically;
- supports Czech and English translations;
- offers a configurable polling interval from 10 to 3600 seconds;
- redacts the host address and serial number from diagnostics.

The integration is read-only. It does not change inverter operating modes, export limits or configuration values.

## Requirements

- a compatible Sunways inverter or communication dongle reachable from Home Assistant;
- default connection port `5488` (configurable);
- the Python dependency `sunways==0.0.5`, installed automatically by Home Assistant.

Compatibility depends on the inverter model, dongle and firmware. A successful setup does not by itself prove that the sign of grid-power values matches a specific physical meter.

## Installation

### HACS custom repository

1. In HACS, open **Integrations** and add this repository as a custom repository of type **Integration**.
2. Install **Sunways Local**.
3. Restart Home Assistant.
4. Go to **Settings → Devices & services → Add integration** and search for **Sunways Local**.

### Manual installation

Copy `custom_components/sunways_local` to `/config/custom_components/sunways_local`, restart Home Assistant and add the integration from the user interface.

## Security and privacy

Measurements remain on the local network. The integration does not require Sunways Portal credentials. Place Home Assistant and the inverter on trusted network segments and do not expose inverter ports directly to the internet.

This project is not affiliated with or endorsed by Sunways Technologies.

## Credits and license

The integration uses the MIT-licensed [Chriss-Leo/sunways](https://github.com/Chriss-Leo/sunways) Python library. See [NOTICE](NOTICE) for attribution.

Licensed under the [Apache License 2.0](LICENSE).

## Support the project

If this integration helps you, you will be able to support its maintenance through the donation link published here after the support profile is activated.

