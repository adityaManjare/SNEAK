import json 

epsilon = 1e-8
d = 0.85
iterations = 30

def rankPages():
    with open("metadata.json") as f:
        metadata = json.load(f)
    N = len(metadata)
    for i in range(iterations):
        new_rank = {}

        initial_score = (1 - d)/N

        for doc_id in metadata:
            new_rank[doc_id] = initial_score

        dangling_share = 0

        for doc_id , info in metadata.items():
            links = info["outgoing_links"]
            current_rank = info["pagerank"]
            if len(links) > 0 :
                share = current_rank / len(links)
                for neighbour in links:
                    new_rank[str(neighbour)] += d * share
            else :
                dangling_share += ( current_rank / N)
        
        max_change = 0
        for doc_id in metadata:
            change = abs(metadata[doc_id]["pagerank"] -(new_rank[doc_id] + dangling_share * d))
            max_change = max(change,max_change)
            
        for doc_id in metadata:
            metadata[doc_id]["pagerank"] = new_rank[doc_id] + dangling_share * d
        
        if max_change < epsilon:
            print(f"Converged after {i + 1} iterations")
            break
    
    with open("metadata.json","w") as f:
        json.dump(metadata,f,indent=4)

    total = sum(info["pagerank"] for info in metadata.values())
    print(total)

# rankPages()
