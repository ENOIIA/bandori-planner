from math import floor
from src.utils.event_type import EventType


# cp活（非歌榜）
def challenge_live_pt(score: int, bonus: float) -> int:
    pt: int = floor((70 + floor(score / 50000)) * bonus)
    return pt


# 对邦
def vs_live_pt(score: int) -> int:
    pt: int = floor(100 + floor(score / 6500))
    return pt


# EX试炼
def live_goals_pt(score: int, bonus: float) -> int:
    pt: int = floor((130 + floor(score / 26000)) * bonus)
    return pt


# 任务Live
def mission_live_pt(score: int, bonus: float, support_band: int) -> int:
    pt = floor((120 + floor(score / 15000)) * bonus) + floor(support_band / 3000)
    return pt


# 5v5
def team_live_festival_pt(score: int) -> int:
    pt: int = 100 + 50 + floor(score / 6500)
    return pt


# 组曲
def medley_live_pt(score: int) -> int:
    pt: int = 30 + floor(score / 18500)
    return pt


# 综合
def calc_pt_per_game(score: int, bonus: float, support_band: int, event_type: EventType) -> int:
    if event_type == EventType.CHALLENGE_LIVE:
        return challenge_live_pt(score, bonus)
    elif event_type == EventType.VS_LIVE:
        return vs_live_pt(score)
    elif event_type == EventType.LIVE_GOALS:
        return live_goals_pt(score, bonus)
    elif event_type == EventType.MISSION_LIVE:
        return mission_live_pt(score, bonus, support_band)
    elif event_type == EventType.TEAM_LIVE_FESTIVAL:
        return team_live_festival_pt(score)
    elif event_type == EventType.MEDLEY_LIVE:
        return medley_live_pt(score)
    else:
        raise RuntimeError("未知的活动类型！")
