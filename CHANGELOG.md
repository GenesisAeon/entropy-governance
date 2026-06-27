# Changelog

All notable changes to **entropy-governance** are documented in this file.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/)
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [1.0.0] — 2026

### Added

- Standardized GenesisAeon ecosystem release tooling: `.zenodo.json`,
  `RELEASE_GUIDE.md`, `CONTRIBUTING.md`, issue/PR templates.

### Changed

- Project metadata (`pyproject.toml`) normalized for the ecosystem-wide
  v1.0.0 milestone: version bumped to `1.0.0`, `implosive-genesis`
  dependency pin raised to `>=1.0.0` to match its released version.

---

## [0.1.0] — 2026-03-11

### Added

- **Core physics engine** (`entropy_governance.core`)
  - `entropy_price(delta_s, delta_t, kappa)` — entropic price P_E = (ΔS/Δt)·κ
  - `crep(t_values, ds_dt, s_max)` — Cumulative Relative Entropy Production
  - `duality_factor(action, volume, alpha)` — blended S∝A / S∝V metric
  - Symbolic SymPy equations `DUALITY_A` and `DUALITY_V`

- **Tesseract time-slices** (`entropy_governance.tesseract`)
  - `TesseractSlice` — 4-D hypercube time-slice generator
  - Optional `implosive-genesis` back-end via `FallbackValidator`

- **Entropy-table bridge** (`entropy_governance.entropy_table_bridge`)
  - `EntropyTableBridge` — export/import entropy metrics as YAML
  - Compatible with [entropy-table](https://github.com/GenesisAeon/entropy-table) schema

- **CLI** (`eg` entry-point)
  - `eg entropy-price` — compute P_E
  - `eg governance-sim` — run full simulation with Tesseract slices and CREP output
  - `eg duality` — compute blended duality metric
  - `eg table-export` — export relations to entropy-table YAML
  - `eg version` — show installed version

- **Documentation** (MkDocs Material)
  - Home / Theoretical Background / API Reference / CLI Reference

- **CI / quality gates**
  - 96 / 96 tests passing, ≥ 98 % coverage
  - Ruff clean (`E, F, B, I, W, UP, C4, SIM`)
  - `uv run mkdocs build --strict` passes with no warnings

**DOI**: https://doi.org/10.5281/zenodo.18962979

[0.1.0]: https://github.com/GenesisAeon/entropy-governance/releases/tag/v0.1.0
