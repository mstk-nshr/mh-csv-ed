import os
import sys
import csv
import toml
from PySide6.QtCore import Qt, QDir, QTimer, QByteArray, QEvent
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTreeView, QTableWidget, QTableWidgetItem, QToolBar,
    QToolButton, QMenu, QMessageBox, QFileDialog, QInputDialog,
    QDialog, QLabel, QLineEdit, QPushButton, QFormLayout, QHeaderView,
    QDockWidget, QTabBar
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
QDockWidget {
    color: #cdd6f4;
    titlebar-close-icon: url(none);
}
QDockWidget::title {
    background-color: #252538;
    color: #cdd6f4;
    padding: 6px;
    border-bottom: 1px solid #3f3f5f;
    font-weight: bold;
}
QDockWidget::close-button, QDockWidget::float-button {
    background-color: #313244;
    border: 1px solid #45475a;
    border-radius: 3px;
    padding: 2px;
}
QDockWidget::close-button:hover, QDockWidget::float-button:hover {
    background-color: #45475a;
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
QTableCornerButton::section {
    background-color: #313244; 
    border: none;
}
QHeaderView { background-color: #313244; }
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
QTabBar::tab {
    background-color: #313244;
    color: #cdd6f4;
    border: 1px solid #45475a;
    border-top: none;
    border-bottom-left-radius: 4px;
    border-bottom-right-radius: 4px;
    padding: 6px 14px;
    font-size: 13px;
}
QTabBar::tab:hover {
    background-color: #45475a;
    color: #ffffff;
    border-color: #585b70;
}
QTabBar::tab:selected {
    background-color: #1e1e2e;
    color: #f5c2e7;
    border-top: 4px solid #cba6f7;
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
QDockWidget {
    color: #333333;
    titlebar-close-icon: url(none);
}
QDockWidget::title {
    background-color: #f0f0f0;
    color: #333333;
    padding: 6px;
    border-bottom: 1px solid #d0d0d0;
    font-weight: bold;
}
QDockWidget::close-button, QDockWidget::float-button {
    background-color: #e8e8e8;
    border: 1px solid #c0c0c0;
    border-radius: 3px;
    padding: 2px;
}
QDockWidget::close-button:hover, QDockWidget::float-button:hover {
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
QTableCornerButton::section {
    background-color: #d0d0d0; 
    border: none;
}
QHeaderView { background-color: #d0d0d0; }
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
QTabBar::tab {
    background-color: #e8e8e8;
    color: #333333;
    border: 1px solid #c0c0c0;
    border-top: none;
    border-bottom-left-radius: 4px;
    border-bottom-right-radius: 4px;
    padding: 6px 14px;
    font-size: 13px;
}
QTabBar::tab:hover {
    background-color: #d0d0d0;
    color: #000000;
    border-color: #a0a0a0;
}
QTabBar::tab:selected {
    background-color: #ffffff;
    color: #000000;
    border-top: 4px solid #4a90d9;
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


class CsvTabData:
    """ドックごとのメタデータを保持する"""
    def __init__(self, dock_widget, file_path=None, encoding='utf-8'):
        self.dock_widget = dock_widget
        self.table_widget = dock_widget.csv_table
        self.file_path = file_path
        self.encoding = encoding
        self.is_edited = False
        self.is_transposed = False
        self._base_title = dock_widget.windowTitle()


class CsvDockWidget(QDockWidget):
    """CSVファイルを表示するドッキング可能なウィジェット"""
    def __init__(self, title, table_widget, main_window):
        super().__init__(title)
        self.setObjectName(f"csv_dock_{title}")
        self.main_window = main_window
        self.csv_table = table_widget
        self.setWidget(table_widget)
        self.setFeatures(
            QDockWidget.DockWidgetClosable |
            QDockWidget.DockWidgetMovable |
            QDockWidget.DockWidgetFloatable
        )
        self.setAllowedAreas(
            Qt.LeftDockWidgetArea |
            Qt.RightDockWidgetArea |
            Qt.TopDockWidgetArea |
            Qt.BottomDockWidgetArea
        )
        self.setMinimumSize(200, 200)
        # テーブルのシグナルをメインウィンドウに転送
        table_widget.setContextMenuPolicy(Qt.CustomContextMenu)
        table_widget.customContextMenuRequested.connect(main_window.show_table_context_menu)
        table_widget.cellChanged.connect(main_window._on_cell_changed)

    def closeEvent(self, event):
        self.main_window._on_dock_close_request(self, event)


class CsvEdMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("mh-csv-ed v0.1.0")
        self.setDockNestingEnabled(True)
        
        self.config_manager = ConfigManager()
        self.current_theme = self.config_manager.get('theme', 'dark')
        
        # ドック管理
        self.tab_data_map = {}       # CsvDockWidget -> CsvTabData
        self._active_dock = None     # 現在アクティブなCsvDockWidget
        self._reference_dock = None  # タブ化の基準となるドック
        
        # シングルクリック / ダブルクリック 判別用タイマー
        self.click_timer = QTimer(self)
        self.click_timer.setSingleShot(True)
        self.click_timer.timeout.connect(self._process_single_click)
        self._pending_click_path = None
        
        self.init_ui()
        self.apply_theme(self.current_theme)
        self.load_directory(self.config_manager.get('last_directory'))
        
        # フォーカス変更を追跡してアクティブなドックを特定
        QApplication.instance().focusChanged.connect(self._on_focus_changed)

        # マウスホイール（中ボタン）クリックでタブを閉じるためのイベントフィルター
        QApplication.instance().installEventFilter(self)
        
        # 空の初期ドックを追加
        self._add_empty_dock()
        
        # 保存済みウィンドウジオメトリを復元
        self.restore_window_geometry()
    
    def restore_window_geometry(self):
        win = self.config_manager.get('app_window', {})
        x = win.get('x', 0)
        y = win.get('y', 0)
        w = win.get('width', 1000)
        h = win.get('height', 600)
        self.setGeometry(x, y, w, h)
        # ドックレイアウト（サイズ・位置）を復元
        dock_state_b64 = win.get('dock_state')
        if dock_state_b64:
            state = QByteArray.fromBase64(dock_state_b64.encode('utf-8'))
            self.restoreState(state)
    
    def closeEvent(self, event):
        # 編集済みドックの確認
        edited_docks = []
        for dock, tab_data in self.tab_data_map.items():
            if tab_data.is_edited:
                edited_docks.append(dock.windowTitle())

        if edited_docks:
            dock_list = "\n".join(f"  • {t}" for t in edited_docks)
            reply = QMessageBox.question(
                self, "確認",
                f"以下のファイルが編集されています。保存せずに終了しますか？\n{dock_list}",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )
            if reply == QMessageBox.No:
                event.ignore()
                return

        # ウィンドウ終了時にジオメトリとドックレイアウトを保存
        geo = self.geometry()
        dock_state = self.saveState().toBase64().data().decode('utf-8')
        self.config_manager.set('app_window', {
            'x': geo.x(),
            'y': geo.y(),
            'width': geo.width(),
            'height': geo.height(),
            'dock_state': dock_state
        })
        super().closeEvent(event)

    def init_ui(self):
        # ツールバーの構築
        self.toolbar = QToolBar("Main Toolbar", self)
        self.toolbar.setObjectName("main_toolbar")
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

        # 行列反転 ボタン
        self.transpose_btn = QToolButton(self)
        self.transpose_btn.setText("行列反転")
        self.transpose_btn.clicked.connect(self.transpose_table)
        self.toolbar.addWidget(self.transpose_btn)

        # 左ペイン: フォルダ・ファイルリスト（QDockWidget）
        self.left_dock = QDockWidget("ファイル一覧", self)
        self.left_dock.setObjectName("file_list_dock")
        self.left_dock.setFeatures(
            QDockWidget.DockWidgetMovable |
            QDockWidget.DockWidgetFloatable |
            QDockWidget.DockWidgetClosable
        )
        self.left_dock.setAllowedAreas(
            Qt.LeftDockWidgetArea |
            Qt.RightDockWidgetArea |
            Qt.TopDockWidgetArea |
            Qt.BottomDockWidgetArea
        )
        self.left_dock.setMinimumSize(200, 200)
        self.left_widget = QWidget(self)
        left_layout = QVBoxLayout(self.left_widget)
        left_layout.setContentsMargins(0, 0, 0, 0)
        
        self.path_label = QLabel(self)
        left_layout.addWidget(self.path_label)

        self.tree_view = QTreeView(self)
        self.tree_view.setHeaderHidden(True)
        left_layout.addWidget(self.tree_view)
        
        self.left_dock.setWidget(self.left_widget)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.left_dock)

        # ファイルシステムのモデル設定
        from PySide6.QtWidgets import QFileSystemModel
        self.file_model = QFileSystemModel()
        self.file_model.setNameFilters(["*.csv"])
        self.file_model.setNameFilterDisables(False)
        self.tree_view.setModel(self.file_model)
        
        # 不要な列を非表示にして名前のみ表示する
        for i in range(1, self.file_model.columnCount()):
            self.tree_view.hideColumn(i)

        # シングルクリック / ダブルクリック の両方を処理
        self.tree_view.clicked.connect(self.on_item_clicked)
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

    def on_item_clicked(self, index):
        """シングルクリック: タイマーを起動してダブルクリックと区別する"""
        path = self.file_model.filePath(index)
        if not self.file_model.isDir(index) and path.lower().endswith('.csv'):
            self._pending_click_path = path
            self.click_timer.start(250)  # 250ms以内にダブルクリックがなければシングルクリック処理

    def on_item_double_clicked(self, index):
        """ダブルクリック: タイマーをキャンセルし、常に新規ドックを追加"""
        self.click_timer.stop()
        self._pending_click_path = None
        path = self.file_model.filePath(index)
        if self.file_model.isDir(index):
            self.load_directory(path)
        else:
            if path.lower().endswith('.csv'):
                self._open_csv_in_new_dock(path)

    def _process_single_click(self):
        """シングルクリックの実際の処理"""
        path = self._pending_click_path
        self._pending_click_path = None
        if path is None:
            return

        current_data = self._current_tab_data()
        if current_data is not None and current_data.is_edited:
            # 現在のドックが編集済み → 閉じずに新規ドックを追加
            self._open_csv_in_new_dock(path)
        else:
            # 現在のドックが未編集 → 現在のドックの内容を置き換え
            self._replace_current_dock(path)

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

    def _read_csv_data(self, path):
        """CSVファイルを読み込み、データとエンコーディングを返す"""
        encodings = [self.config_manager.get('default_encoding', 'utf-8'), 'utf-8', 'cp932', 'utf-8-sig']
        for enc in encodings:
            try:
                with open(path, 'r', encoding=enc, newline='') as f:
                    reader = csv.reader(f)
                    data = list(reader)
                    return data, enc
            except Exception:
                continue
        return None, None

    def _open_csv_in_new_dock(self, path):
        """CSVファイルを新しいドックで開く"""
        data, encoding = self._read_csv_data(path)
        if data is None:
            QMessageBox.critical(self, "エラー", "CSVファイルの読み込みに失敗しました。対応していない文字コードの可能性があります。")
            return

        table = QTableWidget()
        self.populate_table(table, data)

        tab_title = os.path.basename(path)
        dock = CsvDockWidget(tab_title, table, self)
        tab_data = CsvTabData(dock, file_path=path, encoding=encoding)
        tab_data._base_title = tab_title
        self.tab_data_map[dock] = tab_data

        self._add_dock_to_area(dock)

        # 編集済みの空ドックが存在する場合は削除
        self._remove_empty_dock_if_needed()

        self._update_window_title()

    def _add_dock_to_area(self, dock):
        """ドックを右エリアに追加（2つ目以降はタブ化）"""
        self.addDockWidget(Qt.RightDockWidgetArea, dock)
        
        if self._reference_dock is not None and self._reference_dock in self.tab_data_map:
            self.tabifyDockWidget(self._reference_dock, dock)
        else:
            self._reference_dock = dock
        
        # 追加したタブを確実にアクティブ（カレントタブ）にする
        dock.show()
        dock.raise_()
        dock.csv_table.setFocus()
        self._active_dock = dock
        # イベントループ処理後に再度raiseしてタブ選択を確実にする
        QTimer.singleShot(0, dock.raise_)

    def _replace_current_dock(self, path):
        """現在のアクティブなドックの内容を指定のCSVファイルで置き換える"""
        data, encoding = self._read_csv_data(path)
        if data is None:
            QMessageBox.critical(self, "エラー", "CSVファイルの読み込みに失敗しました。対応していない文字コードの可能性があります。")
            return

        current_data = self._current_tab_data()
        if current_data is not None:
            table = current_data.table_widget
            table.blockSignals(True)
            self.populate_table(table, data)
            table.blockSignals(False)

            current_data.file_path = path
            current_data.encoding = encoding
            current_data.is_edited = False
            current_data.is_transposed = False

            current_data._base_title = os.path.basename(path)
            self._update_dock_title(current_data)
        else:
            # アクティブなドックがない場合は新規ドックとして開く
            self._open_csv_in_new_dock(path)

        self._update_window_title()

    @staticmethod
    def _column_label(index):
        """0始まりの列インデックスをExcel形式の列ラベル（A, B, ..., Z, AA, AB, ...）に変換"""
        label = ""
        while index >= 0:
            label = chr(index % 26 + 65) + label
            index = index // 26 - 1
        return label

    def populate_table(self, table, data):
        table.clear()
        if not data:
            table.setRowCount(0)
            table.setColumnCount(0)
            return

        row_count = len(data)
        col_count = max(len(row) for row in data) if data else 0

        table.setRowCount(row_count)
        table.setColumnCount(col_count)

        for row_idx, row in enumerate(data):
            for col_idx, value in enumerate(row):
                item = QTableWidgetItem(value)
                table.setItem(row_idx, col_idx, item)

        # 横ヘッダーを A, B, C, ... に設定
        headers = [self._column_label(c) for c in range(col_count)]
        table.setHorizontalHeaderLabels(headers)

        # ヘッダーのリサイズモード設定
        table.horizontalHeader().setSectionResizeMode(QHeaderView.Interactive)

    def _current_table(self):
        """現在アクティブなドックのQTableWidgetを返す"""
        if self._active_dock is not None:
            return self._active_dock.csv_table
        return None

    def _current_tab_data(self):
        """現在アクティブなドックのCsvTabDataを返す"""
        if self._active_dock is not None:
            return self.tab_data_map.get(self._active_dock)
        return None

    def _update_dock_title(self, tab_data):
        """ドックタイトルを編集状態・反転状態を反映して更新"""
        title = tab_data._base_title
        if tab_data.is_transposed:
            title = f"{title}（行列反転）"
        if tab_data.is_edited:
            title = f"\u25cf {title}"
        tab_data.dock_widget.setWindowTitle(title)

    def _update_window_title(self):
        """ウィンドウタイトルを現在のドックに合わせて更新"""
        data = self._current_tab_data()
        if data is not None and data.file_path:
            title = f"csv-ed - {os.path.basename(data.file_path)}"
            if data.is_transposed:
                title = f"{title}（行列反転）"
            self.setWindowTitle(title)
        elif data is not None:
            self.setWindowTitle("csv-ed - 新規ファイル")
        else:
            self.setWindowTitle("csv-ed")

    def transpose_table(self):
        """現在のテーブルの行と列を入れ替える（行列反転）"""
        table = self._current_table()
        tab_data = self._current_tab_data()
        if table is None or tab_data is None:
            return

        row_count = table.rowCount()
        col_count = table.columnCount()

        # 現在のデータを読み取り
        data = []
        for r in range(row_count):
            row_data = []
            for c in range(col_count):
                item = table.item(r, c)
                row_data.append(item.text() if item else "")
            data.append(row_data)

        # 転置（行と列を入れ替え）
        new_data = []
        for c in range(col_count):
            new_row = []
            for r in range(row_count):
                new_row.append(data[r][c] if c < len(data[r]) else "")
            new_data.append(new_row)

        # テーブルを再構築
        table.blockSignals(True)
        self.populate_table(table, new_data)
        table.blockSignals(False)

        # 反転状態をトグル
        tab_data.is_transposed = not tab_data.is_transposed

        # タイトルを更新
        self._update_dock_title(tab_data)
        self._update_window_title()

    def _on_cell_changed(self, row, col):
        """セルが編集されたときに呼ばれる"""
        table = self.sender()
        if table is None:
            return

        # テーブルから対応するドックを検索
        target_dock = None
        for dock, tab_data in self.tab_data_map.items():
            if tab_data.table_widget is table:
                target_dock = dock
                break

        if target_dock is None:
            return

        tab_data = self.tab_data_map.get(target_dock)
        if tab_data is not None and not tab_data.is_edited:
            tab_data.is_edited = True
            self._update_dock_title(tab_data)

    def _on_focus_changed(self, old, new):
        """フォーカス変更を追跡してアクティブなドックを特定"""
        widget = new
        while widget is not None:
            if isinstance(widget, CsvDockWidget):
                if widget != self._active_dock:
                    self._active_dock = widget
                    self._update_window_title()
                return
            try:
                widget = widget.parent()
            except RuntimeError:
                break

    def _on_dock_close_request(self, dock_widget, event):
        """ドックが閉じられようとしたときに呼ばれる"""
        tab_data = self.tab_data_map.get(dock_widget)
        if tab_data is not None and tab_data.is_edited:
            reply = QMessageBox.question(
                self, "確認",
                f"「{dock_widget.windowTitle()}」は編集されています。保存せずに閉じますか？",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No
            )
            if reply == QMessageBox.No:
                event.ignore()
                return

        # クリーンアップ
        if dock_widget in self.tab_data_map:
            del self.tab_data_map[dock_widget]
        
        # 参照ドックが閉じられた場合は更新
        if dock_widget == self._reference_dock:
            if self.tab_data_map:
                self._reference_dock = next(iter(self.tab_data_map.keys()))
            else:
                self._reference_dock = None
        
        # アクティブドックが閉じられた場合は更新
        if dock_widget == self._active_dock:
            self._active_dock = None
            # 他のドックがあればアクティブに
            if self.tab_data_map:
                self._active_dock = next(iter(self.tab_data_map.keys()))

        self.removeDockWidget(dock_widget)
        dock_widget.deleteLater()
        event.accept()

        # ドックがなくなった場合は空のドックを追加
        if not self.tab_data_map:
            self._add_empty_dock()

        self._update_window_title()

    def _add_empty_dock(self):
        """空の新規ドックを追加する"""
        table = QTableWidget()
        table.setRowCount(3)
        table.setColumnCount(3)
        for r in range(3):
            for c in range(3):
                table.setItem(r, c, QTableWidgetItem(""))
        table.setHorizontalHeaderLabels([self._column_label(c) for c in range(3)])

        dock = CsvDockWidget("新規ファイル", table, self)
        tab_data = CsvTabData(dock, file_path=None, encoding=self.config_manager.get('default_encoding', 'utf-8'))
        tab_data._base_title = "新規ファイル"
        self.tab_data_map[dock] = tab_data

        self._add_dock_to_area(dock)

    def _remove_empty_dock_if_needed(self):
        """編集済みでない空の新規ドックを削除する"""
        to_remove = []
        for dock, tab_data in self.tab_data_map.items():
            if tab_data.file_path is None and not tab_data.is_edited:
                to_remove.append(dock)
        
        for dock in to_remove:
            if dock in self.tab_data_map:
                del self.tab_data_map[dock]
            if dock == self._reference_dock:
                if self.tab_data_map:
                    self._reference_dock = next(iter(self.tab_data_map.keys()))
                else:
                    self._reference_dock = None
            if dock == self._active_dock:
                self._active_dock = None
            self.removeDockWidget(dock)
            dock.deleteLater()

    def save_csv(self):
        """現在のドックのCSVを保存する"""
        tab_data = self._current_tab_data()
        if tab_data is None:
            return

        table = tab_data.table_widget
        file_path = tab_data.file_path

        if file_path is None:
            # 名前を付けて保存
            path, _ = QFileDialog.getSaveFileName(self, "CSVファイルの保存", self.current_dir, "CSV Files (*.csv)")
            if not path:
                return
            tab_data.file_path = path
            file_path = path

        try:
            # テーブルデータを読み取り
            data = []
            for r in range(table.rowCount()):
                row_data = []
                for c in range(table.columnCount()):
                    item = table.item(r, c)
                    row_data.append(item.text() if item else "")
                data.append(row_data)

            # 行列反転中は元の向きに戻して保存
            if tab_data.is_transposed:
                original_data = []
                for c in range(len(data[0]) if data else 0):
                    new_row = []
                    for r in range(len(data)):
                        new_row.append(data[r][c] if c < len(data[r]) else "")
                    original_data.append(new_row)
                data = original_data

            with open(file_path, 'w', encoding=tab_data.encoding, newline='') as f:
                writer = csv.writer(f)
                writer.writerows(data)

            tab_data.is_edited = False
            tab_data._base_title = os.path.basename(file_path)
            self._update_dock_title(tab_data)

            QMessageBox.information(self, "成功", "ファイルを保存しました。")
            self._update_window_title()
            # 左ペインのリストを更新
            self.load_directory(self.current_dir)
        except Exception as e:
            QMessageBox.critical(self, "エラー", f"ファイルの保存中にエラーが発生しました:\n{e}")

    def new_csv(self):
        """新規CSVファイルを新しいドックで作成"""
        self._add_empty_dock()

    def open_csv_dialog(self):
        """ファイルダイアログからCSVを開く（新しいドックで開く）"""
        path, _ = QFileDialog.getOpenFileName(self, "CSVファイルを開く", self.current_dir, "CSV Files (*.csv)")
        if path:
            self._open_csv_in_new_dock(path)

    def open_settings(self):
        dialog = SettingDialog(self.config_manager, self)
        if dialog.exec() == QDialog.Accepted:
            # 設定が変更されたら、ディレクトリを再読み込み
            self.load_directory(self.config_manager.get('last_directory'))

    def show_table_context_menu(self, pos):
        table = self._current_table()
        if table is None:
            return

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

        menu.exec_(table.viewport().mapToGlobal(pos))

    def insert_row(self):
        table = self._current_table()
        if table is None:
            return
        current_row = table.currentRow()
        if current_row == -1:
            current_row = table.rowCount()
        table.insertRow(current_row)
        # 空のアイテムで初期化
        for c in range(table.columnCount()):
            table.setItem(current_row, c, QTableWidgetItem(""))

    def delete_row(self):
        table = self._current_table()
        if table is None:
            return
        current_row = table.currentRow()
        if current_row != -1:
            table.removeRow(current_row)

    def insert_column(self):
        table = self._current_table()
        if table is None:
            return
        current_col = table.currentColumn()
        if current_col == -1:
            current_col = table.columnCount()
        table.insertColumn(current_col)
        # 空のアイテムで初期化
        for r in range(table.rowCount()):
            table.setItem(r, current_col, QTableWidgetItem(""))

    def delete_column(self):
        table = self._current_table()
        if table is None:
            return
        current_col = table.currentColumn()
        if current_col != -1:
            table.removeColumn(current_col)

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

    def eventFilter(self, obj, event):
        """マウスホイール（中ボタン）クリックでタブを閉じる"""
        if event.type() == QEvent.MouseButtonPress and event.button() == Qt.MiddleButton:
            if isinstance(obj, QTabBar):
                tab_index = obj.tabAt(event.position().toPoint())
                if tab_index >= 0:
                    tab_text = obj.tabText(tab_index).replace('&', '')
                    for dock, tab_data in list(self.tab_data_map.items()):
                        if dock.windowTitle() == tab_text:
                            dock.close()
                            return True
        return super().eventFilter(obj, event)


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
