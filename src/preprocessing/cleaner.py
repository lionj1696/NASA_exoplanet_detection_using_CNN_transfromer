import numpy as np


def clean_light_curve(flux: np.ndarray) -> np.ndarray:
    flux = flux.astype(float).copy()

    median = np.nanmedian(flux)
    std = np.nanstd(flux)
    flux[np.abs(flux - median) > 5 * std] = np.nan

    nan_mask = np.isnan(flux)
    if not nan_mask.any():
        return flux

    # Identify contiguous NaN runs and decide per-gap policy
    indices = np.arange(len(flux))
    changes = np.diff(nan_mask.astype(int), prepend=0, append=0)
    gap_starts = np.where(changes == 1)[0]
    gap_ends = np.where(changes == -1)[0]  # exclusive

    for start, end in zip(gap_starts, gap_ends):
        gap_len = end - start
        if gap_len <= 10:
            # Linear interpolation across this gap
            left_idx = start - 1
            right_idx = end
            if left_idx < 0 or right_idx >= len(flux):
                # Can't interpolate at boundaries — leave as NaN
                continue
            left_val = flux[left_idx]
            right_val = flux[right_idx]
            if np.isnan(left_val) or np.isnan(right_val):
                continue
            interp_vals = np.linspace(left_val, right_val, gap_len + 2)[1:-1]
            flux[start:end] = interp_vals
        # gaps > 10: leave as NaN (masked)

    nan_fraction = np.isnan(flux).sum() / len(flux)
    if nan_fraction > 0.30:
        raise ValueError(
            f"More than 30% of flux values are NaN after cleaning "
            f"({nan_fraction:.1%})."
        )

    return flux
