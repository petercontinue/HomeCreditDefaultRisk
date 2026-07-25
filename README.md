# HomeCredit Scout

A full-stack loan pre-check demo built with **FastAPI**, **React**, **PostgreSQL**, and a **LightGBM** default-risk model trained on the [Home Credit Default Risk](https://www.kaggle.com/c/home-credit-default-risk) dataset.

Users fill in about **25 personal and loan fields** (no login required). The system returns:

- **Approve / Decline** recommendation  
- **Maximum suggested loan amount** (when approved)  
- **Readable feedback** (positive factors, concerns, suggestions)

> **Disclaimer:** This project is for learning and demonstration only. It is **not** a real credit underwriting system and must not be used for actual lending decisions.

---

## Features

- LightGBM binary classifier for default probability  
- Business decision layer: approval threshold + max-amount search  
- Responsive React UI (desktop / tablet / mobile)  
- Multilingual UI & API feedback: **English**, **Simplified Chinese**, **Traditional Chinese**, **Japanese**, **Korean**  
- PostgreSQL persistence for each assessment  
- Local frontend/backend; Docker only for PostgreSQL  
- One-click Windows start/stop scripts (`.cmd`)

---

## Tech Stack

| Layer | Technology |
|-------|------------|
| ML | LightGBM, pandas, scikit-learn, joblib |
| Backend | FastAPI, Pydantic, SQLAlchemy, Uvicorn |
| Database | PostgreSQL 16 (Docker) |
| Frontend | React 19, TypeScript, Vite, React Router, React Hook Form |
| Infra | Docker Compose (Postgres only) |

---

## Project Structure

```text
HomeCreditDefaultRisk/
├── dataset/                  # Home Credit CSV files (input data)
├── ml/
│   ├── train.py              # Offline training script
│   ├── preprocess.py         # Feature engineering / preprocessor
│   ├── feature_config.py     # Feature list & form options
│   └── artifacts/            # Trained model outputs (loaded by API)
│       ├── model.txt
│       ├── preprocessor.joblib
│       ├── feature_meta.json
│       └── metrics.json
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── api/              # REST routes
│   │   ├── services/         # Prediction, decision, feedback
│   │   ├── i18n/             # Backend message translations
│   │   ├── models/           # SQLAlchemy models
│   │   └── schemas/          # Pydantic schemas
│   ├── .env                  # Local config (not committed secrets if customized)
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── pages/            # Home / Apply / Result
│   │   ├── i18n/             # Frontend locale packs
│   │   ├── components/       # Header, language switcher
│   │   └── api/              # API client
│   └── package.json
├── docker-compose.yml        # PostgreSQL on host port 6436
├── start-db.cmd / stop-db.cmd
├── start-backend.cmd / stop-backend.cmd
├── start-frontend.cmd / stop-frontend.cmd
└── README.md
```

---

## Prerequisites

- **Python** 3.10+ (3.11 recommended)  
- **Node.js** 18+ and npm  
- **Docker Desktop** (for PostgreSQL)  
- Windows PowerShell or Command Prompt (helper scripts are `.cmd`)

---

## Ports

| Service | Host port |
|---------|-----------|
| Frontend (Vite) | `5173` |
| Backend (FastAPI) | `8000` |
| PostgreSQL (Docker) | `6436` → container `5432` |

PostgreSQL uses **6436** to avoid conflicts with local Postgres or other projects on `5432`–`5435`.

---

## First-Time Setup

Run all commands from the project root:

```text
D:\05code-AI\HomeCreditDefaultRisk
```

### 1. Create Python virtual environment

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r backend\requirements.txt
```

> If `python -m venv .venv` fails with **Permission denied**, the existing `.venv` is likely locked by another process (e.g. Cursor Python extension). You usually **do not need to recreate** it—just activate and use it.

### 2. Install frontend dependencies

```powershell
cd frontend
npm install
cd ..
```

### 3. Start the database

```powershell
.\start-db.cmd
```

Or:

```powershell
docker compose up -d
```

Default connection (also in `backend/.env`):

```text
postgresql+psycopg2://hcdr:hcdr_pass@127.0.0.1:6436/hcdr
```

### 4. Train the model

```powershell
.\.venv\Scripts\Activate.ps1
python ml\train.py
```

Artifacts are written to `ml/artifacts/`. The API loads them at startup via `MODEL_DIR=../ml/artifacts` (relative to `backend/`).

Typical validation AUC on the selected feature subset is around **0.69** (demo-grade; not a full Kaggle competition pipeline).

### 5. Configure environment (optional)

Copy or edit `backend/.env`:

```env
DATABASE_URL=postgresql+psycopg2://hcdr:hcdr_pass@127.0.0.1:6436/hcdr
MODEL_DIR=../ml/artifacts
CORS_ORIGINS=http://localhost:5173,http://127.0.0.1:5173
# APPROVAL_THRESHOLD=0.25   # optional override; otherwise uses trained threshold
```

Frontend API base URL: `frontend/.env`

```env
VITE_API_BASE_URL=http://localhost:8000
```

---

## Daily Start / Stop

You can **double-click** the `.cmd` files in File Explorer, or run them from the project root.

### Start (use three separate windows)

```powershell
.\start-db.cmd
.\start-backend.cmd
.\start-frontend.cmd
```

Then open: [http://127.0.0.1:5173](http://127.0.0.1:5173)

- Keep the **backend** and **frontend** console windows open. Closing them stops those services.  
- `start-db.cmd` may exit after starting the container; that is expected.

### Stop

```powershell
.\stop-backend.cmd
.\stop-frontend.cmd
.\stop-db.cmd
```

### Equivalent manual commands

**Backend:**

```powershell
.venv\Scripts\python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000 --app-dir backend
```

**Frontend:**

```powershell
cd frontend
npm run dev -- --host 127.0.0.1 --port 5173
```

**Database:**

```powershell
docker compose up -d
docker compose down
```

---

## How the System Works

```text
User form (≈25 fields)
    → feature engineering (same as training)
    → LightGBM P(default)
    → if P(default) < approval_threshold → Approve
    → if approved → binary-search max credit amount under threshold
                    (also capped by income multiples / hard limits)
    → generate localized feedback
    → save row to PostgreSQL
    → return result to UI
```

### Model artifacts location

Trained files live under **`ml/artifacts/`**, not inside `backend/`.  
The backend only **loads** them at runtime.

| File | Purpose |
|------|---------|
| `model.txt` | LightGBM model |
| `preprocessor.joblib` | Imputation + categorical encoding |
| `feature_meta.json` | Feature list, threshold, risk bands, version |
| `metrics.json` | Train/valid AUC and threshold tuning info |

### Form fields (high level)

Personal: gender, age, family status, education, housing, realty/car flags, children, family size, accompanier, region rating, contact flags  

Income / work: annual income, income type, years employed, occupation, organization type  

Loan: contract type, requested amount, annuity, goods price (optional)

Dataset categorical values used as model inputs (e.g. `Married`, `Working`) remain in English for model compatibility; UI chrome and feedback are translated.

---

## Internationalization (i18n)

Supported languages (switch from the top-right dropdown):

- English (`en`)  
- Simplified Chinese (`zh-CN`)  
- Traditional Chinese (`zh-TW`)  
- Japanese (`ja`)  
- Korean (`ko`)

Behavior:

- Frontend strings: `frontend/src/i18n/locales/`  
- Backend feedback / validation messages: `backend/app/i18n/messages.py`  
- Preference stored in `localStorage` (`hcdr_locale`)  
- Predict requests send `lang` in the JSON body and `X-Lang` / `Accept-Language` headers  
- Money and datetime formats follow the active locale (English uses month/day/year)

Note: Feedback stored for an existing application is saved in the language used at submission time.

---

## API Reference

Interactive docs (when backend is running):

- Swagger UI: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)  
- ReDoc: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/api/health` | Health check |
| `GET` | `/api/meta/form-options` | Dropdown options for the form |
| `GET` | `/api/meta/languages` | Supported UI languages |
| `POST` | `/api/predict` | Run assessment and persist result |
| `GET` | `/api/predictions/{id}` | Fetch a saved assessment by UUID |

### Example: health

```powershell
Invoke-RestMethod http://127.0.0.1:8000/api/health
```

### Example: predict (abbreviated)

```http
POST /api/predict
Content-Type: application/json
X-Lang: en

{
  "name_contract_type": "Cash loans",
  "code_gender": "F",
  "flag_own_car": "N",
  "flag_own_realty": "Y",
  "cnt_children": 0,
  "amt_income_total": 180000,
  "amt_credit": 450000,
  "amt_annuity": 22000,
  "amt_goods_price": 450000,
  "name_income_type": "Working",
  "name_education_type": "Higher education",
  "name_family_status": "Married",
  "name_housing_type": "House / apartment",
  "age_years": 35,
  "employment_years": 5,
  "cnt_fam_members": 2,
  "organization_type": "Business Entity Type 3",
  "region_rating_client": 2,
  "flag_email": true,
  "flag_phone": true,
  "flag_work_phone": false,
  "lang": "en"
}
```

Response includes `approved`, `default_probability`, `risk_level`, `max_approved_amount`, `feedback`, `model_version`, and `application_id`.

---

## Database

Docker Compose service `postgres`:

- User: `hcdr`  
- Password: `hcdr_pass`  
- Database: `hcdr`  
- Host port: `6436`

Main table: `loan_applications`  
Stores input JSON, probability, approval flag, max amount, feedback JSON, model version, and timestamp.

Tables are created automatically on API startup (`create_all`).

---

## Troubleshooting

### `Failed to fetch` in the browser

The frontend cannot reach the API. Check that:

1. Backend is running on port `8000`  
2. Database is up on port `6436`  
3. You open the UI at `http://127.0.0.1:5173` (or `localhost`) and CORS origins match `backend/.env`

Verify API:

```text
http://127.0.0.1:8000/api/health
```

### Model artifacts not found

Run training first:

```powershell
python ml\train.py
```

Confirm files exist under `ml/artifacts/`.

### PostgreSQL password / connection errors

- Ensure Docker container is healthy: `docker compose ps`  
- Use `127.0.0.1:6436` (not another local Postgres on `5432`)  
- Prefer `127.0.0.1` over `localhost` if IPv6 resolves to a different server

### Port already in use

Stop the conflicting process, or change ports in:

- Backend: `start-backend.cmd` / uvicorn `--port`  
- Frontend: `start-frontend.cmd` / Vite `--port`  
- Database: `docker-compose.yml` host mapping and `DATABASE_URL`

### Permission denied recreating `.venv`

Stop processes using `.venv\Scripts\python.exe`, or simply reuse the existing virtual environment instead of recreating it.

---

## Retraining

After changing features in `ml/feature_config.py` or preprocessing:

```powershell
.\.venv\Scripts\Activate.ps1
python ml\train.py
```

Then **restart the backend** so it reloads `ml/artifacts/`.

Optional: set `APPROVAL_THRESHOLD` in `backend/.env` to override the threshold saved in `feature_meta.json`.

---

## Dataset (not in Git)

Large CSV files under `dataset/` are **gitignored** (several GB). For training locally:

1. Download [Home Credit Default Risk](https://www.kaggle.com/c/home-credit-default-risk/data) from Kaggle  
2. Place the CSV files into `dataset/`  
3. Run `python ml/train.py`

Pretrained demo artifacts under `ml/artifacts/` are included so the API can run without re-training.

Also copy env examples if needed:

```powershell
copy backend\.env.example backend\.env
copy frontend\.env.example frontend\.env
```

---

## License & Data

- Code in this repository: for educational / demo use unless otherwise stated.  
- Dataset: Home Credit Default Risk (Kaggle). Follow Kaggle’s and Home Credit’s data usage terms.  
- Do not deploy this demo as a production credit decision engine without proper compliance, model governance, and legal review.
