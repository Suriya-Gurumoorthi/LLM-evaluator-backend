"""LLM-as-Judge service for evaluating prompts and LLM outputs."""

import asyncio
import json
import re
import logging
from typing import Dict, List, Any, Optional, Tuple

from app.models.llm_calls import (
    gemini_1_5_flash_call,
    gemini_2_5_flash_call,
    gemini_2_5_flash_lite_call,
    mistral_call,
    deepseek_call,
    openai_gpt4_mini_call,
    openai_gpt5_mini_call,
)

logger = logging.getLogger(__name__)

MODEL_TO_FUNC = {
    "gemini_1_5_flash": gemini_1_5_flash_call,
    "gemini_2_5_flash": gemini_2_5_flash_call,
    "gemini_2_5_flash_lite": gemini_2_5_flash_lite_call,
    "mistral": mistral_call,
    "deepseek": deepseek_call,
    "openai_gpt4_mini": openai_gpt4_mini_call,
    "openai_gpt5_mini": openai_gpt5_mini_call,
}

DOMAIN_INFO = {
    "coding": {"name": "Coding", "description": "Programming and software development"},
    "reasoning": {"name": "Reasoning", "description": "Logical reasoning and problem solving"},
    "mathematics": {"name": "Mathematics", "description": "Mathematical problem solving"},
    "writing": {"name": "Writing", "description": "Creative and technical writing"},
    "analysis": {"name": "Analysis", "description": "Data analysis and interpretation"},
    "communication": {"name": "Communication", "description": "Verbal and written communication"},
}

RUBRIC_INFO = {
    "coding": "Code quality, correctness, and best practices",
    "reasoning": "Logical reasoning and problem-solving approach",
    "problem-solving": "Ability to break down and solve complex problems",
    "clarity": "Clear and understandable explanations",
    "completeness": "Thoroughness and attention to detail",
    "creativity": "Innovative and creative solutions",
    "accuracy": "Correctness of information and results",
    "efficiency": "Optimal use of resources and time",
}


