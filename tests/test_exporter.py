"""Tests for exporter module."""

import json
from pathlib import Path

import yaml

from site_blueprint.exporter import export_blueprint, generate_llm_markdown
from site_blueprint.models import (
    ColorPalette,
    DesignTokens,
    ExternalProductionAsset,
    HeaderScale,
    InteractionMetadata,
    PatternSchema,
    SectionBlueprint,
    SiteBlueprint,
    SiteMetadata,
    SpacingElevationTokens,
    TypographyTokens,
)


def create_sample_blueprint() -> SiteBlueprint:
    return SiteBlueprint(
        metadata=SiteMetadata(
            url="https://saas.example.com",
            title="NextGen AI Cloud",
            timestamp="2026-10-04T12:00:00Z",
            status_code=200,
        ),
        tokens=DesignTokens(
            colors=ColorPalette(
                backgrounds=["#0a0a0c"],
                surfaces=["#16161a"],
                text=["#f3f4f6"],
                accents=["#6366f1"],
            ),
            typography=TypographyTokens(
                primary_font_family="Geist, sans-serif",
                base_font_size="16px",
                base_line_height="1.5",
                header_scales={
                    "h1": HeaderScale(
                        tag="h1",
                        font_family="Geist",
                        font_size="64px",
                        font_weight="800",
                        line_height="72px",
                    )
                },
            ),
            spacing_elevation=SpacingElevationTokens(
                dominant_border_radii=["12px", "9999px"],
                box_shadows=["0 20px 25px -5px rgba(0, 0, 0, 0.5)"],
            ),
        ),
        landmarks=[
            SectionBlueprint(
                landmark="header",
                tag_name="header",
                id="navbar",
                interaction=InteractionMetadata(
                    primary_actions_count=1,
                    primary_action_labels=["Get Started"],
                ),
            ),
            SectionBlueprint(
                landmark="main",
                tag_name="main",
                text_preview="Empowering autonomous agent workflows in the cloud.",
                detected_patterns=[
                    PatternSchema(
                        pattern="FeatureCard",
                        instance_count=6,
                        sample_content={"title": "Self-Healing", "desc": "Automatic recovery"},
                    )
                ],
            ),
        ],
        external_production_assets=[
            ExternalProductionAsset(
                category="3d_model",
                detected_engines=["Three.js"],
                direct_asset_urls=["https://saas.example.com/assets/robot.glb"],
                parent_landmark="header",
                suggested_react_wrapper="@react-three/fiber",
            )
        ],
    )


def test_generate_llm_markdown():
    bp = create_sample_blueprint()
    md = generate_llm_markdown(bp)

    assert "SYSTEM PROMPT: VIBE-CODING UI RECONSTRUCTION BLUEPRINT" in md
    assert "https://saas.example.com" in md
    assert "#0a0a0c" in md
    assert "Geist, sans-serif" in md
    assert "64px" in md
    assert "Get Started" in md
    assert "FeatureCard" in md
    assert "@react-three/fiber" in md


def test_export_blueprint_files(tmp_path: Path):
    bp = create_sample_blueprint()
    saved = export_blueprint(bp, tmp_path, export_json=True, export_markdown=True, export_yaml=True)

    assert "json" in saved
    assert "markdown" in saved
    assert "yaml" in saved

    # Verify JSON content
    with open(saved["json"], encoding="utf-8") as f:
        data = json.load(f)
        assert data["metadata"]["url"] == "https://saas.example.com"

    # Verify YAML content
    with open(saved["yaml"], encoding="utf-8") as f:
        ydata = yaml.safe_load(f)
        assert ydata["tokens"]["colors"]["backgrounds"] == ["#0a0a0c"]

    # Verify MD content
    assert saved["markdown"].exists()
    assert len(saved["markdown"].read_text(encoding="utf-8")) > 100
