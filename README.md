# Email Editing App

## Getting Started

### **1. Clone the repository**

```bash
git clone https://github.com/Ikaay1/Email-Editing-App.git
cd <your-repo-name>
```

### **2. Create a Virtual Environment**

> Recommended: Python 3.9+

A virtual environment keeps your project isolated from your system Python packages.

**macOS / Linux**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

**Windows**

```bash
python -m venv .venv
.venv\Scripts\Activate.ps1
```

When activated, your terminal prompt should display (.venv).

### **3. Install Required Dependencies**

With the virtual environment activated, install the project dependencies:

```bash
pip install -r requirements.txt
```

### **3a. Update Dependencies**

If you install new packages while working on the project:

```bash
pip install <package-name>
pip freeze > requirements.txt
```

This regenerates requirements.txt so others can install the same environment.

### **4. Start the app**

To run the app on Streamlit, run:

```bash
streamlit run app.py
```
