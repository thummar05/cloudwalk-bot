from groq import Groq
from app.config import GROQ_API_KEY

client = Groq(api_key=GROQ_API_KEY)


def generate_answer(question: str, context: str) -> str:

    prompt = f"""
    You are a helpful assistant knowledgeable about CloudWalk and its products.
    Answer the question using ONLY the provided context.

    Context:
    {context}

    Question:
    {question}

    Provide a clear, concise answer. If the answer is not in the context,
    say "The information is not available."
    """

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant", 
        messages=[
            {
                "role": "system",
                "content": "You are a CloudWalk knowledge assistant."
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    # ERROR WAS HERE: Changed ["content"] to .content
    return response.choices[0].message.content