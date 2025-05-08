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

    # Separare cod dacă există
    if "cod curent:" in message.lower():
        try:
            parts = message.split("cod curent:")
            intrebare = parts[0].strip()
            cod = parts[1].strip()
        except IndexError:
            cod = ""

    # Caută online pentru întrebarea completă
    cautare = intrebare + (" " + cod[:100] if cod else "")
    rezultate = cauta_pe_internet(cautare)

    # Prompt AI OpenAI
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

Informații suplimentare:
{rezultate}

Formulează un răspuns natural, cu explicații clare și cod curat.
"""

    try:
        response = openai.Completion.create(
            model="text-davinci-003",  # sau gpt-4 dacă ai acces
            prompt=prompt,
            max_tokens=400,
            temperature=0.7,
            n=1,
            stop=None
        )
        result = response.choices[0].text.strip()
        return curata_cod(result)
    except Exception as e:
        return f"Eroare în comunicarea cu OpenAI: {str(e)}"
