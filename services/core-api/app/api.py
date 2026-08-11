"""core-api FastAPI application — users, auth, journal, watchlists, layouts, alerts, audit.

Everything is scoped to the authenticated user (`current_user`); cross-user
access is impossible because every query filters by `owner_id`.
"""
from __future__ import annotations

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from app import models, schemas
from app.audit import audit
from app.auth import (
    create_access_token,
    get_current_user,
    hash_password,
    verify_password,
)
from app.database import get_db, get_settings, init_db

init_db()

app = FastAPI(title="core-api — Trading Desk persistence", version=get_settings().app_version)


# --- Health ---
@app.get("/health")
def health():
    return {"status": "ok", "service": "core-api", "version": get_settings().app_version}


# --- Auth ---
@app.post("/auth/register", response_model=schemas.TokenResponse)
def register(req: schemas.RegisterRequest, db: Session = Depends(get_db)):
    existing = db.query(models.User).filter(models.User.email == req.email).first()
    if existing:
        raise HTTPException(status_code=409, detail="email already registered")
    user = models.User(email=req.email, password_hash=hash_password(req.password), telegram_id=req.telegram_id)
    db.add(user)
    db.commit()
    db.refresh(user)
    audit(db, user.id, "user.register", "user", user.id, {"email": user.email})
    db.commit()
    return schemas.TokenResponse(access_token=create_access_token(user.id, user.email))


@app.post("/auth/login", response_model=schemas.TokenResponse)
def login(req: schemas.LoginRequest, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == req.email).first()
    if user is None or not verify_password(req.password, user.password_hash):
        raise HTTPException(status_code=401, detail="invalid credentials")
    return schemas.TokenResponse(access_token=create_access_token(user.id, user.email))


@app.get("/auth/me", response_model=schemas.UserResponse)
def me(user: models.User = Depends(get_current_user)):
    return user


# --- Journal ---
@app.post("/journal", response_model=schemas.JournalOut)
def create_journal(req: schemas.JournalCreate, user=Depends(get_current_user), db: Session = Depends(get_db)):
    entry = models.JournalEntry(owner_id=user.id, **req.model_dump())
    db.add(entry)
    db.commit()
    db.refresh(entry)
    audit(db, user.id, "journal.create", "journal", entry.id)
    db.commit()
    return entry


@app.get("/journal", response_model=list[schemas.JournalOut])
def list_journal(user=Depends(get_current_user), db: Session = Depends(get_db)):
    return db.query(models.JournalEntry).filter(models.JournalEntry.owner_id == user.id).order_by(models.JournalEntry.created_at.desc()).all()


@app.get("/journal/{entry_id}", response_model=schemas.JournalOut)
def get_journal(entry_id: int, user=Depends(get_current_user), db: Session = Depends(get_db)):
    entry = db.get(models.JournalEntry, entry_id)
    if entry is None or entry.owner_id != user.id:
        raise HTTPException(status_code=404, detail="not found")
    return entry


@app.patch("/journal/{entry_id}", response_model=schemas.JournalOut)
def update_journal(entry_id: int, req: schemas.JournalUpdate, user=Depends(get_current_user), db: Session = Depends(get_db)):
    entry = db.get(models.JournalEntry, entry_id)
    if entry is None or entry.owner_id != user.id:
        raise HTTPException(status_code=404, detail="not found")
    for k, v in req.model_dump(exclude_unset=True).items():
        setattr(entry, k, v)
    db.commit()
    db.refresh(entry)
    audit(db, user.id, "journal.update", "journal", entry.id)
    db.commit()
    return entry


@app.delete("/journal/{entry_id}", status_code=204)
def delete_journal(entry_id: int, user=Depends(get_current_user), db: Session = Depends(get_db)):
    entry = db.get(models.JournalEntry, entry_id)
    if entry is None or entry.owner_id != user.id:
        raise HTTPException(status_code=404, detail="not found")
    audit(db, user.id, "journal.delete", "journal", entry.id)
    db.delete(entry)
    db.commit()


