"""
Test the MCP Server services.

Run:

python -m tests.test_mcp_server
"""

from pprint import pprint

from mcp_server.models import (
    SearchRequest,
    LookupRequest,
    AttributeLookupRequest,
)

from mcp_server.services import (
    execute_search,
    execute_lookup,
    execute_attribute_lookup,
    check_index_stats,
    execute_list_repositories,
    execute_list_files,
    execute_list_classes,
    execute_list_methods,
    execute_list_branches,
    execute_complete_stats,
)

# ==========================================================
# SEARCH TEST
# ==========================================================

print("=" * 80)
print("SEARCH TEST")
print("=" * 80)

search_request = SearchRequest(
    query="APIRouter",
    top_k=3,
)

search_response = execute_search(
    search_request
)

print(f"Results : {search_response.total_results}")

for result in search_response.results:

    print("-" * 80)

    print(f"ID         : {result.id}")

    print(f"Collection : {result.collection}")

    print(f"Score      : {result.score:.4f}")

    print("Metadata")

    pprint(result.metadata)

    print()

# ==========================================================
# LOOKUP TEST
# ==========================================================

print()
print("=" * 80)
print("LOOKUP TEST")
print("=" * 80)

if search_response.results:

    first_id = search_response.results[0].id

    first_collection = search_response.results[0].collection

    lookup_request = LookupRequest(
        id=first_id,
        collection_name=first_collection,
    )

    lookup_response = execute_lookup(
        lookup_request
    )

    print(f"ID         : {lookup_response.id}")

    print(f"Collection : {lookup_response.collection}")

    print()

    print("Metadata")

    pprint(lookup_response.metadata)

else:

    print("No search results available.")

# ==========================================================
# ATTRIBUTE LOOKUP TEST
# ==========================================================

print()
print("=" * 80)
print("ATTRIBUTE LOOKUP TEST")
print("=" * 80)

attribute_request = AttributeLookupRequest(

    collection_name="Classes_Collection_v1",

    attributes={
        "class_name": "APIRouter",
    },

)

attribute_response = execute_attribute_lookup(
    attribute_request
)

print(f"Matches : {attribute_response.total_matches}")

print()

for result in attribute_response.results:

    print("-" * 80)

    print(f"ID         : {result.id}")

    print(f"Collection : {result.collection}")

    print("Metadata")

    pprint(result.metadata)

# ==========================================================
# INDEX STATISTICS TEST
# ==========================================================

print()
print("=" * 80)
print("INDEX STATISTICS TEST")
print("=" * 80)

stats = check_index_stats()

print(f"Repository          : {stats.repository}")

print(f"Files               : {stats.files}")

print(f"Classes             : {stats.classes}")

print(f"Methods             : {stats.methods}")

print(f"Functions           : {stats.functions}")

print(f"Code Blocks         : {stats.code_blocks}")

print()

print(f"Total Documents     : {stats.total_documents}")

print()

print(f"Embedding Model     : {stats.embedding_model}")

print(f"Embedding Dimension : {stats.embedding_dimension}")

print()

print(f"BM25 Ready          : {stats.bm25_ready}")

print(f"Chroma Ready        : {stats.chroma_ready}")

print()

print("=" * 80)
print("ALL TESTS FINISHED")
print("=" * 80)

# ==========================================================
# REPOSITORY REPORT TEST
# ==========================================================

print()
print("=" * 80)
print("REPOSITORY REPORT TEST")
print("=" * 80)

repository_report = execute_list_repositories()

print(f"Repositories : {repository_report.total_repositories}")

print()

for repository in repository_report.repositories:

    print(f"Repository : {repository.repository_name}")

    print(f"Branch     : {repository.branch}")

    print()

# ==========================================================
# FILE REPORT TEST
# ==========================================================

print()
print("=" * 80)
print("FILE REPORT TEST")
print("=" * 80)

file_report = execute_list_files()

print(f"Files : {file_report.total_files}")

print()

for file in file_report.files:

    print(f"{file.file_path} ({file.language})")

# ==========================================================
# CLASS REPORT TEST
# ==========================================================

print()
print("=" * 80)
print("CLASS REPORT TEST")
print("=" * 80)

class_report = execute_list_classes()

print(f"Classes : {class_report.total_classes}")

print()

for cls in class_report.classes:

    print(f"Class        : {cls.class_name}")

    print(f"File         : {cls.file_path}")

    print(f"Methods      : {cls.method_count}")

    print(f"Inheritance  : {cls.inheritance}")

    print()

# ==========================================================
# METHOD REPORT TEST
# ==========================================================

print()
print("=" * 80)
print("METHOD REPORT TEST")
print("=" * 80)

method_report = execute_list_methods()

print(f"Methods : {method_report.total_methods}")

print()

for method in method_report.methods:

    print(f"Method : {method.method_name}")

    print(f"Class  : {method.class_name}")

    print(f"File   : {method.file_path}")

    print(f"Async  : {method.is_async}")

    print()

# ==========================================================
# BRANCH REPORT TEST
# ==========================================================

print()
print("=" * 80)
print("BRANCH REPORT TEST")
print("=" * 80)

branch_report = execute_list_branches()

print(f"Branches : {branch_report.total_branches}")

print()

for branch in branch_report.branches:

    print(f"Repository : {branch.repository_name}")

    print(f"Branch     : {branch.branch}")

    print(f"Files      : {branch.files}")

    print(f"Classes    : {branch.classes}")

    print(f"Methods    : {branch.methods}")

    print(f"Functions  : {branch.functions}")

    print()

# ==========================================================
# COMPLETE REPORT TEST
# ==========================================================

print()
print("=" * 80)
print("COMPLETE REPORT TEST")
print("=" * 80)

dashboard = execute_complete_stats()

print(f"Repository          : {dashboard.repository}")

print(f"Branch              : {dashboard.branch}")

print()

print(f"Files               : {dashboard.files}")

print(f"Classes             : {dashboard.classes}")

print(f"Methods             : {dashboard.methods}")

print(f"Functions           : {dashboard.functions}")

print(f"Code Blocks         : {dashboard.code_blocks}")

print()

print(f"Total Documents     : {dashboard.total_documents}")

print()

print(f"Embedding Model     : {dashboard.embedding_model}")

print(f"Embedding Dimension : {dashboard.embedding_dimension}")

print()

print(f"BM25 Ready          : {dashboard.bm25_ready}")

print(f"Chroma Ready        : {dashboard.chroma_ready}")

print()

print("Collections")

for collection in dashboard.collections:

    print(f"  - {collection}")