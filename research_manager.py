import json

from planner_agent import planner_agent, WebSearchItem, WebSearchPlan
from writer_agent import writer_agent
from model_provider import run_with_fallback
from search_tool import search_web
from config import SEARCH_CONCURRENCY
import asyncio

class ResearchManager:

    async def run(self, query: str):
        """ Run the deep research process, yielding the status updates and the final report"""
        yield "Starting research..."
        search_plan = await self.plan_searches(query)
        yield f"Searches planned, starting {len(search_plan.searches)} searches..."
        search_results = await self.perform_searches(search_plan)
        yield "Searches complete, writing report..."
        report = await self.write_report(query, search_results)
        yield self.render_report(report, search_results)

    async def plan_searches(self, query: str) -> WebSearchPlan:
        """ Plan the searches to perform for the query """
        return await run_with_fallback(
            planner_agent,
            f"Query: {query}",
            output_type=WebSearchPlan,
        )

    async def perform_searches(self, search_plan: WebSearchPlan) -> list[str]:
        """ Perform the searches to perform for the query """
        semaphore = asyncio.Semaphore(SEARCH_CONCURRENCY)

        async def bounded_search(item: WebSearchItem) -> str:
            async with semaphore:
                return await self.search(item)

        tasks = [bounded_search(item) for item in search_plan.searches]
        return await asyncio.gather(*tasks)

    async def search(self, item: WebSearchItem) -> str:
        """ Perform a search for the query """
        raw_results = await asyncio.to_thread(search_web, item.query)
        return json.dumps(
            {
                "query": item.query,
                "reason": item.reason,
                "results": raw_results,
            },
            ensure_ascii=False,
        )

    async def write_report(self, query: str, search_results: list[str]) -> str:
        """ Write the report for the query """
        input_message = f"Original query: {query}\nCollected web results: {search_results}"
        return await run_with_fallback(writer_agent, input_message)

    @staticmethod
    def select_sources(search_results: list[str], count: int = 5) -> list[dict[str, str]]:
        """Select unique sources round-robin across the planned searches."""
        groups = [json.loads(result)["results"] for result in search_results]
        selected: list[dict[str, str]] = []
        seen_urls: set[str] = set()
        for index in range(max((len(group) for group in groups), default=0)):
            for group in groups:
                if index >= len(group):
                    continue
                source = group[index]
                url = source.get("url", "").strip()
                if not url or url in seen_urls:
                    continue
                seen_urls.add(url)
                selected.append(source)
                if len(selected) == count:
                    return selected
        raise RuntimeError(f"Only {len(selected)} unique sources were available; {count} are required.")

    @classmethod
    def render_report(cls, report: str, search_results: list[str]) -> str:
        """Append exactly five source links selected from real search results."""
        links = []
        for source in cls.select_sources(search_results):
            title = source.get("title", "Source").replace("[", "").replace("]", "").strip()
            links.append(f"- [{title}](<{source['url']}>)")
        return f"{report.rstrip()}\n\n## Sources\n\n" + "\n".join(links)
