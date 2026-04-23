from groq import Groq

client = Groq(api_key="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")

def generate_answer(query, context):
    prompt = f"""
    Answer ONLY from the context below.
    
    Context:
    {context}
    
    Question:
    {query}
    """

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",  
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content