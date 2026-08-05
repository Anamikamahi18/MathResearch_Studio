"""ExportService application service for exporting research notes, summaries, JSON, Markdown, and CSV formats."""

from __future__ import annotations

import csv
import json
import logging
from pathlib import Path
from typing import Any

from src.rag.guardrails import FinalResearchResponse

logger = logging.getLogger(__name__)


class ExportService:
    """Application service for generating structured exports in JSON, Markdown, and CSV formats."""

    def __init__(self, export_dir: str | Path = "exports") -> None:
        """Initialize ExportService with output directory.

        Args:
            export_dir: Directory where export files are saved.
        """
        self.export_dir = Path(export_dir)
        self.export_dir.mkdir(parents=True, exist_ok=True)

    def export_research_notes(
        self,
        data: dict[str, Any] | list[dict[str, Any]] | FinalResearchResponse,
        format: str = "markdown",
        output_path: str | Path | None = None,
    ) -> Path:
        """Export research notes or RAG pipeline responses into Markdown, JSON, or CSV.

        Args:
            data: Single dictionary, list of dictionaries, or FinalResearchResponse object.
            format: Target format ("markdown", "json", "csv"). Default: "markdown".
            output_path: Optional output file path.

        Returns:
            Path to the written export file.
        """
        fmt = format.lower()
        target_path = (
            Path(output_path)
            if output_path
            else self.export_dir / f"research_notes.{ 'md' if fmt in ('markdown', 'md') else fmt }"
        )

        # Handle FinalResearchResponse dataclass/object
        if isinstance(data, FinalResearchResponse):
            export_dict = data.to_dict()
        elif isinstance(data, dict):
            export_dict = data
        elif isinstance(data, list):
            export_dict = {"notes": data}
        else:
            export_dict = {"raw_content": str(data)}

        if fmt in ("markdown", "md"):
            return self.export_to_markdown(export_dict, target_path)
        elif fmt == "json":
            return self.export_to_json(export_dict, target_path)
        elif fmt == "csv":
            rows = data if isinstance(data, list) else [export_dict]
            return self.export_to_csv(rows, target_path)
        else:
            raise ValueError(f"Unsupported export format: '{format}'. Allowed: markdown, json, csv.")

    def export_summaries(
        self,
        documents_or_results: list[dict[str, Any]],
        format: str = "json",
        output_path: str | Path | None = None,
    ) -> Path:
        """Export a collection of paper summaries or search results.

        Args:
            documents_or_results: List of paper summary dictionaries or result items.
            format: Target format ("json", "markdown", "csv"). Default: "json".
            output_path: Optional output file path.

        Returns:
            Path to the written export file.
        """
        fmt = format.lower()
        target_path = (
            Path(output_path)
            if output_path
            else self.export_dir / f"paper_summaries.{ 'md' if fmt in ('markdown', 'md') else fmt }"
        )

        if fmt == "json":
            return self.export_to_json(documents_or_results, target_path)
        elif fmt in ("markdown", "md"):
            return self.export_to_markdown({"summaries": documents_or_results}, target_path)
        elif fmt == "csv":
            return self.export_to_csv(documents_or_results, target_path)
        else:
            raise ValueError(f"Unsupported export format: '{format}'. Allowed: json, markdown, csv.")

    def export_to_json(
        self,
        data: Any,
        output_path: str | Path,
    ) -> Path:
        """Write Python data structure to a JSON file.

        Args:
            data: Data object (dict, list, etc.) to serialize to JSON.
            output_path: Target file path.

        Returns:
            Path to written JSON file.
        """
        out_path = Path(output_path)
        out_path.parent.mkdir(parents=True, exist_ok=True)

        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False, default=str)

        logger.info("Exported JSON to: %s", out_path)
        return out_path

    def export_to_markdown(
        self,
        data: dict[str, Any],
        output_path: str | Path,
    ) -> Path:
        """Write formatted research notes to a Markdown file.

        Args:
            data: Dictionary of research note details.
            output_path: Target Markdown file path.

        Returns:
            Path to written Markdown file.
        """
        out_path = Path(output_path)
        out_path.parent.mkdir(parents=True, exist_ok=True)

        lines: list[str] = []

        if "question" in data:
            lines.append(f"# Research Query Notes\n")
            lines.append(f"**Question**: {data.get('question')}\n")
            lines.append(f"**Guardrail Decision**: `{data.get('decision')}` (Status: `{data.get('status')}`)\n")
            lines.append(f"**Reason**: {data.get('reason')}\n")
            lines.append(f"**Confidence**: `{data.get('confidence', 0.0):.4f}`\n\n")

            lines.append("## Answer\n")
            lines.append(f"{data.get('answer_text', '')}\n\n")

            if data.get("citations"):
                lines.append("## Citations\n")
                for cit in data.get("citations", []):
                    lines.append(f"- {cit}")
                lines.append("\n")

            if data.get("bibliography"):
                lines.append("## Bibliography\n")
                for bib in data.get("bibliography", []):
                    lines.append(f"- {bib}")
                lines.append("\n")

            if data.get("warnings"):
                lines.append("## Warnings\n")
                for w in data.get("warnings", []):
                    lines.append(f"- ⚠️ {w}")
                lines.append("\n")

        elif "summaries" in data:
            lines.append("# Paper Summaries Catalog\n\n")
            for item in data.get("summaries", []):
                p_id = item.get("paper_id", "Unknown")
                title = item.get("title", "Untitled")
                authors = ", ".join(item.get("authors", [])) or "N/A"
                lines.append(f"### {title} (`{p_id}`)\n")
                lines.append(f"- **Authors**: {authors}\n")
                lines.append(f"- **Year**: {item.get('year', 'N/A')}\n")
                lines.append(f"- **Sections**: {item.get('section_count', 0)}\n")
                lines.append(f"- **Chunks**: {item.get('chunk_count', 0)}\n\n")

        else:
            lines.append("# Research Export\n\n")
            for k, v in data.items():
                lines.append(f"### {k}\n")
                lines.append(f"```json\n{json.dumps(v, indent=2, default=str)}\n```\n\n")

        out_path.write_text("".join(lines), encoding="utf-8")
        logger.info("Exported Markdown to: %s", out_path)
        return out_path

    def export_to_csv(
        self,
        data: list[dict[str, Any]],
        output_path: str | Path,
    ) -> Path:
        """Write list of dictionary records to a CSV file.

        Args:
            data: List of dictionary records to export as CSV rows.
            output_path: Target CSV file path.

        Returns:
            Path to written CSV file.
        """
        out_path = Path(output_path)
        out_path.parent.mkdir(parents=True, exist_ok=True)

        if not data:
            out_path.write_text("", encoding="utf-8")
            return out_path

        # Flatten nested fields for CSV compatibility
        fieldnames = list(data[0].keys())

        with open(out_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
            writer.writeheader()
            for row in data:
                clean_row = {}
                for k, v in row.items():
                    if isinstance(v, (dict, list)):
                        clean_row[k] = json.dumps(v, ensure_ascii=False, default=str)
                    else:
                        clean_row[k] = v
                writer.writerow(clean_row)

        logger.info("Exported CSV (%d rows) to: %s", len(data), out_path)
        return out_path
