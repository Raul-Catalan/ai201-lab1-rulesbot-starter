# Spec: `retrieve()`

**File:** `retriever.py`
**Status:** Spec incomplete — fill in all blank fields before implementing

---

## Purpose

Given a user's natural language query, find the most relevant chunks from the vector store using semantic similarity search. Return them ranked by relevance so that `generate_response()` can use them as context.

---

## Input / Output Contract

**Inputs:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `query` | `str` | The user's natural language question |
| `n_results` | `int` | Maximum number of chunks to return (default: `N_RESULTS` from `config.py`) |

**Output:** `list[dict]`

Each dict in the returned list must contain exactly these keys:

| Key | Type | Description |
|-----|------|-------------|
| `"text"` | `str` | The chunk text |
| `"game"` | `str` | The game name this chunk came from |
| `"distance"` | `float` | Cosine distance score — lower means more similar to the query |

Results should be ordered from most to least relevant (lowest to highest distance). Returns an empty list `[]` if the collection contains no documents.

---

## Design Decisions

*Complete the fields below before writing any code. Use your AI tool in Plan or Ask mode to help you reason through what belongs here — but the decisions are yours.*

---

### Query approach

*Describe how you will use `_collection.query()` to find relevant chunks. What arguments will you pass, and why?*

```
[We will first pass query_texts with our input query, then n_results with our number of chunks we decided earlier, and in the include arugment the relevant information we want.]
```

---

### Return structure

*Sketch out what one item in your return list looks like as a concrete example. Where does each field come from in the query results?*

```
return_list[0] = {
    "text":"When a player rolls a 1, go forward one space. When a player rolls a 2...",
    "game":"Catan",
    "distance": 0.1
}

Each field comes from the dictionary in the list of dictionaries in the return result.
The text field represents the raw text from the document, will some overlap between chunks.
The game field shows what game the chunk belongs to.
The distance field, is the cosine similiarity score from the user's query and the chunk information.
```

---

### Handling the nested result structure

*`_collection.query()` returns nested lists. Describe what index you need to access to get the actual list of results for a single query, and why the nesting exists.*

```
The query result returns a nested list of lists. The query return expects multiple user queries so for each one, it will return a list of dictionaries inside a list for multiple queries. 
Since we are only sending one query at a time, the result will be at the zero index, which will be a list of dictionaries that are the k closests chunks to the users query.
```

---

### Relevance threshold

*Will you filter out results above a certain distance score, or return all `n_results` regardless of how relevant they are? What are the tradeoffs of each approach?*

```
I will filter out the results above 0.5 distance. 
The trade off of having a threshhold is that it does filter out irrelavant data as well to keep the models answer from bloating. The downside to this is that it may provide less context to the model than we would like, potentially leading to a cannot answer result.
```

---

### Edge cases

*How does your implementation behave when: (a) the collection is empty, (b) the query matches no chunks well, (c) the query matches chunks from multiple games?*

```
[When the collection is empty we just return an empty list that will prompt the model to respond with not enough information to make a response. The query doesn't filter out chunks so the information will get passed to the model. The query does not handle multiple game matches so errors can occur if the user query asks about an aspect about a game that can apply to multiple games, such as "How do I win?"]
```

---

## Implementation Notes

*Fill this in after implementing, before moving to Milestone 3.*

**Test query and top result returned:**

```
Query: [What happens when you roll a 7?]
Top result game: [Risk]
Distance score: [0.597]
Does it make sense? [yes]
```

**One thing about the query results that surprised you:**

```
Given the abstract question of what happens when I roll a 7, the closests chunks resulted from the game of Risk which have special context when the user rolls a 7.
```
