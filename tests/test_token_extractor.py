"""Tests for token_extractor module."""

from ui_sleuth.token_extractor import extract_tokens_from_dict, normalize_font_family


def test_normalize_font_family():
    assert normalize_font_family('"Inter", sans-serif') == "Inter, sans-serif"
    assert normalize_font_family("'Roboto Mono', monospace") == "Roboto Mono, monospace"


def test_extract_tokens_from_dict():
    raw_data = {
        "colors": {
            "backgrounds": ["#ffffff", "#0f172a"],
            "surfaces": ["#f8fafc"],
            "text": ["#020617"],
            "accents": ["#3b82f6"],
            "all_colors": [
                {
                    "hex": "#ffffff",
                    "rgb": "rgb(255, 255, 255)",
                    "role": "background",
                    "frequency": 8,
                    "source_element": "body",
                },
                {
                    "hex": "#3b82f6",
                    "rgb": "rgb(59, 130, 246)",
                    "role": "accent",
                    "frequency": 3,
                    "source_element": "button",
                },
            ],
        },
        "typography": {
            "primary_font_family": "Plus Jakarta Sans, sans-serif",
            "base_font_size": "16px",
            "base_line_height": "24px",
            "header_scales": {
                "h1": {
                    "tag": "h1",
                    "font_family": "Plus Jakarta Sans",
                    "font_size": "56px",
                    "font_weight": "800",
                    "line_height": "64px",
                    "letter_spacing": "-0.02em",
                }
            },
        },
        "spacing_elevation": {
            "dominant_border_radii": ["8px", "16px", "9999px"],
            "box_shadows": ["0 10px 15px -3px rgba(0, 0, 0, 0.1)"],
        },
        "custom_properties": {
            "--color-primary": "#3b82f6",
            "--theme-mode": "dark",
        },
    }

    tokens = extract_tokens_from_dict(raw_data)
    assert len(tokens.colors.backgrounds) == 2
    assert tokens.colors.accents == ["#3b82f6"]
    assert tokens.typography.primary_font_family == "Plus Jakarta Sans, sans-serif"
    assert tokens.typography.header_scales["h1"].font_size == "56px"
    assert tokens.spacing_elevation.dominant_border_radii == ["8px", "16px", "9999px"]
    assert tokens.custom_properties["--color-primary"] == "#3b82f6"
