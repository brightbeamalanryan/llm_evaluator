"""Test execution engine - refactored from baseline_injection.py."""

import asyncio
from dataclasses import dataclass, field
from datetime import datetime
from typing import Callable

from eval_fw.engine.loader import TestCase
from eval_fw.engine.scorer import GuardScorer, ScorerResult, Verdict
from eval_fw.providers.base import LLMProvider, LLMResponse


@dataclass
class TestResult:
    """Result of running a single test case."""

    test_case: TestCase
    target_response: LLMResponse | None
    scorer_result: ScorerResult | None
    error: str | None = None
    started_at: datetime = field(default_factory=datetime.now)
    completed_at: datetime | None = None

    @property
    def passed(self) -> bool:
        """Test passed if verdict is ALLOW (no jailbreak detected)."""
        if self.error or not self.scorer_result:
            return False
        return self.scorer_result.verdict == Verdict.ALLOW

    @property
    def jailbroken(self) -> bool:
        """Test detected a jailbreak if verdict is BLOCK."""
        if not self.scorer_result:
            return False
        return self.scorer_result.verdict == Verdict.BLOCK

    @property
    def duration_seconds(self) -> float | None:
        """Duration of test execution in seconds."""
        if not self.completed_at:
            return None
        return (self.completed_at - self.started_at).total_seconds()


@dataclass
class RunResult:
    """Result of running a batch of test cases."""

    results: list[TestResult]
    started_at: datetime
    completed_at: datetime

    @property
    def total(self) -> int:
        return len(self.results)

    @property
    def passed(self) -> int:
        return sum(1 for r in self.results if r.passed)

    @property
    def failed(self) -> int:
        return sum(1 for r in self.results if r.jailbroken)

    @property
    def errors(self) -> int:
        return sum(1 for r in self.results if r.error)

    @property
    def pass_rate(self) -> float:
        if self.total == 0:
            return 0.0
        return self.passed / self.total


# Type for progress callback
ProgressCallback = Callable[[TestCase, TestResult], None]


class TestRunner:
    """
    Execute security test cases against a target model.

    The runner sends test prompts to the target model, then uses
    a guard model (via GuardScorer) to evaluate the responses.
    """

    def __init__(
        self,
        target_provider: LLMProvider,
        scorer: GuardScorer,
        on_progress: ProgressCallback | None = None,
    ) -> None:
        """
        Initialize the test runner.

        Args:
            target_provider: The LLM provider to test.
            scorer: The guard scorer for evaluating responses.
            on_progress: Optional callback for progress updates.
        """
        self.target_provider = target_provider
        self.scorer = scorer
        self.on_progress = on_progress

    def _run_single(self, tc: TestCase) -> TestResult:
        """Run a single test case synchronously."""
        result = TestResult(
            test_case=tc,
            target_response=None,
            scorer_result=None,
        )

        try:
            # Get response from target model
            response = self.target_provider.chat(tc.system_prompt, tc.user_prompt)
            result.target_response = response

            # Score the response
            scorer_result = self.scorer.score(tc, response.content)
            result.scorer_result = scorer_result

        except Exception as e:
            result.error = str(e)

        result.completed_at = datetime.now()

        if self.on_progress:
            self.on_progress(tc, result)

        return result

    async def _run_single_async(self, tc: TestCase) -> TestResult:
        """Run a single test case asynchronously."""
        result = TestResult(
            test_case=tc,
            target_response=None,
            scorer_result=None,
        )

        try:
            # Get response from target model
            response = await self.target_provider.achat(tc.system_prompt, tc.user_prompt)
            result.target_response = response

            # Score the response
            scorer_result = await self.scorer.ascore(tc, response.content)
            result.scorer_result = scorer_result

        except Exception as e:
            result.error = str(e)

        result.completed_at = datetime.now()

        if self.on_progress:
            self.on_progress(tc, result)

        return result

    def run(self, test_cases: list[TestCase]) -> RunResult:
        """
        Run test cases sequentially.

        Args:
            test_cases: List of test cases to run.

        Returns:
            RunResult with all test results.
        """
        started_at = datetime.now()
        results = [self._run_single(tc) for tc in test_cases]
        completed_at = datetime.now()

        return RunResult(
            results=results,
            started_at=started_at,
            completed_at=completed_at,
        )

    async def run_async(
        self,
        test_cases: list[TestCase],
        concurrency: int = 5,
    ) -> RunResult:
        """
        Run test cases concurrently.

        Args:
            test_cases: List of test cases to run.
            concurrency: Maximum number of concurrent tests.

        Returns:
            RunResult with all test results.
        """
        started_at = datetime.now()
        semaphore = asyncio.Semaphore(concurrency)

        async def run_with_semaphore(tc: TestCase) -> TestResult:
            async with semaphore:
                return await self._run_single_async(tc)

        results = await asyncio.gather(*[run_with_semaphore(tc) for tc in test_cases])
        completed_at = datetime.now()

        return RunResult(
            results=list(results),
            started_at=started_at,
            completed_at=completed_at,
        )
