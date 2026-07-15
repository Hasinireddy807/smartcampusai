# SmartCampusAI

SmartCampusAI is a production-ready, modern AI-powered dashboard for campus administration, student tracking, faculty lookup, attendance analysis, and advanced predictions. It features custom authentication, interactive charts, and an AI campus assistant.

## Features

- **Authentication System**: Secure username/email login and registration with bcrypt password hashing.
- **Dynamic Dashboard**: Responsive layouts displaying real-time campus metrics, announcements, quick actions, and data tables.
- **Interactive Analytics**: Rich charts built with Plotly tracking attendance trends, department distributions, and student growth.
- **AI Assistant**: Built-in OpenAI-powered campus bot to answer queries and perform analysis (gracefully handles missing API keys).
- **CRUD Operations**: Manage students and faculty directories with live updates saved locally to atomic JSON files.
- **Global Settings & Theme**: Support for dashboard toggles and visual modifications.
- **Responsive Premium UI**: Glassmorphic custom CSS cards, hover animations, responsive layout.

## Project Structure

```text
SmartCampusAI/
├── app.py                  # Entry point for Auth, Routing & Main App
├── requirements.txt        # Dependency specification
├── README.md               # User guide and documentation
├── .env                    # System secrets (ignored by git)
├── .env.example            # Environment variables blueprint
├── .gitignore              # Ignored files
├── assets/                 # Custom visual assets and style sheets
│   ├── logo.png
│   ├── banner.png
│   ├── avatar.png
│   └── styles.css
├── database/               # JSON-based data stores
│   ├── users.json
│   ├── activity.json
│   └── settings.json
├── auth/                   # Custom authentication flow modules
│   ├── login.py
│   ├── register.py
│   ├── authentication.py
│   └── password_utils.py
├── utils/                  # Core utility and state management modules
│   ├── config.py
│   ├── json_db.py
│   ├── helper.py
│   ├── charts.py
│   └── session.py
├── components/             # Reusable UI layouts
│   ├── navbar.py
│   ├── sidebar.py
│   ├── cards.py
│   └── footer.py
└── pages/                  # Streamlit Multi-Page navigation scripts
    ├── Dashboard.py
    ├── AI_Assistant.py
    ├── Student.py
    ├── Faculty.py
    ├── Attendance.py
    ├── Analytics.py
    ├── Settings.py
    └── Profile.py
```

## Getting Started

### 1. Prerequisites

- Python 3.11 or higher installed on your system.

### 2. Setup a Virtual Environment

Run the following commands in your terminal:

```bash
# Clone the repository (or extract files)
cd smartcampusai

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Environment Configuration

Copy the example file to `.env` and enter your OpenAI API key (if available):

```bash
cp .env.example .env
```

Open `.env` and set:
```env
OPENAI_API_KEY=sk-your-openai-api-key
```

*Note: The application will run fine and display a friendly message even if the OpenAI key is missing.*

### 5. Running the Application

Launch the Streamlit app with:

```bash
streamlit run app.py
```

Open `http://localhost:8501` in your browser.

## Deployment

The application is fully deployment-ready.

- **Streamlit Community Cloud**: Connect the Github repository, and specify `app.py` as the entrypoint. Add `OPENAI_API_KEY` to the app's Secrets.
- **Render / Railway / Heroku**: Ensure the port is bound correctly. The project uses standard Streamlit configurations.
- **Local Machine**: Runs on standard ports out of the box.

## License

This project is licensed under the MIT License.
