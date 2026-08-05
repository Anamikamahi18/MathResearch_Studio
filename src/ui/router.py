"""Page router for switching between application views."""

from __future__ import annotations

import logging
from typing import Callable

from src.ui import pages
from src.ui.state import get_current_page

logger = logging.getLogger(__name__)


class PageRouter:
    """Router class mapping navigation keys to Streamlit page rendering functions."""

    def __init__(self) -> None:
        """Initialize page router with route mappings."""
        self._routes: dict[str, Callable[[], None]] = {
            "home": pages.render_home_page,
            "upload": pages.render_upload_page,
            "library": pages.render_library_page,
            "search": pages.render_search_page,
            "assistant": pages.render_assistant_page,
            "graph": pages.render_graph_page,
            "notation": pages.render_notation_page,
            "statistics": pages.render_statistics_page,
            "export": pages.render_export_page,
            "settings": pages.render_settings_page,
        }

    def render_current_page(self) -> None:
        """Resolve current active page route from session state and execute render handler."""
        page_key = get_current_page()
        render_fn = self._routes.get(page_key)

        if render_fn:
            logger.debug("Routing to page view: '%s'", page_key)
            render_fn()
        else:
            logger.warning("Unknown page key '%s' requested; defaulting to home", page_key)
            pages.render_home_page()
