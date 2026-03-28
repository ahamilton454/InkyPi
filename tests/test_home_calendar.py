"""Tests for home dashboard calendar agenda ordering."""

from datetime import datetime

import pytz

from plugins.home.home import Home, sort_calendar_agenda_rows


def test_sort_timed_chronological_not_lexicographic():
    """5:00 PM must sort after 8:00 AM (string sort would reverse these)."""
    tz = pytz.timezone("America/New_York")
    day = datetime(2026, 3, 27, 0, 0, 0, tzinfo=tz)
    pm = day.replace(hour=17, minute=0)
    am = day.replace(hour=8, minute=0)
    rows = [
        {"all_day": False, "sort_dt": pm, "title": "Gym", "time": "", "color": "#00f"},
        {"all_day": False, "sort_dt": am, "title": "Cowork", "time": "", "color": "#0f0"},
    ]
    out = sort_calendar_agenda_rows(rows)
    assert [r["title"] for r in out] == ["Cowork", "Gym"]


def test_sort_timed_before_all_day():
    tz = pytz.timezone("UTC")
    day = datetime(2026, 1, 1, 0, 0, 0, tzinfo=tz)
    rows = [
        {
            "all_day": True,
            "sort_dt": day,
            "title": "Holiday",
            "time": "All Day",
            "color": "#4285f4",
        },
        {
            "all_day": False,
            "sort_dt": day.replace(hour=9, minute=0),
            "title": "Meeting",
            "time": "9:00 AM",
            "color": "#000",
        },
    ]
    out = sort_calendar_agenda_rows(rows)
    assert [r["title"] for r in out] == ["Meeting", "Holiday"]


def test_sort_tie_by_title():
    tz = pytz.timezone("UTC")
    t = datetime(2026, 6, 1, 14, 0, 0, tzinfo=tz)
    rows = [
        {"all_day": False, "sort_dt": t, "title": "Zebra", "time": "2:00 PM", "color": "#111"},
        {"all_day": False, "sort_dt": t, "title": "Alpha", "time": "2:00 PM", "color": "#222"},
    ]
    out = sort_calendar_agenda_rows(rows)
    assert [r["title"] for r in out] == ["Alpha", "Zebra"]


def test_sort_all_day_by_title():
    tz = pytz.timezone("UTC")
    day = datetime(2026, 1, 1, 0, 0, 0, tzinfo=tz)
    rows = [
        {"all_day": True, "sort_dt": day, "title": "B", "time": "All Day", "color": "#a"},
        {"all_day": True, "sort_dt": day, "title": "A", "time": "All Day", "color": "#b"},
    ]
    out = sort_calendar_agenda_rows(rows)
    assert [r["title"] for r in out] == ["A", "B"]


def test_filter_day_events_orders_by_clock():
    tz = pytz.timezone("America/New_York")
    home = Home.__new__(Home)
    target = datetime(2026, 3, 27, 12, 0, 0, tzinfo=tz)
    day_start = target.replace(hour=0, minute=0, second=0, microsecond=0)
    events = [
        {
            "datetime": day_start.replace(hour=17, minute=0),
            "end_datetime": day_start.replace(hour=18, minute=0),
            "title": "Late",
            "all_day": False,
            "color": "#c",
        },
        {
            "datetime": day_start.replace(hour=8, minute=0),
            "end_datetime": day_start.replace(hour=9, minute=0),
            "title": "Early",
            "all_day": False,
            "color": "#d",
        },
    ]
    out = Home.filter_day_events(home, events, tz, target)
    assert [e["title"] for e in out] == ["Early", "Late"]


def test_filter_day_events_strips_sort_fields():
    tz = pytz.timezone("UTC")
    home = Home.__new__(Home)
    target = datetime(2026, 2, 1, 0, 0, 0, tzinfo=tz)
    day_start = target.replace(hour=0, minute=0, second=0, microsecond=0)
    events = [
        {
            "datetime": day_start.replace(hour=10, minute=0),
            "end_datetime": day_start.replace(hour=11, minute=0),
            "title": "Only",
            "all_day": False,
            "color": "#eee",
        },
    ]
    out = Home.filter_day_events(home, events, tz, target)
    assert len(out) == 1
    assert set(out[0].keys()) == {
        "sort_dt",
        "clip_start",
        "clip_end",
        "title",
        "all_day",
        "color",
        "time_range",
    }
