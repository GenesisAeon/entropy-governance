"""Tests for entropy_governance.core."""

from __future__ import annotations

import math

import numpy as np
import pytest
import sympy as sp

from entropy_governance.core import (
    DUALITY_A,
    DUALITY_V,
    crep,
    duality_factor,
    entropy_price,
)

# ---------------------------------------------------------------------------
# entropy_price
# ---------------------------------------------------------------------------


class TestEntropyPrice:
    def test_basic(self):
        assert entropy_price(2.0, 1.0) == pytest.approx(2.0)

    def test_kappa_scaling(self):
        assert entropy_price(4.0, 2.0, kappa=0.5) == pytest.approx(1.0)

    def test_negative_delta_s(self):
        assert entropy_price(-3.0, 1.0) == pytest.approx(-3.0)

    def test_delta_t_zero_raises(self):
        with pytest.raises(ValueError, match="delta_t"):
            entropy_price(1.0, 0.0)

    def test_delta_t_negative_raises(self):
        with pytest.raises(ValueError, match="delta_t"):
            entropy_price(1.0, -1.0)

    def test_large_kappa(self):
        result = entropy_price(1.0, 1.0, kappa=1000.0)
        assert result == pytest.approx(1000.0)

    def test_fractional(self):
        result = entropy_price(1.0, 4.0, kappa=2.0)
        assert result == pytest.approx(0.5)


# ---------------------------------------------------------------------------
# crep
# ---------------------------------------------------------------------------


class TestCrep:
    def test_unit_step(self):
        t = np.array([0.0, 1.0])
        ds = np.array([1.0, 1.0])
        assert crep(t, ds, 2.0) == pytest.approx(0.5)

    def test_normalisation(self):
        t = np.array([0.0, 1.0])
        ds = np.array([2.0, 2.0])
        assert crep(t, ds, 2.0) == pytest.approx(1.0)

    def test_zero_production(self):
        t = np.array([0.0, 1.0, 2.0])
        ds = np.zeros(3)
        assert crep(t, ds, 1.0) == pytest.approx(0.0)

    def test_absolute_value(self):
        t = np.array([0.0, 1.0])
        ds = np.array([-1.0, -1.0])
        assert crep(t, ds, 2.0) == pytest.approx(0.5)

    def test_sine_wave(self):
        t = np.linspace(0, 2 * math.pi, 1000)
        ds = np.cos(t)  # derivative of sin
        result = crep(t, ds, s_max=4.0)
        assert result > 0.0

    def test_mismatched_shapes_raises(self):
        with pytest.raises(ValueError, match="shape"):
            crep(np.array([0.0, 1.0]), np.array([1.0]), 1.0)

    def test_s_max_zero_raises(self):
        with pytest.raises(ValueError, match="s_max"):
            crep(np.array([0.0, 1.0]), np.array([1.0, 1.0]), 0.0)

    def test_s_max_negative_raises(self):
        with pytest.raises(ValueError, match="s_max"):
            crep(np.array([0.0, 1.0]), np.array([1.0, 1.0]), -1.0)

    def test_list_inputs(self):
        result = crep([0.0, 1.0], [1.0, 1.0], 2.0)
        assert isinstance(result, float)


# ---------------------------------------------------------------------------
# duality_factor
# ---------------------------------------------------------------------------


class TestDualityFactor:
    def test_pure_action(self):
        result = duality_factor(action=3.0, volume=1.0, alpha=1.0)
        assert result == pytest.approx(3.0)

    def test_pure_volume(self):
        result = duality_factor(action=0.0, volume=math.e, alpha=0.0)
        assert result == pytest.approx(1.0)

    def test_blended(self):
        result = duality_factor(action=2.0, volume=math.e, alpha=0.5)
        assert result == pytest.approx(0.5 * 2.0 + 0.5 * 1.0)

    def test_default_alpha(self):
        result = duality_factor(action=2.0, volume=math.e)
        assert result == pytest.approx(1.5)

    def test_volume_zero_raises(self):
        with pytest.raises(ValueError, match="volume"):
            duality_factor(1.0, 0.0)

    def test_volume_negative_raises(self):
        with pytest.raises(ValueError, match="volume"):
            duality_factor(1.0, -5.0)

    def test_alpha_out_of_range_low(self):
        with pytest.raises(ValueError, match="alpha"):
            duality_factor(1.0, 1.0, alpha=-0.1)

    def test_alpha_out_of_range_high(self):
        with pytest.raises(ValueError, match="alpha"):
            duality_factor(1.0, 1.0, alpha=1.1)

    def test_alpha_boundary_zero(self):
        result = duality_factor(5.0, math.e, alpha=0.0)
        assert result == pytest.approx(1.0)

    def test_alpha_boundary_one(self):
        result = duality_factor(5.0, math.e, alpha=1.0)
        assert result == pytest.approx(5.0)


# ---------------------------------------------------------------------------
# Symbolic duality objects
# ---------------------------------------------------------------------------


class TestDualitySymbols:
    def test_duality_a_is_equation(self):
        assert isinstance(DUALITY_A, sp.Eq)

    def test_duality_v_is_equation(self):
        assert isinstance(DUALITY_V, sp.Eq)

    def test_duality_a_contains_kappa(self):
        kappa = sp.Symbol("kappa", positive=True)
        assert kappa in DUALITY_A.free_symbols

    def test_duality_v_contains_lambda(self):
        lam = sp.Symbol("lambda", positive=True)
        assert lam in DUALITY_V.free_symbols
