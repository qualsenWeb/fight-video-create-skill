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
    "range_keywords",
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

    is_skill_library = meta.get("library_kind") == "skills"
    if is_skill_library:
        index_file = meta.get("index_file")
        if not index_file or not (directory / str(index_file)).is_file():
            errors.append(f"{path}: 技能库缺少有效 index_file")

        move_metadata_path = directory.parent / "招式库" / "00-路由元.json"
        move_data = load_json(move_metadata_path, errors)
        if move_data is not None:
            overlapping_files = sorted(
                set(inventory) & set(move_data.get("inventory", []))
            )
            if overlapping_files:
                errors.append(
                    f"{path}: 技能库与招式库 inventory 重复: {overlapping_files}"
                )

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

        if not is_skill_library:
            continue

        range_keywords = route.get("range_keywords")
        if not isinstance(range_keywords, list) or not range_keywords:
            errors.append(f"{path}: {filename} 缺少 range_keywords")
        elif set(range_keywords) - {"单体", "群体"}:
            errors.append(
                f"{path}: {filename} range_keywords 只能包含单体或群体"
            )

        disallowed_fields = sorted(
            field
            for field in KEYWORD_FIELDS - {"range_keywords"}
            if route.get(field)
        )
        if disallowed_fields:
            errors.append(
                f"{path}: {filename} 技能库不得使用其他匹配字段: "
                f"{disallowed_fields}"
            )

        required_skill_fields = {
            "secondary_keywords": list,
            "condition_prompt": str,
            "condition_options": list,
            "ability_signatures": list,
            "move_library_exclusions": list,
            "avoid_when": list,
        }
        for field, expected_type in required_skill_fields.items():
            value = route.get(field)
            if not isinstance(value, expected_type) or not value:
                errors.append(
                    f"{path}: {filename} 缺少非空 {field}"
                )

        skill_file = directory / str(filename)
        if skill_file.is_file():
            skill_content = skill_file.read_text(encoding="utf-8-sig")
            required_sections = ("二级前置条件", "选中提醒", "招式库互斥")
            missing_sections = [
                section for section in required_sections if section not in skill_content
            ]
            if missing_sections:
                errors.append(
                    f"{path}: {filename} 缺少技能条件章节: {missing_sections}"
                )

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