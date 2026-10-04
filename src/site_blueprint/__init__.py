"""site-blueprint: Reverse-engineering live web pages into token-optimized LLM context blueprints."""

from __future__ import annotations

import warnings

from site_blueprint.cli import app, main
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
from site_blueprint.proxy_manager import ProxyConfig, resolve_proxy_config
from site_blueprint.scrapling_engine import ScraplingEngine

# Suppress known upstream deprecation warning in lxml 6.x when invoked by Scrapling
warnings.filterwarnings(
    "ignore",
    message=r"The 'strip_cdata' option of HTMLParser\(\) has never done anything",
    category=DeprecationWarning,
    module=r"lxml\.html",
)

__version__ = "0.1.0"

__all__ = [
    "ColorPalette",
    "ColorToken",
    "DesignTokens",
    "ExternalProductionAsset",
    "HeaderScale",
    "InteractionMetadata",
    "PatternSchema",
    "ProxyConfig",
    "ScraplingEngine",
    "SectionBlueprint",
    "SiteBlueprint",
    "SiteMetadata",
    "SpacingElevationTokens",
    "TypographyTokens",
    "__version__",
    "app",
    "main",
    "resolve_proxy_config",
]
