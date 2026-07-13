import os
import sys
import csv
import toml
from PySide6.QtCore import Qt, QDir
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QSplitter, QTreeView, QTableWidget, QTableWidgetItem, QToolBar,
    QToolButton, QMenu, QMessageBox, QFileDialog, QInputDialog,
    QDialog, QLabel, QLineEdit, QPushButton, QFormLayout, QHeaderView
)
from PySide6.QtGui import QAction, QIcon, QFont

# アプリケーションのスタイルシート（モダンなダークテーマ）
MODERN_STYLE = """
QMainWindow {
    background-color: #1e1e2e;
}
QToolBar {
    background-color: #252538;
    border-bottom: 1px solid #3f3f5f;
    spacing: 8px;
    padding: 6px;
}
QToolButton {
    background-color: #313244;
    color: #cdd6f4;
    border: 1px solid #45475a;
    border-radius: 6px;
    padding: 6px 14px;
    font-size: 13px;
    font-weight: 500;
}
QToolButton:hover {
    background-color: #45475a;
    border: 1px solid #585b70;
}
QToolButton:pressed {
    background-color: #585b70;
}
QSplitter::handle {
    background-color: #313244;
}
QTreeView {
    background-color: #181825;
    color: #cdd6f4;
    border: 1px solid #313244;
    border-radius: 8px;
    padding: 5px;
    font-size: 13px;
}
QTreeView::item:hover {
    background-color: #313244;
    border-radius: 4px;
}
QTreeView::item:selected {
    background-color: #45475a;
    color: #f5c2e7;
    border-radius: 4px;
}
QTableWidget {
    background-color: #181825;
    color: #cdd6f4;
    gridline-color: #313244;
    border: 1px solid #313244;
    border-radius: 8px;
    font-size: 13px;
}
QTableWidget::item:hover {
    background-color: #313244;
}
QTableWidget::item:selected {
    background-color: #45475a;
    color: #f5c2e7;
}
QHeaderView::section {
    background-color: #252538;
    color: #cdd6f4;
    padding: 6px;
    border: 1px solid #313244;
    font-weight: bold;
}
QMenu {
    background-color: #252538;
    color: #cdd6f4;
    border: 1px solid #313244;
    border-radius: 6px;
    padding: 5px;
}
QMenu::item {
    padding: 6px 20px;
    border-radius: 4px;
}
QMenu::item:selected {
    background-color: #45475a;
}
QDialog {
    background-color: #1e1e2e;
    color: #cdd6f4;
}
QLabel {
    color: #cdd6f4;
    font-size: 13px;
}
QLineEdit {
    background-color: #181825;
    color: #cdd6f4;
    border: 1px solid #313244;
    border-radius: 4px;
    padding: 6px;
}
QPushButton {
    background-color: #313244;
    color: #cdd6f4;
    border: 1px solid #45475a;
    border-radius: 6px;
    padding: 6px 14px;
}
QPushButton:hover {
    background-color: #45475a;
}
"""

# ライトテーマ
LIGHT_STYLE = """
QMainWindow {
    background-color: #f5f5f5;
}
QToolBar {
    background-color: #ffffff;
    border-bottom: 1px solid #d0d0d0;
    spacing: 8px;
    padding: 6px;
}
QToolButton {
    background-color: #e8e8e8;
    color: #333333;
    border: 1px solid #c0c0c0;
    border-radius: 6px;
    padding: 6px 14px;
    font-size: 13px;
    font-weight: 500;
}
QToolButton:hover {
    background-color: #d0d0d0;
    border: 1px solid #a0a0a0;
}
QToolButton:pressed {
    background-color: #b8b8b8;
}
QSplitter::handle {
    background-color: #d0d0d0;
}
QTreeView {
    background-color: #ffffff;
    color: #333333;
    border: 1px solid #d0d0d0;
    border-radius: 8px;
    padding: 5px;
    font-size: 13px;
}
QTreeView::item:hover {
    background-color: #e8e8e8;
    border-radius: 4px;
}
QTreeView::item:selected {
    background-color: #cce5ff;
    color: #004080;
    border-radius: 4px;
}
QTableWidget {
    background-color: #ffffff;
    color: #333333;
    gridline-color: #d0d0d0;
    border: 1px solid #d0d0d0;
    border-radius: 8px;
    font-size: 13px;
}
QTableWidget::item:hover {
    background-color: #e8f4ff;
}
QTableWidget::item:selected {
    background-color: #cce5ff;
    color: #004080;
}
QHeaderView::section {
    background-color: #f0f0f0;
    color: #333333;
    padding: 6px;
    border: 1px solid #d0d0d0;
    font-weight: bold;
}
QMenu {
    background-color: #ffffff;
    color: #333333;
    border: 1px solid #d0d0d0;
    border-radius: 6px;
    padding: 5px;
}
QMenu::item {
    padding: 6px 20px;
    border-radius: 4px;
}
QMenu::item:selected {
    background-color: #cce5ff;
}
QDialog {
    background-color: #f5f5f5;
    color: #333333;
}
QLabel {
    color: #333333;
    font-size: 13px;
}
QLineEdit {
    background-color: #ffffff;
    color: #333333;
    border: 1px solid #d0d0d0;
    border-radius: 4px;
    padding: 6px;
}
QPushButton {
    background-color: #e8e8e8;
    color: #333333;
    border: 1px solid #c0c0c0;
    border-radius: 6px;
    padding: 6px 14px;
}
QPushButton:hover {
    background-color: #d0d0d0;
}
"""

