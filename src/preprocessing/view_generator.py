import logging
import sys
import os
import warnings

import numpy as np
import pandas as pd

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
from config import (
    DATA_PROCESSED_PATH,
    GLOBAL_VIEW_LENGTH,
    LOCAL_VIEW_LENGTH,
    PHASE_WINDOW,
    LABEL_COLUMN,
    PERIOD_COLUMN,
    EPOCH_COLUMN,
    POSITIVE_LABEL,
    NEGATIVE_LABEL,
)
from src.preprocessing.cleaner import clean_light_curve
from src.preprocessing.detrending import detrend_flux
from src.preprocessing.phase_fold import phase_fold

logger = logging.getLogger(__name__)


def _bin_and_normalize(
    phase: np.ndarray,
    flux: np.ndarray,
    n_bins: int,
    phase_min: float,
    phase_max: float,
) -> np.ndarray:
    bin_edges = np.linspace(phase_min, phase_max, n_bins + 1)
    binned = np.full(n_bins, np.nan)

    for i in range(n_bins):
        mask = (phase >= bin_edges[i]) & (phase < bin_edges[i + 1])
        if mask.any():
            binned[i] = np.nanmean(flux[mask])

    # Interpolate empty bins from neighbors
    nan_mask = np.isnan(binned)
    if nan_mask.any() and not nan_mask.all():
        valid_idx = np.where(~nan_mask)[0]
        all_idx = np.arange(n_bins)
        binned = np.interp(all_idx, valid_idx, binned[valid_idx])
    elif nan_mask.all():
        binned = np.zeros(n_bins)

    mean = binned.mean()
    std = binned.std()
    if std == 0.0:
        std = 1.0
    binned = (binned - mean) / std

    return binned.reshape(-1, 1)


def generate_global_view(phase: np.ndarray, flux: np.ndarray) -> np.ndarray:
    return _bin_and_normalize(phase, flux, GLOBAL_VIEW_LENGTH, -0.5, 0.5)


def generate_local_view(phase: np.ndarray, flux: np.ndarray) -> np.ndarray:
    mask = np.abs(phase) <= PHASE_WINDOW
    local_phase = phase[mask]
    local_flux = flux[mask]
    return _bin_and_normalize(
        local_phase, local_flux, LOCAL_VIEW_LENGTH, -PHASE_WINDOW, PHASE_WINDOW
    )


def run_full_preprocessing(csv_path: str) -> None:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

    df = pd.read_csv(csv_path, comment="#")
    df = df[df[LABEL_COLUMN].isin([POSITIVE_LABEL, NEGATIVE_LABEL])].reset_index(
        drop=True
    )

    # Identify flux columns (PDCSAP-style: columns starting with "flux_")
    # Kepler CSV stores the folded/processed flux inline; the raw time-series
    # columns follow the pattern "flux_N" where N is an integer index.
    flux_cols = [c for c in df.columns if c.startswith("flux_")]

    global_views = []
    local_views = []
    labels = []
    koi_ids = []
    skipped = 0

    for idx, row in df.iterrows():
        koi_id = str(row.get("kepoi_name", row.get("kepid", idx)))

        period = row.get(PERIOD_COLUMN)
        epoch = row.get(EPOCH_COLUMN)

        if pd.isna(period) or pd.isna(epoch) or period <= 0:
            logger.warning("Skipping %s: missing or invalid period/epoch.", koi_id)
            skipped += 1
            continue

        if not flux_cols:
            logger.warning(
                "Skipping %s: no flux_N columns found in dataset.", koi_id
            )
            skipped += 1
            continue

        raw_flux = row[flux_cols].values.astype(float)
        time = np.arange(len(raw_flux), dtype=float)  # proxy cadence index

        try:
            cleaned = clean_light_curve(raw_flux)
        except ValueError as exc:
            logger.warning("Skipping %s: %s", koi_id, exc)
            skipped += 1
            continue

        # Replace NaN with median before detrending so savgol_filter doesn't fail
        nan_mask = np.isnan(cleaned)
        if nan_mask.any():
            cleaned[nan_mask] = np.nanmedian(cleaned)

        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            detrended = detrend_flux(cleaned)

        folded_phase, folded_flux = phase_fold(time, detrended, period, epoch)

        global_view = generate_global_view(folded_phase, folded_flux)
        local_view = generate_local_view(folded_phase, folded_flux)

        global_views.append(global_view)
        local_views.append(local_view)
        labels.append(1 if row[LABEL_COLUMN] == POSITIVE_LABEL else 0)
        koi_ids.append(koi_id)

    os.makedirs(DATA_PROCESSED_PATH, exist_ok=True)

    global_arr = np.stack(global_views, axis=0)   # (N, 2001, 1)
    local_arr = np.stack(local_views, axis=0)      # (N, 201, 1)
    labels_arr = np.array(labels, dtype=int)        # (N,)
    koi_ids_arr = np.array(koi_ids, dtype=str)      # (N,)

    np.save(os.path.join(DATA_PROCESSED_PATH, "global_views.npy"), global_arr)
    np.save(os.path.join(DATA_PROCESSED_PATH, "local_views.npy"), local_arr)
    np.save(os.path.join(DATA_PROCESSED_PATH, "labels.npy"), labels_arr)
    np.save(os.path.join(DATA_PROCESSED_PATH, "koi_ids.npy"), koi_ids_arr)

    n_total = len(df)
    n_saved = len(labels_arr)
    n_confirmed = labels_arr.sum()
    n_false_positive = n_saved - n_confirmed

    print(f"\nPreprocessing complete")
    print(f"  Total rows in filtered dataset : {n_total}")
    print(f"  Skipped (errors)               : {skipped}")
    print(f"  Saved                          : {n_saved}")
    print(f"  Class distribution             : CONFIRMED={n_confirmed}, FALSE POSITIVE={n_false_positive}")
    print(f"  Outputs written to             : {DATA_PROCESSED_PATH}")
