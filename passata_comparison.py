import os
import glob
from astropy.io import fits
import numpy as np
import matplotlib.pyplot as plt

wavelengthInNm = 1550
prop_distance = 400000.
pixel_pupil = 120
pixel_pitch = 1/pixel_pupil
receiver_diam = 0.1
nd = 3

sr_passata_sat = fits.open('/home/bstadler/passata/ALASCA_072024/results/seeing_2.5/Tenerife_day_LGSAO/sr_sat.fits')[0].data
dx_sat_sq = wavelengthInNm*1e-9*prop_distance/(pixel_pupil*nd*pixel_pitch)
flux = sr_passata_sat/dx_sat_sq
power = flux*receiver_diam
powerloss_passata = 10*np.log10(power)

sr_passata_589_up = fits.open('/home/bstadler/passata/ALASCA_072024/results/seeing_2.5/Tenerife_day_LGSAO/sr_up_589.fits')[0].data

psf_passata = fits.open('/home/bstadler/passata/ALASCA_072024/results/seeing_2.5/Tenerife_day_LGSAO/psf_589.fits')[0].data
psf_specula = fits.open('/home2/bstadler/ALASCA_LEO/SPECULA/Tenerife_geo_LGSAO/psf_589_up.fits')[0].data

# for i in range(9):
#     print(np.max(psf_passata[:,:,i]))
#     print(np.max(psf_specula[i, :, :]))
#     print(np.sum(psf_passata[:,:,i]-psf_specula[i, :, :]))
#     plt.figure()
#     plt.imshow(psf_passata[:,:,i])
#     plt.colorbar()
#     plt.figure()
#     plt.imshow(psf_specula[i, :, :])
#     plt.colorbar()
#     plt.figure()
#     plt.imshow(psf_passata[:,:,i] - psf_specula[i, :, :])
#     plt.colorbar()
#     plt.show()
data_dir = "/home2/bstadler/ALASCA_LEO/SPECULA/Tenerife_geo_LGSAO"
data = {}

# Load all .fits files in the directory
for fname in glob.glob(os.path.join(data_dir, "*.fits")):
    key = os.path.splitext(os.path.basename(fname))[0]
    with fits.open(fname) as hdul:
        arr = hdul[0].data
    data[key] = arr
    print('key:', key, 'type:', type(data[key]))

powerloss = data["powerloss"]
counts_passata, bins_passata = np.histogram(powerloss_passata, bins=100, density=True)
counts, bins = np.histogram(powerloss, bins=100, density=True)
plt.figure()
plt.title('Power loss at SAT')
plt.stairs(counts_passata, bins_passata, color='black')
plt.stairs(counts, bins, color='red')
plt.legend(['PASSATA', 'SPECULA'])
plt.xlabel('Power loss in dB')
plt.ylabel('Propability density')
plt.ylim([1e-4, 1])
plt.xlim([np.min(powerloss) + 1, 0])
plt.yscale('log')

sr_ngs = data["sr_ngs"]
sr_sat = data["sr_sat"]
sr_589_up = data["sr_589_up"]
sr_passata_ngs = fits.open('/home/bstadler/passata/ALASCA_072024/results/seeing_2.5/Tenerife_day_LGSAO/sr_ngs.fits')[0].data
print(f"The average Strehl Ratio at SAT: {sr_sat.mean():.4f}")
print(f"The average PASSATA Strehl Ratio at SAT: {sr_passata_sat.mean():.4f}")
print(f"The average Strehl Ratio downlink: {sr_ngs.mean():.4f}")
print(f"The average PASSATA Strehl Ratio downlink: {sr_passata_ngs.mean():.4f}")

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
plt.show()