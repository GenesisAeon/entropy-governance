"""Tests for entropy_governance.tesseract."""

from __future__ import annotations

import numpy as np
import pytest

from entropy_governance.tesseract import TesseractSlice


class TestTesseractSliceInit:
    def test_default_dt(self):
        ts = TesseractSlice()
        assert ts.dt == pytest.approx(0.1)

    def test_custom_dt(self):
        ts = TesseractSlice(dt=0.5)
        assert ts.dt == pytest.approx(0.5)

    def test_dt_zero_raises(self):
        with pytest.raises(ValueError, match="dt"):
            TesseractSlice(dt=0.0)

    def test_dt_negative_raises(self):
        with pytest.raises(ValueError, match="dt"):
            TesseractSlice(dt=-1.0)

    def test_has_implosive_genesis_is_bool(self):
        ts = TesseractSlice()
        assert isinstance(ts.has_implosive_genesis, bool)


class TestTesseractSliceSlice:
    def setup_method(self):
        self.ts = TesseractSlice(dt=0.1)

    def test_default_n_steps(self):
        s = self.ts.slice(0.0)
        assert len(s) == 4

    def test_shape(self):
        s = self.ts.slice(1.0, n_steps=6)
        assert s.shape == (6,)

    def test_values(self):
        s = self.ts.slice(0.0, n_steps=3)
        np.testing.assert_allclose(s, [0.0, 0.1, 0.2])

    def test_t_start_offset(self):
        s = self.ts.slice(5.0, n_steps=2)
        np.testing.assert_allclose(s, [5.0, 5.1])

    def test_strictly_increasing(self):
        s = self.ts.slice(0.0, n_steps=10)
        assert np.all(np.diff(s) > 0)

    def test_n_steps_one(self):
        s = self.ts.slice(3.0, n_steps=1)
        assert s.shape == (1,)
        assert s[0] == pytest.approx(3.0)

    def test_n_steps_zero_raises(self):
        with pytest.raises(ValueError, match="n_steps"):
            self.ts.slice(0.0, n_steps=0)

    def test_n_steps_negative_raises(self):
        with pytest.raises(ValueError, match="n_steps"):
            self.ts.slice(0.0, n_steps=-1)

    def test_negative_t_start(self):
        s = self.ts.slice(-1.0, n_steps=3)
        np.testing.assert_allclose(s, [-1.0, -0.9, -0.8])

    def test_returns_ndarray(self):
        s = self.ts.slice(0.0)
        assert isinstance(s, np.ndarray)


class TestTesseractMultiSlice:
    def setup_method(self):
        self.ts = TesseractSlice(dt=0.1)

    def test_shape(self):
        result = self.ts.multi_slice([0.0, 1.0, 2.0], n_steps=4)
        assert result.shape == (3, 4)

    def test_first_row(self):
        result = self.ts.multi_slice([0.0, 10.0])
        np.testing.assert_allclose(result[0], [0.0, 0.1, 0.2, 0.3])

    def test_second_row(self):
        result = self.ts.multi_slice([0.0, 10.0])
        np.testing.assert_allclose(result[1], [10.0, 10.1, 10.2, 10.3])

    def test_empty_list(self):
        result = self.ts.multi_slice([])
        assert result.shape == (0,)

    def test_single_origin(self):
        result = self.ts.multi_slice([5.0], n_steps=2)
        assert result.shape == (1, 2)
