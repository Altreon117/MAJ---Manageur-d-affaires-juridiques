from PyQt6.QtWidgets import QFrame, QVBoxLayout, QLabel

class CardOPJComponent(QFrame):
    def __init__(self, row_data):
        super().__init__()
        
        self.setObjectName("card_opj")
        self.setFixedHeight(80)
        
        layout = QVBoxLayout(self)
        
        texte_brut = str(row_data)
        self.lbl_test = QLabel(f"OPJ -> {texte_brut}")
        layout.addWidget(self.lbl_test)