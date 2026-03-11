"""Core entropy-governance physics: S∝A / S∝V duality, entropic price, CREP."""

from __future__ import annotations

import numpy as np
import sympy as sp

# ---------------------------------------------------------------------------
# Symbolic duality equations (SymPy)
# ---------------------------------------------------------------------------

_t = sp.Symbol("t", real=True, positive=True)
_kappa, _lam = sp.symbols("kappa lambda", positive=True)
_S = sp.Function("S")
_A = sp.Function("A")
_V = sp.Function("V")

# S ∝ A  — action-governed minimal entropy production
DUALITY_A: sp.Eq = sp.Eq(_S(_t), _kappa * _A(_t))

# S ∝ V  — volume-governed maximal information entropy
DUALITY_V: sp.Eq = sp.Eq(_S(_t), _lam * sp.log(_V(_t)))


# ---------------------------------------------------------------------------
# Numerical functions
# ---------------------------------------------------------------------------


def entropy_price(delta_s: float, delta_t: float, kappa: float = 1.0) -> float:
    """Entropic price  P_E = (ΔS / Δt) · κ.

    Args:
        delta_s: Change in entropy ΔS.
        delta_t: Time interval Δt (must be > 0).
        kappa:   Coupling constant κ (default 1.0).

    Returns:
        Entropic price P_E as a float.

    Raises:
        ValueError: If *delta_t* is zero or negative.
    """
    if delta_t <= 0:
        raise ValueError(f"delta_t must be positive, got {delta_t}")
    return (delta_s / delta_t) * kappa


def crep(
    t_values: np.ndarray,
    ds_dt: np.ndarray,
    s_max: float,
) -> float:
    """Cumulative Relative Entropy Production (CREP).

    CREP = ∫|dS/dt| dt / S_max

    Numerically integrates the absolute entropy production rate and normalises
    by *s_max*.

    Args:
        t_values: 1-D array of time points (monotonically increasing).
        ds_dt:    1-D array of dS/dt values at each time point.
        s_max:    Normalisation constant S_max (must be > 0).

    Returns:
        Dimensionless CREP value.

    Raises:
        ValueError: If *s_max* is zero or arrays have different lengths.
    """
    t_values = np.asarray(t_values, dtype=float)
    ds_dt = np.asarray(ds_dt, dtype=float)
    if t_values.shape != ds_dt.shape:
        raise ValueError("t_values and ds_dt must have the same shape")
    if s_max <= 0:
        raise ValueError(f"s_max must be positive, got {s_max}")
    return float(np.trapezoid(np.abs(ds_dt), t_values) / s_max)


def duality_factor(action: float, volume: float, alpha: float = 0.5) -> float:
    """Blended duality metric  D = α·A + (1−α)·ln(V).

    Interpolates between the action-governed (α = 1) and volume-governed
    (α = 0) extremes.

    Args:
        action: Action value A (any real number).
        volume: Volume V (must be > 0 for ln to be defined).
        alpha:  Blend coefficient α ∈ [0, 1] (default 0.5).

    Returns:
        Blended duality metric D.

    Raises:
        ValueError: If *volume* ≤ 0 or *alpha* outside [0, 1].
    """
    if volume <= 0:
        raise ValueError(f"volume must be positive, got {volume}")
    if not 0.0 <= alpha <= 1.0:
        raise ValueError(f"alpha must be in [0, 1], got {alpha}")
    return alpha * action + (1.0 - alpha) * float(np.log(volume))
