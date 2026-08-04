"""Unit tests for RAG query processing layer (Day 5 Step 1 & Step 1.5)."""

from __future__ import annotations

import pytest

from src.rag.query_processing import (
    BaseQueryStrategy,
    IntentDetector,
    LLMQueryStrategy,
    MathematicalEntityExtractor,
    MathematicalSymbolExtractor,
    OperationDetector,
    QueryAnalysis,
    QueryIntent,
    QueryNormalizer,
    QueryProcessor,
    ReferencedEntity,
    RuleBasedQueryStrategy,
)


class TestQueryNormalizer:
    """Test suite for QueryNormalizer."""

    def test_normalize_whitespace_and_punctuation(self) -> None:
        """Test collapsing excess whitespace and punctuation spacing."""
        normalizer = QueryNormalizer()
        raw = "Theorem   3.2 ?"
        expected = "Theorem 3.2?"
        assert normalizer.normalize(raw) == expected

    def test_normalize_definition_spacing(self) -> None:
        """Test definition normalization."""
        normalizer = QueryNormalizer()
        raw = "What is   Definition   2.1  ?"
        expected = "What is Definition 2.1?"
        assert normalizer.normalize(raw) == expected

    def test_normalize_smart_quotes(self) -> None:
        """Test normalizing curly smart quotes to ASCII."""
        normalizer = QueryNormalizer()
        raw = "Explain “Theorem 5”."
        expected = 'Explain "Theorem 5".'
        assert normalizer.normalize(raw) == expected

    def test_normalize_invalid_type(self) -> None:
        """Test TypeError raised for non-string input."""
        normalizer = QueryNormalizer()
        with pytest.raises(TypeError):
            normalizer.normalize(123)  # type: ignore[arg-type]


class TestMathematicalEntityExtractor:
    """Test suite for MathematicalEntityExtractor."""

    def test_extract_single_entities(self) -> None:
        """Test extracting individual statement references."""
        extractor = MathematicalEntityExtractor()

        # Definition 2.1
        res1 = extractor.extract("What is Definition 2.1?")
        assert len(res1) == 1
        assert res1[0].entity_type == "definition"
        assert res1[0].identifier == "2.1"
        assert res1[0].normalized_label == "Definition 2.1"

        # Lemma 4
        res2 = extractor.extract("What is Lemma 4?")
        assert len(res2) == 1
        assert res2[0].entity_type == "lemma"
        assert res2[0].identifier == "4"
        assert res2[0].normalized_label == "Lemma 4"

        # Theorem III
        res3 = extractor.extract("Check Theorem III for details.")
        assert len(res3) == 1
        assert res3[0].entity_type == "theorem"
        assert res3[0].identifier == "III"

        # Corollary 5.3
        res4 = extractor.extract("Refer to Corollary 5.3.")
        assert len(res4) == 1
        assert res4[0].entity_type == "corollary"
        assert res4[0].identifier == "5.3"

    def test_extract_proof_of_entity(self) -> None:
        """Test extracting 'Proof of Theorem 4' decomposition."""
        extractor = MathematicalEntityExtractor()
        res = extractor.extract("Where is the Proof of Theorem 4?")
        assert len(res) == 2
        proof_ent = next(e for e in res if e.entity_type == "proof")
        target_ent = next(e for e in res if e.entity_type == "theorem")
        assert proof_ent.normalized_label == "Proof"
        assert proof_ent.identifier is None
        assert target_ent.identifier == "4"
        assert target_ent.normalized_label == "Theorem 4"
        assert target_ent.metadata.get("linked_from") == "proof"

    def test_extract_multiple_entities(self) -> None:
        """Test extracting multiple theorem references."""
        extractor = MathematicalEntityExtractor()
        res = extractor.extract("Compare theorem 2 and theorem 4.")
        assert len(res) == 2
        identifiers = {e.identifier for e in res}
        assert "2" in identifiers and "4" in identifiers


