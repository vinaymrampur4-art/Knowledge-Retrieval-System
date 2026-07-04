from fastmcp import FastMCP

mcp = FastMCP("Knowledge Retrieval System")

print(type(mcp))

print("\nPublic methods:\n")

for name in dir(mcp):
    if not name.startswith("_"):
        print(name)