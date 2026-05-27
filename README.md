# CurriPath AI

CurriPath AI is a **stateless Django web application** that generates professional, week-by-week learning curricula using the Groq API.

## Highlights

- **Stateless architecture** (no database required).
- **Signed-cookie sessions** for storing generated curriculum data in the browser.
- **Groq-powered curriculum generation** using `llama-3.1-8b-instant`.
- **Tailwind CSS UI** delivered via CDN.
- Ready for **Vercel deployment**.

## Tech Stack

- Python + Django
- Groq SDK
- Tailwind CSS (CDN)
- Gunicorn (runtime server)

## Project Structure

```text
.
├── curripath/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
├── planner/
│   ├── apps.py
│   ├── urls.py
│   └── views.py
├── templates/
│   └── index.html
├── manage.py
├── requirements.txt
├── vercel.json
└── vercel.build.sh
```

## Environment Variables

Set the following environment variable before running:

- `GROQ_API_KEY` — your Groq API key.

## Local Development

1. Create and activate a virtual environment.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Export your API key:
   ```bash
   export GROQ_API_KEY="your_api_key_here"
   ```
4. Run the server:
   ```bash
   python manage.py runserver
   ```

Open `http://127.0.0.1:8000/`.

## Deployment (Vercel)

This project includes:

- `vercel.json` routing requests to `curripath/wsgi.py`
- `vercel.build.sh` to collect static files during build

Configure `GROQ_API_KEY` in your Vercel project environment variables, then deploy.

## How It Works

- `GET /` renders the form and previously generated curriculum from session cookies (if available).
- `POST /` submits `topic`, `timeframe`, and `level`.
- The app calls Groq and stores returned HTML in `request.session["curriculum"]`.
- The response renders the saved curriculum immediately.

## Notes

- No database setup or migrations are needed.
- Session payload is cookie-based, so keep generated output concise to avoid oversized cookies.
