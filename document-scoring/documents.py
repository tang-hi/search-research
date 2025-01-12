from utils import whitespace_tokenize
import math


class Documents:
    def __init__(self):
        self.inverted_index = {}
        self.document_frequency = {}
        self.total_documents = 0
        self.term_frequency = {}
        self.upper_bound = {}
        self.max_idf = 0
        self.calculate_times = 0

    def clean_calculate_times(self):
        self.calculate_times = 0

    def add_document(self, doc_id, doc):
        self.total_documents += 1
        self.term_frequency[doc_id] = {}
        for term in whitespace_tokenize(doc):
            term = term.lower()
            if term not in self.inverted_index:
                self.inverted_index[term] = []
                self.document_frequency[term] = 0
            self.term_frequency[doc_id][term] = self.term_frequency[doc_id].get(
                term, 0) + 1
            if (len(self.inverted_index[term]) != 0) and doc_id == self.inverted_index[term][-1]:
                continue
            self.inverted_index[term].append(doc_id)
            self.document_frequency[term] += 1

    def get_upper_bound(self, term):
        return max(self.term_frequency[doc_id][term] for doc_id in self.inverted_index[term]) * math.log(self.total_documents / self.document_frequency[term])

    def get_document_frequency(self, term):
        return self.document_frequency.get(term, 0)

    def get_term_frequency(self, doc_id, term):
        return self.term_frequency.get(doc_id, {}).get(term, 0)

    def get_posting_list(self, term):
        return self.inverted_index.get(term, [])

    def get_calculate_times(self):
        return self.calculate_times

    def get_tf_idf(self, doc_id, term):
        self.calculate_times += 1
        tf = self.get_term_frequency(doc_id, term)
        df = self.get_document_frequency(term)
        return tf * math.log(self.total_documents / df) if df else 0
