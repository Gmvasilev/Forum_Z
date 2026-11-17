# Gaming Forum

TODO: project description, link to hosted project (if any), local setup instructions,
and images of the database relations (see docs/).


### Installation

```bash
# Clone the repository and navigate to the project directory:
git clone https://github.com/Gmvasilev/Forum_Z
cd Forum_Z

# (Recommended) Create and activate a virtual environment:
# Creation
python -m venv .venv

#Activation

# Windows (Command Prompt):
.venv\Scripts\activate.bat


# macOS / Linux:
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt


```

# DB settings Configuration

```bash

#Windows
copy .env.example .env

#macOS/ Linux
cp .env.example .env 
```

2. Open `.env` and fill in your own values

Settings are loaded and validated by `app/config.py` using [pythantic-settings]