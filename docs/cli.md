# CLI Reference

The `eg` command is the entry-point for entropy-governance.

```bash
eg --help
```

---

## `eg entropy-price`

Compute the entropic price P_E = (ΔS / Δt) · κ.

```bash
eg entropy-price DELTA_S DELTA_T [--kappa FLOAT]
```

| Argument / Option | Default | Description |
|-------------------|---------|-------------|
| `DELTA_S` | — | Change in entropy ΔS |
| `DELTA_T` | — | Time interval Δt (must be > 0) |
| `--kappa` / `-k` | `1.0` | Coupling constant κ |

**Example:**

```bash
eg entropy-price 2.0 1.0 --kappa 1.5
# P_E = 3.000000
```

---

## `eg governance-sim`

Run a governance simulation with Tesseract time-slices and compute CREP.

```bash
eg governance-sim [--steps INT] [--s-max FLOAT] [--dt FLOAT]
```

| Option | Default | Description |
|--------|---------|-------------|
| `--steps` / `-n` | `100` | Number of simulation steps |
| `--s-max` | `10.0` | Normalisation constant S_max |
| `--dt` | `0.1` | Tesseract time step |

**Example:**

```bash
eg governance-sim --steps 500 --s-max 20.0
```

---

## `eg duality`

Compute the blended duality metric D = α·A + (1−α)·ln(V).

```bash
eg duality ACTION VOLUME [--alpha FLOAT]
```

| Argument / Option | Default | Description |
|-------------------|---------|-------------|
| `ACTION` | — | Action value A |
| `VOLUME` | — | Volume V (must be > 0) |
| `--alpha` / `-a` | `0.5` | Blend coefficient α ∈ [0, 1] |

**Example:**

```bash
eg duality 3.0 2.718281828 --alpha 0.5
# D = 2.000000
```

---

## `eg table-export`

Export default S∝A / S∝V relations to an entropy-table YAML file.

```bash
eg table-export [--output PATH] [--domain TEXT]
```

| Option | Default | Description |
|--------|---------|-------------|
| `--output` / `-o` | `domains.yaml` | Output file path |
| `--domain` / `-d` | `governance` | Domain key in the YAML |

**Example:**

```bash
eg table-export --output exports/my-domain.yaml --domain physics
```

---

## `eg version`

Show the installed entropy-governance version.

```bash
eg version
```
