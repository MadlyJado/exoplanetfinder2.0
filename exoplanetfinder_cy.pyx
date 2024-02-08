import os
import lightkurve as lk
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor

folder_path = "FITS"
output_file = "potential_exoplanets.txt"

def process_fits_file(file_path, output_file):
    try:
        lightcurve = lk.read(file_path).normalize(unit='ppm')

        periodogram = lightcurve.to_periodogram(method='bls')

        for flux in lightcurve.flux:
            if flux < 0.95 and periodogram.max_power > 100:
                with open(output_file, "a") as f:
                    f.write(f"Exoplanet candidate found in {file_path}\n")
                    f.write(f"Maximum power in periodogram: {periodogram.max_power}\n\n")
    except Exception as e:
        with open("error_log.txt", "a") as error_log:
            error_log.write(f"Error processing {file_path}: {str(e)}\n")

def execute_fits_files():
    with tqdm(total=len(os.listdir(folder_path)), unit="files") as pbar:
        with ThreadPoolExecutor(max_workers=5000) as executor:
            futures = []

            for filename in os.listdir(folder_path):
                if filename.endswith(".fits"):
                    file_path = os.path.join(folder_path, filename)
                    future = executor.submit(process_fits_file, file_path, output_file)
                    future.add_done_callback(lambda x: pbar.update(1))
                    futures.append(future)

            for future in futures:
                future.result()

