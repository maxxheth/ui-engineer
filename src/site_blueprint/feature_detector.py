"""Detection and isolated exploration of sophisticated UI features and motion engines."""

from __future__ import annotations

import logging
from typing import Any

from playwright.sync_api import Page

from site_blueprint.models import SophisticatedFeature, SophisticatedFeaturesSummary

logger = logging.getLogger(__name__)

PROBE_SOPHISTICATED_FEATURES_JS = """
() => {
    const results = {
        detected_engines: [],
        sticky_tracks: [],
        offscreen_drawers: [],
        disclosures: [],
        marquees: [],
        canvases: []
    };

    const viewportHeight = window.innerHeight || 900;
    const viewportWidth = window.innerWidth || 1440;

    // 1. Motion & Physics Engine Detection
    if (window.gsap) {
        let gsapDesc = 'GSAP (GreenSock)';
        const plugins = [];
        if (window.ScrollTrigger) plugins.push('ScrollTrigger');
        if (window.SplitText) plugins.push('SplitText');
        if (window.Flip) plugins.push('Flip');
        if (window.Draggable) plugins.push('Draggable');
        if (plugins.length > 0) gsapDesc += ` [${plugins.join(', ')}]`;
        results.detected_engines.push(gsapDesc);
    }
    if (window.lenis || document.documentElement.classList.contains('lenis') || window.Lenis) {
        results.detected_engines.push('Lenis Smooth Scroll');
    }
    if (window.LocomotiveScroll || document.querySelector('[data-scroll-container]')) {
        results.detected_engines.push('Locomotive Scroll');
    }
    if (window.THREE || window.__THREE__) {
        results.detected_engines.push('Three.js (WebGL)');
    }
    if (document.querySelector('spline-viewer, [data-spline]')) {
        results.detected_engines.push('Spline 3D Runtime');
    }
    if (document.querySelector('rive-canvas, [data-rive]')) {
        results.detected_engines.push('Rive Vector Motion');
    }
    if (window.lottie || document.querySelector('dotlottie-player, lottie-player')) {
        results.detected_engines.push('Lottie Animations');
    }
    if (document.querySelector('[data-framer-name], [data-framer-component]')) {
        results.detected_engines.push('Framer Motion');
    }

    // 2. Sticky Scroll-Jacked / Pinned Scenes Detection
    // Elements with position: sticky or GSAP ScrollTrigger pin
    const allEls = document.querySelectorAll('*');
    const seenSticky = new Set();

    for (const el of allEls) {
        const style = window.getComputedStyle(el);
        if (style.position === 'sticky') {
            const parent = el.parentElement;
            const parentRect = parent ? parent.getBoundingClientRect() : null;
            const elRect = el.getBoundingClientRect();

            // A sticky scene track typically has a parent taller than the viewport
            const trackHeight = parentRect ? Math.round(parentRect.height) : Math.round(elRect.height);
            const parentTag = parent ? parent.tagName.toLowerCase() : '';
            const parentClass = parent && typeof parent.className === 'string' ? parent.className.trim() : '';
            const selector = parentClass ? `${parentTag}.${parentClass.split(/\\s+/)[0]}` : el.tagName.toLowerCase();

            if (!seenSticky.has(selector) && trackHeight > viewportHeight * 1.2) {
                seenSticky.add(selector);
                const itemsCount = el.querySelectorAll('[class*=\"item\"], [class*=\"card\"], li').length;
                results.sticky_tracks.push({
                    name: `Sticky Track (${selector})`,
                    selector: selector,
                    dimensions: {
                        top: parentRect ? Math.round(parentRect.top + window.scrollY) : 0,
                        left: Math.round(elRect.left),
                        width: Math.round(elRect.width),
                        height: trackHeight
                    },
                    stickyHeight: Math.round(elRect.height),
                    childItemsCount: itemsCount,
                    description: `Pinned scroll scene of height ${trackHeight}px with sticky viewport container (${Math.round(elRect.height)}px). Driven by progressive scrolling.`
                });
            }
        }
    }

    // Also check GSAP ScrollTrigger pinned triggers
    if (window.ScrollTrigger && window.ScrollTrigger.getAll) {
        const triggers = window.ScrollTrigger.getAll();
        for (const st of triggers) {
            if (st.pin && st.trigger) {
                const el = st.trigger;
                const tag = el.tagName.toLowerCase();
                const cls = typeof el.className === 'string' ? el.className.split(/\\s+/)[0] : '';
                const selector = cls ? `${tag}.${cls}` : tag;
                if (!seenSticky.has(selector)) {
                    seenSticky.add(selector);
                    const r = el.getBoundingClientRect();
                    results.sticky_tracks.push({
                        name: `GSAP Pinned Scene (${selector})`,
                        selector: selector,
                        dimensions: {
                            top: Math.round(r.top + window.scrollY),
                            left: Math.round(r.left),
                            width: Math.round(r.width),
                            height: Math.round(st.end - st.start)
                        },
                        stickyHeight: Math.round(r.height),
                        childItemsCount: el.querySelectorAll('*').length,
                        description: `GSAP ScrollTrigger pinned sequence running from scroll offset ${Math.round(st.start)}px to ${Math.round(st.end)}px.`
                    });
                }
            }
        }
    }

    // 3. Off-Screen Drawers, Modals & Floating Overlays
    const seenDrawers = new Set();
    for (const el of allEls) {
        const style = window.getComputedStyle(el);
        const rect = el.getBoundingClientRect();
        const transform = style.transform || '';
        const isOffscreenTransform = transform.includes('matrix') && (
            // check if translated outside normal bounds
            rect.top > viewportHeight * 2 || rect.left > viewportWidth || rect.right < 0 || rect.bottom < -100
        );
        const isLargeModal = (rect.height > 500 || el.scrollHeight > 500) && (
            style.position === 'fixed' || style.position === 'absolute'
        ) && (
            style.display === 'none' ||
            style.visibility === 'hidden' ||
            parseFloat(style.opacity || '1') === 0 ||
            isOffscreenTransform ||
            (el.className && typeof el.className === 'string' && (
                el.className.includes('modal') ||
                el.className.includes('drawer') ||
                el.className.includes('news') ||
                el.className.includes('popup') ||
                el.className.includes('pop-')
            ))
        );

        if (isLargeModal) {
            const tag = el.tagName.toLowerCase();
            const cls = typeof el.className === 'string' ? el.className.trim() : '';
            const selector = cls ? `${tag}.${cls.split(/\\s+/)[0]}` : tag;

            if (!seenDrawers.has(selector) && selector !== 'body' && selector !== 'html') {
                seenDrawers.add(selector);
                const headings = Array.from(el.querySelectorAll('h1, h2, h3, [class*=\"title\"]'))
                    .map(h => (h.innerText || '').trim())
                    .filter(t => t.length > 0)
                    .slice(0, 5);
                const textPreview = (el.innerText || '').trim().slice(0, 150).replace(/[\\r\\n]+/g, ' ');

                results.offscreen_drawers.push({
                    name: `Modal/Drawer (${selector})`,
                    selector: selector,
                    dimensions: {
                        top: Math.round(rect.top + window.scrollY),
                        left: Math.round(rect.left),
                        width: Math.round(rect.width || el.scrollWidth),
                        height: Math.round(rect.height || el.scrollHeight)
                    },
                    headings: headings,
                    textPreview: textPreview,
                    description: `Off-screen or dynamic drawer/modal containing ${headings.length} headings and substantial structured content.`
                });
            }
        }
    }

    // 4. Interactive Disclosures & Accordions
    const accordionTriggers = document.querySelectorAll(
        'details, [aria-expanded], [class*=\"accordion\"], [class*=\"dropdown\"], .home-ser-item, [data-accordion]'
    );
    const seenAccordions = new Set();
    for (const el of accordionTriggers) {
        const tag = el.tagName.toLowerCase();
        const cls = typeof el.className === 'string' ? el.className.split(/\\s+/)[0] : '';
        const selector = cls ? `${tag}.${cls}` : tag;
        if (!seenAccordions.has(selector)) {
            seenAccordions.add(selector);
            const titleEl = el.querySelector('summary, [class*=\"title\"], [class*=\"head\"], h1, h2, h3, h4');
            const title = titleEl ? (titleEl.innerText || '').trim() : '';
            const r = el.getBoundingClientRect();
            results.disclosures.push({
                name: `Interactive Disclosure (${selector})`,
                selector: selector,
                title: title,
                dimensions: {
                    top: Math.round(r.top + window.scrollY),
                    left: Math.round(r.left),
                    width: Math.round(r.width),
                    height: Math.round(r.height)
                },
                description: `Expandable disclosure / accordion element containing interactive sub-content.`
            });
        }
    }

    // 5. Marquees & Continuous Tickers
    const marquees = document.querySelectorAll('[class*=\"marquee\"], [class*=\"ticker\"], [class*=\"client-list\"]');
    for (const el of marquees) {
        const tag = el.tagName.toLowerCase();
        const cls = typeof el.className === 'string' ? el.className.split(/\\s+/)[0] : '';
        const selector = cls ? `${tag}.${cls}` : tag;
        const r = el.getBoundingClientRect();
        results.marquees.push({
            name: `Continuous Stream (${selector})`,
            selector: selector,
            dimensions: {
                top: Math.round(r.top + window.scrollY),
                left: Math.round(r.left),
                width: Math.round(r.width),
                height: Math.round(r.height)
            },
            description: `Infinite marquee or animated ticker stream containing logo/card repetitions.`
        });
    }

    // 6. Dynamic Canvases
    const canvases = document.querySelectorAll('canvas');
    for (const c of canvases) {
        const gl = c.getContext('webgl2') || c.getContext('webgl');
        const r = c.getBoundingClientRect();
        results.canvases.push({
            name: gl ? 'WebGL Shader Canvas' : '2D Dynamic Canvas',
            selector: 'canvas',
            dimensions: {
                top: Math.round(r.top + window.scrollY),
                left: Math.round(r.left),
                width: Math.round(r.width),
                height: Math.round(r.height)
            },
            isWebGL: !!gl,
            description: gl
                ? 'High-performance WebGL 3D or shader animation canvas.'
                : '2D interactive canvas element.'
        });
    }

    return results;
}
"""


