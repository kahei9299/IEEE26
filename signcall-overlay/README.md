# signcall-overlay

## Frontend
npm install
npm run dev

## Backend
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000

Open frontend and it will connect to ws://localhost:8000/ws
