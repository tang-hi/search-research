from wand import WAND
from documents import Documents
from naive import Naive
import time

if __name__ == "__main__":
    documents = Documents()
    with open("/home/hayes/projects/search_research/document-scoring/movie.txt") as f:
        for i, line in enumerate(f):
            documents.add_document(i, line)
    wand = WAND(1.0, documents)
    start = time.time()
    result = wand.process_query(["Girl",  "Love", "Man", "of"], 2)
    print(f"Time: {time.time() - start}")
    result.sort(key=lambda x: (-x[1], x[0]))
    print(f"Calculate times: {wand.get_calculate_times()}")
    print(f"Result: {result}")

    naive = Naive(documents)
    start = time.time()
    result = naive.process_query(["Girl", "Love", "Man", "of"], 2)
    print(f"Time: {time.time() - start}")
    result.sort(key=lambda x: (-x[1], x[0]) )
    print(f"Calculate times: {naive.get_calculate_times()}")
    print(f"Result: {result}")
