# site-blueprint 🛠️✨

> **Reverse-engineer live web pages into ultra-dense, token-optimized JSON/YAML context blueprints specifically designed for downstream LLMs and "vibe-coding" automated UI reconstruction.**

`site-blueprint` is a specialized automation tool and Python package built on modern standards (`uv`, `scrapling`, `pydantic`, `typer`). It bridges the gap between raw web scraping and LLM context windows by extracting design tokens, pruning DOM boilerplate, deduplicating repetitive UI patterns (e.g. card grids), and diagnosing external production disciplines (Three.js 3D models, Rive/Lottie vector animations, WebGL canvases, and background video loops).

---

## 🌟 Key Features

1. **Scrapling Engine Pipeline (`scrapling_engine.py`)**
   - Headless Chromium powered by `scrapling.DynamicFetcher` and `StealthyFetcher` (for Turnstile/bot bypass).
   - Network interception listeners attached to the browser session prior to navigation.
   - Configurable wait conditions (`networkidle`, `load`, or CSS selector) and timeouts.
   - Configurable screen viewport dimensions (e.g. `1440x900`).

2. **Decodo Proxy Integration (`proxy_manager.py`)**
   - Native support for Decodo ISP and residential proxy pools.
   - Automatic proxy parsing, credentials handling, and password redaction.
   - Round-robin proxy rotation pool support via Scrapling's `ProxyRotator`.
   - Auto-detection of `proxies.txt` or `--decodo` flag referencing `.env` or proxy list files.

3. **Design Token Harvesting (`token_extractor.py`)**
   - Client-side JavaScript evaluation that samples computed styles across landmarks (`header`, `main`, `footer`, `section`, `nav`).
   - Normalizes and deduplicates color palettes into semantic roles: `backgrounds`, `surfaces`, `text`, `accents`.
   - Extracts typography stacks, base font sizes, line heights, and header scales (`<h1>` through `<h4>`).
   - Extracts dominant border radii, box-shadow elevation signatures, and CSS custom properties (`--color-*`, `--theme-*`).

4. **Semantic DOM Pruning & Pattern Recognition (`dom_pruner.py`)**
   - Strips non-semantic elements: `<script>`, `<style>`, `<noscript>`, `<svg>`, `<iframe>`, and 1x1 tracking pixels.
   - Maps page by major structural landmarks (`header`, `nav`, `main`, `section`, `article`, `aside`, `footer`).
   - **Pattern Deduplication**: Detects containers with 3+ repetitive sibling cards and collapses them into a concise schema:
     ```json
     {
       "pattern": "FeatureCard",
       "instance_count": 6,
       "sample_content": { "title": "Fast Inference", "description": "..." }
     }
     ```
   - Actionable interaction metadata: counts of forms, inputs, selects, and textareas, plus primary CTA button labels.
   - Concise copy previews (15–25 words) capturing copy intent without wasting LLM tokens.

5. **Specialized Asset & Runtime Inspector (`asset_inspector.py`)**
   - **Network Interception**: Logs binary 3D models (`.glb`, `.gltf`, `.splinecode`, `.usdz`, `.fbx`, `.bin`), vector motion (`.riv`, `.lottie`), and video streams (`.mp4`, `.webm`, `.m3u8`).
   - **Canvas & WebGL Evaluation**: Probes `<canvas>` elements for active 2D/WebGL/WebGL2 contexts and inspects runtime window engines (`Three.js`, `Babylon.js`, `Spline`, `Rive`, `Lottie`, `PixiJS`).
   - **Video Diagnostics**: Inspects playback flags (`autoplay`, `muted`, `loop`, `playsinline`) to distinguish decorative background loops from interactive players.
   - **Runtime Ecosystem Mapping**: Recommends modern React/Next.js wrappers (`@react-three/fiber`, `@rive-app/react-canvas`, `@splinetool/react-spline`, `@lottiefiles/react-lottie-player`).

