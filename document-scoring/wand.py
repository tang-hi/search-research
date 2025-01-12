from posting_list import PostingList
from documents import Documents
import heapq
from math import inf


class WAND:
    def __init__(self, threshold_factor, documents: Documents):
        self.threshold_factor = threshold_factor
        self.threshold = 0
        self.top_k_heap = []
        self.calculate_times = 0
        self.documents = documents
        self.posting_lists = []
        self.curDoc = -1

    def get_calculate_times(self):
        return self.documents.get_calculate_times()

    def find_pivot_term(self):
        accumulated_ub = 0
        for i, posting_list in enumerate(self.posting_lists):
            if posting_list.doc_id() is None:
                continue
            accumulated_ub += self.documents.get_upper_bound(posting_list.term)
            # accumulated_ub += self.documents.get_term_frequency(
            # posting_list.doc_id(), posting_list.term)
            if accumulated_ub >= self.threshold * self.threshold_factor:
                return i
        return None

    def evaluate_document(self, doc_id, terms):
        self.calculate_times += 1
        score = 0
        for term in terms:
            if self.documents.get_term_frequency(doc_id, term) != 0:
                score += self.calculate_socre(doc_id, term)
        return score

    def calculate_socre(self, doc_id, term):
        # self.calculate_times += 1
        return self.documents.get_tf_idf(doc_id, term)

    def next(self):
        while True:
            self.posting_lists.sort(key=lambda x: x.doc_id())
            pivot_index = self.find_pivot_term()
            if pivot_index is None:
                break
            # pivot_term = self.posting_lists[pivot_index].term
            pivot_doc_id = self.posting_lists[pivot_index].doc_id()
            if pivot_doc_id <= self.curDoc:
                self.posting_lists[0].next_geq(self.curDoc + 1)
                continue
            else:
                first_doc_id = self.posting_lists[0].doc_id()
                if first_doc_id == pivot_doc_id:
                    self.curDoc = pivot_doc_id
                    return (self.curDoc, pivot_index)
                else:
                    for i in range(pivot_index):
                        self.posting_lists[i].next_geq(pivot_doc_id)
        return (inf, None)

    def process_query(self, terms, k):
        self.documents.clean_calculate_times()
        self.calculate_times = 0
        self.curDoc = -1
        posting_lists = []
        terms = [term.lower() for term in terms]
        for term in terms:
            posting_lists.append(PostingList(
                term, self.documents.get_posting_list(term)))
        self.posting_lists = posting_lists
        self.top_k_heap = []

        while True:
            doc_id, pivot_index = self.next()
            if doc_id == inf:
                break
            score = self.evaluate_document(doc_id, terms)
            self.top_k_heap.append((doc_id, score))
            self.top_k_heap.sort(key=lambda x: x[1], reverse=True)
            if len(self.top_k_heap) > k:
                self.top_k_heap.pop()
                self.threshold = self.top_k_heap[-1][1]
        return sorted(self.top_k_heap, key=lambda x: x[1], reverse=True)
