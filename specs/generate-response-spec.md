# Spec: `generate_response()`

**File:** `generator.py`
**Status:** Spec incomplete — fill in all blank fields before implementing

---

## Purpose

Given a user query and a list of retrieved rule chunks, generate a response that directly answers the question using only the retrieved text as context. The response must be grounded — it should not draw on the model's general knowledge of board games, only on what was retrieved.

---

## Input / Output Contract

**Inputs:**

| Parameter | Type | Description |
|-----------|------|-------------|
| `query` | `str` | The user's original question |
| `retrieved_chunks` | `list[dict]` | Ranked list of chunks from `retrieve()`, each with `"text"`, `"game"`, and `"distance"` |

**Output:** `str`

A plain string containing the response to show the user. The response should:
- Answer the question using only the retrieved rule text
- Identify which game the answer comes from
- Acknowledge clearly when the answer is not found in the loaded rules

Returns a fallback string (not an error) when `retrieved_chunks` is empty.

---

## Design Decisions

*Complete the fields below before writing any code. Use your AI tool in Plan or Ask mode to help you reason through what belongs here — but the decisions are yours.*

---

### Context formatting

*How will you format the retrieved chunks before passing them to the LLM? Describe the structure — not the code. Consider: will you label chunks by game? Include distance scores? Separate chunks with delimiters?*

```
Here are the rules you can use:

Game: [game]
Rule: [text]
---
Game: [game]
Rule: [text]
---
```

---

### System prompt — grounding instruction

*Write the exact system prompt instruction you will use to prevent the model from answering beyond the retrieved text. This is the most important design decision in this function.*

```
[You are a rule bot that strictly follows rules for board games. Your job is to answer questions on board games using ONLY the rule text provided below. 

- When you provide an answer, you must cite the game it came from at the end of your response like this: [Source: Game Name].
- Do not draw on outside knowledge, your training data, or fill in gaps from what you know about board games.
- Do not guess, infer, or logically deduce rules that are not explicitly written in the text.
- If the answer is not contained in the provided text, you must reply with exactly: "I do not have enough information to answer that." Do not add any other explanation.]
```

---

### System prompt — citation instruction

*Write the exact instruction you will use to tell the model to identify which game its answer comes from.*

```
[When you provide an answer, you must cite the game it came from at the end of your response like this: [Source: Game Name].]
```

---

### Fallback behavior

*What should the response say when the answer isn't found in the loaded rule books? Write the exact fallback message.*

```
[- If the answer is not contained in the provided text, you must reply with exactly: "I do not have enough information to answer that." Do not add any other explanation.]
```

---

### Handling low-relevance chunks

*`retrieved_chunks` may include chunks with high distance scores (weak relevance). Will you filter these out before building context, pass them all in, or handle them another way? What are the tradeoffs?*

```
[Currently I will pass all the relevant chunks in. The tradeoff is that the LLM will always recieve some chunks, but may recieve irrelevant chunks.]
```

---

### Message structure

*Describe how you will structure the messages list for the API call — what goes in the system message vs. the user message?*

```
[The system message will tell the model how to behave and what actions to perform. The user message will hold the raw user query.]
```

---

## Implementation Notes

*Fill this in after implementing and testing.*

**Test query and response:**

```
Query: [How do you get out of Jail in Monopoly?]
Response: [Pay 50$ or use a get out of jail free card or roll doubles on three turns in jail]
Correctly grounded? [yes]
Cited the right game? [yes]
```

**One thing you changed from your original spec after seeing the actual output:**

```
[One thing I changed from my original spec was adding citations as well as explicity stating not to use prior knowledge and training, only the prociveded chunks.]
```
