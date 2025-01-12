from math import inf
from posting_list import PostingList


class Naive:
    def __init__(self, documents):
        self.documents = documents
        self.calculate_times = 0

    def get_calculate_times(self):
        return self.calculate_times

    def process_query(self, terms, k):
        """
        Or query processing
        """
        scores = {}
        posting_lists = []
        self.calculate_times = 0
        terms = [term.lower() for term in terms]
        for term in terms:
            posting_lists.append(PostingList(
                term, self.documents.get_posting_list(term)))
        while True:
            posting_lists.sort(key=lambda x: x.doc_id())
            min_doc_id = posting_lists[0].doc_id()
            if min_doc_id == inf:
                break
            scores[min_doc_id] = 0
            self.calculate_times += 1
            for pl in posting_lists:
                if pl.doc_id() == min_doc_id:
                    scores[min_doc_id] += self.documents.get_tf_idf(
                        min_doc_id, pl.term)
                    pl.next_geq(min_doc_id + 1)

        return sorted(scores.items(), key=lambda x: x[1], reverse=True)[:k]
