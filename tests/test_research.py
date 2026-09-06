import json
import os
import unittest
from unittest.mock import AsyncMock, patch

with patch("dotenv.load_dotenv", return_value=False):
    from research_manager import ResearchManager
    from model_provider import parse_structured_output, StructuredOutputError
    from planner_agent import WebSearchPlan
    import search_tool


def source_group(*urls):
    return json.dumps({"results": [{"url": url, "title": "Source"} for url in urls]})


class ResearchTests(unittest.TestCase):
    def test_sources_are_unique_and_distributed_across_searches(self):
        groups = [source_group("https://example.com/a", "https://example.com/b", "https://example.com/c"),
                  source_group("https://example.com/a", "https://example.com/d", "https://example.com/e")]
        selected = ResearchManager.select_sources(groups)
        self.assertEqual([s["url"] for s in selected], [
            "https://example.com/a", "https://example.com/b", "https://example.com/d",
            "https://example.com/c", "https://example.com/e"])
        report = ResearchManager.render_report("Report", groups)
        self.assertEqual(report.count("- [Source]"), 5)

    def test_insufficient_sources_fail_instead_of_inventing_links(self):
        with self.assertRaisesRegex(RuntimeError, "unique sources"):
            ResearchManager.select_sources([source_group("https://example.com/a")])

    def test_invalid_planner_output_is_rejected(self):
        for invalid in ["not json", "{}", None]:
            with self.subTest(invalid=invalid), self.assertRaises(StructuredOutputError):
                parse_structured_output(invalid, WebSearchPlan)

    def test_fenced_planner_output_is_validated(self):
        plan = parse_structured_output(
            '```json\n{"searches": [{"reason": "Background", "query": "example"}]}\n```',
            WebSearchPlan,
        )
        self.assertEqual(plan.searches[0].query, "example")

    def test_search_provider_failures_use_ddgs(self):
        expected = [{"url": "https://example.com", "title": "Example", "snippet": "Text"}]
        with patch.object(search_tool, "_search_serper", side_effect=RuntimeError("unavailable")), patch.object(
            search_tool, "_search_google", side_effect=RuntimeError("unavailable")
        ), patch.object(search_tool, "_search_ddgs", return_value=expected) as fallback:
            self.assertEqual(search_tool.search_web("test"), expected)
        fallback.assert_called_once_with("test")


class StreamingTests(unittest.IsolatedAsyncioTestCase):
    async def test_initial_status_precedes_model_work(self):
        manager = ResearchManager()
        with patch.object(manager, "plan_searches", new_callable=AsyncMock) as planner:
            stream = manager.run("Example")
            self.assertIn("Starting", await anext(stream))
            planner.assert_not_awaited()
            await stream.aclose()


if __name__ == "__main__":
    unittest.main()
