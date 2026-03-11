# Entropy-Governance

**Entropy-Governance** is a Python framework for modelling the **S∝A / S∝V duality**, computing entropic prices, measuring cumulative relative entropy production (CREP), and running 4-D Tesseract time-slice simulations.

## Theoretical Background

### S∝A — Action-governed minimal entropy production

$$S(t) = \kappa \cdot A(t)$$

Entropy is proportional to the integrated action.  This regime describes systems
in which entropy production is *minimised* and tightly coupled to the dynamical
action.

### S∝V — Volume-governed maximal information entropy

$$S(t) = \lambda \cdot \ln V(t)$$

Entropy scales logarithmically with the phase-space volume.  This is the *maximal
information entropy* regime (Boltzmann / Shannon).

### Entropic Price

$$P_E = \frac{\Delta S}{\Delta t} \cdot \kappa$$

The instantaneous cost of entropy production, weighted by coupling constant κ.

### CREP

$$\text{CREP} = \frac{\int |\dot{S}|\, dt}{S_{\max}}$$

A dimensionless indicator of cumulative irreversibility relative to a reference
maximum.

## Quickstart

```bash
pip install entropy-governance
eg --help
```

```python
from entropy_governance import entropy_price, crep, duality_factor
import numpy as np

# P_E
print(entropy_price(2.0, 1.0, kappa=1.0))   # 2.0

# CREP over a sinusoidal run
t = np.linspace(0, 10, 1000)
c = crep(t, np.sin(t), s_max=10.0)
print(f"CREP = {c:.4f}")
```

## CLI commands

| Command | Description |
|---------|-------------|
| `eg entropy-price ΔS Δt` | Compute entropic price |
| `eg governance-sim` | Run simulation with Tesseract slices |
| `eg duality A V` | Blended duality metric |
| `eg table-export` | Export to entropy-table YAML |
| `eg version` | Show package version |

## Citation

If you use entropy-governance in academic work, please cite:

```
GenesisAeon Team. (2026). entropy-governance: Entropy-Governance Duality (v0.1.0) [Software].
Zenodo. https://doi.org/10.5281/zenodo.18962979
```

> **DOI**: 10.5281/zenodo.18962979
