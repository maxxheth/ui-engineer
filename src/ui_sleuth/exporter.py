"""Multimodal exporter for UI Sleuth: JSON, YAML, and LLM Markdown blocks."""

from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any

import yaml

from ui_sleuth.models import (
    MultiPageCrawlResult,
    SectionBlueprint,
    SiteBlueprint,
    SophisticatedFeature,
)

logger = logging.getLogger(__name__)


def render_kinetic_runbook(features: list[SophisticatedFeature]) -> list[str]:
    """Generates an actionable, copy-pasteable code runbook for detected kinetic micro-interactions."""
    categories = {f.category for f in features}
    kinetic_categories = {
        "magnetic_physics",
        "custom_cursor",
        "typographic_reveal",
        "hover_media_switcher",
        "scroll_parallax",
    }
    if not categories.intersection(kinetic_categories):
        return []

    lines: list[str] = [
        "### Kinetic Micro-Interactions & Cursor Physics Runbook",
        "",
        "> The target experience uses subtle kinetic micro-interactions that define its polished feel.",
        "> Implement the following systems to match the reference site fidelity:",
        "",
    ]

    if "magnetic_physics" in categories:
        lines.extend(
            [
                "#### 1. Magnetic Button Physics (Elastic Pointer Pull)",
                "```typescript",
                "// Elastic spring attraction: elements smoothly gravitate towards pointer coordinates",
                "export function initMagneticElements(selector = '[data-magnetic]') {",
                "  const elements = document.querySelectorAll<HTMLElement>(selector);",
                "  elements.forEach((el) => {",
                "    const strength = parseFloat(el.dataset.magnetic || '20');",
                "    const onMouseMove = (e: MouseEvent) => {",
                "      const rect = el.getBoundingClientRect();",
                "      const dx = (e.clientX - (rect.left + rect.width / 2)) / (rect.width / 2);",
                "      const dy = (e.clientY - (rect.top + rect.height / 2)) / (rect.height / 2);",
                "      el.style.transform = `translate(${dx * strength}px, ${dy * strength}px)`;",
                "      el.style.transition = 'transform 0.15s cubic-bezier(0.25, 1, 0.5, 1)';",
                "    };",
                "    const onMouseLeave = () => {",
                "      el.style.transform = 'translate(0px, 0px)';",
                "      el.style.transition = 'transform 0.7s cubic-bezier(0.175, 0.885, 0.32, 1.275)'; // elastic spring back",
                "    };",
                "    el.addEventListener('mousemove', onMouseMove);",
                "    el.addEventListener('mouseleave', onMouseLeave);",
                "  });",
                "}",
                "```",
                "",
            ]
        )

    if "custom_cursor" in categories:
        lines.extend(
            [
                "#### 2. Interactive Custom Cursor & Floating Card Preview",
                "```typescript",
                "// Fixed pointer follower with lerp coordinates, hover scaling, and floating image card",
                "export function initCustomCursor() {",
                "  const cursor = document.querySelector<HTMLElement>('.cursor-wrap');",
                "  const previewImg = document.querySelector<HTMLImageElement>('.cursor-img');",
                "  if (!cursor) return;",
                "",
                "  let mouseX = 0, mouseY = 0;",
                "  let cursorX = 0, cursorY = 0;",
                "",
                "  window.addEventListener('pointermove', (e) => {",
                "    mouseX = e.clientX;",
                "    mouseY = e.clientY;",
                "  });",
                "",
                "  function render() {",
                "    cursorX += (mouseX - cursorX) * 0.18; // smooth lerp damp",
                "    cursorY += (mouseY - cursorY) * 0.18;",
                "    cursor.style.transform = `translate3d(${cursorX}px, ${cursorY}px, 0)`;",
                "    requestAnimationFrame(render);",
                "  }",
                "  requestAnimationFrame(render);",
                "",
                "  // Button / link expand states",
                "  document.querySelectorAll('[data-cursor]').forEach((el) => {",
                "    const state = el.getAttribute('data-cursor');",
                "    el.addEventListener('mouseenter', () => cursor.classList.add(`is-${state}`));",
                "    el.addEventListener('mouseleave', () => cursor.classList.remove(`is-${state}`));",
                "  });",
                "",
                "  // Floating project preview card on hover",
                "  document.querySelectorAll<HTMLElement>('[data-cursor-img]').forEach((el) => {",
                "    el.addEventListener('mouseenter', () => {",
                "      const imgUrl = el.getAttribute('data-cursor-img');",
                "      if (previewImg && imgUrl) {",
                "        previewImg.src = imgUrl;",
                "        cursor.classList.add('has-img-preview');",
                "      }",
                "    });",
                "    el.addEventListener('mouseleave', () => {",
                "      cursor.classList.remove('has-img-preview');",
                "    });",
                "  });",
                "}",
                "```",
                "",
            ]
        )

    if "typographic_reveal" in categories:
        lines.extend(
            [
                "#### 3. Typographic SplitText Cascade (Masked Entrance)",
                "```typescript",
                "// Staggered upward character / word reveals with overflow masking",
                "export function initTypographicReveals(selector = '.split-text, h1, h2') {",
                "  const headings = document.querySelectorAll<HTMLElement>(selector);",
                "  headings.forEach((heading) => {",
                "    const words = (heading.textContent || '').trim().split(/\\s+/);",
                "    heading.innerHTML = words",
                "      .map(",
                "        (word) => `",
                '        <span class="inline-block overflow-hidden align-top">',
                '          <span class="reveal-word inline-block transition-transform duration-700 ease-out translate-y-full opacity-0">',
                "            ${word}&nbsp;",
                "          </span>",
                "        </span>`",
                "      )",
                "      .join('');",
                "",
                "    const observer = new IntersectionObserver((entries) => {",
                "      entries.forEach((entry) => {",
                "        if (entry.isIntersecting) {",
                "          heading.querySelectorAll<HTMLElement>('.reveal-word').forEach((span, idx) => {",
                "            setTimeout(() => {",
                "              span.style.transform = 'translateY(0%)';",
                "              span.style.opacity = '1';",
                "            }, idx * 25);",
                "          });",
                "          observer.unobserve(heading);",
                "        }",
                "      });",
                "    }, { threshold: 0.15 });",
                "",
                "    observer.observe(heading);",
                "  });",
                "}",
                "```",
                "",
            ]
        )

    if "hover_media_switcher" in categories:
        lines.extend(
            [
                "#### 4. Dynamic Hover Media Switcher",
                "```typescript",
                "// Dynamically cross-fade and play preview media when hovering list items",
                "export function initHoverMediaSwitcher(",
                "  triggerSelector = '[data-video=\"to-play\"]',",
                "  videoTargetSelector = '#hero-active-video'",
                ") {",
                "  const triggers = document.querySelectorAll<HTMLElement>(triggerSelector);",
                "  const video = document.querySelector<HTMLVideoElement>(videoTargetSelector);",
                "  if (!video) return;",
                "",
                "  triggers.forEach((item) => {",
                "    item.addEventListener('mouseenter', () => {",
                "      const videoSrc = item.getAttribute('data-thumb-video') || item.getAttribute('data-video-url');",
                "      if (videoSrc && video.getAttribute('src') !== videoSrc) {",
                "        video.style.opacity = '0';",
                "        setTimeout(() => {",
                "          video.src = videoSrc;",
                "          video.load();",
                "          video.play().catch(() => {});",
                "          video.style.opacity = '1';",
                "        }, 150);",
                "      }",
                "    });",
                "  });",
                "}",
                "```",
                "",
            ]
        )

    return lines


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

        runbook_lines = render_kinetic_runbook(soph.features)
        if runbook_lines:
            lines.extend(runbook_lines)

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


