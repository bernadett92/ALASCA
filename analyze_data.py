import os
import glob
from astropy.io import fits
import numpy as np
import matplotlib.pyplot as plt

data_dir = ("/home2/bstadler/ALASCA_GEO_SPECULA/new")
data = {}

# Load all .fits files in the directory
for fname in glob.glob(os.path.join(data_dir, "*.fits")):
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

counts, bins = np.histogram(powerloss, bins=100, density=True)
plt.figure()
plt.title('Power loss at SAT')
plt.stairs(counts, bins, color='red')
plt.legend(['PASSATA', 'SPECULA'])
plt.xlabel('Power loss in dB')
plt.ylabel('Propability density')
plt.ylim([1e-4, 1])
plt.xlim([np.min(powerloss) + 1, 0])
plt.yscale('log')

res = data["redMod_sat"]
comm = data["comm"]
comm_ngs = data["comm_ngs"]
comm_joined = comm
comm_joined[:,0:2] = -comm_ngs[:,0:2]
init = 50
turb = res[init+1:, :].copy()
# command is applied with a delay of 1 frame
turb[:, :comm.shape[1]] += comm[init:-1, :]
x = np.arange(turb.shape[1])+1
nmodes = np.size(x)
# Plot RMS of residuals, commands and turbulence
plt.figure(figsize=(12, 6))
plt.plot(x,np.sqrt(np.mean(turb**2, axis=0)), label='Turbulence RMS', marker='o')
plt.plot(x,np.sqrt(np.mean(res**2, axis=0)), label='Residuals RMS', marker='o')
plt.plot(x[:comm.shape[1]],np.sqrt(np.mean(comm_joined**2, axis=0)), label='Commands RMS', marker='o')
plt.xlabel("Mode number")
plt.ylabel("RMS")
plt.xscale('log')
plt.yscale('log')
plt.legend()
plt.grid(True)

plt.figure()
plt.plot(sr_sat, color='black')
plt.plot(sr_ngs, color='red')
plt.title("Strehl Ratio satellite")
plt.legend(['uplink', 'downlink'])
plt.xlabel("Frame")
plt.ylabel("SR")
plt.grid(True)

plt.figure()
plt.plot(sr_589_down, color='black')
plt.plot(sr_589_up, color='red')
plt.title("Strehl Ratio LGS")
plt.legend(['downlink', 'uplink'])
plt.xlabel("Frame")
plt.ylabel("SR")
plt.grid(True)
plt.show()

print(f"The average Strehl Ratio at SAT: {sr_sat.mean():.4f}")
print(f"The average Strehl Ratio downlink: {sr_ngs.mean():.4f}")