class TestMathematicalSymbolExtractor:
    """Test suite for MathematicalSymbolExtractor."""

    def test_extract_unicode_symbols(self) -> None:
        """Test extracting Greek letters and blackboard bold symbols."""
        extractor = MathematicalSymbolExtractor()
        symbols = extractor.extract("Show notation for λ, σ, ∇, and ℝ.")
        assert "λ" in symbols
        assert "σ" in symbols
        assert "∇" in symbols
        assert "ℝ" in symbols

    def test_extract_function_and_subscript_notation(self) -> None:
        """Test extracting f(x) and x_i notations."""
        extractor = MathematicalSymbolExtractor()
        symbols = extractor.extract("Evaluate f(x) where x_i is positive.")
        assert "f(x)" in symbols
        assert "x_i" in symbols

    def test_extract_latex_blocks(self) -> None:
        """Test extracting inline math blocks."""
        extractor = MathematicalSymbolExtractor()
        symbols = extractor.extract(r"Solve $e^{i\pi} + 1 = 0$.")
        assert r"$e^{i\pi} + 1 = 0$" in symbols

    def test_symbol_deduplication(self) -> None:
        """Test symbol list is unique."""
        extractor = MathematicalSymbolExtractor()
        symbols = extractor.extract("λ and λ with f(x) and f(x)")
        assert symbols.count("λ") == 1
        assert symbols.count("f(x)") == 1


class TestOperationDetector:
    """Test suite for OperationDetector."""

    def test_detect_operations(self) -> None:
        """Test operation verb detection."""
        detector = OperationDetector()
        assert "define" in detector.detect("What is Definition 2.1?")
        assert "explain" in detector.detect("Explain Theorem 5.")
        assert "summarize" in detector.detect("Summarize this paper.")
        assert "compare" in detector.detect("Compare theorem 2 and theorem 4.")
        assert "show" in detector.detect("Show notation for λ.")
        assert "find" in detector.detect("Which lemma proves theorem 3?")


class TestIntentDetector:
    """Test suite for IntentDetector."""

    def test_intent_detection_categories(self) -> None:
        """Test intent classification across required categories."""
        detector = IntentDetector()

        # Definition
        intent1, conf1 = detector.detect("What is Definition 2.1?")
        assert intent1 in (QueryIntent.DEFINITION, QueryIntent.GENERAL_QUESTION)
        assert conf1 > 0.5

        # Summary
        intent2, conf2 = detector.detect("Summarize this paper.", operations=["summarize"])
        assert intent2 == QueryIntent.SUMMARY
        assert conf2 >= 0.90

        # Comparison
        intent3, conf3 = detector.detect("Compare theorem 2 and theorem 4.", operations=["compare"])
        assert intent3 == QueryIntent.COMPARISON

        # Dependency
        intent4, conf4 = detector.detect("Which lemma proves theorem 3?")
        assert intent4 == QueryIntent.DEPENDENCY

        # Notation
        intent5, conf5 = detector.detect("Show notation for λ.")
        assert intent5 == QueryIntent.NOTATION


class TestStep1Point5Refinements:
    """Test suite for Day 5 Step 1.5 enhancements."""

    def test_multi_entity_extraction_generic_and_numbered(self) -> None:
        """Test extracting both un-numbered generic and numbered entities."""
        extractor = MathematicalEntityExtractor()

        # "Which lemma proves theorem 3?"
        res1 = extractor.extract("Which lemma proves theorem 3?")
        assert len(res1) == 2
        types = [e.entity_type for e in res1]
        assert "lemma" in types and "theorem" in types
        lemma_ent = next(e for e in res1 if e.entity_type == "lemma")
        theorem_ent = next(e for e in res1 if e.entity_type == "theorem")
        assert lemma_ent.identifier is None
        assert lemma_ent.normalized_label == "Lemma"
        assert theorem_ent.identifier == "3"
        assert theorem_ent.normalized_label == "Theorem 3"

        # "Definition 2.1 and Lemma 4"
        res2 = extractor.extract("Definition 2.1 and Lemma 4")
        assert len(res2) == 2
        labels = [e.normalized_label for e in res2]
        assert "Definition 2.1" in labels and "Lemma 4" in labels

        # "Which definition is used in theorem 2?"
        res3 = extractor.extract("Which definition is used in theorem 2?")
        assert len(res3) == 2
        def_ent = next(e for e in res3 if e.entity_type == "definition")
        assert def_ent.identifier is None
        assert def_ent.normalized_label == "Definition"

    def test_proof_decomposition_and_metadata(self) -> None:
        """Test decomposing proof references into Proof + Target entity with linked_from metadata."""
        extractor = MathematicalEntityExtractor()
        res = extractor.extract("Proof of Theorem 4")
        assert len(res) == 2
        proof_ent = next(e for e in res if e.entity_type == "proof")
        target_ent = next(e for e in res if e.entity_type == "theorem")
        assert proof_ent.identifier is None
        assert proof_ent.normalized_label == "Proof"
        assert target_ent.identifier == "4"
        assert target_ent.normalized_label == "Theorem 4"
        assert target_ent.metadata.get("linked_from") == "proof"

    def test_dependency_intent_queries(self) -> None:
        """Test dependency queries return intent=DEPENDENCY and operations containing find."""
        processor = QueryProcessor()

        q1 = processor.process("Which lemma proves theorem 3?")
        assert q1.intent == QueryIntent.DEPENDENCY
        assert "find" in q1.operations
        assert len(q1.referenced_entities) == 2

        q2 = processor.process("Which theorem depends on lemma 5?")
        assert q2.intent == QueryIntent.DEPENDENCY
        assert "find" in q2.operations
        assert len(q2.referenced_entities) == 2

        q3 = processor.process("Which definition is used in theorem 2?")
        assert q3.intent == QueryIntent.DEPENDENCY
        assert "find" in q3.operations
        assert len(q3.referenced_entities) == 2

    def test_confidence_type_attribute(self) -> None:
        """Test confidence_type is present and set to rule_based or llm."""
        processor = QueryProcessor()
        analysis = processor.process("What is Definition 2.1?")
        assert analysis.confidence_type == "rule_based"

        data = analysis.to_dict()
        assert data["confidence_type"] == "rule_based"

        reconstructed = QueryAnalysis.from_dict(data)
        assert reconstructed.confidence_type == "rule_based"

        # LLM Strategy test
        processor.set_strategy(LLMQueryStrategy())
        llm_analysis = processor.process("What is Definition 2.1?")
        assert llm_analysis.confidence_type == "llm"


