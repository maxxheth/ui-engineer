"""Tests for Pydantic models in site_blueprint."""

from site_blueprint.models import (
    ColorPalette,
    ColorToken,
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


def test_color_token_and_palette():
    tok = ColorToken(hex="#ffffff", rgb="rgb(255, 255, 255)", role="background", frequency=5)
    palette = ColorPalette(
        backgrounds=["#ffffff"],
        surfaces=["#f0f0f0"],
        text=["#111111"],
        accents=["#0066cc"],
        all_colors=[tok],
    )
    assert len(palette.all_colors) == 1
    assert palette.backgrounds == ["#ffffff"]


def test_typography_and_scales():
    scale = HeaderScale(
        tag="h1",
        font_family="Inter, sans-serif",
        font_size="48px",
        font_weight="800",
        line_height="56px",
    )
    typo = TypographyTokens(
        primary_font_family="Inter, sans-serif",
        base_font_size="16px",
        base_line_height="1.5",
        header_scales={"h1": scale},
    )
    assert typo.header_scales["h1"].font_size == "48px"


def test_full_blueprint_validation():
    meta = SiteMetadata(
        url="https://example.com",
        title="Example Domain",
        timestamp="2026-10-04T12:00:00Z",
        status_code=200,
    )
    tokens = DesignTokens(
        colors=ColorPalette(backgrounds=["#000000"]),
        typography=TypographyTokens(primary_font_family="Arial"),
        spacing_elevation=SpacingElevationTokens(dominant_border_radii=["8px"]),
        custom_properties={"--color-brand": "#ff4400"},
    )
    section = SectionBlueprint(
        landmark="header",
        tag_name="header",
        id="site-header",
        classes=["top-bar"],
        text_preview="Welcome to the future of AI interfaces",
        interaction=InteractionMetadata(
            primary_actions_count=1,
            primary_action_labels=["Sign In"],
        ),
        detected_patterns=[
            PatternSchema(
                pattern="FeatureCard",
                instance_count=4,
                sample_content={"title": "Fast", "desc": "Lightning fast"},
            )
        ],
    )
    asset = ExternalProductionAsset(
        category="3d_model",
        detected_engines=["Three.js"],
        direct_asset_urls=["https://example.com/robot.glb"],
        parent_landmark="header",
        suggested_react_wrapper="@react-three/fiber",
    )

    bp = SiteBlueprint(
        metadata=meta,
        tokens=tokens,
        landmarks=[section],
        external_production_assets=[asset],
    )

    dumped = bp.model_dump()
    assert dumped["metadata"]["url"] == "https://example.com"
    assert len(dumped["landmarks"]) == 1
    assert dumped["landmarks"][0]["detected_patterns"][0]["instance_count"] == 4