def generate_site_design_system_markdown(crawl_result: MultiPageCrawlResult) -> str:
    """Generate an LLM-ready context block for vibe-coding the site design system and component library."""
    ds = crawl_result.design_system
    tokens = ds.tokens

    lines: list[str] = [
        "# SYSTEM PROMPT: MULTI-PAGE COMPONENT SYSTEM & DESIGN SYSTEM BLUEPRINT",
        "",
        "> You are an elite principal design technologist and full-stack React/Next.js systems architect.",
        f"> Reconstruct the complete design system and multi-page application for `{ds.domain}`",
        "> with pixel-perfect design token alignment, modular component architecture, and comprehensive interaction fidelity.",
        "",
        "---",
        "",
        "## 1. EXECUTIVE SITE ARCHITECTURE & CRAWL METRICS",
        f"- **Root Entry URL:** `{ds.entry_url}`",
        f"- **Domain:** `{ds.domain}`",
        f"- **Total Crawled Pages:** `{ds.total_pages_crawled}`",
        f"- **Crawl Timestamp:** `{crawl_result.crawl_timestamp}`",
        "",
        "### Crawled Route Inventory:",
        "| Route | Page Title | HTTP | Landmarks | Patterns | Features |",
        "|---|---|---|---|---|---|",
    ]

    for p in ds.pages:
        features_str = ", ".join(f"`{f}`" for f in p.features_detected[:2]) or "Standard"
        lines.append(
            f"| `{p.path}` | {p.title or 'N/A'} | `{p.status_code}` | {p.landmark_count} | {p.pattern_count} | {features_str} |"
        )

    lines.extend(
        [
            "",
            "---",
            "",
            "## 2. CONSOLIDATED GLOBAL DESIGN TOKENS",
            "",
            "### A. Unified Color Palette",
            "- **Backgrounds:** "
            + (", ".join(f"`{c}`" for c in tokens.colors.backgrounds) or "None detected"),
            "- **Surfaces & Cards:** "
            + (", ".join(f"`{c}`" for c in tokens.colors.surfaces) or "None detected"),
            "- **Text & Content:** "
            + (", ".join(f"`{c}`" for c in tokens.colors.text) or "None detected"),
            "- **Accents & CTAs:** "
            + (", ".join(f"`{c}`" for c in tokens.colors.accents) or "None detected"),
            "",
            "### B. Unified Typography Stack",
            f"- **Primary Font Family:** `{tokens.typography.primary_font_family}`",
            f"- **Secondary Font Family:** `{tokens.typography.secondary_font_family or 'Same as primary'}`",
            f"- **Base Font Size:** `{tokens.typography.base_font_size}`",
            f"- **Base Line Height:** `{tokens.typography.base_line_height}`",
            "",
            "#### Header Scales:",
        ]
    )

    if tokens.typography.header_scales:
        for _, scale in sorted(tokens.typography.header_scales.items()):
            lines.append(
                f"- **`<{scale.tag}>`:** {scale.font_size} / weight {scale.font_weight} (line-height: {scale.line_height})"
            )
    else:
        lines.append("- *(No specific header scales sampled)*")

    lines.extend(
        [
            "",
            "### C. Spacing, Elevation & Custom Properties",
            "- **Dominant Border Radii:** "
            + (
                ", ".join(f"`{r}`" for r in tokens.spacing_elevation.dominant_border_radii)
                or "None"
            ),
            "- **Box Shadows:** "
            + (", ".join(f"`{s}`" for s in tokens.spacing_elevation.box_shadows[:3]) or "None"),
        ]
    )

    if tokens.custom_properties:
        lines.extend(
            [
                "",
                "#### Detected CSS Variables (:root):",
            ]
        )
        for k, v in sorted(tokens.custom_properties.items()):
            lines.append(f"- `{k}: {v};`")

    lines.extend(
        [
            "",
            "---",
            "",
            "## 3. GLOBAL LAYOUT SHELL COMPONENTS",
        ]
    )

    if ds.global_components:
        for comp in ds.global_components:
            lines.extend(
                [
                    f"### Component: `<{comp.name} />`",
                    f"- **Category:** `{comp.category}`",
                    f"- **Description:** {comp.description}",
                    f"- **Site-Wide Occurrences:** Present on {comp.occurrences} crawled pages",
                    f"- **Layout Pattern:** `{comp.layout_hint or 'flexible shell'}`",
                    "",
                    "#### Suggested TypeScript Props Interface:",
                    "```typescript",
                    f"interface {comp.name}Props {{",
                ]
            )
            for prop in comp.suggested_props:
                opt = "" if prop.required else "?"
                lines.append(f"  {prop.name}{opt}: {prop.prop_type}; // {prop.description}")
            lines.extend(
                [
                    "}",
                    "```",
                    "",
                ]
            )
    else:
        lines.append("- *(No persistent global layout shells detected)*\n")

    lines.extend(
        [
            "---",
            "",
            "## 4. REUSABLE MODULAR COMPONENT LIBRARY",
        ]
    )

    if ds.reusable_components:
        for comp in ds.reusable_components:
            lines.extend(
                [
                    f"### Component: `<{comp.name} />`",
                    f"- **Archetype:** `{comp.category}`",
                    f"- **Total Rendered Instances:** {comp.occurrences} instances across {len(comp.pages_found)} page(s)",
                    "- **Pages Used In:** " + (", ".join(f"`{p}`" for p in comp.pages_found[:4])),
                    f"- **Layout Hint:** `{comp.layout_hint or 'card / flex'}`",
                    "",
                    "#### Suggested TypeScript Interface:",
                    "```typescript",
                    f"interface {comp.name}Props {{",
                ]
            )
            for prop in comp.suggested_props:
                opt = "" if prop.required else "?"
                lines.append(f"  {prop.name}{opt}: {prop.prop_type};")
            lines.extend(
                [
                    "}",
                    "```",
                    "",
                    "#### Sample Extracted Content:",
                    "```json",
                    json.dumps(comp.sample_content, indent=2),
                    "```",
                    "",
                ]
            )
    else:
        lines.append("- *(No repetitive card/section patterns identified)*\n")

    lines.extend(
        [
            "---",
            "",
            "## 5. MOTION, PHYSICS & INTERACTIVE SYSTEMS",
        ]
    )

    if ds.motion_and_runtimes:
        lines.append(
            "- **Detected Motion Runtimes:** "
            + ", ".join(f"`{eng}`" for eng in ds.motion_and_runtimes)
        )
    else:
        lines.append("- **Detected Motion Runtimes:** Standard CSS Transitions / Native DOM")

    if ds.sophisticated_features:
        lines.extend(
            [
                "",
                "### Interactive Features Catalog:",
            ]
        )
        for feat in ds.sophisticated_features:
            lines.extend(
                [
                    f"- **`{feat.name}`** (`{feat.category}`): {feat.description}",
                    f"  - Selector: `{feat.selector}`",
                    f"  - Recommended Implementation: {feat.suggested_implementation}",
                ]
            )

        runbook_lines = render_kinetic_runbook(ds.sophisticated_features)
        if runbook_lines:
            lines.extend(runbook_lines)
    else:
        lines.append("- *(No advanced sticky scroll tracks or off-screen drawers detected)*")

    lines.extend(
        [
            "",
            "---",
            "",
            "## 6. EXTERNAL ASSETS & RICH MEDIA",
        ]
    )

    if ds.external_assets:
        for asset in ds.external_assets:
            lines.extend(
                [
                    f"- **Discipline:** `{asset.category.upper()}`",
                    f"  - Engines: {', '.join(asset.detected_engines)}",
                    f"  - Suggested Wrapper: `{asset.suggested_react_wrapper}`",
                    "  - Asset URLs: "
                    + (
                        ", ".join(f"`{u}`" for u in asset.direct_asset_urls[:2])
                        or "None directly intercepted"
                    ),
                ]
            )
    else:
        lines.append("- *(No external 3D, Rive, or background video streams detected)*")

    lines.extend(
        [
            "",
            "---",
            "",
            "## 7. SYSTEM RECONSTRUCTION WORKFLOW",
            "1. **Core Tokens (`tailwind.config.js` or theme file):** Map the extracted primary color palette, font families, and radius tokens into your design system.",
            "2. **Layout Shell:** Build `<GlobalNavbar />` and `<GlobalFooter />` with persistent routes.",
            "3. **Component Library:** Implement the modular components from Section 4 (`FeatureCard`, `PricingCard`, etc.) in a `components/` directory using the provided TypeScript interfaces.",
            "4. **Interactive Systems:** Wire up motion and drawers as documented in Section 5 with Framer Motion or GSAP ScrollTrigger.",
            "5. **Assemble Routes:** Compose each route in `app/` (or `pages/`) by instantiating the components with mock or API data.",
            "",
        ]
    )

    return "\n".join(lines)


