"""Tesseract time-slices for 4-D governance simulation.

Optionally integrates with ``implosive-genesis`` for fractal chronology
validation.  When that package is not installed the built-in
:class:`_FallbackValidator` is used instead so the module works standalone.
"""

from __future__ import annotations

import numpy as np

# ---------------------------------------------------------------------------
# Optional implosive-genesis integration
# ---------------------------------------------------------------------------

try:
    from implosive_genesis.chronology import (
        ChronologyValidator as _ChronologyValidator,  # type: ignore[import-not-found]
    )

    _HAS_IMPLOSIVE_GENESIS = True
except ModuleNotFoundError:
    _HAS_IMPLOSIVE_GENESIS = False

    class _ChronologyValidator:  # type: ignore[no-redef]
        """Fallback validator used when implosive-genesis is not installed."""

        def validate(self, slices: np.ndarray) -> None:
            """Ensure slices are strictly increasing."""
            if len(slices) > 1 and not np.all(np.diff(slices) > 0):
                raise ValueError("Time slices must be strictly increasing.")


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


class TesseractSlice:
    """4-D hypercube time-slices for governance simulation.

    Each call to :meth:`slice` generates *n_steps* evenly-spaced time points
    starting at *t_start* with step *dt*.  The resulting array is validated
    via a :class:`ChronologyValidator` (implosive-genesis when available,
    built-in fallback otherwise).

    Args:
        dt: Time step between consecutive slices (default 0.1).
    """

    def __init__(self, dt: float = 0.1) -> None:
        if dt <= 0:
            raise ValueError(f"dt must be positive, got {dt}")
        self.dt = dt
        self._validator = _ChronologyValidator()

    @property
    def has_implosive_genesis(self) -> bool:
        """True when the implosive-genesis back-end is active."""
        return _HAS_IMPLOSIVE_GENESIS

    def slice(self, t_start: float, n_steps: int = 4) -> np.ndarray:
        """Generate a 1-D array of *n_steps* time points.

        Args:
            t_start: Starting time.
            n_steps: Number of slices to generate (default 4, minimum 1).

        Returns:
            1-D numpy array of shape ``(n_steps,)``.

        Raises:
            ValueError: If *n_steps* < 1.
        """
        if n_steps < 1:
            raise ValueError(f"n_steps must be >= 1, got {n_steps}")
        slices = np.array([t_start + i * self.dt for i in range(n_steps)])
        self._validator.validate(slices)
        return slices

    def multi_slice(self, t_starts: list[float], n_steps: int = 4) -> np.ndarray:
        """Generate a 2-D array of time slices for multiple origins.

        Args:
            t_starts: List of starting time values.
            n_steps:  Number of steps per origin.

        Returns:
            2-D numpy array of shape ``(len(t_starts), n_steps)``.
        """
        return np.array([self.slice(t, n_steps) for t in t_starts])
