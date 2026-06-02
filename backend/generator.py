import os
import json
from langchain_groq import ChatGroq

class PaperGenerator:
    def __init__(self, model="llama-3.1-8b-instant", temperature=0.3):
        print("Initializing Groq AI Generator...")
        if "GROQ_API_KEY" not in os.environ:
            print("WARNING: GROQ_API_KEY environment variable not set.")
        self.llm = ChatGroq(
            model=model,
            temperature=temperature,
            model_kwargs={"response_format": {"type": "json_object"}}
        )

    def generate_sections(self, context: str, subject: str, mcq_count: int, short_count: int, long_count: int) -> dict:
        if context == "NO_CONTEXT_FOUND":
            err = "No relevant context found. Please check your PDFs."
            return {"section_a": err, "section_b": err, "section_c": err}

        print("Sending JSON Generation Request to Groq...")

        prompt = f"""You are a university exam paper generator. Output ONLY valid JSON.

SUBJECT: {subject}
CONTEXT: {context}

RULES:
1. Only generate questions about '{subject}'. Ignore any other subject in context.
2. section_a: EXACTLY {mcq_count} MCQs. EVERY question MUST have exactly 4 options labeled a) b) c) d) on separate lines. NO EXCEPTIONS.
3. section_b: EXACTLY {short_count} short-answer questions (no options).
4. section_c: EXACTLY {long_count} long-answer questions (no options).
5. Do NOT include answers, hints, or explanations anywhere.

MCQ FORMAT (mandatory for every single MCQ):
1. Question text here?
a) Option one
b) Option two
c) Option three
d) Option four

Output JSON:
{{
    "section_a": "1. Question?\\na) ...\\nb) ...\\nc) ...\\nd) ...\\n\\n2. Question?\\na) ...\\n... (all {mcq_count} MCQs with 4 options each)",
    "section_b": "Q1. Question\\n\\nQ2. Question\\n... (all {short_count} questions)",
    "section_c": "Q1. Question\\n\\nQ2. Question\\n... (all {long_count} questions)"
}}"""

        try:
            response = self.llm.invoke(prompt).content
            return json.loads(str(response))
        except Exception as e:
            return {
                "section_a": f"AI Error: {str(e)}",
                "section_b": "Error",
                "section_c": "Error"
            }