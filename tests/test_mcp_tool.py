from mcp_server.models import SearchRequest
from mcp_server.tools import search_via_query

request = SearchRequest(
    query="What is APIRouter?",
    collection_name="methods",
    top_k=5,
)

response = search_via_query(request)

print(response.model_dump_json(indent=4))