class LLMJudgeService:
    """Service that implements the LLM-as-Judge evaluation pipeline."""

    # ------------------------------------------------------------------ #
    #  System prompt builder
    # ------------------------------------------------------------------ #

    def build_system_prompt(
        self,
        domain_id: str,
        rubrics: List[Dict[str, Any]],
    ) -> str:
        """Build a dynamic system prompt from the selected domain and rubrics.

        The generated prompt tells the target LLM what domain it is operating
        in and which quality dimensions matter.
        """
        domain = DOMAIN_INFO.get(domain_id, {"name": domain_id.replace("-", " ").title(), "description": ""})
        domain_name = domain["name"]
        domain_desc = domain["description"]

        rubric_lines = []
        for r in rubrics:
            desc = r.get("description") or RUBRIC_INFO.get(r.get("id", ""), r.get("name", ""))
            rubric_lines.append(f"- {r['name']}: {desc}")
        rubric_block = "\n".join(rubric_lines)

        return (
            f"You are an expert AI assistant specialized in {domain_name} ({domain_desc}).\n\n"
            f"Your responses will be evaluated on the following criteria:\n"
            f"{rubric_block}\n\n"
            f"Provide thorough, well-structured, and accurate responses that excel across "
            f"all the evaluation dimensions listed above."
        )

    # ------------------------------------------------------------------ #
    #  Generic LLM caller (wraps llm_calls.py functions)
    # ------------------------------------------------------------------ #

    async def call_llm(
        self,
        model_id: str,
        api_key: str,
        system_prompt: str,
        user_message: str,
        max_tokens: int = 4096,
        temperature: float = 0.7,
    ) -> Tuple[str, int, int]:
        """Call any supported LLM. Returns (response_text, in_tokens, out_tokens)."""
        func = MODEL_TO_FUNC.get(model_id)
        if func is None:
            raise ValueError(f"Unsupported model: {model_id}")

        formatted_messages = [{"role": "user", "content": user_message}]
        return await asyncio.to_thread(
            func, formatted_messages, system_prompt, api_key, max_tokens, temperature,
        )

    # ------------------------------------------------------------------ #
    #  Step 1 – Generate LLM output for a single test case
    # ------------------------------------------------------------------ #

    async def generate_test_case_output(
        self,
        model_id: str,
        api_key: str,
        system_prompt: str,
        user_prompt: str,
        test_case_input: str,
    ) -> Dict[str, Any]:
        """Run the target LLM with the dynamic system prompt.

        The *user_prompt* is the prompt being evaluated, and *test_case_input*
        is the concrete input for this test case.
        """
        user_message = f"{user_prompt}\n\nInput:\n{test_case_input}"
        try:
            text, in_tok, out_tok = await self.call_llm(
                model_id, api_key, system_prompt, user_message,
                max_tokens=4096, temperature=0.7,
            )
            return {
                "success": True,
                "generated_text": text,
                "input_tokens": in_tok,
                "output_tokens": out_tok,
            }
        except Exception as exc:
            logger.error("LLM generation failed: %s", exc)
            return {"success": False, "error": str(exc), "generated_text": None}

    # ------------------------------------------------------------------ #
    #  Step 2 – Judge #1: Output quality analysis
    # ------------------------------------------------------------------ #

    async def judge_output_quality(
        self,
        model_id: str,
        api_key: str,
        domain_name: str,
        user_prompt: str,
        test_cases_with_outputs: List[Dict[str, Any]],
    ) -> Dict[str, Any]:
        """Use an LLM to score the quality of generated outputs per test case."""

        tc_section = ""
        for i, tc in enumerate(test_cases_with_outputs):
            expected = tc.get("expected_output") or "N/A"
            tc_section += (
                f"\n--- Test Case {i + 1} ---\n"
                f"Input: {tc['input']}\n"
                f"Expected Output: {expected}\n"
                f"LLM Output: {tc['llm_output']}\n"
            )

        judge_system = (
            "You are an expert evaluator. Your job is to objectively assess "
            "the quality of LLM-generated outputs. Be strict but fair. "
            "Return ONLY valid JSON with no markdown fences or extra text."
        )

        judge_user = (
            f"Domain: {domain_name}\n"
            f"User Prompt (the instruction given to the LLM):\n\"\"\"\n{user_prompt}\n\"\"\"\n\n"
            f"The following test cases were executed with that prompt:\n{tc_section}\n\n"
            f"For EACH test case evaluate the LLM output on a 0-100 scale:\n"
            f"- correctness: factual accuracy and correctness\n"
            f"- relevance: how relevant the output is to the input\n"
            f"- completeness: thoroughness of the response\n"
            f"- overall_score: holistic quality\n\n"
            f"Return JSON exactly like this (no markdown, no extra keys):\n"
            f'{{\n'
            f'  "test_case_scores": [\n'
            f'    {{\n'
            f'      "test_case_index": 1,\n'
            f'      "correctness": 85,\n'
            f'      "relevance": 90,\n'
            f'      "completeness": 80,\n'
            f'      "overall_score": 85,\n'
            f'      "feedback": "..."\n'
            f'    }}\n'
            f'  ],\n'
            f'  "overall_score": 85,\n'
            f'  "overall_feedback": "..."\n'
            f'}}'
        )

        try:
            text, _, _ = await self.call_llm(
                model_id, api_key, judge_system, judge_user,
                max_tokens=4096, temperature=0.3,
            )
            parsed = self._parse_json_from_llm(text)
            if "test_case_scores" not in parsed:
                raise ValueError("Missing test_case_scores in judge response")
            return parsed
        except Exception as exc:
            logger.error("Output quality judge failed: %s", exc)
            return self._fallback_output_judge(test_cases_with_outputs, str(exc))

    # ------------------------------------------------------------------ #
    #  Step 3 – Judge #2: Prompt quality analysis
    # ------------------------------------------------------------------ #

    async def judge_prompt_quality(
        self,
        model_id: str,
        api_key: str,
        domain_name: str,
        user_prompt: str,
        rubrics: List[Dict[str, Any]],
    ) -> Dict[str, Any]:
        """Use an LLM to rate the user prompt quality against selected rubrics."""

        rubric_lines = "\n".join(
            f"- {r['name']} (weight: {r['weight']}%): "
            f"{r.get('description') or RUBRIC_INFO.get(r.get('id', ''), r['name'])}"
            for r in rubrics
        )

        rubric_json_example = ", ".join(
            f'{{"rubric_id": "{r.get("id", "")}", "rubric_name": "{r["name"]}", "score": 80, "feedback": "..."}}'
            for r in rubrics
        )

        judge_system = (
            "You are an expert prompt engineer evaluator. Your job is to "
            "objectively assess the quality of a user-written prompt. "
            "Be strict but fair. Return ONLY valid JSON with no markdown fences or extra text."
        )

        judge_user = (
            f"Domain: {domain_name}\n\n"
            f"Prompt to evaluate:\n\"\"\"\n{user_prompt}\n\"\"\"\n\n"
            f"Evaluate this prompt against these rubrics:\n{rubric_lines}\n\n"
            f"For EACH rubric, rate the prompt quality on a 0-100 scale.\n"
            f"Consider: Is the prompt well-structured? Does it clearly communicate "
            f"what is needed? Would it guide an LLM to produce quality outputs "
            f"in the {domain_name} domain?\n\n"
            f"Return JSON exactly like this (no markdown, no extra keys):\n"
            f'{{\n'
            f'  "rubric_scores": [{rubric_json_example}],\n'
            f'  "overall_score": 80,\n'
            f'  "overall_feedback": "..."\n'
            f'}}'
        )

        try:
            text, _, _ = await self.call_llm(
                model_id, api_key, judge_system, judge_user,
                max_tokens=4096, temperature=0.3,
            )
            parsed = self._parse_json_from_llm(text)
            if "rubric_scores" not in parsed:
                raise ValueError("Missing rubric_scores in judge response")
            return parsed
        except Exception as exc:
            logger.error("Prompt quality judge failed: %s", exc)
            return self._fallback_prompt_judge(rubrics, str(exc))

    # ------------------------------------------------------------------ #
    #  JSON parser (handles markdown code fences, etc.)
    # ------------------------------------------------------------------ #

    @staticmethod
    def _parse_json_from_llm(text: str) -> dict:
        text = text.strip()
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            pass

        for pattern in [
            r"```json\s*([\s\S]*?)\s*```",
            r"```\s*([\s\S]*?)\s*```",
        ]:
            match = re.search(pattern, text)
            if match:
                try:
                    return json.loads(match.group(1))
                except json.JSONDecodeError:
                    continue

        match = re.search(r"\{[\s\S]*\}", text)
        if match:
            try:
                return json.loads(match.group(0))
            except json.JSONDecodeError:
                pass

        raise ValueError(f"Could not parse JSON from LLM response: {text[:300]}")

    # ------------------------------------------------------------------ #
    #  Fallbacks when judge calls fail
    # ------------------------------------------------------------------ #

    @staticmethod
    def _fallback_output_judge(
        test_cases: List[Dict[str, Any]], error: str,
    ) -> Dict[str, Any]:
        scores = [
            {
                "test_case_index": i + 1,
                "correctness": 0,
                "relevance": 0,
                "completeness": 0,
                "overall_score": 0,
                "feedback": f"Judge evaluation failed: {error}",
            }
            for i in range(len(test_cases))
        ]
        return {
            "test_case_scores": scores,
            "overall_score": 0,
            "overall_feedback": f"Output quality judge failed: {error}",
        }

    @staticmethod
    def _fallback_prompt_judge(
        rubrics: List[Dict[str, Any]], error: str,
    ) -> Dict[str, Any]:
        rubric_scores = [
            {
                "rubric_id": r.get("id", ""),
                "rubric_name": r.get("name", ""),
                "score": 0,
                "feedback": f"Judge evaluation failed: {error}",
            }
            for r in rubrics
        ]
        return {
            "rubric_scores": rubric_scores,
            "overall_score": 0,
            "overall_feedback": f"Prompt quality judge failed: {error}",
        }


llm_judge_service = LLMJudgeService()
