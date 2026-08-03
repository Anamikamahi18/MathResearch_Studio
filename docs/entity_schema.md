# Mathematical Entity Schema Specification

## 1. Overview

This document specifies the data model and schema for mathematical entities extracted by the `EntityExtractor` layer in MathResearch Studio (`src/graph/entity_extraction/models.py`).

Entities represent discrete, structured mathematical blocks extracted from scientific papers and are returned as strongly-typed Python dataclass objects (`ExtractedEntity`).

---

## 2. ExtractedEntity Data Fields

| Field Name | Type | Required | Description | Example |
| :--- | :--- | :---: | :--- | :--- |
| `entity_id` | `str` | Yes | Unique deterministic identifier formatted as `{paper_id}_{entity_type}_{raw_id}` | `"paper_001_theorem_thm_001"` |
| `entity_type` | `EntityType` \| `str` | Yes | Enum category (`definition`, `theorem`, `lemma`, `corollary`, `proof`, `example`, `remark`) | `EntityType.THEOREM` |
| `title` | `str` | Yes | Canonical statement title or label | `"Theorem 3.2"` |
| `text` | `str` | Yes | Complete text body of the statement or block | `"Every planar graph is 5-colorable."` |
| `source_paper` | `str` | Yes | Title or file name of source research paper | `"On Planar Graphs"` |
| `section_id` | `str` | Yes | Parent section identifier | `"s2"` |
| `section_title` | `str` | No | Parent section heading | `"2. Main Results"` |
| `page_start` | `int` | Yes | 1-indexed starting page number | `2` |
| `page_end` | `int` | Yes | 1-indexed ending page number | `3` |
| `symbols` | `list[str]` | No | List of extracted LaTeX mathematical symbols | `["\\chi(G)", "V", "E"]` |
| `references` | `list[str]` | No | List of citation markers referenced in text | `["[1]", "[Appel 1977]"]` |
| `dependencies` | `list[str]` | No | List of statement IDs this entity depends on | `["paper_001_lemma_lem_001"]` |

---

## 3. EntityType Enum Categories

```python
class EntityType(str, Enum):
    DEFINITION = "definition"
    THEOREM = "theorem"
    LEMMA = "lemma"
    COROLLARY = "corollary"
    PROOF = "proof"
    EXAMPLE = "example"
    REMARK = "remark"
```

---

## 4. Python Class Definition & Methods

```python
@dataclass
class ExtractedEntity:
    entity_id: str
    entity_type: EntityType | str
    title: str
    text: str
    source_paper: str
    section_id: str = ""
    section_title: str = ""
    page_start: int = 1
    page_end: int = 1
    symbols: list[str] = field(default_factory=list)
    references: list[str] = field(default_factory=list)
    dependencies: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        """Convert entity object to dictionary format."""
        # ...
```
