from dataclasses import dataclass
from typing import Any

@dataclass
class EvaluationResult:
    question: str
    expected_keywords: list[str]
    answer: str
    keyword_recall: float

def keyword_recall(answer: str, expected: list[str]) -> float:
    if not expected:
        return 1.0
    text = answer.lower()
    return sum(k.lower() in text for k in expected) / len(expected)

def evaluate(items: list[dict[str, Any]], pipeline) -> list[EvaluationResult]:
    results = []
    for item in items:
        output = pipeline.answer(item["question"])
        score = keyword_recall(output["answer"], item.get("expected_keywords", []))
        results.append(EvaluationResult(
            item["question"],
            item.get("expected_keywords", []),
            output["answer"],
            score,
        ))
    return results
