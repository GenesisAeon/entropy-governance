"""Tests for entropy_governance.cli."""

from __future__ import annotations

import yaml
from typer.testing import CliRunner

from entropy_governance import __version__
from entropy_governance.cli import app

runner = CliRunner()


class TestVersion:
    def test_exit_code(self):
        result = runner.invoke(app, ["version"])
        assert result.exit_code == 0

    def test_version_string(self):
        result = runner.invoke(app, ["version"])
        assert __version__ in result.output


class TestEntropyPrice:
    def test_basic(self):
        result = runner.invoke(app, ["entropy-price", "2.0", "1.0"])
        assert result.exit_code == 0
        assert "2.000000" in result.output

    def test_kappa_option(self):
        result = runner.invoke(app, ["entropy-price", "4.0", "2.0", "--kappa", "0.5"])
        assert result.exit_code == 0
        assert "1.000000" in result.output

    def test_kappa_short(self):
        result = runner.invoke(app, ["entropy-price", "4.0", "2.0", "-k", "0.5"])
        assert result.exit_code == 0

    def test_invalid_delta_t(self):
        result = runner.invoke(app, ["entropy-price", "1.0", "0.0"])
        assert result.exit_code != 0

    def test_negative_delta_t(self):
        result = runner.invoke(app, ["entropy-price", "1.0", "-1.0"])
        assert result.exit_code != 0


class TestGovernanceSim:
    def test_default(self):
        result = runner.invoke(app, ["governance-sim"])
        assert result.exit_code == 0
        assert "CREP" in result.output

    def test_custom_steps(self):
        result = runner.invoke(app, ["governance-sim", "--steps", "50"])
        assert result.exit_code == 0

    def test_custom_s_max(self):
        result = runner.invoke(app, ["governance-sim", "--s-max", "5.0"])
        assert result.exit_code == 0

    def test_custom_dt(self):
        result = runner.invoke(app, ["governance-sim", "--dt", "0.5"])
        assert result.exit_code == 0

    def test_tesseract_slices_shown(self):
        result = runner.invoke(app, ["governance-sim"])
        assert "Tesseract" in result.output


class TestDuality:
    def test_basic(self):
        result = runner.invoke(app, ["duality", "2.0", "2.718281828"])
        assert result.exit_code == 0
        assert "D = " in result.output

    def test_alpha_one(self):
        result = runner.invoke(app, ["duality", "3.0", "1.0", "--alpha", "1.0"])
        assert result.exit_code == 0
        assert "3.000000" in result.output

    def test_alpha_short(self):
        result = runner.invoke(app, ["duality", "2.0", "1.0", "-a", "0.0"])
        assert result.exit_code == 0

    def test_invalid_volume(self):
        result = runner.invoke(app, ["duality", "1.0", "0.0"])
        assert result.exit_code != 0

    def test_invalid_alpha(self):
        result = runner.invoke(app, ["duality", "1.0", "1.0", "--alpha", "2.0"])
        assert result.exit_code != 0


class TestTableExport:
    def test_custom_output(self, tmp_path):
        out = tmp_path / "custom.yaml"
        result = runner.invoke(app, ["table-export", "--output", str(out)])
        assert result.exit_code == 0
        assert out.exists()

    def test_yaml_content(self, tmp_path):
        out = tmp_path / "export.yaml"
        runner.invoke(app, ["table-export", "--output", str(out)])
        data = yaml.safe_load(out.read_text())
        assert "S_A" in data["domains"]["governance"]
        assert "S_V" in data["domains"]["governance"]

    def test_custom_domain(self, tmp_path):
        out = tmp_path / "export.yaml"
        result = runner.invoke(app, ["table-export", "--output", str(out), "--domain", "physics"])
        assert result.exit_code == 0
        data = yaml.safe_load(out.read_text())
        assert "physics" in data["domains"]

    def test_output_message(self, tmp_path):
        out = tmp_path / "msg.yaml"
        result = runner.invoke(app, ["table-export", "--output", str(out)])
        assert "Exported" in result.output
