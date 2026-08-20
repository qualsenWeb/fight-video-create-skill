#!/usr/bin/env python3
"""Validate route metadata against the reference inventory."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

SKILL_ROOT = Path(__file__).resolve().parents[1]
REFERENCE_ROOT = SKILL_ROOT / "reference"
KEYWORD_FIELDS = {
    "title_keywords",
    "route_keywords",
    "scene_signatures",
    "core_keywords",
    "plot_signatures",
    "script_types",
    "technique_signatures",
}


def load_json(path: Path, errors: list[str]) -> dict[str, Any] | None:
    try:
        return json.loads(path.read_text(encoding="utf-8-sig"))
    except (OSError, json.JSONDecodeError) as error:
        errors.append(f"{path}: 无法读取 JSON: {error}")
        return None


def validate_metadata(path: Path) -> list[str]:
    errors: list[str] = []
    data = load_json(path, errors)
    if data is None:
        return errors

    meta = data.get("meta", {})
    routes = data.get("routes", [])
    inventory = data.get("inventory", [])
    directory = path.parent

    if not isinstance(routes, list):
        return [f"{path}: routes 必须是数组"]
    if not isinstance(inventory, list):
        return [f"{path}: inventory 必须是数组"]

    if meta.get("inventory_count") != len(inventory):
        errors.append(
            f"{path}: inventory_count={meta.get('inventory_count')}，"
            f"实际 inventory={len(inventory)}"
        )

    if len(inventory) != len(set(inventory)):
        errors.append(f"{path}: inventory 存在重复文件")

    route_files = [route.get("file") for route in routes]
    if len(route_files) != len(set(route_files)):
        errors.append(f"{path}: routes 存在重复 file")

    route_ids = [route.get("id") for route in routes]
    if len(route_ids) != len(set(route_ids)):
        errors.append(f"{path}: routes 存在重复 id")

    if set(route_files) != set(inventory):
        missing_routes = sorted(set(inventory) - set(route_files))
        missing_inventory = sorted(set(route_files) - set(inventory))
        if missing_routes:
            errors.append(f"{path}: inventory 中无 route 的文件: {missing_routes}")
        if missing_inventory:
            errors.append(f"{path}: routes 中未入 inventory 的文件: {missing_inventory}")

    managed_file = meta.get("managed_file", path.name)
    if managed_file in inventory:
        errors.append(f"{path}: 路由元自身不能进入 inventory")

    for filename in inventory:
        if not (directory / filename).is_file():
            errors.append(f"{path}: inventory 文件不存在: {filename}")

    for route in routes:
        filename = route.get("file", "<unknown>")
        keyword_count = sum(
            len(route.get(field, []))
            for field in KEYWORD_FIELDS
            if isinstance(route.get(field, []), list)
        )
        if keyword_count < 1:
            errors.append(f"{path}: {filename} 没有可检索关键词")
        if not route.get("retrieval_hint"):
            errors.append(f"{path}: {filename} 缺少 retrieval_hint")

    return errors


def main() -> None:
    metadata_files = sorted(REFERENCE_ROOT.rglob("00-路由元.json"))
    if not metadata_files:
        raise SystemExit("未找到任何 00-路由元.json")

    errors = [
        error
        for metadata_file in metadata_files
        for error in validate_metadata(metadata_file)
    ]
    if errors:
        print("ROUTE VALIDATION FAILED")
        for error in errors:
            print(f"- {error}")
        raise SystemExit(1)

    print(f"ROUTE VALIDATION OK: {len(metadata_files)} metadata files")


if __name__ == "__main__":
    main()