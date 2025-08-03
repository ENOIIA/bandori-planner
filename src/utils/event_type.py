from enum import Enum


class EventType(Enum):
    CHALLENGE_LIVE = ("challenge_live", 50000)
    VS_LIVE = ("vs_live", 6500)
    LIVE_GOALS = ("live_goals", 26000)
    MISSION_LIVE = ("mission_live", 15000)
    TEAM_LIVE_FESTIVAL = ("team_live_festival", 6500)
    MEDLEY_LIVE = ("medley_live", 18500)

    @property
    def type_name(self) -> str:
        return self.value[0]

    @property
    def score_step(self) -> int:
        return self.value[1]

    @property
    def requires_support(self) -> bool:
        # 只有任务 Live 需要 support_band 数据
        return self == EventType.MISSION_LIVE
