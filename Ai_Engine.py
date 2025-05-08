from transformers import pipeline
import re, pandas as pd

# === 1. Model AI + dicționar român ===
qa_pipeline = pipeline("text2text-generation", model="google/flan-t5-base")

context_romana = {
    "cpu": "Unitatea centrală de procesare care execută instrucțiuni.",
    "alu": "Unitatea de operații logice și aritmetice.",
    "ram": "Memorie temporară rapidă accesibilă procesorului.",
    "rom": "Memorie permanentă pentru inițializarea sistemului.",
    "vhdl": "Limbaj hardware pentru definirea arhitecturilor logice.",
    "assembly": "Limbaj de nivel jos apropiat de structura procesorului."
}

# === 2. Analiză Assembly ===
def analyze_assembly_code(code: str) -> str:
    lines = code.splitlines()
    suggestions = []
    for i, line in enumerate(lines):
        if re.search(r"\bmul\b.*\b2\b", line, re.IGNORECASE):
            suggestions.append(f"Linia {i+1}: Înlocuiește 'MUL ... 2' cu 'SHL ... 1'.")
        if re.search(r"mov\s+(\w+),\s*\1", line, re.IGNORECASE):
            suggestions.append(f"Linia {i+1}: Instrucțiunea MOV e redundantă (același registru).")
    return "\n".join(suggestions) if suggestions else "Codul pare curat și optimizat!"

# === 3. Analiză fișiere JSON ===
def analyze_json_metrics(file_path: str) -> str:
    df = pd.read_json(file_path)
    summary = f"""
📊 Analiză JSON:
- Coloane: {', '.join(df.columns)}
- Medii: {df.mean(numeric_only=True).to_dict()}
- Corelații:
{df.corr(numeric_only=True).round(2).to_string()}
"""
    return summary

# === 4. Funcție unică de chat AI ===
def chat_response(message: str, code: str = "", data_path: str = "") -> str:
    message = message.lower()

    # Dacă vrea analiză de cod JSON
    if "json" in message or "metrice" in message:
        if data_path:
            return analyze_json_metrics(data_path)
        return "Te rog să încarci un fișier JSON pentru analiză."

    # Dacă e cod assembly
    if "assembly" in message or "optimizează" in message or "cod" in message:
        explanation = analyze_assembly_code(code)
        prompt = f"Explică acest cod și sugestiile pentru utilizator: {explanation}. Întrebarea: {message}"
    else:
        # Dicționar fallback
        for key in context_romana:
            if key in message:
                prompt = f"Explică ce înseamnă '{key}' pe înțelesul tuturor: {context_romana[key]}. Întrebarea completă: {message}"
                break
        else:
            prompt = f"Formulează un răspuns clar și empatic în limba română pentru: '{message}'"

    result = qa_pipeline(prompt, max_new_tokens=120)[0]["generated_text"]
    return result
