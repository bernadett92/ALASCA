import os
import numpy as np
from astropy.io import fits

def create_scaled_amplitudes(n_actuators, base_amplitude=50):
    """
    Create amplitude vector with scaling pattern:
    [1, 1, 1/sqrt(2), 1/sqrt(2), 1/sqrt(2), 1/sqrt(3), 1/sqrt(3), 1/sqrt(3), 1/sqrt(3), ...]

    Parameters:
    -----------
    n_actuators : int
        Total number of actuators
    base_amplitude : float
        Base amplitude in nm (default: 50nm)

    Returns:
    --------
    amplitudes : ndarray
        Scaled amplitude vector
    """
    amplitudes = np.zeros(n_actuators)

    # Pattern: n repetitions of 1/sqrt(n)
    # Group 1: 2 actuators with factor 1 (1/sqrt(1))
    # Group 2: 3 actuators with factor 1/sqrt(2)
    # Group 3: 4 actuators with factor 1/sqrt(3)
    # etc.

    idx = 0
    group = 1

    while idx < n_actuators:
        # Number of actuators in this group
        group_size = group + 1

        # Scale factor for this group
        scale_factor = 1.0 / np.sqrt(group)

        # Fill the group (up to remaining actuators)
        end_idx = min(idx + group_size, n_actuators)
        amplitudes[idx:end_idx] = scale_factor

        print(f"Group {group}: actuators {idx:4d}-{end_idx-1:4d} (size={end_idx-idx:2d}), factor=1/√{group} = {scale_factor:.4f}")

        idx = end_idx
        group += 1

    # Apply base amplitude
    amplitudes *= base_amplitude

    return amplitudes

def main():
    # Create scaled amplitudes for all valid actuators
    n_actuators = 57  # Number of valid actuators -1 (from influence functions)
    base_amplitude = 20  # 50nm

    print(f"Creating scaled amplitude vector for {n_actuators} actuators")
    print(f"Base amplitude: {base_amplitude:.1f} nm")
    print("")

    amplitudes = create_scaled_amplitudes(n_actuators, base_amplitude)

    # Print statistics
    print(f"\nAmplitude statistics:")
    print(f"  Minimum: {np.min(amplitudes):.2f} nm")
    print(f"  Maximum: {np.max(amplitudes):.2f} nm")
    print(f"  Mean:    {np.mean(amplitudes):.2f} nm")
    print(f"  Std:     {np.std(amplitudes):.2f} nm")

    # Show first and last few values
    print(f"\nFirst 10 amplitudes [nm]: {amplitudes[:10]}")
    print(f"Last 10 amplitudes [nm]:  {amplitudes[-10:]}")

    # Save amplitude vector
    os.makedirs('calibration/data', exist_ok=True)

    output_file = '/home/bstadler/passata/ALASCA_072024/calibration/seeing_2.5/data/pushpull_57modes_amp20.fits'
    fits.writeto(output_file, amplitudes, overwrite=True)
    print(f"\n✓ Saved scaled amplitude vector: {output_file}")

    # Create comparison with uniform amplitudes
    uniform_amplitudes = np.full(n_actuators, base_amplitude)
    uniform_file = '/home/bstadler/passata/ALASCA_LEO/calibration_20cm_sh_TURBO50_elevation15deg_PAA25murad_SPECULA/data/pushpull_57modes_amp20.fits'
    fits.writeto(uniform_file, uniform_amplitudes, overwrite=True)
    print(f"✓ Saved uniform amplitude vector: {uniform_file}")

    return amplitudes

if __name__ == "__main__":
    amplitudes = main()