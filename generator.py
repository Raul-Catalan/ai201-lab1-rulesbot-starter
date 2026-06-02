from groq import Groq
from config import GROQ_API_KEY, LLM_MODEL

_client = Groq(api_key=GROQ_API_KEY)


def generate_response(query, retrieved_chunks):
    """
    Generate a grounded answer from retrieved rule chunks.

    TODO — Milestone 3:

    `retrieved_chunks` is the list returned by retrieve(). Each item is a dict:
      - "text"     : the chunk text
      - "game"     : the game name
      - "distance" : similarity score (you can use this to filter weak matches)

    Before writing code, talk through these with your group:
      - How will you format the chunks into a context block for the prompt?
      - What instructions will stop the model from answering beyond what the
        rules say? (Grounding is the whole point — a confident wrong answer
        is worse than an honest "I don't know.")
      - How will you surface which game each answer comes from?

    Your response should:
      1. Answer using only the retrieved context — not the model's general knowledge
      2. Make clear which game the answer comes from
      3. Say so clearly when the answer isn't in the loaded rules

    Return the response as a plain string.
    """
    if not retrieved_chunks:
        return (
            "I couldn't find anything relevant in the loaded rule books. "
            "Try rephrasing your question — or check that your ingestion pipeline is working."
        )

    # Your implementation here.
    context_string = "Here are the rules you can use:\n\n"
    for chunk in retrieved_chunks:
        context_string += f"Game: {chunk['game']}\n"
        context_string += f"Rule: {chunk['text']}\n"
        context_string += "---\n"
        
    # 2. Strict grounding instruction (exact copy from spec)
    system_instruction = (
        "You are a rule bot that strictly follows rules for board games. Your job is to answer "
        "questions on board games using ONLY the rule text provided below. \n\n"
        "- When you provide an answer, you must cite the game it came from at the end of your response like this: [Source: Game Name].\n"
        "- Do not draw on outside knowledge, your training data, or fill in gaps from what you know about board games.\n"
        "- Do not guess, infer, or logically deduce rules that are not explicitly written in the text.\n"
        "- If the answer is not contained in the provided text, you must reply with exactly: "
        '"I do not have enough information to answer that." Do not add any other explanation.'
    )

    # 3. Combine context and the user's question into the user message
    user_message = f"{context_string}\n\nQuestion: {query}"

    # 4. Call the LLM
    response = _client.chat.completions.create(
        model=LLM_MODEL, # Use the model variable from your config.py
        messages=[
            {"role": "system", "content": system_instruction},
            {"role": "user", "content": user_message}
        ]
    )

    # 5. Return just the plain string response
    print("LLM response:", response.choices[0].message.content)
    return response.choices[0].message.content