import numpy as np


def phase_fold(
    time: np.ndarray,
    flux: np.ndarray,
    period: float,
    epoch: float,
) -> tuple[np.ndarray, np.ndarray]:
    phase = ((time - epoch) / period) % 1.0
    phase = phase - 0.5  # center transit at 0, range [-0.5, 0.5]

    sort_idx = np.argsort(phase)
    return phase[sort_idx], flux[sort_idx]
