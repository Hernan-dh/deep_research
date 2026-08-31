from pydantic import BaseModel, Field
from agents import Agent
from config import HOW_MANY_SEARCHES
from model_provider import PRIMARY_MODEL


INSTRUCTIONS = f"""
You are a research assistant. Given a user query, come up with a set of web searches
to perform to best answer the query. Output {HOW_MANY_SEARCHES} terms to query for.
Return only a valid JSON object with a "searches" array. Each item must contain string
fields named "reason" and "query". Do not use Markdown fences or add commentary.
"""

class WebSearchItem(BaseModel):
    reason: str = Field(description="Your reasoning for why this search is important to the query.")
    query: str = Field(description="The search term to use for the web search.")


class WebSearchPlan(BaseModel):
    searches: list[WebSearchItem] = Field(description="A list of web searches to perform to best answer the query.")
    
planner_agent = Agent(
    name="Planner Agent",
    instructions=INSTRUCTIONS,
    model=PRIMARY_MODEL,
)
