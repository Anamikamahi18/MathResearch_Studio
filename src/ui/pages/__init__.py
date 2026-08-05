"""Page views package for MathResearch Studio UI."""

from src.ui.pages.assistant import render_assistant_page
from src.ui.pages.export import render_export_page
from src.ui.pages.graph import render_graph_page
from src.ui.pages.home import render_home_page
from src.ui.pages.library import render_library_page
from src.ui.pages.notation import render_notation_page
from src.ui.pages.search import render_search_page
from src.ui.pages.settings import render_settings_page
from src.ui.pages.statistics import render_statistics_page
from src.ui.pages.upload import render_upload_page

__all__ = [
    "render_home_page",
    "render_upload_page",
    "render_library_page",
    "render_search_page",
    "render_assistant_page",
    "render_graph_page",
    "render_notation_page",
    "render_statistics_page",
    "render_export_page",
    "render_settings_page",
]
