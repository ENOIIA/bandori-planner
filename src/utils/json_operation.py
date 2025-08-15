import json
import os
from PyQt6.QtWidgets import QTableWidget, QFileDialog, QTableWidgetItem, QWidget, QHBoxLayout, QPushButton

from src.utils.event_type import EventType
from src.utils.table_operation import get_data


def save_band_as_json(table: QTableWidget) -> None:
    bands: list[dict] = get_data(table, EventType.MISSION_LIVE)
    bands_json = json.dumps(bands, indent=4, ensure_ascii=False)
    
    file_path, _ = QFileDialog.getSaveFileName(
        table.parent(),
        "保存乐队数据",
        os.path.expanduser("./"),
        "JSON Files (*.json)"
    )
    
    if file_path:
        if not file_path.endswith('.json'):
            file_path += '.json'
            
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(bands_json)
        except Exception as e:
            print(f"保存文件时出错: {e}")


def load_band_from_json(table: QTableWidget) -> None:
    file_path, _ = QFileDialog.getOpenFileName(
        table.parent(),
        "打开乐队数据",
        os.path.expanduser("./"),
        "JSON Files (*.json)"
    )

    if not file_path:
        return

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            bands = json.load(f)
    except Exception as e:
        print(f"读取文件时出错: {e}")
        return

    table.setRowCount(0)

    for band in bands:
        row = table.rowCount()
        table.insertRow(row)
        for col, value in enumerate(band.values()):
            table.setItem(row, col, QTableWidgetItem(str(value)))

        btn_widget = QWidget()
        btn_layout = QHBoxLayout()

        delete_btn = QPushButton("删除")

        delete_btn.clicked.connect(lambda _, r=row: table.removeRow(r))

        btn_layout.addWidget(delete_btn)
        btn_widget.setLayout(btn_layout)

        table.setCellWidget(row, 4, btn_widget)
            