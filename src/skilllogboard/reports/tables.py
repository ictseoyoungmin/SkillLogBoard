"""Registry for report table types."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class TableDefinition:
    table_type: str
    title: str
    requires_metric: bool = False


TABLE_REGISTRY: dict[str, TableDefinition] = {
    "leaderboard": TableDefinition("leaderboard", "Leaderboard", True),
    "seed-summary": TableDefinition("seed-summary", "Seed Summary", True),
    "ablation-summary": TableDefinition("ablation-summary", "Ablation Summary", True),
    "config-diff": TableDefinition("config-diff", "Config Diff"),
    "rule-audit": TableDefinition("rule-audit", "Rule Audit"),
}


def list_table_types() -> list[str]:
    return sorted(TABLE_REGISTRY)


def get_table_definition(table_type: str) -> TableDefinition:
    try:
        return TABLE_REGISTRY[table_type]
    except KeyError as exc:
        raise ValueError(f"Unsupported report table type: {table_type}") from exc
