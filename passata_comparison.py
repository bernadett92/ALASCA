import os
import glob
from astropy.io import fits
import matplotlib.pyplot as plt

passata_dir = "/home/bstadler/passata/ALASCA_072024/results/seeing_2.5/Tenerife_day_LGSAO_physProp/"
specula_dir = "/home2/bstadler/ALASCA_GEO_SPECULA/new/"

# Load PASSATA data
sr_passata_sat = fits.open(passata_dir + 'sr_sat.fits')[0].data
sr_passata_589_up = fits.open(passata_dir + 'sr_up_589.fits')[0].data
sr_passata_589_down = fits.open(passata_dir + 'sr_down.fits')[0].data
sr_passata_ngs = fits.open(passata_dir + 'sr_ngs.fits')[0].data

# Load SPECULA data
data = {}
for fname in glob.glob(os.path.join(specula_dir, "*.fits")):
    key = os.path.splitext(os.path.basename(fname))[0]
    with fits.open(fname) as hdul:
        arr = hdul[0].data
    data[key] = arr
    print('key:', key, 'type:', type(data[key]))
powerloss = data["powerloss"]
sr_ngs = data["sr_ngs"]
sr_sat = data["sr_sat"]
sr_589_up = data["sr_589_up"]
sr_589_down = data["sr_589_down"]

plt.figure()
plt.plot(sr_passata_sat, color='black')
plt.plot(sr_sat, color='red')
plt.title("Strehl Ratio SAT uplink")
plt.legend(['PASSATA', 'SPECULA'])
plt.xlabel("Frame")
plt.ylabel("SR")
plt.grid(True)

plt.figure()
plt.plot(sr_passata_ngs, color='black')
plt.plot(sr_ngs, color='red')
plt.title("Strehl Ratio SAT downlink")
plt.legend(['PASSATA', 'SPECULA'])
plt.xlabel("Frame")
plt.ylabel("SR")
plt.grid(True)

plt.figure()
plt.plot(sr_passata_589_up, color='black')
plt.plot(sr_589_up, color='red')
plt.title("Strehl Ratio 589 up")
plt.legend(['PASSATA', 'SPECULA'])
plt.xlabel("Frame")
plt.ylabel("SR")
plt.grid(True)

plt.figure()
plt.plot(sr_passata_589_down, color='black')
plt.plot(sr_589_down, color='red')
plt.title("Strehl Ratio 589 down")
plt.legend(['PASSATA', 'SPECULA'])
plt.xlabel("Frame")
plt.ylabel("SR")
plt.grid(True)
plt.show()

print(f"The average Strehl Ratio at SAT: {sr_sat.mean():.4f}")
print(f"The average PASSATA Strehl Ratio at SAT: {sr_passata_sat.mean():.4f}")
print(f"The average Strehl Ratio downlink: {sr_ngs.mean():.4f}")
print(f"The average PASSATA Strehl Ratio downlink: {sr_passata_ngs.mean():.4f}")