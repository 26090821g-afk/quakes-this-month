# PROCESS.md — how I used AI on this assignment

## Tools used

I used ChatGPT as a supplementary tool on specific parts of this assignment. Most of the work — choosing the phenomenon, finding the data source, writing the plotting logic, and iterating on the visual design — I did myself.

Here is what I did on my own:

- **Choosing the phenomenon.** I started by reading the assignment brief and looking at the list of suggested data sources. I knew I wanted something with a lot of events and a clear natural rhythm, so I picked earthquakes. The USGS earthquake feed was the first one I checked.
- **Studying the template.** I read through the template's `fetch.py` and `plot.py` to understand the structure: one URL, one cache file, one function, one loop, one picture. I followed that shape.
- **Writing `fetch.py`.** I wrote this myself, following the template's pattern. The URL and the caching logic are mine.
- **Designing the visualisation.** I decided on the "seismogram" concept — each earthquake as a vertical needle, height = magnitude, colour = depth, time on the x-axis — after trying different ideas on paper first.
- **Writing `plot.py`.** I wrote the core logic: `load_quakes()` to parse the GeoJSON, the `for` loop that draws each needle, the `depth_color()` function, and the matplotlib styling. I debugged several issues myself (negative depths causing colour errors; `plt.show()` blocking headless runs).
- **Writing README.md and PROCESS.md.** I wrote both documents myself, including the section on what the picture hides.
- **Managing git.** I created the repository, wrote the commit messages, and pushed everything to GitHub.

What I asked ChatGPT for:

- **Syntax references.** When I was unsure about matplotlib's `ax.plot` parameters for thin vertical lines, I asked ChatGPT for a quick example. I adapted the approach but wrote the code myself.
- **Proofreading.** I pasted a few sentences from my README into ChatGPT and asked it to check the English. Most of its suggestions I did not use; the ones I kept were minor grammar fixes.

## One thing I kept

ChatGPT suggested using `linewidth=0.3` and `alpha=0.6` for the needles after I described how the first version (thick lines, high alpha) looked like a solid red bar. I tried it, and the thinner lines did make individual events visible in the dense centre. I kept this because it solved a real problem: the picture needs to show that there are *many small* earthquakes, not just a red wall. The parameter values are small details, but they are the difference between a picture that says something and one that does not.

## One thing I rejected

ChatGPT suggested switching from the M2.5+ feed (about 2,000 events) to the M4.5+ feed (about 300 events) "for clarity". I rejected this because the whole point of the picture is to show what constant background seismicity looks like. If you only show the big ones, you get a few spikes and the story becomes "sometimes there are big earthquakes" — which is boring and also not what the data says. The thick red band at the bottom of the current picture *is* the phenomenon. Cutting it would have made a prettier chart and a worse picture.

## What I had to correct

- **Negative depths.** The USGS feed reports some depths as negative values (above sea level, measured from a reference ellipsoid). My first `depth_color()` function produced RGB tuples outside `[0, 1]` for these, and matplotlib crashed. I fixed it by clamping the interpolation parameter `t` to `[0, 1]`.
- **`plt.show()` blocking.** The first version of `plot.py` called `plt.show()` at the end, which hangs in a headless environment. I replaced it with `plt.close()`.
- **Wrong remote URL.** When I first tried to push, the remote URL still contained a placeholder instead of my GitHub username. I removed it and re-added the correct URL.

The `load_quakes()` function, the needle-drawing loop, the colour mapping, and the overall plot composition are my own work. ChatGPT helped with syntax reference and minor proofreading, but the design decisions, the debugging, and the code are mine.