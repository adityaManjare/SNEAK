
def edit_dist(word1 , word2):
    n = len(word1) + 1
    m = len(word2) + 1
    grid = [[0 for i in range(m)]  for _ in range(n)]
    for i in range(n):
        for j in range(m):
            if(i == 0):
                grid[i][j] = j
            elif(j == 0):
                grid[i][j] = i
    for i in range(1 , n):
        for j in range(1 , m):
            if word1[i-1] == word2[j-1]:
                grid[i][j] = grid[i-1][j-1]
            else:
                grid[i][j] = min( grid[i-1][j] , grid[i][j-1] ,   grid[i-1][j-1]) + 1
    return grid[n-1][m-1]


class BKNode:
    def __init__(self, value):
        self.value = value
        self.childs = {}

    
class BKTree:
    def __init__(self):
        self.parent = None

    def insert(self, node):
        if self.parent is None:
            self.parent = BKNode(node)
        else:
            it = self.parent
            x = edit_dist(it.value , node)
            while x in it.childs:
                it = it.childs[x]
                x = edit_dist(it.value, node)
            it.childs[x] = BKNode(node) 


    def rec(self,query ,it  ,threshold , ans):
        if it is None:
            return
        x = edit_dist(query , it.value)
        if x <= threshold:
            ans.append(it.value)
        for edge, child in it.childs.items():
            if x-threshold <= edge <= x+threshold:
                self.rec(query, child, threshold, ans)
    def search(self , query , threshold):
        ans = []
        self.rec(query, self.parent, threshold, ans)

        return sorted(ans, key = lambda word : edit_dist(query,word))[:5]



# import json


# bk = BKTree()
 
# with open("index.json") as f:
#     index = json.load(f)

# for value , _ in index.items():
#     bk.insert(value)

# print(bk.search("sneha" , 3))
