from math import inf


class PostingList:
    def __init__(self, term, postings):
        self.term = term
        self.postings = postings
        self.current_index = 0

    def doc_id(self):
        if self.current_index < len(self.postings):
            return self.postings[self.current_index]
        return inf

    def term(self):
        return self.term

    def next_geq(self, doc_id):
        while self.current_index < len(self.postings) and self.postings[self.current_index] < doc_id:
            self.current_index += 1
        if self.current_index < len(self.postings):
            return self.postings[self.current_index]
        else:
            return None
