"""entropy-table YAML bridge — export governance metrics to a domain file."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml


class EntropyTableBridge:
    """Export entropy-governance metrics to an entropy-table compatible YAML file.

    The produced YAML follows the ``domains.<name>`` structure used by the
    entropy-table project.

    Args:
        domain: Logical domain name written under the ``domains`` key
                (default ``"governance"``).
    """

    def __init__(self, domain: str = "governance") -> None:
        if not domain:
            raise ValueError("domain must be a non-empty string")
        self.domain = domain
        self.relations: dict[str, Any] = {}
        self.metadata: dict[str, Any] = {}

    def add_relation(self, key: str, value: Any) -> None:
        """Register a key-value relation for the domain.

        Args:
            key:   Relation identifier (non-empty string).
            value: Numeric or string value.

        Raises:
            ValueError: If *key* is empty.
        """
        if not key:
            raise ValueError("key must be a non-empty string")
        self.relations[key] = value

    def set_metadata(self, **kwargs: Any) -> None:
        """Attach arbitrary metadata to the exported YAML."""
        self.metadata.update(kwargs)

    def export(self, filepath: Path | str = "domains.yaml") -> Path:
        """Write domain relations to a YAML file.

        Args:
            filepath: Destination path (default ``"domains.yaml"``).

        Returns:
            Resolved :class:`pathlib.Path` of the written file.
        """
        filepath = Path(filepath)
        filepath.parent.mkdir(parents=True, exist_ok=True)

        data: dict[str, Any] = {"domains": {self.domain: dict(self.relations)}}
        if self.metadata:
            data["metadata"] = dict(self.metadata)

        with filepath.open("w", encoding="utf-8") as fh:
            yaml.dump(data, fh, sort_keys=False, allow_unicode=True)

        return filepath

    @classmethod
    def from_yaml(cls, filepath: Path | str, domain: str = "governance") -> EntropyTableBridge:
        """Load an existing YAML file into a new bridge instance.

        Args:
            filepath: Path to an entropy-table YAML file.
            domain:   Domain key to read from the file.

        Returns:
            Populated :class:`EntropyTableBridge` instance.

        Raises:
            KeyError: If *domain* is not found in the file.
        """
        filepath = Path(filepath)
        with filepath.open(encoding="utf-8") as fh:
            data = yaml.safe_load(fh)

        domains = data.get("domains", {})
        if domain not in domains:
            raise KeyError(f"Domain '{domain}' not found in {filepath}")

        bridge = cls(domain=domain)
        for k, v in domains[domain].items():
            bridge.add_relation(k, v)

        if "metadata" in data:
            bridge.set_metadata(**data["metadata"])

        return bridge
