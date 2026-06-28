from web_crawler.postings_reader import read_postings


def bool_and(a ,b ): # here i a and b are lists 
    ans = []
    i = j = 0
    while i < len(a) and j < len(b):
        if a[i] == b[j]:
            ans.append(a[i])
            i += 1 
            j += 1
        elif a[i] < b[j]:
            i += 1
        else:
            j += 1
    return ans

def bool_or(a,b):
    ans = []
    i = j = 0
    while i < len(a) and j < len(b):
        if a[i] == b[j]:
            ans.append(a[i])
            i += 1 
            j += 1
        elif a[i] < b[j]:
            ans.append(a[i])
            i += 1
        else:
            ans.append(b[j])
            j += 1
    while i < len(a) :
        ans.append(a[i])
        i += 1
    while j < len(b) :
        ans.append(b[j])
        j += 1
    return ans


def bool_not(a , b):
    ans = []
    i = j = 0
    while i < len(a) and j < len(b):
        if a[i] == b[j]:
            i += 1 
            j += 1
        elif a[i] < b[j]:
            ans.append(a[i])
            i += 1
        else:
            j += 1
    while i < len(a) :
        ans.append(a[i])
        i += 1
    return ans




def bool_search(query:str, index):
    tokens = query.split()
    if not tokens:
        return []
    precedence = {
        "NOT" : 2,
        "AND" : 1,
        "OR" : 0
    }
    oprtr = []
    oprnd = []
    for token in tokens:
        if token in precedence :
            while oprtr and precedence[oprtr[-1]] >= precedence[token]:
                b = oprnd.pop()
                a = oprnd.pop() 
                op = oprtr.pop()
                if op == "AND":
                    c = bool_and(a,b)
                elif op == "OR":
                    c = bool_or(a,b)
                else:
                    c = bool_not(a,b)
                oprnd.append(c)
            oprtr.append(token)
        else:
            a = [x.doc_id for x in read_postings(token,index)]
            oprnd.append(a)
    while oprtr:
        b = oprnd.pop()
        a = oprnd.pop()
        op = oprtr.pop()
        if op == "AND":
            c = bool_and(a,b)
        elif op == "OR":
            c = bool_or(a,b)
        else:
            c = bool_not(a,b)
        oprnd.append(c)
    return oprnd.pop()

