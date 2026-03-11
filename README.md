# entropy-governance

**Entropy-Governance Duality framework** — S∝A (action-governed) vs. S∝V (volume-governed), entropic pricing, CREP and Tesseract time-slices.
Direct bridge to `entropy-table` and optional fractal integration with `implosive-genesis`.

[![CI](https://github.com/GenesisAeon/entropy-governance/actions/workflows/ci.yml/badge.svg)](https://github.com/GenesisAeon/entropy-governance/actions/workflows/ci.yml)
[![Coverage](https://img.shields.io/badge/coverage-98%25-brightgreen)](https://github.com/GenesisAeon/entropy-governance/actions/workflows/ci.yml)
[![Python 3.11+](https://img.shields.io/badge/python-3.11%2B-blue)](https://www.python.org)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![PyPI](https://img.shields.io/pypi/v/entropy-governance)](https://pypi.org/project/entropy-governance/)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.18962979.svg)](https://doi.org/10.5281/zenodo.18962979)

---

## Install

```bash
pip install entropy-governance
# or
uv add entropy-governance
```

## Quickstart

```bash
# Entropic price P_E = (ΔS/Δt)·κ
eg entropy-price 2.0 1.0

# Governance simulation with Tesseract slices + CREP
eg governance-sim --steps 200 --s-max 10.0

# Blended duality metric D = α·A + (1−α)·ln(V)
eg duality 3.0 2.718281828 --alpha 0.5

# Export to entropy-table YAML
eg table-export --output domains.yaml
```

## Physics

### S∝A — Action-governed minimal entropy production

```
S(t) = κ · A(t)
```

The entropy is proportional to the integrated action — minimal production regime.

### S∝V — Volume-governed maximal information entropy

```
S(t) = λ · ln V(t)
```

The entropy scales logarithmically with volume — maximal information regime.

### Entropic Price

```
P_E = (ΔS / Δt) · κ
```

Rate of entropy change weighted by a coupling constant.

### CREP — Cumulative Relative Entropy Production

```
CREP = ∫|dS/dt| dt / S_max
```

Dimensionless measure of total entropy production normalised by a reference maximum.

### Tesseract Time-Slices

4-D hypercube time slices for governance simulation — generates evenly-spaced time arrays with optional chronology validation via `implosive-genesis`.

## API

```python
from entropy_governance import entropy_price, crep, duality_factor, TesseractSlice, EntropyTableBridge
import numpy as np

# Entropic price
p = entropy_price(delta_s=2.0, delta_t=1.0, kappa=1.5)

# CREP over a simulation run
t = np.linspace(0, 10, 1000)
ds_dt = np.sin(t) * 0.5
c = crep(t, ds_dt, s_max=10.0)

# Tesseract slices
ts = TesseractSlice(dt=0.1)
slices = ts.slice(t_start=0.0, n_steps=4)

# entropy-table bridge
bridge = EntropyTableBridge(domain="governance")
bridge.add_relation("S_A", 0.618)
bridge.add_relation("S_V", 1.618)
bridge.export("domains.yaml")
```

## Development

```bash
uv sync --dev
pre-commit install
uv run pytest          # runs with coverage report
uv run ruff check .
```

## Citation

If you use entropy-governance in academic work, please cite:

```
GenesisAeon Team. (2026). entropy-governance: Entropy-Governance Duality (v0.1.0) [Software].
Zenodo. https://doi.org/10.5281/zenodo.18962979
```

> **DOI**: 10.5281/zenodo.18962979
> **PyPI**: `pip install entropy-governance==0.1.0`

---

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for the full release history.

---

Built on [diamond-setup](https://github.com/GenesisAeon/diamond-setup) · [SymPy](https://www.sympy.org/) · [NumPy](https://numpy.org/) · [Typer](https://typer.tiangolo.com/) · [Rich](https://rich.readthedocs.io/)
