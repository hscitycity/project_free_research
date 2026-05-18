-- ======================================================
-- 화성시 자유주제 정책연구모임 2026 — Supabase Schema
-- Supabase SQL Editor 에서 순서대로 실행하세요
-- ======================================================

-- 1. 공지사항 테이블
CREATE TABLE IF NOT EXISTS notices (
  id         SERIAL PRIMARY KEY,
  title      TEXT    NOT NULL,
  content    TEXT    NOT NULL DEFAULT '',
  category   TEXT    NOT NULL DEFAULT '일반',  -- '일반' | '중요' | '신규'
  is_pinned  BOOLEAN NOT NULL DEFAULT FALSE,
  created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- 2. 연구모임 팀 테이블
CREATE TABLE IF NOT EXISTS teams (
  id               SERIAL PRIMARY KEY,
  order_num        INTEGER NOT NULL,
  name             TEXT    NOT NULL,
  task             TEXT    NOT NULL DEFAULT '',
  color            TEXT    NOT NULL DEFAULT '#43A047',
  "desc"           TEXT    NOT NULL DEFAULT '',
  card_submissions JSONB   NOT NULL DEFAULT '{}',
  created_at       TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- 3. 활동 내역 테이블
CREATE TABLE IF NOT EXISTS activities (
  id            SERIAL PRIMARY KEY,
  team_id       INTEGER REFERENCES teams(id) ON DELETE CASCADE,
  activity_date DATE    NOT NULL,
  title         TEXT    NOT NULL,
  description   TEXT    NOT NULL DEFAULT '',
  attendees     INTEGER NOT NULL DEFAULT 0,
  amount_used   INTEGER NOT NULL DEFAULT 0,
  created_at    TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- 4. 사이트 설정 테이블 (사이드바 일정/타임라인)
CREATE TABLE IF NOT EXISTS settings (
  key        TEXT PRIMARY KEY,
  value      TEXT NOT NULL DEFAULT ''
);

-- ======================================================
-- 5. 연구모임 팀 초기 데이터 삽입
-- ======================================================
INSERT INTO teams (order_num, name, task, color, "desc", card_submissions) VALUES
(1, 'RE ; PARK',
 '공원 친화형 이륜차 차단시설 표준모델 개발',
 '#2E7D32', '', '{}'),

(2, 'H-UP',
 '화성형 지구단위계획 수립을 위한 운영체계 연구',
 '#1565C0', '', '{}'),

(3, '보타닉가드',
 'AI기반 스마트 정원관리 구축방안',
 '#558B2F', '', '{}'),

(4, '트램타고 도시산책',
 '트램 노선을 중심으로 한 도시공간 재편 전략 마련',
 '#6D4C41', '', '{}'),

(5, '도시공간 안전연구회',
 '공장도시의 숨은 위험, "공간안전"으로 답하다: 비도시 공장밀집지역 공간안전 관리모델 구축 연구',
 '#C62828', '', '{}'),

(6, '따로 또 같이',
 '지역공동체 활성화를 위한 공공지원제도의 통합적 운용 방안',
 '#6A1FA2', '', '{}'),

(7, 'AIM',
 'AI시대에 대응하는 지속가능한 AI교육 운영모델 연구',
 '#0277BD', '', '{}'),

(8, '비봉 습지 LIGHT ON',
 '비봉습지공원 핫플 프로젝트',
 '#00838F', '', '{}'),

(9, 'TOPTIER 재정',
 '화성시 보통교부세 교부단체 전환을 위한 재정확충 전략 연구',
 '#E65100', '', '{}')

ON CONFLICT DO NOTHING;
