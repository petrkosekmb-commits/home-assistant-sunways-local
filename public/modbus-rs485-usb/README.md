# Sunways: direct RS485–USB connection to Home Assistant

[Česky](README.cs.md)

This folder shares a configuration for Home Assistant's built-in **Modbus** integration. It is based on Petr Kosek's home installation and a configuration backup dated 21 October 2026.

## Connection

`Sunways → RS485 → RS485–USB adapter (FTDI) → Home Assistant`

Home Assistant originally ran on a Raspberry Pi. It now runs in a Proxmox virtual machine with the USB adapter passed through to that VM. Data is read locally using **Modbus RTU**, without a cloud account.

This is a separate Modbus YAML configuration. It is not the implementation of the network-based Sunways Local integration in the parent repository.

## Files

- [sunways-readonly.yaml](sunways-readonly.yaml): the recommended starting example, containing sensor reads only. It excludes switches, automations and scripts that write to the inverter.
The full home configuration containing inverter controls and operational automations is not published here.

The local IP address was removed and the specific USB adapter identifier was replaced with a placeholder. Blank lines were normalized. The original attribution to Jan Jirousek dated 25 January 2024 was retained. The read register map is retained; control sections, templates and operational automations are omitted.

## Settings used in this installation

| Setting | Value |
| --- | --- |
| Transport | Modbus RTU over a serial USB port |
| Baud rate | 9600 |
| Data bits | 8 |
| Parity | none (`N`) |
| Stop bits | 1 |
| Inverter address (`slave`) | 247 |
| Example port | `/dev/serial/by-id/usb-YOUR_RS485_ADAPTER-if00-port0` |

These values describe one installation, not universal settings for every Sunways inverter. Verify your inverter model, firmware, address and register map.

## Using the read-only version

1. Back up your HA configuration. Find your actual USB adapter path in HA's hardware listing and replace the `port` placeholder. For a VM, first ensure USB passthrough to HA.
2. If HA packages are already enabled, place the file at a path such as `/config/packages/sunways-readonly.yaml`. Otherwise, enable packages by merging this into the existing `configuration.yaml` section:

```yaml
homeassistant:
  packages: !include_dir_named packages
```

Do not create a second `homeassistant:` section. The sample already contains its own top-level `modbus:` key; do not include it unchanged beneath `modbus: !include ...`.

3. Avoid duplicate `sunways` hubs, duplicate `unique_id` values and multiple readers of the same serial port.
4. Check the HA configuration, resolve any schema differences in your HA version, and only then restart.
5. Verify live sensor updates and compare values against the inverter display. Grid and battery power signs must be checked for each installation.

This is a shared example from an existing installation, not a universally tested installation package. Some original schema options may differ between HA versions.

## RS485–TCP adapters such as USR-DR134

The published configuration uses **USB**, not a USR-DR134. Its register map may be useful, but it is not a ready, tested configuration for that network adapter.

A network adapter requires checking its mode, IP address and port, as well as the matching HA transport (Modbus TCP versus RTU carried over TCP). Simply replacing a serial port with an IP address is insufficient. USR-DR134 compatibility with this configuration or the network-based Sunways Local integration has not been verified.
