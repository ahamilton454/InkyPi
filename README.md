# InkyPi 

<img src="./docs/images/inky_clock.jpg" />


## About InkyPi 
InkyPi is an open source, customizable E Ink display powered by a Raspberry Pi. It keeps setup simple and flexible, making it easy to show the content that matters most with a straightforward web interface for setup and configuration.

**Features**:
- Natural paper like aesthetic: crisp, minimalist visuals that are easy on the eyes, with no glare or backlight
- Web interface lets the display update and configure from any device on the network
- Minimize distractions: no LEDs, noise, or notifications, just the content that matters
- Easy installation and configuration that welcomes beginners and makers alike
- Open source project that makes it simple to modify, customize, and create plugins
- Set up scheduled playlists to show different plugins at designated times

**Plugins**:

- Image Upload: Upload and display any image from the browser
- Daily Newspaper/Comic: Show daily comics and front pages from major newspapers around the world
- Clock: Choose customizable clock faces for displaying time
- AI Image/Text: Generate images and dynamic text from prompts using OpenAI's models
- Weather: Display current weather conditions and multi day forecasts with a customizable layout
- Calendar: View a calendar from Google, Outlook, or Apple Calendar with customizable layouts

Additional plugins are coming soon. For documentation on building custom plugins, see [Building InkyPi Plugins](./docs/building_plugins.md).

See [the wiki](https://github.com/fatihak/InkyPi/wiki) for a list of community maintained third party plugins.

## Hardware 
- Raspberry Pi (4 | 3 | Zero 2 W)
    - Recommended: 40 pin pre soldered header
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
        - See [Waveshare e-paper displays](https://www.waveshare.com/product/raspberry-pi/displays/e-paper.htm?&aff_id=111126) or visit their [Amazon store](https://amzn.to/3HPRTEZ) for additional models. Note that some models, such as IT8951 based displays, are not supported. See the later section on [Waveshare e-Paper](#waveshare-display-support) compatibility for more information.
- Picture Frame or 3D Stand
    - See [community.md](./docs/community.md) for 3D models, custom builds, and other community submissions

**Disclosure:** The links above are affiliate links. They may provide a commission from qualifying purchases, at no extra cost, which helps support maintenance and development for this project.

## Installation
To install InkyPi, follow these steps:

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
     Option: 
    
    * -W \<waveshare device model\> - specify this parameter **ONLY** if installing for a Waveshare display.  After the -W option specify the Waveshare device model e.g. epd7in3f.

    e.g. for Inky displays use:
    ```bash
    sudo bash install/install.sh
    ```

    and for [Waveshare displays](#waveshare-display-support) use:
    ```bash
    sudo bash install/install.sh -W epd7in3f
    ```


After installation completes, the script prompts for a Raspberry Pi reboot. Once the system reboots, the display updates to show the InkyPi splash screen.

Note: 
- The installation script requires sudo privileges to install and run the service. A fresh installation of Raspberry Pi OS helps avoid potential conflicts with existing software or configurations.
- The installation process automatically enables the required SPI and I2C interfaces on the Raspberry Pi.

For more details, including instructions for imaging the microSD with Raspberry Pi OS, refer to [installation.md](./docs/installation.md). It also helps to check out [this YouTube tutorial](https://youtu.be/L5PvQj1vfC4).

## Update
To update InkyPi with the latest changes, follow these steps:
1. Navigate to the project directory:
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
This process applies new updates and additional dependencies without requiring a full reinstallation.

## Uninstall
To uninstall InkyPi, run the following command:

```bash
sudo bash install/uninstall.sh
```

## Roadmap
The InkyPi project continues to grow, with more features and improvements planned ahead.

- Plugins, plugins, plugins
- Modular layouts to mix and match plugins
- Support for buttons with customizable action bindings
- Improved Web UI on mobile devices

Check out the public [trello board](https://trello.com/b/SWJYWqe4/inkypi) to explore upcoming features and vote on future priorities.

## Waveshare Display Support

Waveshare offers a range of e-Paper displays similar to the Inky screens from Pimoroni, but with slightly different requirements. Inky displays auto configure through the inky Python library, while Waveshare displays require model specific drivers from their [Python EPD library](https://github.com/waveshareteam/e-Paper/tree/master/RaspberryPi_JetsonNano/python/lib/waveshare_epd).

This project has been tested with several Waveshare models. **Displays based on the IT8951 controller are not supported**, and **screens smaller than 4 inches are not recommended** because of limited resolution.

If the display model has a corresponding driver in the link above, it is likely compatible. When running the installation script, use the -W option to specify the display model (without the .py extension). The script automatically fetches and installs the correct driver.

## License

InkyPi is distributed under the GPL 3.0 License. See [LICENSE](./LICENSE) for more information.

This project includes fonts and icons with separate licensing and attribution requirements. See [Attribution](./docs/attribution.md) for details.

## Issues

Check out the [troubleshooting guide](./docs/troubleshooting.md). If more help is needed, open an issue on the [GitHub Issues](https://github.com/fatihak/InkyPi/issues) page.

If using a Pi Zero W, note that known issues can appear during installation. See the [Known Issues during Pi Zero W Installation](./docs/troubleshooting.md#known-issues-during-pi-zero-w-installation) section in the troubleshooting guide for additional details.

## Sponsoring

InkyPi is maintained and developed with the help of sponsors. If the project proves useful, consider supporting its continued development.

<p align="center">
<a href="https://github.com/sponsors/fatihak" target="_blank"><img src="https://user-images.githubusercontent.com/345274/133218454-014a4101-b36a-48c6-a1f6-342881974938.png" alt="Become a Patreon" height="35" width="auto"></a>
<a href="https://www.patreon.com/akzdev" target="_blank"><img src="https://c5.patreon.com/external/logo/become_a_patron_button.png" alt="Become a Patreon" height="35" width="auto"></a>
<a href="https://www.buymeacoffee.com/akzdev" target="_blank"><img src="https://cdn.buymeacoffee.com/buttons/default-orange.png" alt="Buy Me A Coffee" height="35" width="auto"></a>
</p>


## Acknowledgements

These similar projects are also worth a look:

- [PaperPi](https://github.com/txoof/PaperPi) - helpful project that supports Waveshare devices
    - Thanks to @txoof for assisting with the InkyPi installation process
- [InkyCal](https://github.com/aceinnolab/Inkycal) - modular plugins for building custom dashboards
- [PiInk](https://github.com/tlstommy/PiInk) - inspiration behind InkyPi's Flask web UI
- [rpi_weather_display](https://github.com/sjnims/rpi_weather_display) - alternative E Ink weather dashboard with advanced power efficiency
