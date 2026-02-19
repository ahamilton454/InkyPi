# InkyPi Detailed Installation

## Flashing Raspberry Pi OS 

1. Install the Raspberry Pi Imager from the [official download page](https://www.raspberrypi.com/software/)
2. Insert the target SD Card into your computer and launch the Raspberry Pi Imager software
    - Raspberry Pi Device: Choose your Pi model
    - Operating System: Select the recommended system
    - Storage: Select the target SD Card

<img src="./images/raspberry_pi_imager.png" alt="Raspberry Pi Imager" width="500"/>

3. Click Next and choose Edit Settings on the Use OS customization? screen
    - General:
        - Set hostname: enter your desired hostname
            -  This will be used to ssh into the device & access the InkyPi UI on your network.
        - Set username & password
            - Do not use the default username and password on a Raspberry PI as this poses a security risk
        - Configure wireless LAN to your network
            - The InkyPi web server will only be accessible to devices on this network
        - Set local settings to your Time zone
    - Service:
        - Enable SSH:
            - Use password authentication
    - Options: leave default values

<p float="left">
  <img src="./images/raspberry_pi_imager_general.png" width="250" />
  <img src="./images/raspberry_pi_imager_options.png" width="250" /> 
  <img src="./images/raspberry_pi_imager_services.png" width="250" />
</p>

4. Click Yes to apply OS customization options and confirm

## Installing InkyPi

Run the installer from the repository root.

```bash
sudo bash install/install.sh
```

### Waveshare displays

Waveshare installations use a display model identifier.

```bash
sudo bash install/install.sh -W <waveshare_device_model>
```

The installer downloads a matching driver file into `src/display/waveshare_epd/` using the model name (for example, `<waveshare_device_model>.py`) and also downloads `epdconfig.py` into the same directory.

## Updating InkyPi

Use the update script to install system dependencies, upgrade Python packages in the existing virtual environment, refresh the `inkypi` executable, update JS/CSS vendor assets, and restart the systemd service.

```bash
sudo bash install/update.sh
```

The update script requires an existing virtual environment at `/usr/local/inkypi/venv_inkypi`.

### System services configured by the installer

The installer configures these services:

- Enables SPI and I2C.
- Installs and enables `earlyoom`.
- On Raspberry Pi OS Bookworm (version `12`), installs and enables `zramswap` (via `zram-tools`) and writes `/etc/default/zramswap`.
