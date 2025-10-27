# Setup instructions for any system

1. Clone the repository:
   git clone <your-repo-url>
   cd ImageCryptography

2. Create a virtual environment (recommended):
   python -m venv .venv

3. Activate the virtual environment:
   # Windows PowerShell
   . .\.venv\Scripts\Activate.ps1
   # macOS/Linux
   source .venv/bin/activate

4. Install dependencies:
   pip install -r requirements.txt

5. Run the code:
   python MainCode/main.py

# Notes
- Do NOT commit .venv to git. It is ignored by .gitignore.
- If you add new dependencies, run: pip freeze > requirements.txt
- CURRENT CODE IS RUNNING IN PYTHON 3.14; this is my first project using python so be wary for bugs and stuff!

In order to 