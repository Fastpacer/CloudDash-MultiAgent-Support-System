from app.retrieval.retriever import retrieve_documents


query = "AWS alerts stopped firing after credential update"

results = retrieve_documents(query)

for index, result in enumerate(results, start=1):

    print(f"\nResult {index}")
    print("=" * 50)

    print(result["metadata"])

    print(result["content"][:500])