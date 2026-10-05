"""Tests for feature_detector module."""

from unittest.mock import MagicMock

from site_blueprint.exporter import generate_llm_markdown
from site_blueprint.feature_detector import detect_and_explore_features
from site_blueprint.models import (
    DesignTokens,
    SiteBlueprint,
    SiteMetadata,
    SophisticatedFeature,
    SophisticatedFeaturesSummary,
)


def test_feature_detector_mocked_page():
    mock_page = MagicMock()
    mock_page.evaluate.return_value = {
        "detected_engines": ["GSAP (GreenSock) [ScrollTrigger, SplitText]", "Lenis Smooth Scroll"],
        "sticky_tracks": [
            {
                "name": "Sticky Track (section.home-testi)",
                "selector": "section.home-testi",
                "dimensions": {"top": 10700, "left": 50, "width": 1200, "height": 2880},
                "stickyHeight": 900,
                "childItemsCount": 4,
                "description": "Pinned scroll scene of height 2880px with sticky viewport container.",
            }
        ],
        "offscreen_drawers": [
            {
                "name": "Modal/Drawer (div.client-news)",
                "selector": "div.client-news",
                "dimensions": {"top": 7800, "left": 0, "width": 1200, "height": 8400},
                "headings": ["Outcome", "Featured", "Deets"],
                "textPreview": "Our collaboration helped Surge grow...",
                "description": "Off-screen or dynamic drawer/modal.",
            }
        ],
        "disclosures": [
            {
                "name": "Interactive Disclosure (div.home-ser-item)",
                "selector": "div.home-ser-item",
                "title": "Product Design",
                "dimensions": {"top": 2400, "left": 50, "width": 1200, "height": 400},
                "description": "Expandable disclosure.",
            }
        ],
        "marquees": [
            {
                "name": "Continuous Stream (div.home-client-list)",
                "selector": "div.home-client-list",
                "dimensions": {"top": 13800, "left": 50, "width": 1200, "height": 100},
                "description": "Infinite marquee.",
            }
        ],
        "canvases": [
            {
                "name": "WebGL Shader Canvas",
                "selector": "canvas",
                "dimensions": {"top": 200, "left": 50, "width": 800, "height": 600},
                "isWebGL": True,
                "description": "High-performance WebGL 3D canvas.",
            }
        ],
    }

    summary = detect_and_explore_features(mock_page, explore=True)
    assert summary.has_sophisticated_features is True
    assert "GSAP (GreenSock) [ScrollTrigger, SplitText]" in summary.detected_engines
    assert "Lenis Smooth Scroll" in summary.detected_engines
    assert len(summary.features) == 6
    assert len(summary.recommended_explorations) >= 3

    # Check categories
    categories = {f.category for f in summary.features}
    assert "motion_physics_engine" in categories
    assert "sticky_scroll_track" in categories
    assert "offscreen_drawer" in categories
    assert "interactive_disclosure" in categories
    assert "marquee_stream" in categories
    assert "webgl_canvas" in categories


def test_sophisticated_features_in_markdown():
    summary = SophisticatedFeaturesSummary(
        has_sophisticated_features=True,
        detected_engines=["GSAP ScrollTrigger", "Lenis"],
        features=[
            SophisticatedFeature(
                category="sticky_scroll_track",
                name="Sticky Track (section.home-testi)",
                selector="section.home-testi",
                description="Pinned scene spanning 2880px scroll track.",
                dimensions={"top": 10700, "height": 2880},
                requires_independent_exploration=True,
                suggested_implementation="Use Framer Motion useScroll().",
            )
        ],
        recommended_explorations=["Preserve sticky phase-switching for section.home-testi."],
    )

    blueprint = SiteBlueprint(
        metadata=SiteMetadata(
            url="https://test.com",
            timestamp="2026-10-04T12:00:00Z",
        ),
        tokens=DesignTokens(),
        sophisticated_features=summary,
    )

    md = generate_llm_markdown(blueprint)
    assert "## 4. SOPHISTICATED INTERACTIVE FEATURES & MOTION MANIFEST" in md
    assert "GSAP ScrollTrigger, Lenis" in md
    assert "Sticky Track (section.home-testi)" in md
    assert "Preserve sticky phase-switching" in md
    assert "## 5. SEMANTIC COMPONENT ARCHITECTURE & LANDMARKS" in md
    assert "## 6. RECONSTRUCTION IMPLEMENTATION INSTRUCTIONS" in md
