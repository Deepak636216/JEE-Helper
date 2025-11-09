# Project Reorganization - Migration Guide

## Changes Made

The project has been reorganized into a cleaner, more maintainable structure.

### New Directory Structure

```
NCERT/
├── backend/                  # All backend code
│   ├── app/
│   │   └── services/        # ai_tutor.py, utils.py
│   ├── data/
│   │   ├── textbooks/       # Moved from root/Textbooks
│   │   └── problems/        # Moved from root/Topic_prblm
│   ├── logs/                # Application logs
│   └── main.py             # FastAPI entry point
├── frontend/                # React app (unchanged)
├── config/                  # Environment files
│   ├── .env               # Moved from root
│   └── .env.example       # Template
├── docs/                    # All documentation
└── scripts/                # Startup scripts
    ├── start_backend.bat
    └── start_frontend.bat
```

### Files Moved

**Backend:**
- `ai_tutor.py` → `backend/app/services/ai_tutor.py`
- `utils.py` → `backend/app/services/utils.py`
- `app.py` → `backend/app/legacy_app.py` (backup)
- `requirements.txt` → `backend/requirements.txt`

**Data:**
- `Textbooks/*` → `backend/data/textbooks/`
- `Topic_prblm/*` → `backend/data/problems/`
- `template.json` → `backend/data/template.json`

**Configuration:**
- `.env` → `config/.env`

**Documentation:**
- All `.md` files → `docs/`

**Scripts:**
- `start_backend.bat` → `scripts/start_backend.bat`

### Import Path Updates

The following import paths have been updated:

**In `backend/main.py`:**
```python
# OLD
from ai_tutor import PhysicsAITutor
from utils import ProblemLoader

# NEW
from app.services.ai_tutor import PhysicsAITutor
from app.services.utils import ProblemLoader
```

**In `backend/app/services/ai_tutor.py`:**
- Updated to load `.env` from `config/` directory

**In `backend/app/services/utils.py`:**
- Updated default problems directory to `backend/data/problems/`

### Files You Can Safely Delete (After Testing)

Once you've verified everything works with the new structure:

```bash
# Root directory cleanup
ai_tutor.py          # Copied to backend/app/services/
utils.py             # Copied to backend/app/services/
app.py               # Copied to backend/app/legacy_app.py
requirements.txt     # Copied to backend/requirements.txt
template.json        # Copied to backend/data/
```

**Directories (keep for reference until fully migrated):**
- `Textbooks/` → Data copied to `backend/data/textbooks/`
- `Topic_prblm/` → Data copied to `backend/data/problems/`

## Testing the New Structure

1. **Test Backend:**
   ```bash
   cd backend
   python -m uvicorn main:app --reload
   ```
   Visit: http://localhost:8000

2. **Test Frontend:**
   ```bash
   cd frontend
   npm run dev
   ```
   Visit: http://localhost:5173

3. **Verify API Integration:**
   - Submit a question
   - Request a hint
   - View solutions
   - Check logs in `backend/logs/`

## Rollback (If Needed)

If something doesn't work:

1. The original files are still in the root directory
2. You can revert by using the original structure
3. Check `backend/app/legacy_app.py` for the old app.py

## Next Steps

1. Test thoroughly with the new structure
2. Update any external scripts or documentation
3. Clean up old files once verified
4. Consider adding more structure:
   - `backend/app/api/routes/` for organized API routes
   - `backend/app/models/` for Pydantic models
   - `backend/app/core/` for configurations

## Notes

- Environment variables now loaded from `config/.env`
- Logs now written to `backend/logs/`
- All data centralized in `backend/data/`
- Scripts centralized in `scripts/`
- Documentation centralized in `docs/`
