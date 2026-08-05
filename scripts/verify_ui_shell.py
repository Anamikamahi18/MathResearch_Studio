#!/usr/bin/env python3
"""Verification script for Day 6 Step 1: Streamlit Application Shell."""

from __future__ import annotations

import logging
import sys
from pathlib import Path

# Ensure project root is on sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from src.ui.config import AppConfig, DEFAULT_APP_CONFIG
from src.ui.router import PageRouter
from src.ui.state import init_session_state, get_current_page, set_current_page

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)


def main() -> None:
    """Run verification for Streamlit UI shell, router, configuration, and components."""
    print("\n============================================================")
    print(" DAY 6 STEP 1: STREAMLIT UI SHELL VERIFICATION")
    print("============================================================\n")

    # 1. Verify Configuration
    print("[1] Verifying AppConfig...")
    cfg = DEFAULT_APP_CONFIG
    print(f"    App Title:        '{cfg.title}'")
    print(f"    App Version:      '{cfg.version}'")
    print(f"    Default Route:    '{cfg.default_page}'")
    print(f"    Supported Pages:  {len(cfg.pages)} routes")
    assert len(cfg.pages) == 10, "Expected 10 navigation routes"

    # 2. Verify Page Router Route Mapping
    print("\n[2] Verifying PageRouter route resolution...")
    router = PageRouter()
    expected_routes = [
        "home",
        "upload",
        "library",
        "search",
        "assistant",
        "graph",
        "notation",
        "statistics",
        "export",
        "settings",
    ]

    for route_key in expected_routes:
        assert route_key in router._routes, f"Missing route mapping for '{route_key}'"
        route_handler = router._routes[route_key]
        assert callable(route_handler), f"Route handler for '{route_key}' is not callable"
        info = cfg.get_page_info(route_key)
        print(f"    Route '{route_key:<11}' -> {info['icon']} {info['label']:<22} (Handler: {route_handler.__name__})")

    # 3. Verify Theme CSS Generation
    print("\n[3] Verifying Theme CSS generation...")
    from src.ui.theme import get_custom_css
    css = get_custom_css(cfg)
    assert "mrs-card" in css
    assert "mrs-branding" in css
    assert "mrs-header" in css
    assert "mrs-footer" in css
    print(f"    Theme CSS generated successfully ({len(css)} bytes)")

    # 4. Verify Component & Sidebar Module Exports
    print("\n[4] Verifying Component & Sidebar exports...")
    from src.ui.components import (
        render_header,
        render_footer,
        render_page_title,
        render_empty_state,
        render_loading_spinner,
        render_error_banner,
    )
    from src.ui.sidebar import render_branding, render_navigation, render_status

    print("    Components verified: header, footer, page_title, empty_state, loading, error")
    print("    Sidebar modules verified: branding, navigation, status")

    print("\n============================================================")
    print(" VERIFICATION COMPLETED SUCCESSFULLY FOR STREAMLIT UI SHELL")
    print("============================================================\n")


if __name__ == "__main__":
    main()
