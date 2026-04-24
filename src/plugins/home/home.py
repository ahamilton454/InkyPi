"""
Dashboard Plugin for InkyPi
Displays a composite layout with weather, calendar, NASA APOD, and timestamp
"""

from plugins.base_plugin.base_plugin import BasePlugin
from PIL import Image, ImageDraw, ImageFont
from utils.app_utils import resolve_path
import requests
import logging
from datetime import datetime, timedelta, timezone
import pytz
import icalendar
import recurring_ical_events
from io import BytesIO
import math
import os
from random import randint

logger = logging.getLogger(__name__)

# Open-Meteo API URLs (Free, no API key needed!)
OPEN_METEO_FORECAST_URL = "https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={long}&hourly=temperature_2m,weathercode,precipitation_probability&daily=weathercode,temperature_2m_max,temperature_2m_min,precipitation_probability_max,sunrise,sunset&current_weather=true&timezone=auto&forecast_days=3"

# Weather code to human-readable description
WEATHER_DESCRIPTIONS = {
    0: "Clear", 1: "Mostly Clear", 2: "Partly Cloudy", 3: "Overcast",
    45: "Foggy", 48: "Icy Fog",
    51: "Light Drizzle", 53: "Drizzle", 55: "Heavy Drizzle",
    56: "Freezing Drizzle", 57: "Heavy Freezing Drizzle",
    61: "Light Rain", 63: "Rain", 65: "Heavy Rain",
    66: "Freezing Rain", 67: "Heavy Freezing Rain",
    71: "Light Snow", 73: "Snow", 75: "Heavy Snow",
    77: "Snow Grains", 80: "Light Showers", 81: "Showers", 82: "Heavy Showers",
    85: "Light Snow Showers", 86: "Heavy Snow Showers",
    95: "Thunderstorm", 96: "Thunderstorm w/ Hail", 99: "Heavy Thunderstorm",
}
OPEN_METEO_AIR_QUALITY_URL = "https://air-quality-api.open-meteo.com/v1/air-quality?latitude={lat}&longitude={long}&hourly=uv_index&timezone=auto&forecast_days=3"
OPEN_METEO_UNIT_PARAMS = {
    "metric": "temperature_unit=celsius&wind_speed_unit=ms",
    "imperial": "temperature_unit=fahrenheit&wind_speed_unit=mph"
}

UNITS = {
    "metric": {"temperature": "°C"},
    "imperial": {"temperature": "°F"}
}


