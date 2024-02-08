from exoplanetfinder_cy import process_fits_file, execute_fits_files
import time


t1 = time.time()
execute_fits_files()
t2 = time.time()
print(f"Time taken: {t2-t1} seconds")
