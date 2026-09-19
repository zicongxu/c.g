APP_STYLE = """
QWidget {
    color: #40372F;
    font-family: -apple-system, BlinkMacSystemFont, "PingFang SC";
    font-size: 14px;
}
QMainWindow, QWidget#root {
    background: #FBF7EF;
}
QScrollArea#pageScroll {
    background: #FBF7EF;
    border: 0;
}
QFrame#brandHeader {
    background: #EEF7E4;
    border: 1px solid #D8E9C8;
    border-radius: 18px;
}
QLabel#brandEyebrow {
    color: #578D25;
    font-size: 11px;
    font-weight: 800;
    letter-spacing: 1px;
}
QLabel#brandTitle {
    color: #30281F;
    font-size: 25px;
    font-weight: 800;
}
QLabel#brandSubtitle {
    color: #70675E;
    font-size: 14px;
}
QLabel#privacyPill {
    color: #4E7C27;
    background: #DDEECE;
    border-radius: 10px;
    padding: 4px 10px;
    font-size: 11px;
    font-weight: 650;
}
QLabel#mascotFrame {
    background: rgba(255, 255, 255, 150);
    border: 1px solid #D5E7C4;
    border-radius: 14px;
}
QFrame#stageBar {
    background: transparent;
    border: 0;
}
QLabel#stagePill {
    min-height: 31px;
    border-radius: 15px;
    font-size: 12px;
    font-weight: 700;
}
QLabel#stagePill[state="current"] {
    color: #FFFFFF;
    background: #7DB83B;
}
QLabel#stagePill[state="complete"] {
    color: #4E7D27;
    background: #DFEFD0;
}
QLabel#stagePill[state="upcoming"] {
    color: #978F85;
    background: #EFEAE1;
}
QLabel#stageArrow {
    color: #B8AFA3;
    font-size: 20px;
}
QLabel#secondary {
    color: #827A71;
}
QFrame#panel, QFrame#resultsPanel {
    background: #FFFFFF;
    border: 1px solid #E5DED2;
    border-radius: 12px;
}
QFrame#dropArea {
    background: #FFFDF9;
    border: 2px dashed #C9D7B9;
    border-radius: 14px;
}
QFrame#dropArea[hovered="true"] {
    background: #F7FBEF;
    border-color: #8EBB65;
}
QFrame#dropArea[pressed="true"] {
    background: #EAF4DF;
    border-color: #68A52B;
}
QFrame#dropArea:focus {
    border: 2px solid #5F9D28;
}
QFrame#dropArea[selected="true"] {
    background: #F1F8E9;
    border: 2px solid #7DB83B;
}
QFrame#dropArea[selected="true"][hovered="true"] {
    background: #EAF5DE;
    border-color: #68A52B;
}
QFrame#dropArea[active="true"] {
    background: #E8F4DB;
    border: 2px solid #68A52B;
}
QFrame#dropArea:disabled {
    background: #F2EEE7;
    border-color: #DCD5CB;
}
QLabel#dropEyebrow {
    color: #659F2B;
    font-size: 12px;
    font-weight: 800;
}
QLabel#dropTitle {
    color: #332B24;
    font-size: 17px;
    font-weight: 700;
}
QLabel#sectionTitle, QLabel#resultTitle {
    color: #332B24;
    font-weight: 700;
}
QFrame#resultItem {
    background: #FCFAF5;
    border: 1px solid #E7E0D5;
    border-radius: 9px;
}
QLabel#videoThumbnail {
    background: transparent;
    border: 0;
}
QScrollArea#resultsScroll, QWidget#resultsContainer {
    background: transparent;
    border: 0;
}
QPushButton {
    min-height: 34px;
    padding: 0 16px;
    border-radius: 8px;
    border: 1px solid #D8D0C4;
    background: #FFFDF9;
    color: #51483F;
    font-weight: 650;
}
QPushButton:hover {
    background: #F2F7EA;
    border-color: #A7C988;
}
QPushButton:pressed { background: #E7F1DC; }
QPushButton:disabled {
    color: #B5AEA5;
    background: #F2EEE7;
    border-color: #E6E0D7;
}
QPushButton#primary {
    color: #FFFFFF;
    background: #78B536;
    border-color: #78B536;
    font-weight: 800;
}
QPushButton#primary:hover {
    background: #69A82B;
    border-color: #69A82B;
}
QPushButton#danger {
    color: #B35D50;
    background: #FFF7F4;
    border-color: #EDCFC9;
}
QLineEdit, QComboBox {
    min-height: 34px;
    padding: 0 10px;
    border-radius: 8px;
    border: 1px solid #DCD4C8;
    background: #FFFDF9;
    color: #40372F;
    selection-background-color: #A9CF7E;
}
QLineEdit:focus, QComboBox:focus { border-color: #7DB83B; }
QComboBox::drop-down { border: 0; width: 24px; }
QCheckBox { spacing: 8px; }
QCheckBox::indicator {
    width: 17px;
    height: 17px;
    border-radius: 5px;
    border: 1px solid #BDB4A8;
    background: #FFFDF9;
}
QCheckBox::indicator:checked {
    background: #7DB83B;
    border-color: #7DB83B;
}
QProgressBar {
    height: 9px;
    border: 0;
    border-radius: 4px;
    background: #E9E2D7;
    text-align: center;
}
QProgressBar::chunk {
    border-radius: 4px;
    background: #7DB83B;
}
QScrollBar:vertical {
    width: 8px;
    background: transparent;
}
QScrollBar::handle:vertical {
    background: #C8D9B7;
    border-radius: 4px;
    min-height: 24px;
}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0; }
QMessageBox { background: #FBF7EF; }
QToolTip {
    color: #FFFFFF;
    background: #51483F;
    border: 0;
    padding: 5px;
}
"""
