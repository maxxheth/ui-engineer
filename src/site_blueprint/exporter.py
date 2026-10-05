"""Multimodal exporter for site-blueprint: JSON, YAML, and LLM Markdown blocks."""

from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any

import yaml

from site_blueprint.models import SectionBlueprint, SiteBlueprint

logger = logging.getLogger(__name__)


def generate_llm_markdown(blueprint: SiteBlueprint) -> str:
    """Generate an LLM-ready context block with an embedded prompt template for vibe-coding."""
    meta = blueprint.metadata
    tokens = blueprint.tokens
    assets = blueprint.external_production_assets

    lines: list[str] = [
        "# SYSTEM PROMPT: VIBE-CODING UI RECONSTRUCTION BLUEPRINT",
        "",
        "> You are an elite frontend UI/UX engineer and React/Next.js systems architect.",
        "> Reverse-engineer and implement the following web page with pixel-level aesthetic fidelity,",
        "> responsive layout precision, and interactive state completeness based strictly on this blueprint.",
        "",
        "---",
        "",
        "## 1. TARGET SPECIFICATION & METADATA",
        f"- **Source URL:** `{meta.url}`",
        f"- **Page Title:** {meta.title or 'N/A'}",
        f"- **Description:** {meta.description or 'N/A'}",
        f"- **Target Viewport:** `{meta.viewport.get('width', 1440)}x{meta.viewport.get('height', 900)}`",
        f"- **HTTP Status:** `{meta.status_code}`",
        f"- **Scraped At:** `{meta.timestamp}`",
        "",
        "---",
        "",
        "## 2. HARVESTED DESIGN SYSTEM TOKENS",
        "",
        "### A. Color Palette",
        "- **Backgrounds:** "
        + (", ".join(f"`{c}`" for c in tokens.colors.backgrounds) or "None detected"),
        "- **Surfaces & Cards:** "
        + (", ".join(f"`{c}`" for c in tokens.colors.surfaces) or "None detected"),
        "- **Text & Content:** "
        + (", ".join(f"`{c}`" for c in tokens.colors.text) or "None detected"),
        "- **Accents & CTAs:** "
        + (", ".join(f"`{c}`" for c in tokens.colors.accents) or "None detected"),
        "",
        "### B. Typography Stack",
        f"- **Primary Font Family:** `{tokens.typography.primary_font_family}`",
        f"- **Base Font Size:** `{tokens.typography.base_font_size}`",
        f"- **Base Line Height:** `{tokens.typography.base_line_height}`",
        "",
        "#### Header Scales:",
    ]

    if tokens.typography.header_scales:
        for tag, scale in tokens.typography.header_scales.items():
            lines.append(
                f"- **`<{tag}>`:** size: `{scale.font_size}`, weight: `{scale.font_weight}`, "
                f"line-height: `{scale.line_height}`"
                + (f", tracking: `{scale.letter_spacing}`" if scale.letter_spacing else "")
            )
    else:
        lines.append("- *No explicit heading tags detected in sampled DOM.*")

    lines.extend(
        [
            "",
            "### C. Elevation & Spacing",
            "- **Dominant Border Radii:** "
            + (
                ", ".join(f"`{r}`" for r in tokens.spacing_elevation.dominant_border_radii)
                or "None"
            ),
            "- **Box Shadow Signatures:**",
        ]
    )

    if tokens.spacing_elevation.box_shadows:
        for sh in tokens.spacing_elevation.box_shadows:
            lines.append(f"  - `{sh}`")
    else:
        lines.append("  - *Flat elevation (no heavy box shadows detected)*")

    if tokens.custom_properties:
        lines.extend(["", "### D. CSS Variables (:root)"])
        for k, v in list(tokens.custom_properties.items())[:15]:
            lines.append(f"- `{k}`: `{v}`")

    lines.extend(
        [
            "",
            "---",
            "",
            "## 3. EXTERNAL PRODUCTION ASSETS & RUNTIME ENGINES",
        ]
    )

    if assets:
        for idx, a in enumerate(assets, 1):
            lines.append(
                f"### Asset #{idx}: {a.category.upper()} ({', '.join(a.detected_engines)})"
            )
            lines.append(f"- **Mount Landmark:** `{a.parent_landmark}`")
            lines.append(f"- **Recommended Runtime Wrapper:** `{a.suggested_react_wrapper}`")
            if a.direct_asset_urls:
                lines.append("- **Direct Asset URLs:**")
                for u in a.direct_asset_urls[:5]:
                    lines.append(f"  - `{u}`")
            if a.details:
                lines.append(f"- **Technical Diagnostics:** `{json.dumps(a.details)}`")
            lines.append("")
    else:
        lines.append("*(No external 3D, WebGL canvas, or background video streams detected)*")
        lines.append("")

    # 4. Sophisticated Features & Motion Engines
    soph = blueprint.sophisticated_features
    if soph and soph.has_sophisticated_features:
        lines.extend(
            [
                "---",
                "",
                "## 4. SOPHISTICATED INTERACTIVE FEATURES & MOTION MANIFEST",
                "",
            ]
        )
        if soph.detected_engines:
            lines.append(
                f"- **Detected Motion / Physics Engines:** {', '.join(soph.detected_engines)}"
            )
            lines.append("")

        for f in soph.features:
            cat_display = f.category.replace("_", " ").title()
            lines.append(f"### {cat_display}: {f.name} (`{f.selector}`)")
            lines.append(f"- **Description:** {f.description}")
            if f.dimensions:
                dim_str = ", ".join(f"{k}: {v}px" for k, v in f.dimensions.items())
                lines.append(f"- **Dimensions:** `{dim_str}`")
            if f.suggested_implementation:
                lines.append(f"- **Recommended Implementation:** {f.suggested_implementation}")
            if f.details:
                lines.append(f"- **Extracted Diagnostics:** `{json.dumps(f.details)}`")
            lines.append("")

        if soph.recommended_explorations:
            lines.append("### Recommended Independent Explorations")
            for rec in soph.recommended_explorations:
                lines.append(f"- 🔍 {rec}")
            lines.append("")

    lines.extend(
        [
            "---",
            "",
            "## 5. SEMANTIC COMPONENT ARCHITECTURE & LANDMARKS",
            "",
        ]
    )

    def render_section(sec: SectionBlueprint, depth: int = 0) -> None:
        indent = "  " * depth
        prefix = f"{indent}- **`<{sec.landmark}>`**"
        if sec.id:
            prefix += f' `id="{sec.id}"`'
        if sec.classes:
            prefix += f' `class="{" ".join(sec.classes)}"`'
        if sec.layout_hint:
            prefix += f" *[Layout: {sec.layout_hint}]*"
        lines.append(prefix)

        if sec.text_preview:
            lines.append(f'{indent}  - **Copy Preview:** *"{sec.text_preview}"*')

        inter = sec.interaction
        if inter.primary_actions_count > 0 or inter.forms_count > 0 or inter.inputs_count > 0:
            act_info = []
            if inter.primary_action_labels:
                act_info.append(f"CTAs: {inter.primary_action_labels}")
            if inter.forms_count > 0:
                act_info.append(f"Forms: {inter.forms_count}")
            if inter.inputs_count > 0:
                act_info.append(f"Inputs: {inter.inputs_count}")
            lines.append(f"{indent}  - **Interactivity:** {', '.join(act_info)}")

        if sec.detected_patterns:
            for pat in sec.detected_patterns:
                lines.append(
                    f"{indent}  - **Collapsed Pattern:** `{pat.pattern}` x{pat.instance_count} instances"
                )
                if pat.sample_content:
                    lines.append(f"{indent}    - *Sample Data:* `{json.dumps(pat.sample_content)}`")

        for sub in sec.subsections:
            render_section(sub, depth + 1)

    if blueprint.landmarks:
        for lm in blueprint.landmarks:
            render_section(lm, depth=0)
    else:
        lines.append("*(No major structural landmarks extracted)*")

    lines.extend(
        [
            "",
            "---",
            "",
            "## 6. RECONSTRUCTION IMPLEMENTATION INSTRUCTIONS",
            "1. **Component Structure:** Break each structural landmark above into a modular component (`Header`, `HeroSection`, `FeatureGrid`, `Footer`).",
            "2. **Design Tokens:** Define the color palette and typography rules using Tailwind CSS classes or CSS modules corresponding to the harvested tokens.",
            "3. **Repetitive Patterns:** For all collapsed patterns (e.g. `FeatureCard`), create a dedicated reusable component and map over mock data using the sample content structure.",
            "4. **Sophisticated Features & Motion:** If sticky scroll tracks, off-screen drawers, or motion engines were detected in Section 4, implement them using the recommended component wrappers (e.g. Framer Motion `useScroll`, Radix UI Dialog/Drawer, `@darkroom.engineering/lenis`).",
            "5. **Production Disciplines:** If 3D, Rive, or Video assets were detected, integrate the suggested wrapper libraries (`@react-three/fiber`, `@rive-app/react-canvas`, HTML5 video loop).",
            "6. **Responsiveness:** Maintain standard responsive breakpoints (`sm: 640px`, `md: 768px`, `lg: 1024px`, `xl: 1280px`).",
            "",
        ]
    )

    return "\n".join(lines)


