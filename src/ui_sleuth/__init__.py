"""UI Sleuth: Reverse-engineering live web pages into token-optimized LLM context blueprints."""

from __future__ import annotations

import warnings

from ui_sleuth.cli import app, main
from ui_sleuth.crawler import SiteCrawler, extract_links_from_html, normalize_url, slugify_url
from ui_sleuth.exporter import (
    export_blueprint,
    export_site_design_system,
    generate_llm_markdown,
    generate_site_design_system_markdown,
)
from ui_sleuth.models import (
    ColorPalette,
    ColorToken,
    ComponentProp,
    CrawledPageSummary,
    DesignTokens,
    ExternalProductionAsset,
    HeaderScale,
    InteractionMetadata,
    MultiPageCrawlResult,
    PatternSchema,
    SectionBlueprint,
    SiteBlueprint,
    SiteComponent,
    SiteDesignSystem,
    SiteMetadata,
    SpacingElevationTokens,
    TypographyTokens,
)
from ui_sleuth.proxy_manager import ProxyConfig, resolve_proxy_config
from ui_sleuth.scrapling_engine import ScraplingEngine

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
    "ComponentProp",
    "CrawledPageSummary",
    "DesignTokens",
    "ExternalProductionAsset",
    "HeaderScale",
    "InteractionMetadata",
    "MultiPageCrawlResult",
    "PatternSchema",
    "ProxyConfig",
    "ScraplingEngine",
    "SectionBlueprint",
    "SiteBlueprint",
    "SiteComponent",
    "SiteCrawler",
    "SiteDesignSystem",
    "SiteMetadata",
    "SpacingElevationTokens",
    "TypographyTokens",
    "__version__",
    "app",
    "export_blueprint",
    "export_site_design_system",
    "extract_links_from_html",
    "generate_llm_markdown",
    "generate_site_design_system_markdown",
    "main",
    "normalize_url",
    "resolve_proxy_config",
    "slugify_url",
]
