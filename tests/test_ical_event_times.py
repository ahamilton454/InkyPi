"""Tests for ICS interval parsing and timeline layout helpers."""

from datetime import datetime, timedelta

import pytz

from utils.ical_event_times import (
    clip_interval_to_day,
    layout_timeline_blocks,
    timeline_window_for_day,
)


def test_clip_interval_cross_midnight():
    tz = pytz.UTC
    day_start = datetime(2026, 3, 28, 0, 0, 0, tzinfo=tz)
    day_end = day_start + timedelta(days=1)
    # Event 10 PM previous day -> 2 AM this day
    start = datetime(2026, 3, 27, 22, 0, 0, tzinfo=tz)
    end = datetime(2026, 3, 28, 2, 0, 0, tzinfo=tz)
    c = clip_interval_to_day(start, end, day_start, day_end)
    assert c is not None
    cs, ce = c
    assert cs == day_start
    assert ce == end


def test_clip_interval_no_overlap():
    tz = pytz.UTC
    day_start = datetime(2026, 3, 28, 0, 0, 0, tzinfo=tz)
    day_end = day_start + timedelta(days=1)
    start = datetime(2026, 3, 29, 10, 0, 0, tzinfo=tz)
    end = datetime(2026, 3, 29, 11, 0, 0, tzinfo=tz)
    assert clip_interval_to_day(start, end, day_start, day_end) is None


def test_layout_timeline_basic_percent():
    tz = pytz.UTC
    ws = datetime(2026, 1, 1, 8, 0, 0, tzinfo=tz)
    we = datetime(2026, 1, 1, 10, 0, 0, tzinfo=tz)
    rows = [
        {
            "clip_start": datetime(2026, 1, 1, 8, 30, 0, tzinfo=tz),
            "clip_end": datetime(2026, 1, 1, 9, 0, 0, tzinfo=tz),
            "title": "A",
            "color": "#111",
            "time_range": "8:30 – 9:00",
        }
    ]
    out = layout_timeline_blocks(rows, ws, we, min_height_pct=2.0)
    assert len(out) == 1
    assert out[0]["top_pct"] == 25.0
    assert out[0]["height_pct"] >= 2.0
    assert out[0]["col"] == 0
    assert out[0]["col_count"] == 1


def test_timeline_window_contains_early_event():
    tz = pytz.UTC
    day_start = datetime(2026, 6, 1, 0, 0, 0, tzinfo=tz)
    timed = [
        {
            "clip_start": day_start.replace(hour=5, minute=0),
            "clip_end": day_start.replace(hour=5, minute=30),
        }
    ]
    w0, w1 = timeline_window_for_day(day_start, timed)
    assert w0 <= timed[0]["clip_start"]
    assert w1 >= timed[0]["clip_end"]
