"""Service for running the full LLM-as-Judge evaluation pipeline.

Flow:
  1. Build a dynamic system prompt from the selected domain + rubrics.
  2. For each test case, call the target LLM (with the system prompt)
     to generate an output.
  3. Call Judge LLM #1 – analyse every test-case output and score it.
  4. Call Judge LLM #2 – analyse the user prompt quality against rubrics.
  5. Return all results.
"""

import logging
from typing import List, Dict, Any

from app.schemas.prompt_management import (
    PromptEvaluationRequest,
    OutputJudgeResult,
    OutputJudgeTestCaseScore,
    PromptJudgeResult,
    PromptJudgeRubricScore,
)
from app.services.llm_judge_service import llm_judge_service, DOMAIN_INFO
from app.services.similarity_comparator import similarity_comparator

logger = logging.getLogger(__name__)


class EvaluationService:
    """Orchestrates the complete evaluation pipeline."""

    async def run_evaluation(
        self,
        evaluation_request: PromptEvaluationRequest,
    ) -> Dict[str, Any]:
        model_id = (evaluation_request.llm_model or "").strip()
        api_key = evaluation_request.api_key
        domain_id = evaluation_request.domain_id

        rubrics_dicts = [
            {
                "id": r.id,
                "name": r.name,
                "weight": r.weight,
                "description": r.description or "",
            }
            for r in evaluation_request.rubrics
        ]

        domain_info = DOMAIN_INFO.get(
            domain_id,
            {"name": domain_id.replace("-", " ").title(), "description": ""},
        )
        domain_name = domain_info["name"]

        # ── Step 1: build dynamic system prompt ──────────────────────────
        system_prompt = llm_judge_service.build_system_prompt(domain_id, rubrics_dicts)
        logger.info("System prompt built for domain=%s", domain_id)

        # ── Step 2: generate LLM output for each test case ──────────────
        test_case_results: List[Dict[str, Any]] = []
        test_cases_for_judge: List[Dict[str, Any]] = []
        similarity_scores: List[float] = []

        for idx, tc in enumerate(evaluation_request.test_cases):
            gen = await llm_judge_service.generate_test_case_output(
                model_id, api_key, system_prompt,
                evaluation_request.prompt, tc.input,
            )

            result: Dict[str, Any] = {
                "test_case_id": tc.id,
                "test_case_index": idx + 1,
                "input": tc.input,
                "expected_output": tc.expectedOutput,
                "has_expected_output": bool(tc.expectedOutput and tc.expectedOutput.strip()),
                "generated_output": gen.get("generated_text"),
                "generation_success": gen["success"],
                "success": gen["success"],
                "error": gen.get("error"),
                "similarity_score": None,
                "is_match": None,
                "comparison_result": None,
            }

            if gen["success"] and result["has_expected_output"]:
                try:
                    comp = similarity_comparator.compare_with_threshold(
                        text1=gen["generated_text"],
                        text2=tc.expectedOutput,
                        threshold=0.7,
                    )
                    result["similarity_score"] = comp["similarity_score"]
                    result["is_match"] = comp["is_match"]
                    result["comparison_result"] = comp
                    similarity_scores.append(comp["similarity_score"])
                except Exception as exc:
                    logger.warning("Similarity comparison failed: %s", exc)

            test_case_results.append(result)

            if gen["success"]:
                test_cases_for_judge.append({
                    "input": tc.input,
                    "expected_output": tc.expectedOutput or "",
                    "llm_output": gen["generated_text"],
                })

        # ── Step 3: Judge #1 – output quality ────────────────────────────
        output_judge_raw: Dict[str, Any] = {"test_case_scores": [], "overall_score": 0, "overall_feedback": ""}
        if test_cases_for_judge:
            output_judge_raw = await llm_judge_service.judge_output_quality(
                model_id, api_key, domain_name,
                evaluation_request.prompt,
                test_cases_for_judge,
            )

        # ── Step 4: Judge #2 – prompt quality ────────────────────────────
        prompt_judge_raw = await llm_judge_service.judge_prompt_quality(
            model_id, api_key, domain_name,
            evaluation_request.prompt,
            rubrics_dicts,
        )

        # ── Build typed judge results ────────────────────────────────────
        output_judge = OutputJudgeResult(
            test_case_scores=[
                OutputJudgeTestCaseScore(**s)
                for s in output_judge_raw.get("test_case_scores", [])
            ],
            overall_score=output_judge_raw.get("overall_score", 0),
            overall_feedback=output_judge_raw.get("overall_feedback", ""),
        )

        prompt_judge = PromptJudgeResult(
            rubric_scores=[
                PromptJudgeRubricScore(**s)
                for s in prompt_judge_raw.get("rubric_scores", [])
            ],
            overall_score=prompt_judge_raw.get("overall_score", 0),
            overall_feedback=prompt_judge_raw.get("overall_feedback", ""),
        )

        # ── Aggregate metrics ────────────────────────────────────────────
        overall_metrics = self._calculate_overall_metrics(
            test_case_results, similarity_scores,
        )

        return {
            "evaluation_id": None,
            "prompt": evaluation_request.prompt,
            "model_used": model_id,
            "total_test_cases": len(evaluation_request.test_cases),
            "successful_generations": sum(
                1 for r in test_case_results if r.get("generation_success")
            ),
            "test_case_results": test_case_results,
            "overall_metrics": overall_metrics,
            "rubrics": rubrics_dicts,
            "domain_id": domain_id,
            "output_judge_result": output_judge.model_dump(),
            "prompt_judge_result": prompt_judge.model_dump(),
        }

    # ------------------------------------------------------------------ #

    @staticmethod
    def _calculate_overall_metrics(
        test_case_results: List[Dict[str, Any]],
        similarity_scores: List[float],
    ) -> Dict[str, Any]:
        total = len(test_case_results)
        successes = sum(1 for r in test_case_results if r.get("generation_success"))
        failures = total - successes

        metrics: Dict[str, Any] = {
            "total_test_cases": total,
            "successful_generations": successes,
            "failed_generations": failures,
            "test_cases_with_expected_output": sum(
                1 for r in test_case_results if r.get("has_expected_output")
            ),
            "test_cases_without_expected_output": sum(
                1 for r in test_case_results if not r.get("has_expected_output")
            ),
        }

        if similarity_scores:
            metrics.update({
                "average_similarity_score": sum(similarity_scores) / len(similarity_scores),
                "min_similarity_score": min(similarity_scores),
                "max_similarity_score": max(similarity_scores),
                "matches_above_threshold": sum(
                    1 for r in test_case_results if r.get("is_match") is True
                ),
                "matches_below_threshold": sum(
                    1 for r in test_case_results if r.get("is_match") is False
                ),
            })
        else:
            metrics.update({
                "average_similarity_score": None,
                "min_similarity_score": None,
                "max_similarity_score": None,
                "matches_above_threshold": 0,
                "matches_below_threshold": 0,
            })

        metrics["generation_success_rate"] = (
            (successes / total * 100) if total else 0.0
        )
        return metrics


evaluation_service = EvaluationService()
