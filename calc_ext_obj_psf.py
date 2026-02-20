import specula
specula.init(0)  # Default target device

import matplotlib.pyplot as plt
from astropy.io import fits
from os import path
from specula.lib.calc_corr_phase_cube import calc_corr_phase_cube

seed = 1
L0 = 20
pixel_square_phasescreens = 8192
imwidth = 124 # = pixel_pupil*pyr.fft_res
seeing4calib = 3.5
zenit_angle = 56.0
pixel_pitch = 0.008333
pixel_pupil = 120
nmodes = 57
nframes = 10
psf_lambda = 589 # pyramid wavelength
pyr_fov = 5.0
pixel_scale_psf = 0.040498272

dir = '/home/bstadler/passata/ALASCA_072024/calibration/seeing_2.5_specula'
ifunc_dir = path.join(dir, 'ifunc')
ps_dir = path.join(dir, 'phasescreens')
ifunc_tag = 'CaNaPy_dm_ifunc_120pix_59masters_57modes'

aber_name = 'aber_s3.50asec_fitonly_nm57_steps10.fits'
aber_PSF_name = 'PSF_s3.50asec_fitonly_nm57_steps10_l589nm_n124pix.fits'

masked = True
doPsf = True

airmass = 1/specula.xp.cos(zenit_angle/180*specula.xp.pi)
seeing4calib *= airmass**(3./5.)
seeing4calib = specula.xp.round(seeing4calib*10)/10.
cube, outPsf = calc_corr_phase_cube(seeing4calib, L0, pixel_pitch, pixel_pupil, nmodes, ps_dir, ifunc_dir, ifunc_tag,
                            nframes, psf_lambda, imwidth, specula.xp, masked, pixel_square_phasescreens, seed, doPsf)

sOutPsf = specula.xp.size(outPsf,0)
npsf = 360
outPsf = outPsf[int(sOutPsf/2-npsf/2):int(sOutPsf/2+npsf/2),int(sOutPsf/2-npsf/2):int(sOutPsf/2+npsf/2)]

fits.writeto(path.join(dir,'data', aber_name), cube.get(), overwrite=True)
fits.writeto(path.join(dir,'data', aber_PSF_name), outPsf.get(), overwrite=True)

plt.figure()
plt.imshow(outPsf.get())
plt.colorbar()
plt.show()