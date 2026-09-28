# /// script
# requires-python = ">=3.10"
# dependencies = ["matplotlib", "numpy"]
# ///

"""
Read the GeoJSON in data/, make one picture, save it to out/.

    uv run plot.py

Each earthquake in the past month becomes a vertical needle.
Height = magnitude. Color = depth (shallow red, deep blue).
Left to right = oldest to newest. The picture is a seismogram
of the whole planet over 30 days.
"""

import json
from datetime import datetime, timezone
from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import numpy as np

FILE = "usgs-earthquakes-2.5-month.geojson"
PICTURE = "quakes-this-month.png"

HERE = Path(__file__).parent
DATA = HERE / "data" / FILE
OUT = HERE / "out"


def load_quakes(path):
    """Read the GeoJSON file and return a list of (time, magnitude, depth) tuples.
    Skip any earthquake with a null magnitude."""
    raw = json.loads(path.read_text(encoding="utf-8"))
    quakes = []
    for feature in raw["features"]:
        props = feature["properties"]
        mag = props.get("mag")
        if mag is None:
            continue
        time_ms = props["time"]
        depth_km = feature["geometry"]["coordinates"][2]
        quakes.append((time_ms, mag, depth_km))
    return quakes


def depth_color(depth):
    """Map a depth in km to a color: shallow = warm red, deep = cool blue."""
    # Most earthquakes are within 0-200 km; clamp at 300 for the color scale
    # Some depths are negative (above sea level), so clamp at 0
    t = max(0, min(depth / 300.0, 1.0))
    # Interpolate from red (0 km) through purple (150 km) to blue (300+ km)
    r = max(0, min(1.0 - 0.8 * t, 1.0))
    b = max(0, min(0.2 + 0.8 * t, 1.0))
    return (r, 0.3, b)


def main():
    quakes = load_quakes(DATA)
    print(f"{DATA.name}: {len(quakes)} earthquakes loaded")

    # Sort by time (oldest first)
    quakes.sort(key=lambda q: q[0])

    times, mags, depths = [], [], []
    for time_ms, mag, depth in quakes:
        dt = datetime.fromtimestamp(time_ms / 1000, tz=timezone.utc)
        times.append(dt)
        mags.append(mag)
        depths.append(depth)

    print(f"magnitudes: {min(mags):.1f} to {max(mags):.1f}")
    print(f"depths: {min(depths):.1f} to {max(depths):.1f} km")
    print(f"time span: {times[0].strftime('%Y-%m-%d')} to {times[-1].strftime('%Y-%m-%d')}")

    fig, ax = plt.subplots(figsize=(20, 7), facecolor="#0a0a12")
    ax.set_facecolor("#0a0a12")

    # The loop: draw one needle per earthquake
    for i, (dt, mag, depth) in enumerate(zip(times, mags, depths)):
        color = depth_color(depth)
        ax.plot([i, i], [0, mag], color=color, linewidth=0.3, alpha=0.6)
        ax.plot(i, mag, ".", color=color, markersize=1.8, alpha=0.8)

    # Mark the baseline
    ax.axhline(0, color="#333340", linewidth=0.8)

    # X-axis: show dates at roughly 5 evenly spaced positions
    n = len(quakes)
    tick_positions = np.linspace(0, n - 1, 6, dtype=int)
    tick_labels = [times[p].strftime("%b %d") for p in tick_positions]
    ax.set_xticks(tick_positions)
    ax.set_xticklabels(tick_labels, color="#888899", fontsize=9)

    ax.set_ylim(0, max(mags) + 1)
    ax.set_ylabel("magnitude", color="#ccccdd", fontsize=11)
    ax.set_title(f"Earthquakes M2.5+ worldwide — past 30 days ({len(quakes)} events)",
                 color="#e8e8f0", fontsize=13, pad=12)

    # Color legend for depth
    for km, label in [(10, "shallow\n0 km"), (150, "mid\n150 km"), (300, "deep\n300+ km")]:
        ax.plot([], [], "|", color=depth_color(km), markersize=15,
                label=label)
    leg = ax.legend(loc="upper left", framealpha=0, fontsize=8,
                    labelcolor="#888899", ncol=3, handletextpad=0.3,
                    columnspacing=1.2)

    # Clean up the spines and ticks
    for spine in ax.spines.values():
        spine.set_color("#333340")
    ax.tick_params(colors="#888899", labelsize=9)

    fig.tight_layout()
    try:
        OUT.mkdir(exist_ok=True)
    except PermissionError:
        pass  # directory already exists
    fig.savefig(OUT / PICTURE, dpi=150, facecolor=fig.get_facecolor())
    print(f"saved out/{PICTURE}")
    plt.close()


if __name__ == "__main__":
    main()
