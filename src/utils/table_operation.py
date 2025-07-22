from PyQt6.QtWidgets import QTableWidget, QTableWidgetItem

from src.utils.calculate_score import calc_pt_per_game
from src.utils.event_type import EventType


def get_data_with_support_team(table: QTableWidget) -> list[dict]:
    data: list = []
    for row in range(table.rowCount()):
        row_data: dict = {
            "band_name": table.item(row, 0).text(),
            "bonus": int(table.item(row, 1).text()),
            "achivable_max": int(table.item(row, 2).text()),
            "support_band": int(table.item(row, 3).text())
        }
        data.append(row_data)
    return data


def get_data_without_support_team(table: QTableWidget) -> list[dict]:
    data: list = []
    for row in range(table.rowCount()):
        row_data: dict = {
            "band_name": table.item(row, 0).text(),
            "bonus": int(table.item(row, 1).text()),
            "achivable_max": int(table.item(row, 2).text())
        }
        data.append(row_data)
    return data


def get_data(table: QTableWidget, event_type: EventType) -> list[dict]:
    if event_type in (
        EventType.CHALLENGE_LIVE,
        EventType.VS_LIVE,
        EventType.LIVE_GOALS,
        EventType.TEAM_LIVE_FESTIVAL,
        EventType.MEDLEY_LIVE
    ):
        data: list = get_data_without_support_team(table)
    elif event_type == EventType.MISSION_LIVE:
        data: list = get_data_with_support_team(table)
    else:
        raise RuntimeError("未知的活动类型！")
    return data


def get_score_step(event_type: EventType) -> int:
    return event_type.score_step


def set_pt_dict_with_support_team(event_type: EventType, table: QTableWidget, pt_dict: dict) -> dict:

    bands_info: list = get_data(table, event_type)
    score_step: int = get_score_step(event_type)

    for band_info in bands_info:

        band_name: str = band_info["band_name"]
        bonus: float = (band_info["bonus"] + 100) / 100
        achivable_max: int = band_info["achivable_max"]
        support_band: int = band_info["support_band"]

        pt_dict = add_pt_achieve_method(achivable_max, band_name, bonus, event_type, pt_dict, score_step, support_band)

    return pt_dict


def set_pt_dict_without_support_team(event_type: EventType, table: QTableWidget, pt_dict: dict) -> dict:

    bands_info: list = get_data(table, event_type)
    score_step: int = get_score_step(event_type)

    for band_info in bands_info:

        band_name: str = band_info["band_name"]
        bonus: float = (band_info["bonus"] + 100) / 100
        achivable_max: int = band_info["achivable_max"]
        support_band: int = 0

        pt_dict = add_pt_achieve_method(achivable_max, band_name, bonus, event_type, pt_dict, score_step, support_band)

    return pt_dict


def add_pt_achieve_method(achivable_max: int, band_name: str, bonus: float, event_type: EventType, pt_dict: dict, score_step: int, support_band: int) -> dict:
    for score in range(0, achivable_max, score_step):
        pt: int = calc_pt_per_game(score, bonus, support_band, event_type)
        lower_limit: int = score
        upper_limit: int = score + score_step - 1

        # 如果某个pt已存在某种达成方式，与已有的方式进行比较
        # 如果已有方式分数下限更高，直接跳过
        if (pt in pt_dict) and (pt_dict[pt]["lower_limit"] > lower_limit):
            continue
        # 如果新方式分数下限更高，更新达成方式
        else:
            if lower_limit > achivable_max / 3:
                pt_dict[pt]: dict = {"band_name": band_name, "lower_limit": lower_limit, "upper_limit": upper_limit}

    return pt_dict


# 遍历可达分数，正向计算用每种配队能打出哪些pt
def set_pt_dict(event_type: EventType, table: QTableWidget) -> dict:
    if not validate_table_data(table, event_type):
        raise RuntimeError("表格存在空单元格，请检查输入内容是否完整！")
    pt_dict: dict = {}
    if event_type == EventType.MISSION_LIVE:
        pt_dict = set_pt_dict_with_support_team(event_type, table, pt_dict)
    elif event_type in (
        EventType.CHALLENGE_LIVE,
        EventType.VS_LIVE,
        EventType.LIVE_GOALS,
        EventType.TEAM_LIVE_FESTIVAL,
        EventType.MEDLEY_LIVE
    ):
        pt_dict = set_pt_dict_without_support_team(event_type, table, pt_dict)
    else:
        raise RuntimeError("未知的活动类型！")
    return pt_dict


def validate_table_data(table: QTableWidget, event_type: EventType) -> bool:

    # 必填列：0: band_name, 1: bonus, 2: achivable_max
    required_columns: list = [0, 1, 2]
    if event_type == EventType.MISSION_LIVE:
        required_columns.append(3)
    for row in range(table.rowCount()):
        for col in required_columns:
            item: QTableWidgetItem = table.item(row, col)
            if item is None or item.text().strip() == "":
                return False
    return True
