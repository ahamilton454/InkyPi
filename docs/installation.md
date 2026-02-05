# InkyPi Andrew Detailed Installation

## Overview

This document describes the Raspberry Pi OS imaging workflow used to prepare a Raspberry Pi for an InkyPi installation.

## Flashing Raspberry Pi OS

1. Install the Raspberry Pi Imager from the [official download page](https://www.raspberrypi.com/software/).
2. Insert the target SD card into the workstation and launch Raspberry Pi Imager.
3. Configure the image settings:
   - Raspberry Pi Device: Select the Pi model.
   - Operating System: Select the recommended system.
   - Storage: Select the target SD card.

<img src="./images/raspberry_pi_imager.png" alt="Raspberry Pi Imager" width="500"/>

4. Select **Next**, then select **Edit Settings** on the **Use OS customization?** screen.
   - General:
     - Set hostname.
       - This hostname is used for SSH and for the InkyPi UI hostname on the local network.
     - Set username and password.
       - Do not use default credentials.
     - Configure wireless LAN.
       - The InkyPi web server is accessible only on this network.
     - Set local settings (time zone).
   - Service:
     - Enable SSH.
       - Use password authentication.
   - Options: Keep default values.

<p float="left">
  <img src="./images/raspberry_pi_imager_general.png" width="250" />
  <img src="./images/raspberry_pi_imager_options.png" width="250" />
  <img src="./images/raspberry_pi_imager_services.png" width="250" />
</p>

5. Select **Yes** to apply OS customization options and confirm.

## Debian package prerequisites

The installer references `install/debian-requirements.txt` for Debian packages to install.

Package list:

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