class Home(BasePlugin):
    def generate_settings_template(self):
        template_params = super().generate_settings_template()
        template_params['api_key'] = {
            "required": True,
            "service": "NASA",
            "expected_key": "NASA_SECRET"
        }
        return template_params

    def generate_image(self, settings, device_config):
        """Generate the complete dashboard composite image"""
        logger.info("Dashboard plugin: Starting image generation")

        # Get device configuration
        dimensions = device_config.get_resolution()
        if device_config.get_config("orientation") == "vertical":
            dimensions = dimensions[::-1]

        timezone_str = device_config.get_config("timezone", default="America/New_York")
        time_format = device_config.get_config("time_format", default="12h")
        tz = pytz.timezone(timezone_str)

        # Create blank canvas
        width, height = dimensions
        canvas = Image.new('RGB', (width, height), '#f8f8f8')

        # Define regions
        left_width = width // 2
        right_width = width - left_width
        weather_height = height // 2
        nasa_height = height - weather_height
        timestamp_height = max(40, height // 8)
        calendar_height = height - timestamp_height

        # Track if any section succeeded
        any_success = False

        # 1. Generate weather section (top left: 400x240)
        logger.info("Fetching weather data...")
        try:
            lat = settings.get('latitude')
            long = settings.get('longitude')
            if not lat or not long:
                raise RuntimeError("Location not configured. Please set latitude and longitude in settings.")

            units = settings.get('units', 'metric')
            if units not in ['metric', 'imperial']:
                raise RuntimeError("Invalid temperature units.")

            weather_img = self.generate_weather_section(
                lat, long, units, (left_width, weather_height), tz, time_format
            )
            canvas.paste(weather_img, (0, 0))
            any_success = True
            logger.info("Weather section generated successfully")
        except Exception as e:
            error_msg = f"Weather Error:\n{str(e)}"
            logger.error(f"Failed to generate weather section: {str(e)}")
            error_img = self.generate_error_section(
                (left_width, weather_height), "Weather", str(e)
            )
            canvas.paste(error_img, (0, 0))

        # 2. Generate NASA APOD section (bottom left: 400x240)
        logger.info("Fetching NASA APOD...")
        try:
            nasa_img = self.generate_nasa_section(
                settings, device_config, (left_width, nasa_height)
            )
            canvas.paste(nasa_img, (0, weather_height))
            any_success = True
            logger.info("NASA section generated successfully")
        except Exception as e:
            error_msg = f"NASA Error:\n{str(e)}"
            logger.error(f"Failed to generate NASA section: {str(e)}")
            error_img = self.generate_error_section(
                (left_width, nasa_height), "NASA APOD", str(e)
            )
            canvas.paste(error_img, (0, weather_height))

        # 3. Generate calendar section (right side top: 400x420)
        logger.info("Fetching calendar events...")
        try:
            calendar_urls = settings.get('calendarURLs[]')
            calendar_colors = settings.get('calendarColors[]')

            # Backwards compatibility for old single-URL setting
            if not calendar_urls:
                single_url = settings.get('calendarURL')
                if not single_url:
                    raise RuntimeError("Calendar URL not configured. Please add your Google Calendar ICS URL in settings.")
                calendar_urls = [single_url]
                calendar_colors = [settings.get('calendarColor', '#4285f4')]

            calendar_img = self.generate_calendar_section(
                calendar_urls, calendar_colors, (right_width, calendar_height), tz, time_format
            )
            canvas.paste(calendar_img, (left_width, 0))
            any_success = True
            logger.info("Calendar section generated successfully")
        except Exception as e:
            error_msg = f"Calendar Error:\n{str(e)}"
            logger.error(f"Failed to generate calendar section: {str(e)}")
            error_img = self.generate_error_section(
                (right_width, calendar_height), "Calendar", str(e)
            )
            canvas.paste(error_img, (left_width, 0))

        # 4. Generate timestamp section (right side bottom: 400x60)
        logger.info("Adding timestamp...")
        try:
            timestamp_img = self.generate_timestamp_section(
                (right_width, timestamp_height), tz, time_format
            )
            canvas.paste(timestamp_img, (left_width, calendar_height))
            any_success = True
            logger.info("Timestamp section generated successfully")
        except Exception as e:
            logger.error(f"Failed to generate timestamp section: {str(e)}")
            error_img = self.generate_error_section(
                (right_width, timestamp_height), "Timestamp", str(e)
            )
            canvas.paste(error_img, (left_width, calendar_height))

        # If no section succeeded, raise an error
        if not any_success:
            raise RuntimeError("Failed to generate any dashboard section. Please check your settings and API keys.")

        # Draw divider lines between sections
        draw = ImageDraw.Draw(canvas)
        line_color = '#999'
        # Vertical divider between left and right columns
        draw.line([(left_width, 0), (left_width, height)], fill=line_color, width=2)
        # Horizontal divider on left side (weather / NASA)
        draw.line([(0, weather_height), (left_width, weather_height)], fill=line_color, width=2)

        logger.info("Dashboard generation complete")
        return canvas

    def generate_weather_section(self, lat, long, units, dimensions, tz, time_format):
        """Generate weather + UV index section for today + 2 days"""
        weather_data = self.get_open_meteo_data(lat, long, units)
        uv_data = self.get_open_meteo_uv_data(lat, long)

        now = datetime.now(tz)

        # Current conditions
        current = weather_data.get("current_weather", {})
        current_temp = round(current.get("temperature", 0))
        weather_code = current.get("weathercode", 0)
        condition_text = WEATHER_DESCRIPTIONS.get(weather_code, "")

        # Determine if it's night using sunrise/sunset
        daily = weather_data.get("daily", {})
        sunrise_list = daily.get("sunrise", [])
        sunset_list = daily.get("sunset", [])
        is_night = False
        if sunrise_list and sunset_list:
            try:
                sunrise = datetime.fromisoformat(sunrise_list[0]).astimezone(tz)
                sunset = datetime.fromisoformat(sunset_list[0]).astimezone(tz)
                is_night = now < sunrise or now > sunset
            except (ValueError, IndexError):
                pass

        # Daily forecast data
        daily_dates = daily.get("time", [])
        daily_codes = daily.get("weathercode", [])
        daily_highs = daily.get("temperature_2m_max", [])
        daily_lows = daily.get("temperature_2m_min", [])
        daily_precip = daily.get("precipitation_probability_max", [])

        # Build today's hourly outlook (next few hours)
        hourly = weather_data.get("hourly", {})
        hourly_times = hourly.get("time", [])
        hourly_temps = hourly.get("temperature_2m", [])
        hourly_codes = hourly.get("weathercode", [])
        hourly_precip = hourly.get("precipitation_probability", [])

        outlook_parts = []
        hours_checked = 0
        for i, time_str in enumerate(hourly_times):
            try:
                dt = datetime.fromisoformat(time_str).astimezone(tz)
                if dt > now and dt.date() == now.date() and hours_checked < 12:
                    hours_checked += 1
            except (ValueError, IndexError):
                continue

        # Build a brief outlook text for today
        today_outlook = ""
        if hours_checked > 0 and daily_precip:
            precip_today = round(daily_precip[0]) if daily_precip else 0
            today_high = round(daily_highs[0]) if daily_highs else "--"
            today_desc = WEATHER_DESCRIPTIONS.get(daily_codes[0] if daily_codes else 0, "")
            if precip_today >= 50:
                today_outlook = f"{today_desc}, high {today_high}°. Rain likely."
            elif precip_today >= 20:
                today_outlook = f"{today_desc}, high {today_high}°. Chance of rain."
            else:
                today_outlook = f"{today_desc}, high of {today_high}°."

        # UV index per day
        uv_by_day = self.parse_uv_index_multi(uv_data, tz, 3)

        # Build forecast days
        day_names = ["Today"]
        for i in range(1, 3):
            day_names.append((now + timedelta(days=i)).strftime("%a"))

        forecast_days = []
        for i in range(min(3, len(daily_dates))):
            forecast_days.append({
                "name": day_names[i] if i < len(day_names) else "",
                "icon": self.get_weather_icon(daily_codes[i] if i < len(daily_codes) else 0),
                "high": round(daily_highs[i]) if i < len(daily_highs) else "--",
                "low": round(daily_lows[i]) if i < len(daily_lows) else "--",
                "rain": round(daily_precip[i]) if i < len(daily_precip) else 0,
                "uv": uv_by_day[i] if i < len(uv_by_day) else 0,
            })

        temp_unit = UNITS[units]["temperature"]

        template_params = {
            "current_temperature": str(current_temp),
            "temperature_unit": temp_unit,
            "condition_text": condition_text,
            "weather_icon": self.get_weather_icon(weather_code, is_night),
            "today_outlook": today_outlook,
            "forecast_days": forecast_days,
        }

        image = self.render_image(dimensions, "weather_compact.html", "dashboard.css", template_params)

        if not image:
            raise RuntimeError("Failed to render weather section")

        return image

    def generate_calendar_section(self, calendar_urls, calendar_colors, dimensions, tz, time_format):
        """Generate calendar agenda section. Shows today (midnight-7pm) or tomorrow (7pm-midnight)."""
        # Fetch events from all calendars, tagging each with its color
        all_events = []
        for url, color in zip(calendar_urls, calendar_colors):
            try:
                events = self.fetch_calendar_events(url, tz)
                for event in events:
                    event['color'] = color
                all_events.extend(events)
            except Exception as e:
                logger.warning(f"Failed to fetch calendar {url}: {e}")

        now = datetime.now(tz)
        current_hour = now.hour

        # Midnight-7pm: show today. 7pm-midnight: show tomorrow.
        if current_hour < 19:
            target_date = now
            showing_today = True
        else:
            target_date = now + timedelta(days=1)
            showing_today = False

        filtered_events = self.filter_day_events(all_events, tz, target_date)

        formatted_events = []
        for event in filtered_events[:10]:
            formatted_events.append({
                "time": event.get("time", ""),
                "title": event.get("title", ""),
                "all_day": event.get("all_day", False),
                "color": event.get("color", "#4285f4")
            })

        date_str = target_date.strftime("%A, %B %d")
        label = "Today" if showing_today else "Tomorrow"

        template_params = {
            "date": date_str,
            "label": label,
            "events": formatted_events,
            "time_format": time_format,
        }

        image = self.render_image(dimensions, "calendar_compact.html", "dashboard.css", template_params)

        if not image:
            raise RuntimeError("Failed to render calendar section")

        return image

    def generate_nasa_section(self, settings, device_config, dimensions):
        """Generate NASA APOD section"""
        api_key = device_config.load_env_key("NASA_SECRET")
        if not api_key:
            raise RuntimeError("NASA API Key not configured in .env file. Add NASA_SECRET to your .env file.")

        params = {"api_key": api_key}

        # Check if random or specific date
        if settings.get("randomizeApod") == "true":
            start = datetime(2015, 1, 1)
            end = datetime.today()
            delta_days = (end - start).days
            random_date = start + timedelta(days=randint(0, delta_days))
            params["date"] = random_date.strftime("%Y-%m-%d")

        try:
            response = requests.get("https://api.nasa.gov/planetary/apod", params=params, timeout=10)

            if response.status_code == 403:
                raise RuntimeError("Invalid NASA API key. Check your NASA_SECRET in .env file.")
            elif response.status_code == 429:
                raise RuntimeError("NASA API rate limit exceeded. Try again later.")
            elif response.status_code != 200:
                logger.error(f"NASA API error {response.status_code}: {response.text}")
                raise RuntimeError(f"NASA API error (status {response.status_code}).")

            data = response.json()

            if data.get("media_type") != "image":
                raise RuntimeError("Today's APOD is a video, not an image. Try enabling 'Randomize' in settings.")

            image_url = data.get("hdurl") or data.get("url")

            img_response = requests.get(image_url, timeout=15)
            img_response.raise_for_status()
            image = Image.open(BytesIO(img_response.content))

            # Resize to fit dimensions while maintaining aspect ratio
            image = self.resize_and_crop(image, dimensions)

            # Add subtle gradient overlay at top and bottom edges
            image = image.convert('RGBA')
            gradient = Image.new('RGBA', dimensions, (0, 0, 0, 0))
            gradient_draw = ImageDraw.Draw(gradient)
            fade_height = dimensions[1] // 6
            # Top fade
            for y in range(fade_height):
                alpha = int(60 * (1 - y / fade_height))
                gradient_draw.line([(0, y), (dimensions[0], y)], fill=(0, 0, 0, alpha))
            # Bottom fade
            for y in range(fade_height):
                alpha = int(60 * (1 - y / fade_height))
                gradient_draw.line([(0, dimensions[1] - 1 - y), (dimensions[0], dimensions[1] - 1 - y)], fill=(0, 0, 0, alpha))
            image = Image.alpha_composite(image, gradient).convert('RGB')

        except requests.exceptions.Timeout:
            raise RuntimeError("NASA API request timed out. Check your internet connection.")
        except requests.exceptions.ConnectionError:
            raise RuntimeError("Cannot connect to NASA API. Check your internet connection.")
        except RuntimeError:
            # Re-raise our custom RuntimeErrors
            raise
        except Exception as e:
            logger.error(f"Failed to load APOD image: {str(e)}")
            raise RuntimeError(f"Failed to load APOD image: {str(e)}")

        return image

    def generate_timestamp_section(self, dimensions, tz, time_format):
        """Generate last updated timestamp section"""
        now = datetime.now(tz)
        if time_format == "24h":
            time_str = now.strftime("%H:%M")
        else:
            time_str = now.strftime("%-I:%M %p")

        template_params = {
            "time_str": time_str,
        }

        image = self.render_image(dimensions, "timestamp.html", "dashboard.css", template_params)

        if not image:
            raise RuntimeError("Failed to render timestamp section")

        return image

    def generate_error_section(self, dimensions, section_name, error_message):
        """Generate an error display section with red text"""
        width, height = dimensions
        img = Image.new('RGB', dimensions, 'white')
        draw = ImageDraw.Draw(img)

        # Add a light red background
        draw.rectangle([(0, 0), (width, height)], fill='#ffe6e6', outline='#ff0000', width=2)

        # Try to load fonts
        try:
            title_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 18)
            error_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 12)
        except:
            title_font = ImageFont.load_default()
            error_font = ImageFont.load_default()

        # Draw section name
        title_text = f"❌ {section_name} Error"
        padding = 10
        y_pos = padding

        # Draw title
        draw.text((padding, y_pos), title_text, fill='#cc0000', font=title_font)
        y_pos += 30

        # Draw error message with word wrapping
        max_width = width - (padding * 2)

        # Split error message into lines
        words = error_message.split()
        lines = []
        current_line = []

        for word in words:
            current_line.append(word)
            test_line = ' '.join(current_line)
            bbox = draw.textbbox((0, 0), test_line, font=error_font)
            if bbox[2] - bbox[0] > max_width:
                if len(current_line) > 1:
                    current_line.pop()
                    lines.append(' '.join(current_line))
                    current_line = [word]
                else:
                    # Word is too long, add it anyway
                    lines.append(word)
                    current_line = []

        if current_line:
            lines.append(' '.join(current_line))

        # Draw each line
        for line in lines[:8]:  # Limit to 8 lines to prevent overflow
            draw.text((padding, y_pos), line, fill='#990000', font=error_font)
            y_pos += 18

        return img

    # Helper methods for data fetching

    def get_open_meteo_data(self, lat, long, units):
        """Fetch weather data from Open-Meteo"""
        try:
            unit_params = OPEN_METEO_UNIT_PARAMS.get(units, OPEN_METEO_UNIT_PARAMS["metric"])
            url = OPEN_METEO_FORECAST_URL.format(lat=lat, long=long) + f"&{unit_params}"
            response = requests.get(url, timeout=10)

            if not 200 <= response.status_code < 300:
                logger.error(f"Open-Meteo API returned status {response.status_code}: {response.content}")
                raise RuntimeError(f"Open-Meteo API error (status {response.status_code}). Check your location coordinates.")

            return response.json()
        except requests.exceptions.Timeout:
            raise RuntimeError("Open-Meteo API request timed out. Check your internet connection.")
        except requests.exceptions.ConnectionError:
            raise RuntimeError("Cannot connect to Open-Meteo API. Check your internet connection.")
        except RuntimeError:
            # Re-raise our custom RuntimeErrors
            raise
        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"Network error fetching weather: {str(e)}")

    def get_open_meteo_uv_data(self, lat, long):
        """Fetch UV index data from Open-Meteo"""
        try:
            url = OPEN_METEO_AIR_QUALITY_URL.format(lat=lat, long=long)
            response = requests.get(url, timeout=10)

            if not 200 <= response.status_code < 300:
                logger.error(f"Open-Meteo UV API returned status {response.status_code}: {response.content}")
                raise RuntimeError(f"UV data API error (status {response.status_code}).")

            return response.json()
        except requests.exceptions.Timeout:
            raise RuntimeError("UV data request timed out.")
        except requests.exceptions.ConnectionError:
            raise RuntimeError("Cannot connect to UV data API.")
        except RuntimeError:
            # Re-raise our custom RuntimeErrors
            raise
        except requests.exceptions.RequestException as e:
            raise RuntimeError(f"Network error fetching UV data: {str(e)}")

    def parse_uv_index(self, uv_data, tz):
        """Parse UV index for today and tomorrow"""
        result = self.parse_uv_index_multi(uv_data, tz, 2)
        return result[0], result[1] if len(result) > 1 else 0

    def parse_uv_index_multi(self, uv_data, tz, num_days):
        """Parse max UV index for multiple days"""
        hourly_data = uv_data.get('hourly', {})
        times = hourly_data.get('time', [])
        uv_values = hourly_data.get('uv_index', [])

        current_time = datetime.now(tz)
        day_maxes = [0] * num_days
        dates = [(current_time + timedelta(days=i)).date() for i in range(num_days)]

        for i, time_str in enumerate(times):
            try:
                dt = datetime.fromisoformat(time_str).astimezone(tz)
                uv = uv_values[i] if i < len(uv_values) else 0
                for d, target_date in enumerate(dates):
                    if dt.date() == target_date:
                        day_maxes[d] = max(day_maxes[d], uv)
                        break
            except (ValueError, IndexError) as e:
                logger.warning(f"Error parsing UV data: {e}")
                continue

        return [round(v, 1) for v in day_maxes]

    def get_weather_icon(self, weather_code, is_night=False):
        """Map weather code to icon path, with day/night variants"""
        suffix = "n" if is_night else "d"
        icon_map = {
            0: "01",   # Clear
            1: "02",   # Mainly clear
            2: "03",   # Partly cloudy
            3: "04",   # Overcast
            45: "50",  # Fog
            48: "50",  # Fog
            51: "09",  # Drizzle
            53: "09",  # Drizzle
            55: "09",  # Heavy drizzle
            61: "10",  # Rain
            63: "10",  # Rain
            65: "10",  # Heavy rain
            71: "13",  # Snow
            73: "13",  # Snow
            75: "13",  # Heavy snow
            80: "09",  # Showers
            81: "09",  # Showers
            82: "09",  # Heavy showers
            95: "11",  # Thunderstorm
            96: "11",  # Thunderstorm w/ hail
            99: "11",  # Heavy thunderstorm
        }

        base = icon_map.get(weather_code, "01")
        icon = f"{base}{suffix}"
        plugins_dir = resolve_path("plugins")
        icon_path = os.path.join(plugins_dir, "weather", "icons", f"{icon}.png")
        # Fall back to day variant if night variant doesn't exist
        if not os.path.exists(icon_path):
            icon_path = os.path.join(plugins_dir, "weather", "icons", f"{base}d.png")
        return icon_path

    def fetch_calendar_events(self, calendar_url, tz):
        """Fetch and parse calendar events from ICS URL"""
        try:
            # Handle webcal:// URLs
            if calendar_url.startswith("webcal://"):
                calendar_url = calendar_url.replace("webcal://", "https://")

            response = requests.get(calendar_url, timeout=10)

            if response.status_code == 404:
                raise RuntimeError("Calendar URL not found (404). Check that the URL is correct.")
            elif response.status_code == 403:
                raise RuntimeError("Access denied to calendar (403). Make sure the calendar is shared/public.")
            elif response.status_code != 200:
                raise RuntimeError(f"Calendar API error (status {response.status_code}).")

            response.raise_for_status()

            try:
                cal = icalendar.Calendar.from_ical(response.text)
            except Exception as e:
                raise RuntimeError(f"Invalid calendar format. Make sure the URL is a valid ICS/iCal URL: {str(e)}")

            # Get events for the next 2 days
            start = datetime.now(tz)
            end = start + timedelta(days=2)

            events = recurring_ical_events.of(cal).between(start, end)

            parsed_events = []
            for event in events:
                try:
                    title = str(event.get("summary", "No Title"))
                    dtstart = event.decoded("dtstart")

                    all_day = False
                    if isinstance(dtstart, datetime):
                        event_dt = dtstart.astimezone(tz)
                    else:
                        # It's a date object (all-day event)
                        event_dt = datetime.combine(dtstart, datetime.min.time())
                        event_dt = tz.localize(event_dt)
                        all_day = True

                    parsed_events.append({
                        "title": title,
                        "datetime": event_dt,
                        "all_day": all_day
                    })
                except Exception as e:
                    logger.warning(f"Error parsing event: {e}")
                    continue

            return parsed_events

        except requests.exceptions.Timeout:
            raise RuntimeError("Calendar request timed out. Check your internet connection.")
        except requests.exceptions.ConnectionError:
            raise RuntimeError("Cannot connect to calendar URL. Check your internet connection.")
        except RuntimeError:
            # Re-raise our custom RuntimeErrors
            raise
        except Exception as e:
            logger.error(f"Failed to fetch calendar: {str(e)}")
            raise RuntimeError(f"Calendar fetch error: {str(e)}")

    def filter_day_events(self, events, tz, target_date):
        """Filter events for a specific day"""
        if isinstance(target_date, datetime):
            day_start = target_date.replace(hour=0, minute=0, second=0, microsecond=0)
        else:
            day_start = datetime.combine(target_date, datetime.min.time())
            day_start = tz.localize(day_start)
        day_end = day_start + timedelta(days=1)

        day_events = []
        for event in events:
            event_dt = event["datetime"]
            if day_start <= event_dt < day_end:
                if event["all_day"]:
                    time_str = "All Day"
                else:
                    time_str = event_dt.strftime("%I:%M %p").lstrip("0")

                day_events.append({
                    "time": time_str,
                    "title": event["title"],
                    "all_day": event["all_day"],
                    "color": event.get("color", "#4285f4")
                })

        day_events.sort(key=lambda x: (not x["all_day"], x["time"]))

        return day_events

    def resize_and_crop(self, image, target_size):
        """Resize and crop image to fit target size while maintaining aspect ratio"""
        target_width, target_height = target_size
        img_width, img_height = image.size

        # Calculate aspect ratios
        target_ratio = target_width / target_height
        img_ratio = img_width / img_height

        if img_ratio > target_ratio:
            # Image is wider, crop width
            new_height = target_height
            new_width = int(new_height * img_ratio)
            image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
            # Crop center
            left = (new_width - target_width) // 2
            image = image.crop((left, 0, left + target_width, target_height))
        else:
            # Image is taller, crop height
            new_width = target_width
            new_height = int(new_width / img_ratio)
            image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
            # Crop center
            top = (new_height - target_height) // 2
            image = image.crop((0, top, target_width, top + target_height))

        return image