class ConfigManager:
    def __init__(self):
        self.config_dir = os.path.join(os.environ.get('LOCALAPPDATA', ''), 'mh-csv-ed')
        self.config_path = os.path.join(self.config_dir, 'config.toml')
        self.config_data = {}
        self.load_config()

    def load_config(self):
        if os.path.exists(self.config_path):
            try:
                self.config_data = toml.load(self.config_path)
            except Exception as e:
                print(f"Failed to load config: {e}")
                self.config_data = {}
        else:
            self.config_data = {}

        # デフォルト値の設定
        if 'last_directory' not in self.config_data:
            self.config_data['last_directory'] = os.path.expanduser('~')
        if 'default_encoding' not in self.config_data:
            self.config_data['default_encoding'] = 'utf-8'
        if 'theme' not in self.config_data:
            self.config_data['theme'] = 'dark'
        if 'app_window' not in self.config_data:
            self.config_data['app_window'] = {}
        app_window = self.config_data['app_window']
        app_window.setdefault('x', 0)
        app_window.setdefault('y', 0)
        app_window.setdefault('width', 1000)
        app_window.setdefault('height', 600)

    def save_config(self):
        try:
            os.makedirs(self.config_dir, exist_ok=True)
            with open(self.config_path, 'w', encoding='utf-8') as f:
                toml.dump(self.config_data, f)
        except Exception as e:
            print(f"Failed to save config: {e}")

    def get(self, key, default=None):
        return self.config_data.get(key, default)

    def set(self, key, value):
        self.config_data[key] = value
        self.save_config()


class SettingDialog(QDialog):
    def __init__(self, config_manager, parent=None):
        super().__init__(parent)
        self.config_manager = config_manager
        self.setWindowTitle("設定")
        self.resize(400, 150)
        self.init_ui()

    def init_ui(self):
        layout = QFormLayout(self)
        
        self.dir_input = QLineEdit(self)
        self.dir_input.setText(self.config_manager.get('last_directory'))
        
        dir_layout = QHBoxLayout()
        dir_layout.addWidget(self.dir_input)
        self.browse_btn = QPushButton("参照...", self)
        self.browse_btn.clicked.connect(self.browse_dir)
        dir_layout.addWidget(self.browse_btn)
        
        layout.addRow("デフォルトディレクトリ:", dir_layout)

        self.encoding_input = QLineEdit(self)
        self.encoding_input.setText(self.config_manager.get('default_encoding'))
        layout.addRow("デフォルトエンコーディング:", self.encoding_input)

        buttons_layout = QHBoxLayout()
        self.save_btn = QPushButton("保存", self)
        self.save_btn.clicked.connect(self.save_settings)
        self.cancel_btn = QPushButton("キャンセル", self)
        self.cancel_btn.clicked.connect(self.reject)
        
        buttons_layout.addStretch()
        buttons_layout.addWidget(self.save_btn)
        buttons_layout.addWidget(self.cancel_btn)
        layout.addRow(buttons_layout)

    def browse_dir(self):
        dir_path = QFileDialog.getExistingDirectory(self, "デフォルトディレクトリの選択", self.dir_input.text())
        if dir_path:
            self.dir_input.setText(dir_path)

    def save_settings(self):
        self.config_manager.set('last_directory', self.dir_input.text())
        self.config_manager.set('default_encoding', self.encoding_input.text())
        self.accept()


class CsvEdMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("csv-ed")
        
        self.config_manager = ConfigManager()
        self.current_csv_path = None
        self.current_encoding = self.config_manager.get('default_encoding', 'utf-8')
        self.current_theme = self.config_manager.get('theme', 'dark')
        
        self.init_ui()
        self.apply_theme(self.current_theme)
        self.load_directory(self.config_manager.get('last_directory'))
        
        # 保存済みウィンドウジオメトリを復元
        self.restore_window_geometry()
    
    def restore_window_geometry(self):
        win = self.config_manager.get('app_window', {})
        x = win.get('x', 0)
        y = win.get('y', 0)
        w = win.get('width', 1000)
        h = win.get('height', 600)
        self.setGeometry(x, y, w, h)
    
    def closeEvent(self, event):
        # ウィンドウ終了時にジオメトリを保存
        geo = self.geometry()
        self.config_manager.set('app_window', {
            'x': geo.x(),
            'y': geo.y(),
            'width': geo.width(),
            'height': geo.height()
        })
        super().closeEvent(event)

    def init_ui(self):
        # ツールバーの構築
        self.toolbar = QToolBar("Main Toolbar", self)
        self.toolbar.setMovable(False)
        self.addToolBar(self.toolbar)

        # menu ボタン
        self.menu_btn = QToolButton(self)
        self.menu_btn.setText("menu")
        self.menu_menu = QMenu(self)
        self.new_action = QAction("新規CSV作成", self)
        self.new_action.triggered.connect(self.new_csv)
        self.open_action = QAction("CSVファイルを開く...", self)
        self.open_action.triggered.connect(self.open_csv_dialog)
        self.exit_action = QAction("終了", self)
        self.exit_action.triggered.connect(self.close)
        self.menu_menu.addAction(self.new_action)
        self.menu_menu.addAction(self.open_action)
        self.menu_menu.addSeparator()
        # テーマ切替サブメニュー
        self.theme_menu = QMenu("テーマ", self)
        self.dark_mode_action = QAction("ダークモード", self)
        self.dark_mode_action.setCheckable(True)
        self.dark_mode_action.setChecked(self.current_theme == 'dark')
        self.dark_mode_action.triggered.connect(lambda: self.apply_theme('dark'))
        self.light_mode_action = QAction("ライトモード", self)
        self.light_mode_action.setCheckable(True)
        self.light_mode_action.setChecked(self.current_theme == 'light')
        self.light_mode_action.triggered.connect(lambda: self.apply_theme('light'))
        self.theme_menu.addAction(self.dark_mode_action)
        self.theme_menu.addAction(self.light_mode_action)
        self.menu_menu.addMenu(self.theme_menu)
        self.menu_menu.addSeparator()
        self.menu_menu.addAction(self.exit_action)
        self.menu_btn.setMenu(self.menu_menu)
        self.menu_btn.setPopupMode(QToolButton.InstantPopup)
        self.toolbar.addWidget(self.menu_btn)

        # UpDir ボタン
        self.updir_btn = QToolButton(self)
        self.updir_btn.setText("UpDir")
        self.updir_btn.clicked.connect(self.go_up_dir)
        self.toolbar.addWidget(self.updir_btn)

        # save ボタン
        self.save_btn = QToolButton(self)
        self.save_btn.setText("save")
        self.save_btn.clicked.connect(self.save_csv)
        self.toolbar.addWidget(self.save_btn)

        # テーマ切替ボタン
        self.theme_btn = QToolButton(self)
        self.theme_btn.setText("☀ ライト")
        self.theme_btn.clicked.connect(self.toggle_theme)
        self.toolbar.addWidget(self.theme_btn)

        # 設定 ボタン
        self.config_btn = QToolButton(self)
        self.config_btn.setText("設定")
        self.config_btn.clicked.connect(self.open_settings)
        self.toolbar.addWidget(self.config_btn)

        # メインエリア (QSplitter)
        self.splitter = QSplitter(Qt.Horizontal, self)
        self.setCentralWidget(self.splitter)

        # 左ペイン: フォルダ・ファイルリスト
        self.left_widget = QWidget(self)
        left_layout = QVBoxLayout(self.left_widget)
        left_layout.setContentsMargins(0, 0, 0, 0)
        
        self.path_label = QLabel(self)
        left_layout.addWidget(self.path_label)

        self.tree_view = QTreeView(self)
        self.tree_view.setHeaderHidden(True)
        left_layout.addWidget(self.tree_view)
        
        self.splitter.addWidget(self.left_widget)

        # 右ペイン: CSV編集グリッド
        self.right_widget = QWidget(self)
        right_layout = QVBoxLayout(self.right_widget)
        right_layout.setContentsMargins(0, 0, 0, 0)

        self.table_widget = QTableWidget(self)
        self.table_widget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.table_widget.customContextMenuRequested.connect(self.show_table_context_menu)
        right_layout.addWidget(self.table_widget)

        self.splitter.addWidget(self.right_widget)

        # ペイン幅の初期比率を設定
        self.splitter.setSizes([300, 700])

        # ファイルシステムのモデル設定
        from PySide6.QtWidgets import QFileSystemModel
        self.file_model = QFileSystemModel()
        self.file_model.setNameFilters(["*.csv"])
        self.file_model.setNameFilterDisables(False)
        self.tree_view.setModel(self.file_model)
        
        # 不要な列を非表示にして名前のみ表示する
        for i in range(1, self.file_model.columnCount()):
            self.tree_view.hideColumn(i)

        self.tree_view.doubleClicked.connect(self.on_item_double_clicked)

    def load_directory(self, path):
        if not os.path.exists(path):
            path = os.path.expanduser('~')
        
        path = os.path.abspath(path)
        self.current_dir = path
        self.path_label.setText(f"  現在のフォルダ: {os.path.basename(path) or path}")
        self.file_model.setRootPath(path)
        self.tree_view.setRootIndex(self.file_model.index(path))
        self.config_manager.set('last_directory', path)

    def on_item_double_clicked(self, index):
        path = self.file_model.filePath(index)
        if self.file_model.isDir(index):
            self.load_directory(path)
        else:
            if path.lower().endswith('.csv'):
                self.load_csv_file(path)

    def is_root_directory(self, path):
        """Check if the given path is a root directory (e.g., C:\\)"""
        return os.path.dirname(path) == path

    def get_available_drives(self):
        """Get available drives on the system"""
        drives = []
        if sys.platform == "win32":
            import string
            for letter in string.ascii_uppercase:
                drive = f"{letter}:\\"
                if os.path.exists(drive):
                    drives.append(drive)
        else:
            # Unix: root is "/"
            if os.path.exists("/"):
                drives.append("/")
        return drives

    def show_drive_list_dialog(self):
        """Show a dialog to select a drive from available drives"""
        drives = self.get_available_drives()
        if not drives:
            return

        from PySide6.QtWidgets import QInputDialog
        item, ok = QInputDialog.getItem(
            self, "ドライブの選択", "移動先のドライブを選択してください:", drives, 0, False
        )
        if ok and item:
            self.load_directory(item)

    def go_up_dir(self):
        if self.is_root_directory(self.current_dir):
            self.show_drive_list_dialog()
        else:
            parent_dir = os.path.dirname(self.current_dir)
            if parent_dir and parent_dir != self.current_dir:
                self.load_directory(parent_dir)

    def load_csv_file(self, path):
        self.current_csv_path = path
        encodings = [self.config_manager.get('default_encoding', 'utf-8'), 'utf-8', 'cp932', 'utf-8-sig']
        
        data = []
        loaded = False
        for enc in encodings:
            try:
                with open(path, 'r', encoding=enc, newline='') as f:
                    reader = csv.reader(f)
                    data = list(reader)
                    self.current_encoding = enc
                    loaded = True
                    break
            except Exception:
                continue

        if not loaded:
            QMessageBox.critical(self, "エラー", "CSVファイルの読み込みに失敗しました。対応していない文字コードの可能性があります。")
            return

        self.populate_table(data)
        self.setWindowTitle(f"csv-ed - {os.path.basename(path)}")

    def populate_table(self, data):
        self.table_widget.clear()
        if not data:
            self.table_widget.setRowCount(0)
            self.table_widget.setColumnCount(0)
            return

        row_count = len(data)
        col_count = max(len(row) for row in data) if data else 0

        self.table_widget.setRowCount(row_count)
        self.table_widget.setColumnCount(col_count)

        for row_idx, row in enumerate(data):
            for col_idx, value in enumerate(row):
                item = QTableWidgetItem(value)
                self.table_widget.setItem(row_idx, col_idx, item)

        # ヘッダーのリサイズモード設定
        self.table_widget.horizontalHeader().setSectionResizeMode(QHeaderView.Interactive)

    def save_csv(self):
        if not self.current_csv_path:
            # 名前を付けて保存
            path, _ = QFileDialog.getSaveFileName(self, "CSVファイルの保存", self.current_dir, "CSV Files (*.csv)")
            if not path:
                return
            self.current_csv_path = path

        try:
            with open(self.current_csv_path, 'w', encoding=self.current_encoding, newline='') as f:
                writer = csv.writer(f)
                for r in range(self.table_widget.rowCount()):
                    row_data = []
                    for c in range(self.table_widget.columnCount()):
                        item = self.table_widget.item(r, c)
                        row_data.append(item.text() if item else "")
                    writer.writerow(row_data)
            
            QMessageBox.information(self, "成功", "ファイルを保存しました。")
            self.setWindowTitle(f"csv-ed - {os.path.basename(self.current_csv_path)}")
            # 左ペインのリストを更新
            self.load_directory(self.current_dir)
        except Exception as e:
            QMessageBox.critical(self, "エラー", f"ファイルの保存中にエラーが発生しました:\n{e}")

    def new_csv(self):
        self.current_csv_path = None
        self.current_encoding = self.config_manager.get('default_encoding', 'utf-8')
        self.setWindowTitle("csv-ed - 新規ファイル")
        
        # デフォルトで3行3列の空のグリッドを作成
        self.table_widget.clear()
        self.table_widget.setRowCount(3)
        self.table_widget.setColumnCount(3)
        for r in range(3):
            for c in range(3):
                self.table_widget.setItem(r, c, QTableWidgetItem(""))

    def open_csv_dialog(self):
        path, _ = QFileDialog.getOpenFileName(self, "CSVファイルを開く", self.current_dir, "CSV Files (*.csv)")
        if path:
            self.load_csv_file(path)

    def open_settings(self):
        dialog = SettingDialog(self.config_manager, self)
        if dialog.exec() == QDialog.Accepted:
            # 設定が変更されたら、ディレクトリを再読み込み
            self.load_directory(self.config_manager.get('last_directory'))

    def show_table_context_menu(self, pos):
        menu = QMenu(self)
        
        insert_row_action = QAction("上に行を挿入", self)
        insert_row_action.triggered.connect(self.insert_row)
        menu.addAction(insert_row_action)

        delete_row_action = QAction("行を削除", self)
        delete_row_action.triggered.connect(self.delete_row)
        menu.addAction(delete_row_action)

        menu.addSeparator()

        insert_col_action = QAction("左に列を挿入", self)
        insert_col_action.triggered.connect(self.insert_column)
        menu.addAction(insert_col_action)

        delete_col_action = QAction("列を削除", self)
        delete_col_action.triggered.connect(self.delete_column)
        menu.addAction(delete_col_action)

        menu.exec_(self.table_widget.viewport().mapToGlobal(pos))

    def insert_row(self):
        current_row = self.table_widget.currentRow()
        if current_row == -1:
            current_row = self.table_widget.rowCount()
        self.table_widget.insertRow(current_row)
        # 空のアイテムで初期化
        for c in range(self.table_widget.columnCount()):
            self.table_widget.setItem(current_row, c, QTableWidgetItem(""))

    def delete_row(self):
        current_row = self.table_widget.currentRow()
        if current_row != -1:
            self.table_widget.removeRow(current_row)

    def insert_column(self):
        current_col = self.table_widget.currentColumn()
        if current_col == -1:
            current_col = self.table_widget.columnCount()
        self.table_widget.insertColumn(current_col)
        # 空のアイテムで初期化
        for r in range(self.table_widget.rowCount()):
            self.table_widget.setItem(r, current_col, QTableWidgetItem(""))

    def delete_column(self):
        current_col = self.table_widget.currentColumn()
        if current_col != -1:
            self.table_widget.removeColumn(current_col)

    def apply_theme(self, theme):
        """テーマを適用する"""
        self.current_theme = theme
        self.config_manager.set('theme', theme)
        
        # アプリケーション全体にスタイルシートを適用
        if theme == 'light':
            app = QApplication.instance()
            if app:
                app.setStyleSheet(LIGHT_STYLE)
            self.theme_btn.setText("🌙 ダーク")
            self.light_mode_action.setChecked(True)
            self.dark_mode_action.setChecked(False)
        else:
            app = QApplication.instance()
            if app:
                app.setStyleSheet(MODERN_STYLE)
            self.theme_btn.setText("☀ ライト")
            self.dark_mode_action.setChecked(True)
            self.light_mode_action.setChecked(False)

    def toggle_theme(self):
        """テーマを切り替える"""
        if self.current_theme == 'dark':
            self.apply_theme('light')
        else:
            self.apply_theme('dark')


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(MODERN_STYLE)
    
    # フォントの設定 (Windows向けにメイリオ等の標準日本語フォントを指定)
    font = QFont("Segoe UI", 9)
    if sys.platform == "win32":
        font = QFont("Yu Gothic UI", 9)
    app.setFont(font)
    
    window = CsvEdMainWindow()
    window.show()
    sys.exit(app.exec())
