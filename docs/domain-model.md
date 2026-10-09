# Domain model

## Candidate entities

### User
- user_id
- user_name (unique)
- user_email (unique)
- password_hash ???

### Session
Поля:
- session_id
- user_id
- started_at
- ended_at

Связи:
- User 1 ---- N Session
- содержит много Event

### Event
Поля:
- event_id
- session_id
- timestamp
- app

Связи:
- Session 1 ---- N Event

### Statistics
Поля:
- statistics_id
- user_id
- statistic_date
- total_focus_time
- idle_ratio
- top_apps
- sessions_count

Связи:
- User 1 ---- N Statistics
- связано с Session
- связано с User

## Потенциальные расширения

### App
Поля:
- app_id
- app_name 
- mode_name ???

Связи:
- связано с Event


### Mode (study, work, relax)
Поля:
- mode_id
- mode_name

Связи:
- связано с Event
- связано с Session