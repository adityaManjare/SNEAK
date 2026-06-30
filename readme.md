# 🔎 SNEAK - The Lightweight Search Engine

SNEAK is a lightweight search engine built from scratch in Python that demonstrates the core components of modern Information Retrieval systems. It includes a web crawler, positional inverted indexing, Boolean and phrase search, TF-IDF ranking, PageRank, binary index serialization, and an LRU query cache.

The project was built to understand how real search engines work internally—from crawling webpages to efficiently retrieving ranked search results.

---

## ✨ Features

- 🌐 BFS-based Web Crawler
- 📄 HTML Parsing & Text Extraction
- 🔤 Tokenization & Text Normalization
- 🚫 Stop-word Removal
- 🌱 Porter Stemming
- 📚 Positional Inverted Index
- 🔍 Boolean Search (AND / OR / NOT)
- 💬 Phrase Search
- 📈 TF-IDF Ranking
- 🌍 PageRank-based Ranking
- ⚡ LRU Query Cache
- 💾 Binary Posting List Serialization
- 📊 Benchmark Suite

---

# Architecture

```
                      Seed URL
                          │
                          ▼
                   BFS Web Crawler
                          │
                          ▼
                HTML Parsing & Cleaning
                          │
                          ▼
                    Text Preprocessing
      (Tokenization • Stop-word Removal • Stemming)
                          │
                          ▼
                Positional Inverted Index
                          │
         ┌────────────────┴────────────────┐
         │                                 │
         ▼                                 ▼
   postings.bin                     metadata.json
         │                                 │
         └────────────────┬────────────────┘
                          │
                          ▼
                    Search Engine Core
                          │
                   Query Type Detection
                          │
        ┌─────────────────┼─────────────────┐
        │                 │                 │
        ▼                 ▼                 ▼
 Boolean Search     Phrase Search    Free-text Search
        │                 │                 │
        └─────────────────┼─────────────────┘
                          │
                          ▼
               Candidate Document Set
                          │
                          ▼
               TF-IDF + PageRank Ranking
                          │
                          ▼
                     LRU Query Cache
                          │
                          ▼
                    Ranked Search Results
```

---

# Tech Stack

- Python
- FastAPI
- SQLite
- BeautifulSoup
- SQLAlchemy

---

# Search Pipeline

```
Crawler
      ↓
HTML Parsing
      ↓
Text Cleaning
      ↓
Tokenization
      ↓
Stop-word Removal
      ↓
Porter Stemming
      ↓
Positional Inverted Index
      ↓
Binary Serialization
      ↓
Boolean / Phrase Search
      ↓
TF-IDF + PageRank Ranking
      ↓
LRU Cache
      ↓
Results
```

---

# Dataset

| Metric | Value |
|---------|------:|
| Dataset | BooksToScrape |
| Crawl Strategy | Breadth First Search |
| Crawl Depth | 5 |
| Indexed Documents | **924** |
| Vocabulary Size | **11,775** |

---

# Ranking Strategy

Final ranking score combines lexical relevance with link authority.

```
Final Score =
0.8 × TF-IDF
+
0.2 × PageRank
```

| Parameter | Value |
|-----------|------:|
| TF-IDF Weight | 0.8 |
| PageRank Weight | 0.2 |
| Damping Factor | 0.85 |
| Iterations | 30 |

---

# Storage Benchmark

Binary serialization dramatically reduces index size.

| Format | Size |
|---------|------:|
| JSON | **33.12 MB** |
| Binary | **2.93 MB** |

### Storage Reduction

**91.15% smaller than JSON**

---

# Search Performance

Benchmarked over **33 unique search queries** with **100 executions per query**.

| Metric | Time |
|--------|------:|
| Average Cold Search | **1.145 ms** |
| Average Warm Search | **0.395 ms** |
| Fastest Search | **0.002 ms** |
| Slowest Search | **4.604 ms** |

---

# Cache Performance

| Metric | Value |
|---------|------:|
| Cache Hits | **2376** |
| Cache Misses | **924** |
| Cache Hit Rate | **72%** |
| Cache Evictions | **0** |

---

# Project Structure

```
SNEAK/
│
├── sneak/
│   ├── spider.py
│   ├── index_builder.py
│   ├── search_engine.py
│   ├── ranking.py
│   ├── bool_search.py
│   ├── phrase_search.py
│   ├── pagerank.py
│   └── cache.py
│
├── postings.bin
├── metadata.json
├── index.json
├── app.db
├── benchmark.py
├── main.py
└── README.md
```

---

# API Endpoints

### Crawl Website

```
POST /dev/crawler
```

---

### Search

```
GET /search?query=<query>
```

---

### Cache Statistics

```
GET /cache/stats
```

---

### Benchmark

```
GET /benchmark?query=<query>
```

---

# Future Improvements

- Edit Distance based Query Correction
- BK-Tree for Approximate Matching
- Auto-complete Suggestions
- Wildcard Queries
- BM25 Ranking
- Index Compression (Variable Byte / Delta Encoding)
- Snippet Generation
- Incremental Index Updates
- Multi-threaded Crawling

---

# Highlights

- Built an end-to-end search engine from scratch.
- Implemented a positional inverted index supporting Boolean and phrase queries.
- Combined TF-IDF with PageRank for ranked retrieval.
- Reduced index storage by **91%** through binary serialization.
- Achieved **sub-millisecond warm query latency** using an LRU cache.
- Indexed **924 webpages** with a vocabulary of **11,775 unique terms**.

---

## Example Query

```
GET /search?query="mystery AND history"
```

Returns ranked documents ordered using the combined TF-IDF + PageRank score.

---

## License

This project is intended for educational and learning purposes.