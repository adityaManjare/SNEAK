# todo 

# history of all our query 

class trie_node:
    def __init__(self):
        self.children = {}
        self.top_k = []

class autocomplete:
    def __init__(self,k):
        self.root = None
        self.k = k
    def insert(self,query,query_history):
        if self.root is None:
            self.root = trie_node()
        query = query.strip()
        it = self.root
        for c in query:
            # if len(it.top_k) == self.k  and query_history[it.top_k[-1]] < query_history[query] and query not in it.top_k:
            #     it.top_k.append(query)
            #     it.top_k = sorted(it.top_k , key = lambda item : -query_history[item])[:self.k]
            # elif query not in it.top_k:
            #     it.top_k.append(query)
            #     it.top_k = sorted(it.top_k , key = lambda item : -query_history[item])
            if query not in it.top_k:
                it.top_k.append(query)
            it.top_k = sorted(it.top_k , key = lambda item : -query_history[item])[:min(self.k , len(it.top_k))]
            if c in it.children:
                it = it.children[c]
            else:
                it.children[c] = trie_node()
                it = it.children[c]
        # if len(it.top_k) == self.k  and query_history[it.top_k[-1]] < query_history[query] and query not in it.top_k:
        #     it.top_k.append(query)
        #     it.top_k = sorted(it.top_k , key = lambda item : -query_history[item])[:self.k]
        # elif query not in it.top_k:
        #     it.top_k.append(query)
        #     it.top_k = sorted(it.top_k , key = lambda item : -query_history[item])
        if query not in it.top_k:
            it.top_k.append(query)
        it.top_k = sorted(it.top_k , key = lambda item : -query_history[item])[:min(self.k , len(it.top_k))]

    def search(self,query):
        if self.root is None:
            return []
        query = query.strip()
        it = self.root
        ans = []
        vis = set()
        flag = False
        for c in query:
            if c in it.children:
                for word in it.top_k:
                    if word not in vis:
                        vis.add(word)
                        ans.append(word)
                it = it.children[c]
            else:
                flag = True
                break
        if not flag or len(it.top_k) >= self.k:
            return it.top_k
        else:
            fin = []
            for word in it.top_k :
                fin.append(word)
            for word in reversed(ans):
                if len(fin) == self.k:
                    return fin
                if word not in fin:
                    fin.append(word)
            return fin
