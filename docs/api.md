# API Reference

## `entropy_governance.core`

### `entropy_price`

```python
entropy_price(delta_s: float, delta_t: float, kappa: float = 1.0) -> float
```

Computes the **entropic price** P_E = (ΔS / Δt) · κ.

| Parameter | Type | Description |
|-----------|------|-------------|
| `delta_s` | `float` | Change in entropy ΔS |
| `delta_t` | `float` | Time interval Δt (must be > 0) |
| `kappa`   | `float` | Coupling constant κ (default 1.0) |

**Raises:** `ValueError` if `delta_t ≤ 0`.

---

### `crep`

```python
crep(t_values: np.ndarray, ds_dt: np.ndarray, s_max: float) -> float
```

**Cumulative Relative Entropy Production** — CREP = ∫|dS/dt| dt / S_max.

| Parameter  | Type         | Description |
|------------|--------------|-------------|
| `t_values` | `np.ndarray` | Time points (monotonically increasing) |
| `ds_dt`    | `np.ndarray` | Entropy production rate dS/dt |
| `s_max`    | `float`      | Normalisation constant (must be > 0) |

**Raises:** `ValueError` if arrays have mismatched shapes or `s_max ≤ 0`.

---

### `duality_factor`

```python
duality_factor(action: float, volume: float, alpha: float = 0.5) -> float
```

Blended duality metric D = α·A + (1−α)·ln(V).

| Parameter | Type    | Description |
|-----------|---------|-------------|
| `action`  | `float` | Action value A |
| `volume`  | `float` | Volume V (must be > 0) |
| `alpha`   | `float` | Blend coefficient α ∈ [0, 1] (default 0.5) |

**Raises:** `ValueError` if `volume ≤ 0` or `alpha ∉ [0, 1]`.

---

### Symbolic constants

| Name        | Type      | Description |
|-------------|-----------|-------------|
| `DUALITY_A` | `sympy.Eq` | S(t) = κ · A(t) — action-governed |
| `DUALITY_V` | `sympy.Eq` | S(t) = λ · ln V(t) — volume-governed |

---

## `entropy_governance.tesseract`

### `TesseractSlice`

```python
TesseractSlice(dt: float = 0.1)
```

4-D hypercube time-slices for governance simulation.

#### Methods

**`slice(t_start, n_steps=4) → np.ndarray`**

Generate `n_steps` evenly-spaced time points starting at `t_start`.

**`multi_slice(t_starts, n_steps=4) → np.ndarray`**

Generate a 2-D array of shape `(len(t_starts), n_steps)`.

#### Properties

**`has_implosive_genesis`** → `bool`
True when the `implosive-genesis` back-end is active.

---

## `entropy_governance.entropy_table_bridge`

### `EntropyTableBridge`

```python
EntropyTableBridge(domain: str = "governance")
```

Export and import entropy-governance metrics as entropy-table compatible YAML.

#### Methods

| Method | Description |
|--------|-------------|
| `add_relation(key, value)` | Add a key-value pair to the domain |
| `set_metadata(**kwargs)` | Attach metadata to the export |
| `export(filepath) → Path` | Write YAML file |
| `from_yaml(filepath, domain) → EntropyTableBridge` | Class method — load from file |
