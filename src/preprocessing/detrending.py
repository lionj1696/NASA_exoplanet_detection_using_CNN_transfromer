import numpy as np
from scipy.signal import savgol_filter


def detrend_flux(flux: np.ndarray) -> np.ndarray:
    flux = flux.astype(float).copy()

    baseline = savgol_filter(flux, window_length=101, polyorder=2)

    baseline[baseline == 0.0] = 1.0

    return flux / baseline
