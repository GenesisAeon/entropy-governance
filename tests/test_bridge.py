"""Tests for entropy_governance.entropy_table_bridge."""

from __future__ import annotations

from pathlib import Path

import pytest
import yaml

from entropy_governance.entropy_table_bridge import EntropyTableBridge


class TestEntropyTableBridgeInit:
    def test_default_domain(self):
        b = EntropyTableBridge()
        assert b.domain == "governance"

    def test_custom_domain(self):
        b = EntropyTableBridge(domain="physics")
        assert b.domain == "physics"

    def test_empty_domain_raises(self):
        with pytest.raises(ValueError, match="domain"):
            EntropyTableBridge(domain="")

    def test_empty_relations(self):
        b = EntropyTableBridge()
        assert b.relations == {}

    def test_empty_metadata(self):
        b = EntropyTableBridge()
        assert b.metadata == {}


class TestAddRelation:
    def test_add_float(self):
        b = EntropyTableBridge()
        b.add_relation("S_A", 0.618)
        assert b.relations["S_A"] == pytest.approx(0.618)

    def test_add_string(self):
        b = EntropyTableBridge()
        b.add_relation("label", "test")
        assert b.relations["label"] == "test"

    def test_overwrite(self):
        b = EntropyTableBridge()
        b.add_relation("x", 1.0)
        b.add_relation("x", 2.0)
        assert b.relations["x"] == pytest.approx(2.0)

    def test_empty_key_raises(self):
        b = EntropyTableBridge()
        with pytest.raises(ValueError, match="key"):
            b.add_relation("", 1.0)

    def test_multiple_relations(self):
        b = EntropyTableBridge()
        b.add_relation("a", 1)
        b.add_relation("b", 2)
        b.add_relation("c", 3)
        assert len(b.relations) == 3


class TestSetMetadata:
    def test_single_entry(self):
        b = EntropyTableBridge()
        b.set_metadata(version="0.1.0")
        assert b.metadata["version"] == "0.1.0"

    def test_multiple_entries(self):
        b = EntropyTableBridge()
        b.set_metadata(author="Test", version="1.0")
        assert b.metadata["author"] == "Test"
        assert b.metadata["version"] == "1.0"

    def test_update(self):
        b = EntropyTableBridge()
        b.set_metadata(version="0.1.0")
        b.set_metadata(version="0.2.0")
        assert b.metadata["version"] == "0.2.0"


class TestExport:
    def test_creates_file(self, tmp_path):
        b = EntropyTableBridge()
        b.add_relation("S_A", 0.618)
        out = b.export(tmp_path / "out.yaml")
        assert out.exists()

    def test_returns_path(self, tmp_path):
        b = EntropyTableBridge()
        result = b.export(tmp_path / "out.yaml")
        assert isinstance(result, Path)

    def test_yaml_structure(self, tmp_path):
        b = EntropyTableBridge(domain="test")
        b.add_relation("x", 42.0)
        out = b.export(tmp_path / "out.yaml")
        data = yaml.safe_load(out.read_text())
        assert data["domains"]["test"]["x"] == pytest.approx(42.0)

    def test_default_path(self, tmp_path, monkeypatch):
        monkeypatch.chdir(tmp_path)
        b = EntropyTableBridge()
        b.add_relation("k", 1.0)
        b.export()
        assert (tmp_path / "domains.yaml").exists()

    def test_metadata_written(self, tmp_path):
        b = EntropyTableBridge()
        b.set_metadata(version="0.1.0")
        out = b.export(tmp_path / "out.yaml")
        data = yaml.safe_load(out.read_text())
        assert "metadata" in data
        assert data["metadata"]["version"] == "0.1.0"

    def test_no_metadata_key_when_empty(self, tmp_path):
        b = EntropyTableBridge()
        out = b.export(tmp_path / "out.yaml")
        data = yaml.safe_load(out.read_text())
        assert "metadata" not in data

    def test_creates_parent_dirs(self, tmp_path):
        b = EntropyTableBridge()
        out = b.export(tmp_path / "deep" / "nested" / "out.yaml")
        assert out.exists()

    def test_string_path(self, tmp_path):
        b = EntropyTableBridge()
        out = b.export(str(tmp_path / "out.yaml"))
        assert isinstance(out, Path)
        assert out.exists()


class TestFromYaml:
    def _write_yaml(self, tmp_path, data):
        p = tmp_path / "domains.yaml"
        p.write_text(yaml.dump(data))
        return p

    def test_load_relations(self, tmp_path):
        data = {"domains": {"gov": {"S_A": 0.618, "S_V": 1.618}}}
        p = self._write_yaml(tmp_path, data)
        b = EntropyTableBridge.from_yaml(p, domain="gov")
        assert b.relations["S_A"] == pytest.approx(0.618)

    def test_domain_mismatch_raises(self, tmp_path):
        data = {"domains": {"other": {}}}
        p = self._write_yaml(tmp_path, data)
        with pytest.raises(KeyError, match="missing"):
            EntropyTableBridge.from_yaml(p, domain="missing")

    def test_metadata_loaded(self, tmp_path):
        data = {"domains": {"gov": {}}, "metadata": {"version": "1.0"}}
        p = self._write_yaml(tmp_path, data)
        b = EntropyTableBridge.from_yaml(p, domain="gov")
        assert b.metadata["version"] == "1.0"

    def test_roundtrip(self, tmp_path):
        b = EntropyTableBridge(domain="rt")
        b.add_relation("alpha", 0.5)
        b.add_relation("beta", 1.5)
        b.set_metadata(source="test")
        out = b.export(tmp_path / "rt.yaml")
        b2 = EntropyTableBridge.from_yaml(out, domain="rt")
        assert b2.relations == pytest.approx({"alpha": 0.5, "beta": 1.5})
