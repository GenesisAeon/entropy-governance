"""Entropy-Governance CLI — `eg` entry-point."""

from __future__ import annotations

from pathlib import Path
from typing import Annotated

import numpy as np
import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from . import __version__
from .core import crep as _crep
from .core import duality_factor as _duality_factor
from .core import entropy_price as _entropy_price
from .entropy_table_bridge import EntropyTableBridge
from .tesseract import TesseractSlice

_HELP = (
    "[bold]Entropy-Governance[/bold] — S∝A vs S∝V duality, "
    "entropic pricing, CREP and Tesseract time-slices."
)

app = typer.Typer(
    name="eg",
    help=_HELP,
    add_completion=True,
    rich_markup_mode="rich",
)
console = Console()
err_console = Console(stderr=True)


# ---------------------------------------------------------------------------
# version
# ---------------------------------------------------------------------------


@app.command()
def version() -> None:
    """Show the entropy-governance version."""
    console.print(f"entropy-governance [bold]{__version__}[/bold]")


# ---------------------------------------------------------------------------
# entropy-price
# ---------------------------------------------------------------------------


@app.command(name="entropy-price")
def cmd_entropy_price(
    delta_s: Annotated[float, typer.Argument(help="Change in entropy ΔS")],
    delta_t: Annotated[float, typer.Argument(help="Time interval Δt (> 0)")],
    kappa: Annotated[float, typer.Option("--kappa", "-k", help="Coupling constant κ")] = 1.0,
) -> None:
    """Calculate the [bold]entropic price[/bold]  P_E = (ΔS / Δt) · κ."""
    try:
        price = _entropy_price(delta_s, delta_t, kappa)
    except ValueError as exc:
        err_console.print(f"[red]Error:[/red] {exc}")
        raise typer.Exit(code=1) from exc

    console.print(
        Panel(
            f"P_E = [bold green]{price:.6f}[/bold green]",
            title="Entropic Price",
            expand=False,
        )
    )


# ---------------------------------------------------------------------------
# governance-sim
# ---------------------------------------------------------------------------


@app.command(name="governance-sim")
def cmd_governance_sim(
    steps: Annotated[int, typer.Option("--steps", "-n", help="Number of simulation steps")] = 100,
    s_max: Annotated[float, typer.Option("--s-max", help="Normalisation constant S_max")] = 10.0,
    dt: Annotated[float, typer.Option("--dt", help="Tesseract time step")] = 0.1,
) -> None:
    """Run a [bold]governance simulation[/bold] with Tesseract time-slices and compute CREP."""
    t = np.linspace(0, 10, steps)
    ds_dt = np.sin(t) * 0.5

    crep_val = _crep(t, ds_dt, s_max)

    ts = TesseractSlice(dt=dt)
    slices = ts.slice(t_start=0.0, n_steps=4)

    tbl = Table(title="Tesseract Slices", show_header=True)
    tbl.add_column("Slice #", style="dim")
    tbl.add_column("t", justify="right")
    for i, s in enumerate(slices):
        tbl.add_row(str(i), f"{s:.4f}")

    console.print(tbl)
    console.print(
        Panel(
            f"CREP = [bold cyan]{crep_val:.6f}[/bold cyan]",
            title=f"Simulation result  (steps={steps}, S_max={s_max})",
            expand=False,
        )
    )


# ---------------------------------------------------------------------------
# duality
# ---------------------------------------------------------------------------


@app.command()
def duality(
    action: Annotated[float, typer.Argument(help="Action value A")],
    volume: Annotated[float, typer.Argument(help="Volume V (> 0)")],
    alpha: Annotated[
        float, typer.Option("--alpha", "-a", help="Blend coefficient α ∈ [0,1]")
    ] = 0.5,
) -> None:
    """Compute the [bold]blended duality metric[/bold]  D = α·A + (1−α)·ln(V)."""
    try:
        d = _duality_factor(action, volume, alpha)
    except ValueError as exc:
        err_console.print(f"[red]Error:[/red] {exc}")
        raise typer.Exit(code=1) from exc

    console.print(
        Panel(
            f"D = [bold magenta]{d:.6f}[/bold magenta]",
            title=f"Duality (α={alpha})",
            expand=False,
        )
    )


# ---------------------------------------------------------------------------
# table-export
# ---------------------------------------------------------------------------


@app.command(name="table-export")
def cmd_table_export(
    output: Annotated[Path, typer.Option("--output", "-o", help="Output YAML path")] = Path(
        "domains.yaml"
    ),
    domain: Annotated[str, typer.Option("--domain", "-d", help="Domain key")] = "governance",
) -> None:
    """Export default S∝A / S∝V relations to an [bold]entropy-table YAML[/bold]."""
    bridge = EntropyTableBridge(domain=domain)
    bridge.add_relation("S_A", 0.618)
    bridge.add_relation("S_V", 1.618)
    bridge.add_relation("crep_baseline", 0.5)
    bridge.set_metadata(generated_by="entropy-governance", version=__version__)
    path = bridge.export(output)
    console.print(f"[bold yellow]Exported to[/bold yellow] {path}")


# ---------------------------------------------------------------------------
# entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    app()
