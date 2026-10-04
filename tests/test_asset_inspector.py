"""Tests for asset_inspector module."""

from site_blueprint.asset_inspector import (
    NetworkAssetCollector,
    synthesize_production_assets,
)


class DummyResponse:
    def __init__(self, url: str, status: int = 200, headers: dict[str, str] | None = None):
        self.url = url
        self.status = status
        self.headers = headers or {}


def test_network_collector_filtering():
    collector = NetworkAssetCollector()

    collector.handle_response(DummyResponse("https://example.com/models/scene.glb", 200))
    collector.handle_response(DummyResponse("https://example.com/assets/hero.splinecode", 200))
    collector.handle_response(DummyResponse("https://example.com/animations/bot.riv", 200))
    collector.handle_response(DummyResponse("https://example.com/animations/spinner.lottie", 200))
    collector.handle_response(DummyResponse("https://example.com/videos/bg_loop.mp4", 200))
    collector.handle_response(
        DummyResponse("https://example.com/styles.css", 200, {"content-type": "text/css"})
    )

    assert len(collector.assets_3d) == 2
    assert "https://example.com/models/scene.glb" in collector.assets_3d
    assert "https://example.com/assets/hero.splinecode" in collector.assets_3d

    assert len(collector.assets_motion) == 2
    assert "https://example.com/animations/bot.riv" in collector.assets_motion
    assert "https://example.com/animations/spinner.lottie" in collector.assets_motion

    assert len(collector.assets_video) == 1
    assert "https://example.com/videos/bg_loop.mp4" in collector.assets_video


def test_synthesize_production_assets_3d_and_video():
    collector = NetworkAssetCollector()
    collector.assets_3d = ["https://cdn.example.com/model.glb"]

    dom_probe = {
        "detected_window_engines": ["Three.js"],
        "canvases": [
            {
                "index": 0,
                "context_type": "webgl2",
                "parent_landmark": "main > section#hero",
                "width": 800,
                "height": 600,
            }
        ],
        "videos": [
            {
                "index": 0,
                "parent_landmark": "header",
                "sources": ["https://cdn.example.com/bg.mp4"],
                "autoplay": True,
                "muted": True,
                "loop": True,
                "playsinline": True,
                "controls": False,
                "is_background_loop": True,
            },
            {
                "index": 1,
                "parent_landmark": "section#demo",
                "sources": ["https://cdn.example.com/demo.mp4"],
                "autoplay": False,
                "muted": False,
                "loop": False,
                "playsinline": False,
                "controls": True,
                "is_background_loop": False,
            },
        ],
    }

    assets = synthesize_production_assets(collector, dom_probe)

    # 1. 3D Model Asset
    model_asset = next((a for a in assets if a.category == "3d_model"), None)
    assert model_asset is not None
    assert "Three.js" in model_asset.detected_engines
    assert "@react-three/fiber" in model_asset.suggested_react_wrapper
    assert model_asset.direct_asset_urls == ["https://cdn.example.com/model.glb"]

    # 2. Rich Video Assets
    video_assets = [a for a in assets if a.category == "rich_video"]
    assert len(video_assets) == 2

    bg_video = video_assets[0]
    assert bg_video.details["is_background_loop"] is True
    assert "Standard HTML5 video loop" in bg_video.suggested_react_wrapper

    interactive_video = video_assets[1]
    assert interactive_video.details["is_background_loop"] is False
    assert "Interactive Video Player" in interactive_video.suggested_react_wrapper
