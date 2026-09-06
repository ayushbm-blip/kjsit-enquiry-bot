# KJSIT College Enquiry Bot

A multilingual AI enquiry system for KJSIT, built with RAG (Retrieval-Augmented
Generation), FAISS, and a free Groq LLM API, with a Streamlit chat UI.

## What's already done for you
- `data/` — 11 clean, verified data files covering admissions, fees, subjects
  (all 4 years / 8 semesters of Computer Engineering), placements, library,
  infrastructure, and contact info.
- `rag_engine.py` — the RAG pipeline (loads data, builds a searchable index,
  answers questions). Includes anti-hallucination and multilingual instructions.
- `app.py` — the chat interface, already wired to `rag_engine.py`.

## Setup (do this once)

1. **Get a free Groq API key**: go to https://console.groq.com, sign up, and
   create an API key. No credit card required.

2. **Install Python dependencies**:
   ```
   pip install -r requirements.txt --break-system-packages
   ```
   (On Windows, drop `--break-system-packages` if it errors — that flag is
   only needed on some Linux/Mac setups.)

3. **Set your API key as an environment variable**:
   - Mac/Linux: `export GROQ_API_KEY=your_key_here`
   - Windows CMD: `set GROQ_API_KEY=your_key_here`
   - Windows PowerShell: `$env:GROQ_API_KEY="your_key_here"`

   You'll need to do this every time you open a new terminal, unless you add
   it to your shell's startup file.

## Running it

**Test the AI logic alone first** (recommended before touching the UI):
```
python rag_engine.py
```
This starts a terminal chat. Try the test questions below. Type `quit` to exit.

**Run the full chat UI**:
```
streamlit run app.py
```
This opens a browser tab with the chat interface.

## Test questions to run first

English:
- What is the annual fee for Computer Science branch in Open category?
- What documents are required for admission?
- What subjects are taught in Semester 3 of Computer Engineering?
- What is the library timing during exams?
- What is the placement contact email?

Hindi/Marathi (tests multilingual — type in Devanagari):
- कॉलेज की फीस कितनी है?
- एडमिशन के लिए कौन से डॉक्यूमेंट चाहिए?

Edge cases (should say "I don't have that information", NOT make something up):
- What is the fee for the MBA program?
- Who is the sports coach?
- What's the weather today?

## If something goes wrong

**"GROQ_API_KEY environment variable is not set"**
→ You skipped step 3 above, or opened a new terminal since setting it.

**Answers are vague or miss obvious facts**
→ Open `rag_engine.py`, find `search_kwargs={"k": 5}`, try raising it to `k=8`.

**Answers mix up unrelated facts**
→ Open `rag_engine.py`, find `chunk_size=300`, try lowering it to `chunk_size=200`.

**It's answering in English even when asked in Hindi/Marathi**
→ This is rare since the prompt already forces language-matching, but if it
  happens, it's usually the underlying model being inconsistent — try
  rephrasing the question or asking again.

**Still stuck?**
→ Whoever is doing deployment (see main project plan) should try adding more
  topics to `data/` before the demo — the more it needs to know, the less
  likely it hallucinates.

## Still missing (add later if time allows)
- Hostel details (needs manual copy from college website)
- Scholarships (data conflicting across colleges — needs office verification)
- Academic calendar / important dates for current year