def detect_and_explore_features(
    page: Page,
    explore: bool = True,
) -> SophisticatedFeaturesSummary:
    """Probes the live page for sophisticated animation, sticky scenes, drawers, and interactive systems."""
    try:
        raw_probe: dict[str, Any] = page.evaluate(PROBE_SOPHISTICATED_FEATURES_JS)
    except Exception as e:
        logger.warning("Feature detection probe failed: %s", e)
        return SophisticatedFeaturesSummary(
            has_sophisticated_features=False,
            detected_engines=[],
            features=[],
            recommended_explorations=[],
        )

    features: list[SophisticatedFeature] = []
    recommended: list[str] = []

    detected_engines = raw_probe.get("detected_engines", [])
    if detected_engines:
        features.append(
            SophisticatedFeature(
                category="motion_physics_engine",
                name="Motion & Physics Runtime",
                selector="window",
                description=f"Active animation frameworks: {', '.join(detected_engines)}",
                dimensions={},
                requires_independent_exploration=False,
                exploration_status="explored",
                suggested_implementation="Integrate Framer Motion (`useScroll`, `useTransform`) or GSAP ScrollTrigger for fidelity.",
                details={"engines": detected_engines},
            )
        )
        recommended.append(
            f"Page uses {', '.join(detected_engines)}. Model transitions using declarative motion primitives (e.g. Framer Motion layout animations)."
        )

    # Sticky tracks
    sticky_tracks = raw_probe.get("sticky_tracks", [])
    for track in sticky_tracks:
        features.append(
            SophisticatedFeature(
                category="sticky_scroll_track",
                name=track["name"],
                selector=track["selector"],
                description=track["description"],
                dimensions=track["dimensions"],
                requires_independent_exploration=True,
                exploration_status="explored" if explore else "detected",
                suggested_implementation="Replicate with CSS `position: sticky; top: 0` container inside a relative scroll track, or Framer Motion `useScroll()` with sequence steps.",
                details={
                    "stickyHeight": track.get("stickyHeight"),
                    "childItemsCount": track.get("childItemsCount"),
                },
            )
        )
        recommended.append(
            f"Explore {track['selector']}: Pinned scene spanning {track['dimensions'].get('height', 0)}px scroll track. Do not flatten into static cards; preserve sticky phase-switching."
        )

    # Offscreen drawers & modals
    drawers = raw_probe.get("offscreen_drawers", [])
    for drawer in drawers:
        features.append(
            SophisticatedFeature(
                category="offscreen_drawer",
                name=drawer["name"],
                selector=drawer["selector"],
                description=drawer["description"],
                dimensions=drawer["dimensions"],
                requires_independent_exploration=True,
                exploration_status="explored" if explore else "detected",
                suggested_implementation="Implement as an isolated Dialog/Drawer component (e.g. Radix UI Dialog or Vaul drawer) triggered by card click.",
                details={
                    "headings": drawer.get("headings", []),
                    "textPreview": drawer.get("textPreview", ""),
                },
            )
        )
        recommended.append(
            f"Explore {drawer['selector']}: Deep off-screen drawer container ({drawer['dimensions'].get('height', 0)}px tall) holding dynamic case study or form details."
        )

    # Interactive disclosures
    disclosures = raw_probe.get("disclosures", [])
    for disc in disclosures:
        features.append(
            SophisticatedFeature(
                category="interactive_disclosure",
                name=disc["name"],
                selector=disc["selector"],
                description=disc["description"],
                dimensions=disc["dimensions"],
                requires_independent_exploration=False,
                exploration_status="explored",
                suggested_implementation="Implement using `@radix-ui/react-accordion` or HTML5 `<details>` with Framer Motion `AnimatePresence` height animation.",
                details={"title": disc.get("title")},
            )
        )

    # Marquees
    marquees = raw_probe.get("marquees", [])
    for mq in marquees:
        features.append(
            SophisticatedFeature(
                category="marquee_stream",
                name=mq["name"],
                selector=mq["selector"],
                description=mq["description"],
                dimensions=mq["dimensions"],
                requires_independent_exploration=False,
                exploration_status="explored",
                suggested_implementation="Replicate with CSS infinite marquee animation (`@keyframes marquee { 0% { transform: translateX(0); } 100% { transform: translateX(-50%); } }`) with duplicated items.",
                details={},
            )
        )

    # Canvases
    canvases = raw_probe.get("canvases", [])
    for c in canvases:
        features.append(
            SophisticatedFeature(
                category="webgl_canvas",
                name=c["name"],
                selector=c["selector"],
                description=c["description"],
                dimensions=c["dimensions"],
                requires_independent_exploration=True,
                exploration_status="explored",
                suggested_implementation="Wrap with `@react-three/fiber` / `@react-three/drei` Canvas for WebGL or HTML5 Canvas with requestAnimationFrame loop.",
                details={"isWebGL": c.get("isWebGL")},
            )
        )

    has_features = len(features) > 0

    return SophisticatedFeaturesSummary(
        has_sophisticated_features=has_features,
        detected_engines=detected_engines,
        features=features,
        recommended_explorations=recommended,
    )
