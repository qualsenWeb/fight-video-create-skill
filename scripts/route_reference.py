#!/usr/bin/env python3
"""Deterministic keyword router for the fight reference library."""

from __future__ import annotations

import argparse
import json
import re
import unicodedata
from pathlib import Path
from typing import Any

SKILL_ROOT = Path(__file__).resolve().parents[1]
REFERENCE_ROOT = SKILL_ROOT / "reference"
SCOPE_PATHS = {
    "scenes": REFERENCE_ROOT / "scenes" / "00-路由元.json",
    "design": REFERENCE_ROOT
    / "action-storyboard-design"
    / "00-路由元.json",
    "moves": REFERENCE_ROOT
    / "action-storyboard-design"
    / "招式库"
    / "00-路由元.json",
    "skills": REFERENCE_ROOT
    / "action-storyboard-design"
    / "技能库"
    / "00-路由元.json",
    "scripts": REFERENCE_ROOT / "example-scripts" / "00-路由元.json",
}
FIELD_WEIGHTS = {
    "scenes": {
        "title_keywords": 4,
        "route_keywords": 2,
        "scene_signatures": 1,
    },
    "design": {
        "core_keywords": 3,
        "plot_signatures": 1,
    },
    "moves": {
        "title_keywords": 4,
        "route_keywords": 2,
        "technique_signatures": 1,
    },
    "skills": {
        "range_keywords": 1,
    },
    "scripts": {
        "title_keywords": 4,
        "script_types": 3,
        "route_keywords": 2,
        "scene_signatures": 1,
    },
}


def normalize(value: str) -> str:
    value = unicodedata.normalize("NFKC", value).casefold()
    return re.sub(r"[\W_]+", "", value, flags=re.UNICODE)


def load_metadata(scope: str) -> dict[str, Any]:
    path = SCOPE_PATHS[scope]
    try:
        return json.loads(path.read_text(encoding="utf-8-sig"))
    except FileNotFoundError as error:
        raise SystemExit(f"路由元不存在: {path}") from error
    except json.JSONDecodeError as error:
        raise SystemExit(f"路由元 JSON 无效: {path}: {error}") from error


def matched_terms(query: str, terms: list[str]) -> list[str]:
    normalized_query = normalize(query)
    if not normalized_query:
        return []

    matches: list[str] = []
    seen: set[str] = set()
    for term in terms:
        normalized_term = normalize(str(term))
        if not normalized_term or normalized_term in seen:
            continue
        if normalized_term in normalized_query:
            matches.append(str(term))
            seen.add(normalized_term)
    return matches


def score_route(scope: str, query: str, route: dict[str, Any]) -> dict[str, Any]:
    field_hits: dict[str, list[str]] = {}
    unique_hits: dict[str, int] = {}
    weighted_score = 0

    for field, weight in FIELD_WEIGHTS[scope].items():
        hits = matched_terms(query, route.get(field, []))
        if not hits:
            continue
        field_hits[field] = hits
        weighted_score += len(hits) * weight
        for hit in hits:
            unique_hits.setdefault(normalize(hit), weight)

    result = {
        "id": route.get("id"),
        "file": route.get("file"),
        "name": route.get("name") or Path(str(route.get("file", ""))).stem,
        "hit_count": len(unique_hits),
        "weighted_score": weighted_score,
        "field_hits": field_hits,
        "matched_keywords": [
            hit for hits in field_hits.values() for hit in hits
        ],
        "retrieval_hint": route.get("retrieval_hint", ""),
        "avoid_when": route.get("avoid_when", []),
    }
    if scope == "skills":
        result["selection_notice"] = {
            "secondary_keywords": route.get("secondary_keywords", []),
            "condition_prompt": route.get("condition_prompt", ""),
            "condition_options": route.get("condition_options", []),
            "move_library_exclusions": route.get(
                "move_library_exclusions", []
            ),
        }
    return result


def route(scope: str, query: str) -> dict[str, Any]:
    metadata = load_metadata(scope)
    scored = [score_route(scope, query, item) for item in metadata.get("routes", [])]
    eligible = sorted(
        (item for item in scored if item["hit_count"] >= 1),
        key=lambda item: (
            -item["hit_count"],
            -item["weighted_score"],
            str(item["id"]),
        ),
    )
    available = [
        {
            "id": item.get("id"),
            "file": item.get("file"),
            "name": item.get("name") or Path(str(item.get("file", ""))).stem,
            "retrieval_hint": item.get("retrieval_hint", ""),
        }
        for item in metadata.get("routes", [])
    ]
    match_rule = (
        "仅按单体或群体范围召回候选；不自动指定主技能；二级条件不参与匹配"
        if scope == "skills"
        else "至少命中一个路由关键词；先按唯一命中数、再按字段权重排序"
    )
    return {
        "scope": scope,
        "query": query,
        "match_rule": match_rule,
        "primary": None if scope == "skills" else (eligible[0] if eligible else None),
        "eligible": eligible,
        "available": available,
        "routing_rules": metadata.get("routing_rules", []),
        "conflict_resolution": metadata.get("conflict_resolution", []),
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="按 JSON 路由元中的关键词检索打斗资料。"
    )
    parser.add_argument("scope", choices=sorted(SCOPE_PATHS))
    parser.add_argument("--query", required=True, help="用户原文与提炼关键词")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    print(json.dumps(route(args.scope, args.query), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()