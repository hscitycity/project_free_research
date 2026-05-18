from fastapi import FastAPI, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
from database import supabase
from models import NoticeCreate, NoticeUpdate, ActivityCreate, ActivityUpdate, TeamUpdate
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

BUDGET_PER_TEAM = 300000  # 팀당 총 지원금액 30만원

def check_admin(x_admin_key: str = Header(None)):
    if x_admin_key != os.getenv("ADMIN_SECRET"):
        raise HTTPException(status_code=401, detail="관리자 권한이 없습니다")

# ─────────────────────────────────────────
# 공지사항 API
# ─────────────────────────────────────────

@app.get("/api/notices")
def get_notices():
    res = supabase.table("notices").select("*").order("is_pinned", desc=True).order("created_at", desc=True).execute()
    return res.data

@app.post("/api/notices")
def create_notice(notice: NoticeCreate, x_admin_key: str = Header(None)):
    check_admin(x_admin_key)
    res = supabase.table("notices").insert(notice.dict()).execute()
    return res.data

@app.put("/api/notices/{notice_id}")
def update_notice(notice_id: int, notice: NoticeUpdate, x_admin_key: str = Header(None)):
    check_admin(x_admin_key)
    res = supabase.table("notices").update(notice.dict(exclude_none=True)).eq("id", notice_id).execute()
    return res.data

@app.delete("/api/notices/{notice_id}")
def delete_notice(notice_id: int, x_admin_key: str = Header(None)):
    check_admin(x_admin_key)
    supabase.table("notices").delete().eq("id", notice_id).execute()
    return {"message": "삭제 완료"}

# ─────────────────────────────────────────
# 팀 API
# ─────────────────────────────────────────

@app.get("/api/teams")
def get_teams():
    teams = supabase.table("teams").select("*").order("order_num").execute().data
    activities = supabase.table("activities").select("*").order("activity_date", desc=True).execute().data

    result = []
    for team in teams:
        team_activities = [a for a in activities if a["team_id"] == team["id"]]
        total_used = sum(a["amount_used"] for a in team_activities)
        result.append({
            **team,
            "activities": team_activities,
            "total_used": total_used,
            "balance": BUDGET_PER_TEAM - total_used
        })
    return result

# ─────────────────────────────────────────
# 팀 API (수정)
# ─────────────────────────────────────────

@app.put("/api/teams/{team_id}")
def update_team(team_id: int, team: TeamUpdate, x_admin_key: str = Header(None)):
    check_admin(x_admin_key)
    res = supabase.table("teams").update(team.dict(exclude_none=True)).eq("id", team_id).execute()
    return res.data

# ─────────────────────────────────────────
# 활동 API
# ─────────────────────────────────────────

@app.get("/api/teams/{team_id}/activities")
def get_activities(team_id: int):
    activities = supabase.table("activities").select("*").eq("team_id", team_id).order("activity_date", desc=True).execute().data
    total_used = sum(a["amount_used"] for a in activities)
    return {
        "activities": activities,
        "total_used": total_used,
        "balance": BUDGET_PER_TEAM - total_used
    }

@app.post("/api/activities")
def create_activity(activity: ActivityCreate, x_admin_key: str = Header(None)):
    check_admin(x_admin_key)
    res = supabase.table("activities").insert(activity.dict()).execute()
    return res.data

@app.put("/api/activities/{activity_id}")
def update_activity(activity_id: int, activity: ActivityUpdate, x_admin_key: str = Header(None)):
    check_admin(x_admin_key)
    res = supabase.table("activities").update(activity.dict(exclude_none=True)).eq("id", activity_id).execute()
    return res.data

@app.delete("/api/activities/{activity_id}")
def delete_activity(activity_id: int, x_admin_key: str = Header(None)):
    check_admin(x_admin_key)
    supabase.table("activities").delete().eq("id", activity_id).execute()
    return {"message": "삭제 완료"}

# ─────────────────────────────────────────
# 사이트 설정 API
# ─────────────────────────────────────────

@app.get("/api/settings")
def get_settings():
    res = supabase.table("settings").select("*").execute()
    return {row["key"]: row["value"] for row in (res.data or [])}

@app.put("/api/settings/{key}")
def update_setting(key: str, body: dict, x_admin_key: str = Header(None)):
    check_admin(x_admin_key)
    supabase.table("settings").upsert({"key": key, "value": body.get("value", "")}).execute()
    return {"message": "저장 완료"}
