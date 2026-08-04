"""Prompt template registry and reusable prompt templates for mathematics research."""

from __future__ import annotations

from src.rag.prompt_builder.models import PromptTemplate

DEFAULT_RESEARCH_RULES: list[str] = [
    "You are an AI assistant helping mathematics researchers analyze academic papers.",
    "Answer the question ONLY using the supplied mathematical context.",
    "Never invent theorems, lemmas, definitions, or mathematical proofs.",
    "Preserve all mathematical notation, symbols, variables, and LaTeX expressions exactly as written.",
    "Keep theorem, definition, lemma, and section numbering unchanged.",
    "If the supplied context does not contain enough information to fully answer the question, explicitly state that the uploaded papers do not contain enough information.",
]

DEFAULT_SYSTEM_PROMPT = (
    "You are an AI Research Assistant specializing in academic mathematics.\n"
    "Follow these strict research rules:\n"
    + "\n".join(f"- {rule}" for rule in DEFAULT_RESEARCH_RULES)
)


class TemplateRegistry:
    """Registry providing specialized prompt templates for different query intents."""

    def __init__(self) -> None:
        """Initialize TemplateRegistry with default templates."""
        self._templates: dict[str, PromptTemplate] = {}
        self._register_default_templates()

    def _register_default_templates(self) -> None:
        """Register built-in templates."""
        self._templates["default"] = PromptTemplate(
            template_name="default",
            system_prompt=DEFAULT_SYSTEM_PROMPT,
            research_rules=DEFAULT_RESEARCH_RULES,
            user_prompt_template="Question:\n{query}\n\nPlease answer the question based strictly on the provided context.",
            context_separator="====================================================",
            version="v1.0",
        )

        self._templates["definition"] = PromptTemplate(
            template_name="definition",
            system_prompt=DEFAULT_SYSTEM_PROMPT + "\n- Focus on extracting formal mathematical definitions and conditions.",
            research_rules=DEFAULT_RESEARCH_RULES + ["Extract formal definitions precisely."],
            user_prompt_template="Definition Query:\n{query}\n\nProvide the complete formal mathematical definition from the context.",
            context_separator="====================================================",
            version="v1.0",
        )

        self._templates["theorem_proof"] = PromptTemplate(
            template_name="theorem_proof",
            system_prompt=DEFAULT_SYSTEM_PROMPT + "\n- Focus on formal theorem statements and proof steps.",
            research_rules=DEFAULT_RESEARCH_RULES + ["State the exact theorem hypotheses and conclusions."],
            user_prompt_template="Theorem/Proof Query:\n{query}\n\nState the theorem and detail the proof steps provided in the context.",
            context_separator="====================================================",
            version="v1.0",
        )

        self._templates["dependency"] = PromptTemplate(
            template_name="dependency",
            system_prompt=DEFAULT_SYSTEM_PROMPT + "\n- Focus on dependency chains, antecedent lemmas, and proof prerequisites.",
            research_rules=DEFAULT_RESEARCH_RULES + ["Trace dependency relationships between lemmas and theorems."],
            user_prompt_template="Dependency Query:\n{query}\n\nIdentify the prerequisite lemmas, definitions, or theorems used in the proof.",
            context_separator="====================================================",
            version="v1.0",
        )

        self._templates["summary"] = PromptTemplate(
            template_name="summary",
            system_prompt=DEFAULT_SYSTEM_PROMPT + "\n- Focus on high-level mathematical summaries and key contributions.",
            research_rules=DEFAULT_RESEARCH_RULES + ["Provide a concise summary grounded strictly in the abstract and main sections."],
            user_prompt_template="Summary Query:\n{query}\n\nSummarize the key mathematical results presented in the context.",
            context_separator="====================================================",
            version="v1.0",
        )

    def get_template(self, template_name: str = "default") -> PromptTemplate:
        """Retrieve a PromptTemplate by name.

        Args:
            template_name: Name of template.

        Returns:
            PromptTemplate instance (falls back to 'default' if not found).
        """
        return self._templates.get(template_name.lower(), self._templates["default"])

    def register_template(self, template: PromptTemplate) -> None:
        """Register a custom PromptTemplate.

        Args:
            template: PromptTemplate instance.
        """
        self._templates[template.template_name.lower()] = template
