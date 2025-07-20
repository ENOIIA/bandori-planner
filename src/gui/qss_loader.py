from PyQt6.QtCore import QFile, QTextStream


class QSSLoader:
    def __init__(self):
        pass

    @staticmethod
    def read_qss_file(qss_file_name):
        file = QFile(qss_file_name)
        if file.open(QFile.OpenModeFlag.ReadOnly | QFile.OpenModeFlag.Text):
            stream = QTextStream(file)
            content = stream.readAll()
            file.close()
            return content
        return ''