def export_site_design_system(
    crawl_result: MultiPageCrawlResult,
    output_dir: str | Path,
    export_json: bool = True,
    export_markdown: bool = True,
    export_yaml: bool = True,
) -> dict[str, Path]:
    """Export the multi-page crawl results into a unified design system and per-page blueprints."""
    out_path = Path(output_dir)
    out_path.mkdir(parents=True, exist_ok=True)

    saved_paths: dict[str, Path] = {}
    ds = crawl_result.design_system

    # 1. site_design_system.json
    if export_json:
        json_file = out_path / "site_design_system.json"
        json_content = ds.model_dump_json(indent=2)
        json_file.write_text(json_content, encoding="utf-8")
        saved_paths["design_system_json"] = json_file

        # Convenience alias blueprint.json
        bp_json = out_path / "blueprint.json"
        bp_json.write_text(json_content, encoding="utf-8")
        saved_paths["blueprint_json"] = bp_json

        # manifest.json
        manifest_file = out_path / "manifest.json"
        manifest_data = {
            "entry_url": ds.entry_url,
            "domain": ds.domain,
            "total_pages_crawled": ds.total_pages_crawled,
            "timestamp": crawl_result.crawl_timestamp,
            "pages": [p.model_dump() for p in ds.pages],
        }
        manifest_file.write_text(json.dumps(manifest_data, indent=2), encoding="utf-8")
        saved_paths["manifest_json"] = manifest_file

    # 2. site_design_system.md
    if export_markdown:
        md_file = out_path / "site_design_system.md"
        md_content = generate_site_design_system_markdown(crawl_result)
        md_file.write_text(md_content, encoding="utf-8")
        saved_paths["design_system_markdown"] = md_file

        # Convenience alias blueprint.md
        bp_md = out_path / "blueprint.md"
        bp_md.write_text(md_content, encoding="utf-8")
        saved_paths["blueprint_markdown"] = bp_md

    # 3. site_design_system.yaml
    if export_yaml:
        yaml_file = out_path / "site_design_system.yaml"
        ds_data: dict[str, Any] = ds.model_dump(mode="json")
        yaml_content = yaml.dump(ds_data, sort_keys=False, allow_unicode=True)
        yaml_file.write_text(yaml_content, encoding="utf-8")
        saved_paths["design_system_yaml"] = yaml_file

        # Convenience alias blueprint.yaml
        bp_yaml = out_path / "blueprint.yaml"
        bp_yaml.write_text(yaml_content, encoding="utf-8")
        saved_paths["blueprint_yaml"] = bp_yaml

    # 4. Individual per-page blueprints in output_dir / "pages" / <slug>
    for page_url, bp in crawl_result.pages.items():
        page_summary = next((p for p in ds.pages if p.url == page_url), None)
        slug = page_summary.slug if page_summary else "page"
        page_dir = out_path / "pages" / slug
        page_dir.mkdir(parents=True, exist_ok=True)

        if export_json:
            (page_dir / "blueprint.json").write_text(bp.model_dump_json(indent=2), encoding="utf-8")
        if export_markdown:
            (page_dir / "blueprint.md").write_text(generate_llm_markdown(bp), encoding="utf-8")
        if export_yaml:
            p_data: dict[str, Any] = bp.model_dump(mode="json")
            (page_dir / "blueprint.yaml").write_text(
                yaml.dump(p_data, sort_keys=False, allow_unicode=True), encoding="utf-8"
            )

    logger.info("Successfully exported multi-page site design system to %s", out_path)
    return saved_paths