# --- Watchlist ---
@app.post("/watchlist", response_model=schemas.WatchlistOut)
def add_watchlist(req: schemas.WatchlistCreate, user=Depends(get_current_user), db: Session = Depends(get_db)):
    item = models.WatchlistEntry(owner_id=user.id, **req.model_dump())
    db.add(item)
    db.commit()
    db.refresh(item)
    audit(db, user.id, "watchlist.create", "watchlist", item.id)
    db.commit()
    return item


@app.get("/watchlist", response_model=list[schemas.WatchlistOut])
def list_watchlist(user=Depends(get_current_user), db: Session = Depends(get_db)):
    return db.query(models.WatchlistEntry).filter(models.WatchlistEntry.owner_id == user.id).all()


@app.delete("/watchlist/{item_id}", status_code=204)
def delete_watchlist(item_id: int, user=Depends(get_current_user), db: Session = Depends(get_db)):
    item = db.get(models.WatchlistEntry, item_id)
    if item is None or item.owner_id != user.id:
        raise HTTPException(status_code=404, detail="not found")
    audit(db, user.id, "watchlist.delete", "watchlist", item.id)
    db.delete(item)
    db.commit()


# --- Chart layouts (persisted server-side — Phase 5) ---
@app.post("/layouts", response_model=schemas.LayoutOut)
def upsert_layout(req: schemas.LayoutCreate, user=Depends(get_current_user), db: Session = Depends(get_db)):
    layout = db.query(models.ChartLayout).filter(
        models.ChartLayout.owner_id == user.id, models.ChartLayout.symbol == req.symbol
    ).first()
    if layout is None:
        layout = models.ChartLayout(owner_id=user.id, symbol=req.symbol)
        db.add(layout)
    layout.range = req.range
    layout.indicators = req.indicators
    layout.drawings = req.drawings
    db.commit()
    db.refresh(layout)
    audit(db, user.id, "layout.upsert", "layout", layout.id, {"symbol": req.symbol})
    db.commit()
    return layout


@app.get("/layouts/{symbol:path}", response_model=schemas.LayoutOut)
def get_layout(symbol: str, user=Depends(get_current_user), db: Session = Depends(get_db)):
    layout = db.query(models.ChartLayout).filter(
        models.ChartLayout.owner_id == user.id, models.ChartLayout.symbol == symbol
    ).first()
    if layout is None:
        raise HTTPException(status_code=404, detail="not found")
    return layout


# --- Alerts ---
@app.post("/alerts", response_model=schemas.AlertOut)
def create_alert(req: schemas.AlertCreate, user=Depends(get_current_user), db: Session = Depends(get_db)):
    alert = models.Alert(owner_id=user.id, **req.model_dump())
    db.add(alert)
    db.commit()
    db.refresh(alert)
    audit(db, user.id, "alert.create", "alert", alert.id)
    db.commit()
    return alert


@app.get("/alerts", response_model=list[schemas.AlertOut])
def list_alerts(user=Depends(get_current_user), db: Session = Depends(get_db)):
    return db.query(models.Alert).filter(models.Alert.owner_id == user.id).all()


@app.delete("/alerts/{alert_id}", status_code=204)
def delete_alert(alert_id: int, user=Depends(get_current_user), db: Session = Depends(get_db)):
    alert = db.get(models.Alert, alert_id)
    if alert is None or alert.owner_id != user.id:
        raise HTTPException(status_code=404, detail="not found")
    audit(db, user.id, "alert.delete", "alert", alert.id)
    db.delete(alert)
    db.commit()


# --- Audit trail (own access; admin-scoped in prod) ---
@app.get("/audit", response_model=list[schemas.AuditOut])
def list_audit(user=Depends(get_current_user), db: Session = Depends(get_db)):
    # In production, restrict to admins. For now return the actor's logs.
    return db.query(models.AuditLog).filter(models.AuditLog.actor_id == user.id).order_by(models.AuditLog.created_at.desc()).limit(200).all()
