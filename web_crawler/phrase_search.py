from web_crawler.postings_reader import read_postings


def merge_positions(pos1, pos2):
    i = j = 0
    matched = []

    while i < len(pos1) and j < len(pos2):

        if pos2[j] == pos1[i] + 1:
            matched.append(pos2[j])
            i += 1
            j += 1

        elif pos1[i] + 1 < pos2[j]:
            i += 1

        else:
            j += 1

    return matched


def phrase_search(query,index):
    words = query.split()
    if not words:
        return []

    postings = [read_postings(word, index) for word in words]

    #yup similar to how we do list initialization 
    current = {
        p.doc_id: p.positions
        for p in postings[0]
    }

    for k in range(1, len(words)):
        nxt = {
            p.doc_id: p.positions
            for p in postings[k]
        }
        new_current = {}
        for doc in current:

            if doc not in nxt:
                continue
            matched = merge_positions(current[doc], nxt[doc])
            if matched:
                new_current[doc] = matched

        current = new_current
        if not current:
            return []

    return list(current.keys())