import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QComboBox, QMessageBox
)
from PyQt5.QtCore import Qt

epsilon_0 = 8.8541878128e-12

class CapacitorWindow(QMainWindow):
    """
    Главное окно, позволяющее ввести:
      - Напряжение (В)
      - Расстояние между пластинами (м)
      - Относительную диэлектрическую проницаемость
      - Режим (подключён или отключён от источника)
    После ввода данных и нажатия кнопки "Рассчитать" отображается
    напряжённость E и заряд Q.
    """
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Расчёт плоского конденсатора")
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        self.input_layout = QHBoxLayout()
        self.voltage_label = QLabel("Напряжение (В):")
        self.voltage_edit = QLineEdit()
        self.distance_label = QLabel("Расстояние (м):")
        self.distance_edit = QLineEdit()
        self.er_label = QLabel("Диэлектрик (εr):")
        self.er_edit = QLineEdit()
        self.mode_label = QLabel("Источник:")
        self.mode_combo = QComboBox()
        self.mode_combo.addItems(["Подключён", "Отключён"])
        self.input_layout.addWidget(self.voltage_label)
        self.input_layout.addWidget(self.voltage_edit)
        self.input_layout.addWidget(self.distance_label)
        self.input_layout.addWidget(self.distance_edit)
        self.input_layout.addWidget(self.er_label)
        self.input_layout.addWidget(self.er_edit)
        self.input_layout.addWidget(self.mode_label)
        self.input_layout.addWidget(self.mode_combo)
        self.layout.addLayout(self.input_layout)

        self.calc_button = QPushButton("Рассчитать")
        self.calc_button.clicked.connect(self.calculate)
        self.layout.addWidget(self.calc_button)

        self.result_label = QLabel("")
        self.result_label.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.layout.addWidget(self.result_label)

    def calculate(self):
        """
        Считывает данные, вычисляет напряжённость E и заряд Q.
        Если конденсатор подключён к источнику, напряжение не меняется, а заряд определяется C*U.
        Если конденсатор отключён, заряд остаётся таким же, как при начальной зарядке в вакууме,
        но при введении диэлектрика напряжение падает, и поле меняется.
        """
        try:
            U = float(self.voltage_edit.text())
            d = float(self.distance_edit.text())
            er = float(self.er_edit.text())
        except ValueError:
            QMessageBox.warning(self, "Ошибка", "Неверный формат входных данных.")
            return
        if d <= 0 or er <= 0:
            QMessageBox.warning(self, "Ошибка", "Дистанция и εr должны быть положительными.")
            return
        mode = self.mode_combo.currentText()
        if mode == "Подключён":
            Q = epsilon_0 * er * (1.0 / d) * U
            E = U / d
        else:
            Q_initial = epsilon_0 * (1.0 / d) * U
            U_final = Q_initial / (epsilon_0 * er * (1.0 / d))
            Q = Q_initial
            E = U_final / d
        self.result_label.setText(
            f"Напряжённость E = {E:.4e} В/м\n"
            f"Заряд Q = {Q:.4e} Кл"
        )

def main():
    """
    Создаёт приложение, окно CapacitorWindow и запускает основной цикл.
    """
    app = QApplication(sys.argv)
    window = CapacitorWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
