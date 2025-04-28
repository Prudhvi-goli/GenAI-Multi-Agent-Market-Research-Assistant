import os
from dotenv import load_dotenv
from transformers import pipeline
from config import MODEL_NAME, DEVICE

load_dotenv()
HF_TOKEN = os.getenv("HF_TOKEN")

def generate_use_cases(research_summary: str) -> list:
    try:
        generator = pipeline(
            "text-generation",
            model=MODEL_NAME,
            device=DEVICE,
            token=HF_TOKEN
        )

        prompt = f"""
        You are an AI business consultant. Based on the following industry summary, generate 5 well-structured GenAI/ML use cases tailored to the company.

        Each use case should follow this format:
        Title: <name of the use case>
        Description: <what it does>
        AI Technique: <LLM, RAG, CV, etc.>
        Expected Impact: <improvement or value delivered>

        Industry Summary:
        {research_summary}

        Output:
        """

        response = generator(
            prompt,
            max_new_tokens=800,
            num_return_sequences=1,
            temperature=0.8,
            do_sample=True,
            truncation=True,
            pad_token_id=generator.tokenizer.eos_token_id
        )

        output = response[0]["generated_text"].strip()[len(prompt):]
        # Break by new use case
        use_cases = [uc.strip() for uc in output.split("Title:") if uc.strip()]
        return ["Title:" + uc for uc in use_cases]  # Re-attach 'Title:' to each

    except Exception as e:
        return [f"Error: {str(e)}"]
