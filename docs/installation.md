# InkyPi Detailed Installation

## Debian package requirements

The installer relies on the following Debian packages (see [`install/debian-requirements.txt`](../install/debian-requirements.txt)):

- `libtiff-dev`
- `python3`
- `python3-venv`
- `python3-pip`
- `avahi-daemon`
- `libopenblas-dev`
- `libopenjp2-7`
- `chromium-headless-shell`
- `libfreetype6-dev`
- `fonts-noto-color-emoji`
- `swig`
- `liblgpio-dev`
- `libheif-dev`
- `jq`

## Service management (systemd)

InkyPi installs a systemd unit that starts the application with:

```text
/usr/local/bin/inkypi run
```

The unit file is located at [`install/inkypi.service`](../install/inkypi.service).

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