def export_blueprint(
    blueprint: SiteBlueprint,
    output_dir: str | Path,
    export_json: bool = True,
    export_markdown: bool = True,
    export_yaml: bool = True,
) -> dict[str, Path]:
    """Export the blueprint into chosen formats (blueprint.json, blueprint.md, blueprint.yaml)."""
    out_path = Path(output_dir)
    out_path.mkdir(parents=True, exist_ok=True)

    saved_paths: dict[str, Path] = {}

    # 1. blueprint.json
    if export_json:
        json_file = out_path / "blueprint.json"
        json_content = blueprint.model_dump_json(indent=2)
        json_file.write_text(json_content, encoding="utf-8")
        saved_paths["json"] = json_file
        logger.info("Saved blueprint JSON to %s", json_file)

    # 2. blueprint.md
    if export_markdown:
        md_file = out_path / "blueprint.md"
        md_content = generate_llm_markdown(blueprint)
        md_file.write_text(md_content, encoding="utf-8")
        saved_paths["markdown"] = md_file
        logger.info("Saved blueprint Markdown to %s", md_file)

    # 3. blueprint.yaml
    if export_yaml:
        yaml_file = out_path / "blueprint.yaml"
        # Convert Pydantic model to clean dict
        data: dict[str, Any] = blueprint.model_dump(mode="json")
        yaml_content = yaml.dump(data, sort_keys=False, allow_unicode=True)
        yaml_file.write_text(yaml_content, encoding="utf-8")
        saved_paths["yaml"] = yaml_file
        logger.info("Saved blueprint YAML to %s", yaml_file)

    return saved_paths