class TestQueryAnalysisSerialization:
    """Test suite for QueryAnalysis data model and dictionary serialization."""

    def test_to_dict_and_from_dict(self) -> None:
        """Test roundtrip serialization of QueryAnalysis."""
        entity = ReferencedEntity(entity_type="definition", identifier="2.1", normalized_label="Definition 2.1")
        analysis = QueryAnalysis(
            original_query="What is Definition 2.1?",
            normalized_query="What is Definition 2.1?",
            intent=QueryIntent.DEFINITION,
            operations=["define"],
            referenced_entities=[entity],
            symbols=["x"],
            confidence=0.95,
            confidence_type="rule_based",
        )

        data = analysis.to_dict()
        assert data["intent"] == "definition"
        assert data["confidence_type"] == "rule_based"
        assert len(data["referenced_entities"]) == 1

        reconstructed = QueryAnalysis.from_dict(data)
        assert reconstructed.intent == QueryIntent.DEFINITION
        assert reconstructed.normalized_query == analysis.normalized_query
        assert reconstructed.referenced_entities[0].normalized_label == "Definition 2.1"
        assert reconstructed.confidence_type == "rule_based"


class TestQueryProcessorService:
    """Test suite for the primary QueryProcessor service."""

    def test_processor_integration(self) -> None:
        """Test end-to-end processing of benchmark queries."""
        processor = QueryProcessor()

        # "What is Definition 2.1?"
        res1 = processor.process("What is Definition 2.1?")
        assert res1.normalized_query == "What is Definition 2.1?"
        assert len(res1.referenced_entities) == 1
        assert res1.referenced_entities[0].normalized_label == "Definition 2.1"

        # "Theorem   3.2 ?" -> "Theorem 3.2?"
        res2 = processor.process("Theorem   3.2 ?")
        assert res2.normalized_query == "Theorem 3.2?"

    def test_batch_process(self) -> None:
        """Test batch query processing."""
        processor = QueryProcessor()
        queries = ["Explain Theorem 5.", "Summarize this paper."]
        results = processor.batch_process(queries)
        assert len(results) == 2
        assert results[0].normalized_query == "Explain Theorem 5."
        assert results[1].normalized_query == "Summarize this paper."

    def test_strategy_swapping(self) -> None:
        """Test pluggable strategy interface for future LLM replacement."""
        processor = QueryProcessor()
        assert isinstance(processor.strategy, RuleBasedQueryStrategy)

        llm_strategy = LLMQueryStrategy()
        processor.set_strategy(llm_strategy)
        assert processor.strategy == llm_strategy

        analysis = processor.process("What is Definition 2.1?")
        assert "LLMQueryStrategy" in analysis.metadata["strategy"]
        assert analysis.confidence_type == "llm"

    def test_invalid_query_type(self) -> None:
        """Test error handling for non-string query inputs."""
        processor = QueryProcessor()
        with pytest.raises(TypeError):
            processor.process(None)  # type: ignore[arg-type]
