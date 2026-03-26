# InkyPi

A Raspberry Pi-powered e-paper dashboard for calm, glanceable information displays.
<img src="./docs/images/inky_clock.jpg" />
## Contents
- [About InkyPi](#about-inkypi)
- [Hardware](#hardware)
- [Installation](#installation)
- [Getting Started](#getting-started)
- [Updating InkyPi](#updating-inkypi)
- [Uninstalling InkyPi](#uninstalling-inkypi)
- [Waveshare Display Support](#waveshare-display-support)
- [Roadmap](#roadmap)
- [License](#license)
- [Issues](#issues)
- [Sponsoring](#sponsoring)
- [Acknowledgements](#acknowledgements)


## About InkyPi 
InkyPi is an open-source, customizable e-paper display platform powered by a Raspberry Pi. It is designed to be easy to install and flexible to extend, so it can display the information that matters most on a calm, glanceable screen controlled through a simple web interface.

### Key features
- Natural, paper-like aesthetic with crisp, minimalist visuals that are easy on the eyes and have no glare or backlight.
- Web-based configuration interface that runs in the browser on any device on the local network.
- Minimal distractions: no LEDs, fan noise, or pop-up notifications—only the content that matters.
- Straightforward installation and configuration, suitable for both first-time Raspberry Pi users and experienced makers.
- Fully open-source design that encourages modification, customization, and the creation of new plugins.
- Support for scheduled playlists so different plugins can appear at different times of day.

### Built-in plugins

- Image Upload: upload and display static images directly from a browser.
- Daily Newspaper/Comic: display daily comics and front pages from major newspapers around the world.
- Clock: configurable clock faces for displaying the current time.
- AI Image/Text: generate images and dynamic text from prompts using AI models.
- Weather: display current conditions and multi-day forecasts with configurable layouts.
- Calendar: display calendars from services such as Google, Outlook, or Apple Calendar with customizable layouts.

Additional plugins are planned. For documentation on creating custom plugins, see [Building InkyPi Plugins](./docs/building_plugins.md).

See [the wiki](https://github.com/fatihak/InkyPi/wiki) for a list of community-maintained third-party plugins.

## Hardware
The list below covers the minimum hardware required to run InkyPi comfortably.
- Raspberry Pi 4, 3, or Zero 2 W
    - A 40-pin pre-soldered header is recommended for easier assembly.
- MicroSD Card (min 8 GB) like [this one](https://amzn.to/3G3Tq9W)
- E-Ink Display:
    - Inky Impression by Pimoroni
        - **[13.3 Inch Display](https://collabs.shop/q2jmza)**
        - **[7.3 Inch Display](https://collabs.shop/q2jmza)**
        - **[5.7 Inch Display](https://collabs.shop/ns6m6m)**
        - **[4 Inch Display](https://collabs.shop/cpwtbh)**
    - Inky wHAT by Pimoroni
        - **[4.2 Inch Display](https://collabs.shop/jrzqmf)**
    - Waveshare e-Paper Displays
        - Spectra 6 (E6) Full Color **[4 inch](https://www.waveshare.com/4inch-e-paper-hat-plus-e.htm?&aff_id=111126)** **[7.3 inch](https://www.waveshare.com/7.3inch-e-paper-hat-e.htm?&aff_id=111126)** **[13.3 inch](https://www.waveshare.com/13.3inch-e-paper-hat-plus-e.htm?&aff_id=111126)**
        - Black and White **[7.5 inch](https://www.waveshare.com/7.5inch-e-paper-hat.htm?&aff_id=111126)** **[13.3 inch](https://www.waveshare.com/13.3inch-e-paper-hat-k.htm?&aff_id=111126)**
        - See [Waveshare e-paper displays](https://www.waveshare.com/product/raspberry-pi/displays/e-paper.htm?&aff_id=111126) or visit their [Amazon store](https://amzn.to/3HPRTEZ) for additional models. Note that some models like the IT8951 based displays are not supported. See later section on [Waveshare e-Paper](#waveshare-display-support) compatibility for more information.
- Picture frame or 3D-printed stand
    - See [community.md](./docs/community.md) for example 3D models, custom builds, and other submissions from the community.

**Disclosure:** The hardware links above are affiliate links. Purchases made through them may generate a commission at no additional cost and help support ongoing maintenance and development of this project.

## Installation
These instructions assume Raspberry Pi OS is already installed on the microSD card.
To install InkyPi on a Raspberry Pi, follow these steps on a system running Raspberry Pi OS:

1. Clone the repository:
    ```bash
    git clone https://github.com/fatihak/InkyPi.git
    ```
2. Navigate to the project directory:
    ```bash
    cd InkyPi
    ```
3. Run the installation script with sudo:
    ```bash
    sudo bash install/install.sh [-W <waveshare device model>]
    ``` 
Install script options (advanced):
    
* `-W <waveshare device model>` — specify this parameter **only** when installing for a Waveshare display. After `-W`, provide the Waveshare device model (for example, `epd7in3f`).

For Pimoroni Inky displays, use:
    ```bash
    sudo bash install/install.sh
    ```

For compatible Waveshare displays (see [Waveshare Display Support](#waveshare-display-support)), use:
    ```bash
    sudo bash install/install.sh -W epd7in3f
    ```


After installation completes, the script prompts for a reboot. Once the system restarts, the display updates to show the InkyPi splash screen.

Notes and prerequisites:
- The installation script requires sudo privileges to install and run the service, and it is recommended to start with a fresh installation of Raspberry Pi OS to avoid conflicts with existing software or configurations.
- The installation process automatically enables the required SPI and I2C interfaces on the Raspberry Pi.

For more details, including instructions on how to image your microSD with Raspberry Pi OS, refer to [installation.md](./docs/installation.md). You can also checkout [this YouTube tutorial](https://youtu.be/L5PvQj1vfC4).
## Getting Started
This section describes how to access the web interface and configure a simple first dashboard.

After installation and reboot, InkyPi runs as a background service on the Raspberry Pi and periodically refreshes the connected display.

To begin using InkyPi through the web interface, follow these steps:

1. Ensure the Raspberry Pi and the device used to control it are connected to the same local network.
2. Open a web browser on your laptop, tablet, or phone.
3. Navigate to the InkyPi web interface using the Raspberry Pi hostname (for example, inkypi.local) or its IP address.

From the web interface, the following actions are available:

- Enable and configure plugins such as Clock, Weather, Calendar, Image Upload, and AI Image/Text.
- Arrange plugins into playlists so different content is shown at different times of day.
- Adjust layout options so that information appears clearly on the chosen display size and orientation.

For example, a common setup uses a playlist that shows a calendar view during working hours and switches to a minimalist clock in the evening.

### Example: Workday dashboard

As a simple starting point, the following configuration works well for a general-purpose workday display:

1. Enable the Calendar plugin and connect it to a calendar account.
2. Enable the Weather plugin and choose a compact layout.
3. Create a playlist that shows the calendar view during typical working hours and switches to a large clock in the evening.
4. Set the playlist as the active schedule for the display.

## Updating InkyPi
To update an existing InkyPi installation with the latest code and configuration changes, follow these steps:
1. Navigate to the project directory on the Raspberry Pi:
    ```bash
    cd InkyPi
    ```
2. Fetch the latest changes from the repository:
    ```bash
    git pull
    ```
3. Run the update script with sudo:
    ```bash
    sudo bash install/update.sh
    ```
This process applies new code changes and any additional dependencies without requiring a full reinstallation.

Configuration files and saved playlists are preserved during the update process.

## Uninstalling InkyPi
To uninstall InkyPi and remove the installed services from the Raspberry Pi, run the following command:

```bash
sudo bash install/uninstall.sh
```

This removes the InkyPi service and related files from the system. Any content created through the web interface (such as uploaded images) may also be removed, so important data should be backed up first.

## Roadmap
The InkyPi project is actively developed, with many features and improvements planned for future releases.

- Expanded plugin library with more data sources and visualizations.
- Modular layouts to mix and match plugins on the same screen.
- Support for physical buttons with customizable action bindings.
- Improved web UI, including a better experience on mobile devices.

Check out the public [trello board](https://trello.com/b/SWJYWqe4/inkypi) to explore upcoming features and vote on what you'd like to see next!

## Waveshare Display Support
This section summarizes which Waveshare e-paper displays work well with InkyPi and how to select the correct driver.

Waveshare offers a range of e-Paper displays, similar to the Inky screens from Pimoroni, but with slightly different requirements. While Inky displays auto-configure via the inky Python library, Waveshare displays require model-specific drivers from their [Python EPD library](https://github.com/waveshareteam/e-Paper/tree/master/RaspberryPi_JetsonNano/python/lib/waveshare_epd).

This project has been tested with several Waveshare models and follows the general guidance below.
**Displays based on the IT8951 controller are not supported**, and **screens smaller than 4 inches are not recommended** due to limited resolution.
If a display model has a corresponding driver in the library linked above, it is likely to be compatible. When running the installation script, use the `-W` option to specify the display model (without the .py extension); the script will fetch and install the corresponding driver.

## License
This project is distributed under the GPL 3.0 license; see [LICENSE](./LICENSE) for details.
This project also includes fonts and icons with separate licensing and attribution requirements; see [Attribution](./docs/attribution.md) for details.

## Issues

Check out the [troubleshooting guide](./docs/troubleshooting.md). If you're still having trouble, feel free to create an issue on the [GitHub Issues](https://github.com/fatihak/InkyPi/issues) page.

If a Pi Zero W is used, note that there are known issues during the installation process. See the [Known Issues during Pi Zero W Installation](./docs/troubleshooting.md#known-issues-during-pi-zero-w-installation) section in the troubleshooting guide for additional details.

## Sponsoring
InkyPi is maintained and developed with the help of individual and organizational sponsors.
If the project is useful, consider supporting its continued development.

<p align="center">
<a href="https://github.com/sponsors/fatihak" target="_blank"><img src="https://user-images.githubusercontent.com/345274/133218454-014a4101-b36a-48c6-a1f6-342881974938.png" alt="Become a Patreon" height="35" width="auto"></a>
<a href="https://www.patreon.com/akzdev" target="_blank"><img src="https://c5.patreon.com/external/logo/become_a_patron_button.png" alt="Become a Patreon" height="35" width="auto"></a>
<a href="https://www.buymeacoffee.com/akzdev" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/default-orange.png" alt="Buy Me A Coffee" height="35" width="auto"></a>
</p>


## Acknowledgements

InkyPi builds on and is inspired by the following projects and contributors:
- Shout out to @txoof for assisting with the InkyPi installation process.
- [InkyCal](https://github.com/aceinnolab/Inkycal) - has modular plugins for building custom dashboards
- [PiInk](https://github.com/tlstommy/PiInk) - inspiration behind InkyPi's flask web ui
- [rpi_weather_display](https://github.com/sjnims/rpi_weather_display) - alternative eink weather dashboard with advanced power efficiency
