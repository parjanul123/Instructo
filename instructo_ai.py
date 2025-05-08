from transformers import pipeline
from web_search import cauta_pe_internet


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

# === Model AI ===
qa_pipeline = pipeline("text2text-generation", model="google/flan-t5-base")


# === Funcția principală pentru răspunsul AI ===
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

    # Prompt AI prietenos
    prompt = f"""
Scrie în limba română clar, ca pentru un student.

Întrebare:
{intrebare}

Cod analizat:
{cod}

Informații suplimentare:
{rezultate}

Formulează un răspuns natural, cu explicații clare și cod curat.
"""

    result = qa_pipeline(prompt, max_new_tokens=300)[0]["generated_text"]
    return curata_cod(result)
