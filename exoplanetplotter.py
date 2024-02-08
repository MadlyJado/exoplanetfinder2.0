import asyncio
import lightkurve as lk
import os
import numpy as np


lightcurvepaths = []


def ReadPotentialExoplanets():
    with open("potential_exoplanets.txt", "r") as f:
        for line in f.readlines():
            if "FITS/" in line:
                linestr = str(line)
                splittedstr = linestr.split("in ")
                path = os.curdir+"/"+splittedstr[1][0:len(splittedstr[1])-1]
                lightcurvepaths.append(path)


def main():
    print("Reading all potential exoplanets from file...")
    ReadPotentialExoplanets()
    print("Plotting periodograms from lightcurve files to show potential exoplanets...")
    for path in lightcurvepaths:
        lc = lk.read(path).normalize(unit="ppm")
        period = np.linspace(1, 600, 10000)
        pg = lc.to_periodogram(method='bls', period=period)
        pg.plot()
        planet_b_period = pg.period_at_max_power
        planet_b_t0 = pg.transit_time_at_max_power
        planet_b_dur = pg.duration_at_max_power
        ax = lc.fold(period=planet_b_period, epoch_time=planet_b_t0).scatter()
        ax.set_xlim(-5, 5)
        planet_b_model = pg.get_transit_model(period=planet_b_period,
                                              transit_time=planet_b_t0,
                                              duration=planet_b_dur)
        ax = lc.fold(planet_b_period, planet_b_t0).scatter()
        planet_b_model.fold(planet_b_period, planet_b_t0).plot(ax=ax, c='r', lw=2)
        ax.set_xlim(-5, 5)
        

    print("Plotting Done!")


if __name__ == "__main__":
    main()
