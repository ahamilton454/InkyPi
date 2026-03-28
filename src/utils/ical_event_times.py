"""
Parse iCalendar event start/end for dashboard-style views.
Aligned with plugins.calendar.calendar.parse_data_points behavior.
"""

from __future__ import annotations

from datetime import date, datetime, time, timedelta
from typing import Any, Optional, Tuple

DEFAULT_TIMED_DURATION = timedelta(hours=1)


def parse_event_interval(event: Any, tz) -> Tuple[datetime, datetime, bool]:
    """
    Return (start_dt, end_dt, all_day) in tz. For timed events without end,
    uses start + DEFAULT_TIMED_DURATION. All-day uses date-only rules; end is
    exclusive (iCal), represented as midnight at the first day after the last day.
    """
    dtstart = event.decoded("dtstart")
    if isinstance(dtstart, datetime):
        start_dt = dtstart.astimezone(tz)
        end_dt = None
        if "dtend" in event:
            dtend = event.decoded("dtend")
            if isinstance(dtend, datetime):
                end_dt = dtend.astimezone(tz)
            else:
                d = dtend if isinstance(dtend, date) else dtend.date()
                end_dt = tz.localize(datetime.combine(d, time.min))
        elif "duration" in event:
            end_dt = start_dt + event.decoded("duration")
        else:
            end_dt = start_dt + DEFAULT_TIMED_DURATION
        if end_dt <= start_dt:
            end_dt = start_dt + DEFAULT_TIMED_DURATION
        return start_dt, end_dt, False

    # All-day: dtstart is a date
    start_d = dtstart if isinstance(dtstart, date) else dtstart.date()
    start_dt = tz.localize(datetime.combine(start_d, time.min))
    if "dtend" in event:
        dtend = event.decoded("dtend")
        if isinstance(dtend, datetime):
            end_dt = dtend.astimezone(tz)
        else:
            end_d = dtend if isinstance(dtend, date) else dtend.date()
            end_dt = tz.localize(datetime.combine(end_d, time.min))
    else:
        end_dt = start_dt + timedelta(days=1)
    if end_dt <= start_dt:
        end_dt = start_dt + timedelta(days=1)
    return start_dt, end_dt, True


def clip_interval_to_day(
    start: datetime, end: datetime, day_start: datetime, day_end: datetime
) -> Optional[Tuple[datetime, datetime]]:
    """Intersect [start, end) with [day_start, day_end). Returns None if empty."""
    clip_start = max(start, day_start)
    clip_end = min(end, day_end)
    if clip_start >= clip_end:
        return None
    return clip_start, clip_end


def format_time_for_device(dt: datetime, time_format: str) -> str:
    """Match home dashboard conventions (12h with lstrip leading zero on hour)."""
    if time_format == "24h":
        return dt.strftime("%H:%M")
    return dt.strftime("%I:%M %p").lstrip("0")


def format_time_range(
    start: datetime, end: datetime, time_format: str, all_day: bool
) -> str:
    if all_day:
        return "All day"
    a = format_time_for_device(start, time_format)
    b = format_time_for_device(end, time_format)
    return f"{a} – {b}"


def timeline_window_for_day(
    day_start: datetime,
    clipped_timed: list,
    fixed_start_hour: int = 6,
    fixed_end_hour: int = 22,
) -> Tuple[datetime, datetime]:
    """
    Default window: fixed local hours on that calendar day.
    Optional: expand using min/max clip times + 30m, clamped to 05:00–23:00.
    """
    base_start = day_start.replace(
        hour=fixed_start_hour, minute=0, second=0, microsecond=0
    )
    base_end = day_start.replace(hour=fixed_end_hour, minute=0, second=0, microsecond=0)
    if not clipped_timed:
        return base_start, base_end
    earliest = min(r["clip_start"] for r in clipped_timed)
    latest = max(r["clip_end"] for r in clipped_timed)
    pad = timedelta(minutes=30)
    dyn_start = min(earliest, base_start) - pad
    dyn_end = max(latest, base_end) + pad
    clamp_lo = day_start.replace(hour=5, minute=0, second=0, microsecond=0)
    clamp_hi = day_start.replace(hour=23, minute=0, second=0, microsecond=0)
    w_start = max(clamp_lo, dyn_start)
    w_end = min(clamp_hi, dyn_end)
    if w_end <= w_start:
        return base_start, base_end
    return w_start, w_end


def layout_timeline_blocks(
    timed_rows: list,
    window_start: datetime,
    window_end: datetime,
    min_height_pct: float = 4.0,
) -> list:
    """
    timed_rows: dicts with clip_start, clip_end, title, color, time_range.
    Adds top_pct, height_pct, col, col_count, width_pct, left_pct for CSS.
    """
    total_s = (window_end - window_start).total_seconds()
    if total_s <= 0:
        return []

    items = []
    for r in timed_rows:
        cs, ce = r["clip_start"], r["clip_end"]
        vis_s = max(cs, window_start)
        vis_e = min(ce, window_end)
        if vis_s >= vis_e:
            continue
        top_pct = (vis_s - window_start).total_seconds() / total_s * 100.0
        height_pct = (vis_e - vis_s).total_seconds() / total_s * 100.0
        if height_pct < min_height_pct:
            height_pct = min_height_pct
        items.append(
            {
                **r,
                "_vis_start": vis_s,
                "_vis_end": vis_e,
                "top_pct": round(top_pct, 4),
                "height_pct": round(height_pct, 4),
            }
        )

    if not items:
        return []

    items.sort(key=lambda x: (x["_vis_start"], x["title"]))
    columns: list = []
    for it in items:
        placed = False
        for i, last_end in enumerate(columns):
            if last_end <= it["_vis_start"]:
                it["col"] = i
                columns[i] = it["_vis_end"]
                placed = True
                break
        if not placed:
            it["col"] = len(columns)
            columns.append(it["_vis_end"])

    col_count = max((it["col"] for it in items), default=-1) + 1
    if col_count < 1:
        col_count = 1
    width_pct = 100.0 / col_count
    for it in items:
        it["col_count"] = col_count
        it["width_pct"] = round(width_pct, 4)
        it["left_pct"] = round(it["col"] * width_pct, 4)
        dur_s = (it["_vis_end"] - it["_vis_start"]).total_seconds()
        it["is_short"] = dur_s <= 1800
        it.pop("_vis_start", None)
        it.pop("_vis_end", None)

    return items


def hour_ticks(window_start: datetime, window_end: datetime, time_format: str) -> list:
    """Return list of {label, top_pct} for full-hour marks within the window."""
    total_s = (window_end - window_start).total_seconds()
    if total_s <= 0:
        return []
    ticks = []
    cur = window_start.replace(minute=0, second=0, microsecond=0)
    if cur < window_start:
        cur += timedelta(hours=1)
    while cur < window_end:
        top_pct = (cur - window_start).total_seconds() / total_s * 100.0
        label = format_time_for_device(
            cur.replace(minute=0, second=0, microsecond=0), time_format
        )
        ticks.append({"label": label, "top_pct": round(top_pct, 4)})
        cur += timedelta(hours=1)
    return ticks
