import openai
import os
from web_search import cauta_pe_internet

# === Configurare OpenAI API ===
openai.api_key = os.getenv("OPENAI_API_KEY")  # Asigură-te că ai setat cheia în mediu

# === Curățare cod (Assembly/VHDL) ===
def curata_cod(text: str) -> str:
    return (
        text.replace("\t", "    ")
            .replace(" ;", ";")
            .replace(" :", ":")
            .replace("\r", "")
            .strip()
    )

# === Citire documentații text ===
def incarca_documentatie(fisier):
    with open(fisier, encoding="utf-8") as f:
        content = f.read()
    blocks = content.split("\n\n")
    doc = {}
    for block in blocks:
        lines = block.strip().splitlines()
        if lines:
            cmd_name = lines[0].strip("[]").lower()
            doc[cmd_name] = "\n".join(lines[1:])
    return doc

# === Încarcă fișierele de documentație ===
documentatie_asm = incarca_documentatie("resurse/documentatie_assembly.txt")
documentatie_vhdl = incarca_documentatie("resurse/documentatie_vhdl.txt")
functii_hardware = incarca_documentatie("resurse/functii_hardware.txt")

# === Funcția principală pentru răspunsul AI cu OpenAI GPT-4 ===
def chat_response(message: str) -> str:
    message = message.strip()
    intrebare = message
    cod = ""

    if "cod curent:" in message.lower():
        try:
            parts = message.split("cod curent:")
            intrebare = parts[0].strip()
            cod = parts[1].strip()
        except IndexError:
            cod = ""

    # Încercăm să căutăm online, dar cu fallback pe documentație
    try:
        rezultate = cauta_pe_internet(intrebare + (" " + cod[:100] if cod else ""))
    except:
        rezultate = "⚠️ Nu am putut căuta pe internet. Folosesc doar documentația locală."

    # Verificăm dacă există ceva în documentație
    documentatie_relevanta = ""
    if "assembly" in intrebare.lower() or "asm" in intrebare.lower():
        documentatie_relevanta = documentatie_asm.get(intrebare.lower(), "")
    elif "vhdl" in intrebare.lower():
        documentatie_relevanta = documentatie_vhdl.get(intrebare.lower(), "")

    # Prompt AI OpenAI (format pentru noul API)
    prompt = f"""
Tu ești un asistent tehnic pentru programare VHDL și Assembly.
- Scrie doar în limba română.
- Nu menționa surse externe.
- Răspunde clar și concis, ca pentru un student.
- Dacă se cere cod, oferă un exemplu corect și complet.

Întrebare:
{intrebare}

Cod analizat (dacă e):
{cod}

Informații suplimentare (căutare sau documentație):
{rezultate}

Documentație locală (dacă există):
{documentatie_relevanta}

Formulează un răspuns natural, cu explicații clare și cod curat.
"""

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",  # sau "gpt-3.5-turbo" dacă nu ai acces la GPT-4
            messages=[
                {"role": "system", "content": "Ești un asistent tehnic pentru VHDL și Assembly."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=400,
            temperature=0.7,
        )
        result = response.choices[0].message['content'].strip()
        return curata_cod(result)
    except Exception as e:
        return f"Eroare în comunicarea cu OpenAI: {str(e)}"