6. **Sophisticated Feature Detection & Exploration (`feature_detector.py`)**
   - **Motion Runtimes**: Detects GSAP (ScrollTrigger, SplitText), Lenis smooth scrolling, Three.js, Rive, and Lottie.
   - **Sticky Tracks**: Identifies CSS and JS sticky scroll containers, pinning mechanics, and horizontal scroll tracks.
   - **Off-Screen Drawers & Modals**: Detects hidden drawers/modals, triggers them open to evaluate active DOM state and extract copy/structure, and restores original layout.
   - **Interactive Elements**: Inspects accordions, expandable FAQ modules, tabs, and marquees.

7. **Multimodal & Export Layer (`exporter.py`, `cli.py`)**
   - Full-page screenshots saved alongside blueprints (`--screenshot`), with progressive scrolling, texture clamp safeguards, and GSAP stabilization.
   - `blueprint.json`: Validated against strict Pydantic schemas.
   - `blueprint.md`: LLM-ready context block with embedded vibe-coding instructions, ready to copy-paste directly into Claude, GPT-4, or Gemini.
   - `blueprint.yaml`: Ultra-dense YAML representation for minimal token consumption.

---

## 🚀 Quickstart

### Prerequisites
- Python 3.11+
- `uv` (fast Python package manager)

### Installation
```bash
git clone <repo-url>
cd ui-engineer
uv sync
```

### Basic Extraction
```bash
uv run site-blueprint extract https://example.com --output ./output --screenshot
```

### Using Wait Conditions & Viewport
```bash
uv run site-blueprint extract https://example.com \
  --output ./output \
  --wait-until networkidle \
  --timeout 30 \
  --viewport 1920x1080 \
  --screenshot
```

### Decodo Proxy Support
Pass a single proxy, a proxy list file, or enable Decodo environment variables:
```bash
# Direct proxy URL
uv run site-blueprint extract https://example.com --proxy "http://username:password@isp.decodo.com:10001"

# Load pool from file (rotates across ports round-robin)
uv run site-blueprint extract https://example.com --proxy-file ./proxies.txt

# Automatically use Decodo proxy configuration
uv run site-blueprint extract https://example.com --decodo
```

Environment variables supported in `.env`:
```env
DECODO_PROXY_URL="http://your_username:your_password@isp.decodo.com:10001"
# or
DECODO_USERNAME="your_username"
DECODO_PASSWORD="your_password"
DECODO_HOST="isp.decodo.com"
DECODO_PORT_START=10001
DECODO_PORT_END=10010
```

### Stealth Mode (Cloudflare Turnstile Bypass)
```bash
uv run site-blueprint extract https://protected-site.com --stealth
```

---

## 📋 CLI Reference

```
Usage: site-blueprint extract [OPTIONS] [url]

Options:
  -u, --url <str>               Target URL (alternative to positional argument)
  -o, --output <path>           Output directory for generated blueprints [default: output]
  -s, --screenshot              Capture a full-page screenshot alongside the blueprint
      --wait-until <str>        Wait condition: 'networkidle', 'load', or CSS selector [default: networkidle]
  -t, --timeout <int>           Timeout in seconds [default: 30]
      --viewport <str>          Emulated viewport dimensions (WIDTHxHEIGHT) [default: 1440x900]
      --proxy <str>             Single proxy URL
      --proxy-file <str>        Path to text file containing proxy URLs
      --decodo                  Enable Decodo ISP proxy integration
      --stealth                 Use StealthyFetcher to bypass Cloudflare
  -f, --format <str>            Output format: 'all', 'json', 'markdown', or 'yaml' [default: all]
      --headless / --no-headless Run browser in headless or visible mode [default: headless]
      --real-chrome / --no-real-chrome Use installed Google Chrome executable
  -d, --delay <float>           Post-load stabilization delay in seconds [default: 2.0]
      --auto-scroll / --no-auto-scroll Progressively scroll page to trigger lazy loading [default: auto-scroll]
      --explore / --no-explore  Detect and independently explore sophisticated features [default: explore]
  -v, --verbose                 Enable verbose debug logging
      --help                    Show this message and exit.
```

---

## 🧪 Testing & Code Quality

Run tests with `pytest`:
```bash
uv run pytest
```

Check formatting and lint rules with strict `ruff` settings:
```bash
uv run ruff check
uv run ruff format --check
```

Run strict static type analysis with `pyright`:
```bash
uv run pyright
```
