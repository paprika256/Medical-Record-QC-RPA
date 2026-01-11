# gui_qc.py
import sys
import os
import ctypes
import time

from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                             QTextEdit, QDesktopWidget, QStyleFactory, QProgressBar, 
                             QLabel, QStatusBar, QMessageBox)
from PyQt5.QtCore import QThread, QObject, pyqtSignal, Qt, QTimer
from PyQt5.QtGui import QFont, QIcon

# 导入你的核心逻辑和输出模块
from output import setup_gui_handler, clear_log, info, warning, success, error, reset_counters
from history_qc import get_csv_path
import subprocess

# --- 自动模式需要的模块 ---
try:
    from pywinauto import Application
    from pywinauto.findwindows import ElementNotFoundError
    from pywinauto.timings import TimeoutError as PywinautoTimeoutError
    from ui_map_qc import CONTROLS_QC
    PYWINAUTO_AVAILABLE = True
except ImportError:
    PYWINAUTO_AVAILABLE = False
    warning("pywinauto 模块未找到，自动质控模式将不可用。")

# --- 管理员权限检测与重启功能 ---
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def relaunch_as_admin():
    if sys.platform == 'win32':
        try:
            ctypes.windll.shell32.ShellExecuteW(
                None, "runas", sys.executable, " ".join(sys.argv), None, 1
            )
            sys.exit(0)
        except Exception as e:
            warning(f"请求管理员权限失败: {e}")
            return False
    return True

# --- 新增：轻量级的后台扫描工作者 ---
class AutoScanWorker(QObject):
    finished = pyqtSignal()
    case_found = pyqtSignal(str)
    scan_failed = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)

    def run(self):
        """在后台执行pywinauto扫描，不阻塞UI"""
        try:
            # 使用非常短的超时来连接，避免长时间等待
            app = Application(backend="win32").connect(title="首页录入", timeout=0.5)
            dlg = app.window(title="首页录入")
            
            if not dlg.exists() or not dlg.is_visible():
                self.scan_failed.emit("未找到可见的'首页录入'窗口。")
                self.finished.emit()
                return

            case_number_ctrl = dlg.child_window(**CONTROLS_QC["case_number"])
            case_number = case_number_ctrl.window_text().strip()

            if case_number:
                self.case_found.emit(case_number)
            else:
                self.scan_failed.emit("检测到首页，但无病案号。")

        except (ElementNotFoundError, PywinautoTimeoutError):
            self.scan_failed.emit("正在扫描新首页...")
        except Exception as e:
            self.scan_failed.emit(f"扫描时出错: {str(e)[:50]}...")
        finally:
            self.finished.emit()


# --- 重量级的质控工作线程 (保持不变) ---
class Worker(QObject):
    finished = pyqtSignal()
    progress_update = pyqtSignal(int, str)
    qc_done = pyqtSignal(str, int, int)

    def run(self):
        try:
            from main_qc import run_quality_control
            results = run_quality_control(progress_callback=self.progress_update)
            if results:
                case_number, total_checks, num_issues = results
                self.qc_done.emit(case_number, total_checks, num_issues)
        except Exception as e:
            error(f"工作线程发生严重错误: {e}")
        finally:
            self.finished.emit()

# --- 主窗口 ---
class QualityControlApp(QWidget):
    def __init__(self):
        super().__init__()
        self.is_admin_mode = is_admin()
        
        # 状态管理
        self.auto_mode_enabled = False
        self.is_scanning = False  # 防止并发扫描
        self.is_qc_running = False # 防止在质控时触发新的扫描
        self.checked_cases = {}  # {case_number: timestamp}
        self.auto_qc_timer = QTimer(self)
        self.current_auto_status_message = ""

        # 线程管理
        self.qc_thread = None
        self.qc_worker = None
        self.scan_thread = None
        self.scan_worker = None

        self.initUI()

    def initUI(self):
        # ... (UI初始化代码与之前版本相同，此处省略以保持简洁)
        # --- 窗口基本设置 ---
        self.setWindowTitle('首页质控助手')
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setGeometry(0, 0, 800, 700)
        self.center()
        icon_path = os.path.join(os.path.dirname(__file__), 'img', 'logo.ico')
        if os.path.exists(icon_path):
            self.setWindowIcon(QIcon(icon_path))
        
        # --- 控件创建 ---
        self.main_action_button = QPushButton('', self)
        self.main_action_button.setFixedHeight(40)
        self.main_action_button.setFont(QFont('Microsoft YaHei', 12, QFont.Bold))

        self.progress_bar = QProgressBar(self)
        self.progress_bar.setFixedHeight(12)
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setVisible(False)

        self.status_label = QLabel('准备就绪', self)
        self.status_label.setFont(QFont('Microsoft YaHei', 9))

        self.output_box = QTextEdit(self)
        self.output_box.setReadOnly(True)
        self.output_box.setFont(QFont('Microsoft YaHei', 11))
        self.output_box.setStyleSheet("""
            QTextEdit {
                background-color: #fbfdff; color: #1f2937; border: 1px solid #e2e8f0;
                border-radius: 6px; padding: 8px;
            }
        """)

        # --- 布局管理 ---
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.main_action_button)

        progress_layout = QHBoxLayout()
        progress_layout.addWidget(self.status_label, 1)
        progress_layout.addWidget(self.progress_bar, 3)
        main_layout.addLayout(progress_layout)

        main_layout.addWidget(self.output_box, 1)

        self.statusBar = QStatusBar(self)
        self.statusBar.setFont(QFont('Microsoft YaHei', 10))
        self.statusBar.showMessage('状态：准备就绪')

        bottom_layout = QHBoxLayout()
        self.history_button = QPushButton('历史', self)
        self.history_button.setFixedSize(64, 28)
        self.history_button.setFont(QFont('Microsoft YaHei', 9))
        self.history_button.clicked.connect(self.on_history_clicked)
        
        self.toggle_mode_button = QPushButton('切换到自动模式', self)
        self.toggle_mode_button.setFixedSize(120, 28)
        self.toggle_mode_button.setFont(QFont('Microsoft YaHei', 9))
        self.toggle_mode_button.clicked.connect(self.toggle_auto_mode)

        bottom_layout.addWidget(self.history_button)
        bottom_layout.addWidget(self.toggle_mode_button)
        bottom_layout.addStretch(1)
        bottom_layout.addWidget(self.statusBar)
        main_layout.addLayout(bottom_layout)

        self.setLayout(main_layout)

        setup_gui_handler(self.output_box)

        if self.is_admin_mode:
            self.setup_for_admin_mode()
        else:
            self.setup_for_non_admin_mode()

        # 配置定时器
        self.auto_qc_timer.setInterval(20000)
        self.auto_qc_timer.timeout.connect(self.trigger_auto_scan)

    def setup_for_admin_mode(self):
        # ... (与之前版本相同)
        self.main_action_button.setText('▶ 开始质控')
        self.main_action_button.setStyleSheet("""
            QPushButton {
                background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 #3b82f6, stop:1 #2563eb);
                color: white; border: none; border-radius: 6px; padding: 8px; font-size: 13pt;
            }
            QPushButton:hover { background-color: #1e40af; }
            QPushButton:pressed { background-color: #1e3a8a; }
            QPushButton:disabled { background-color: #e6eefc; color: #9aa7d6; }
        """)
        self.main_action_button.clicked.connect(self.start_qc_process)
        
        if not PYWINAUTO_AVAILABLE:
            self.toggle_mode_button.setEnabled(False)
            self.toggle_mode_button.setToolTip("pywinauto 模块未安装，无法使用自动模式")

        success("程序已在管理员模式下运行。")
        info("点击“开始质控”按钮以运行手动质控，或切换到自动模式。")


    def setup_for_non_admin_mode(self):
        # ... (与之前版本相同)
        self.main_action_button.setText('以管理员身份重启')
        self.main_action_button.setStyleSheet("""
            QPushButton { background-color: #64748b; color: white; border: none; border-radius: 6px; padding: 8px; font-size: 13pt; }
            QPushButton:hover { background-color: #52606d; }
            QPushButton:pressed { background-color: #3f4b57; }
        """)
        self.main_action_button.clicked.connect(relaunch_as_admin)
        self.toggle_mode_button.setEnabled(False)
        
        warning("警告：程序未以管理员身份运行。")
        info("请点击上方按钮以管理员身份重启本程序。")

    def trigger_auto_scan(self):
        """由QTimer触发，启动一个轻量级扫描线程"""
        if self.is_scanning or self.is_qc_running or not PYWINAUTO_AVAILABLE:
            return

        self.is_scanning = True
        
        self.scan_thread = QThread()
        self.scan_worker = AutoScanWorker()
        self.scan_worker.moveToThread(self.scan_thread)

        self.scan_thread.started.connect(self.scan_worker.run)
        self.scan_worker.finished.connect(self.on_scan_finished)
        self.scan_worker.case_found.connect(self.on_case_found)
        self.scan_worker.scan_failed.connect(self.update_auto_status)

        self.scan_thread.start()

    def on_scan_finished(self):
        """扫描线程结束后的清理工作"""
        self.is_scanning = False
        if self.scan_thread:
            self.scan_thread.quit()
            self.scan_thread.wait()
            self.scan_thread = None
            self.scan_worker = None

    def on_case_found(self, case_number):
        """当扫描线程发现病案号时的处理逻辑"""
        current_time = time.time()
        last_check_time = self.checked_cases.get(case_number)

        if last_check_time and (current_time - last_check_time) < 3600:
            self.update_auto_status(f"病案号 {case_number} 在1小时内已质控，跳过。")
            return
        
        # 发现新病案，准备质控
        self.checked_cases[case_number] = current_time
        self.start_qc_process(case_number_hint=case_number)

    def start_qc_process(self, case_number_hint=None):
        """启动重量级质控流程"""
        if self.is_qc_running:
            return

        self.is_qc_running = True
        self.toggle_mode_button.setEnabled(False) # 禁用模式切换
        if not self.auto_mode_enabled:
            self.main_action_button.setEnabled(False)
            self.main_action_button.setText("...质控运行中...")
        
        self.progress_bar.setVisible(True)
        clear_log()
        reset_counters()
        
        if case_number_hint:
             info(f"<b>▶ 自动模式：开始质控病案号 <span style='font-size:12pt; color:blue;'>{case_number_hint}</span></b>")
        else:
             info("▶ 手动模式：开始执行质控流程...")

        self.statusBar.showMessage('状态：正在运行...')

        self.qc_thread = QThread()
        self.qc_worker = Worker()
        self.qc_worker.moveToThread(self.qc_thread)

        self.qc_thread.started.connect(self.qc_worker.run)
        self.qc_worker.finished.connect(self.on_qc_finished)
        self.qc_worker.progress_update.connect(self.update_progress)
        self.qc_worker.qc_done.connect(self.on_qc_results_ready)

        self.qc_thread.start()

    def on_qc_finished(self):
        """质控流程结束后的UI状态处理"""
        self.is_qc_running = False
        self.progress_bar.setVisible(False)
        self.statusBar.showMessage('状态：完成', 5000)
        
        if self.qc_thread:
            self.qc_thread.quit()
            self.qc_thread.wait()
            self.qc_thread = None
            self.qc_worker = None

        if self.auto_mode_enabled:
            self.toggle_mode_button.setEnabled(True)
            self.update_auto_status("自动模式：正在扫描新首页...")
        else:
            self.main_action_button.setEnabled(True)
            self.main_action_button.setText("▶ 开始质控")
            self.toggle_mode_button.setEnabled(True)
            self.status_label.setText("准备就绪")

    def toggle_auto_mode(self):
        """切换自动/手动模式"""
        self.auto_mode_enabled = not self.auto_mode_enabled
        if self.auto_mode_enabled:
            self.auto_qc_timer.start()
            self.main_action_button.setEnabled(False)
            self.main_action_button.setText("自动模式运行中...")
            self.toggle_mode_button.setText("切换到手动模式")
            self.statusBar.showMessage("状态：自动模式已开启")
            self.update_auto_status("自动模式：正在扫描新首页...")
        else:
            self.auto_qc_timer.stop()
            self.main_action_button.setEnabled(True)
            self.main_action_button.setText("▶ 开始质控")
            self.toggle_mode_button.setText("切换到自动模式")
            self.statusBar.showMessage("状态：准备就绪")
            self.update_auto_status("准备就绪")

    def update_auto_status(self, message: str):
        """动态更新状态栏文本，避免刷屏"""
        if self.auto_mode_enabled and message != self.current_auto_status_message:
            self.status_label.setText(message)
            self.current_auto_status_message = message
    
    # --- 其他辅助函数 (on_qc_results_ready, update_progress, on_history_clicked, center, closeEvent) ---
    # 这些函数与之前版本基本相同，此处省略以保持简洁
    def update_progress(self, value, text):
        self.progress_bar.setValue(int(value))
        if not self.auto_mode_enabled:
            self.status_label.setText(str(text))

    def on_qc_results_ready(self, case_number, total_checks, num_issues):
        passed = total_checks - num_issues
        summary = (f"<b>病案号: {case_number}</b><br><br>"
                   f"质控完成！<br>"
                   f"通过检查 {passed} 项，存在问题 {num_issues} 个（共检查 {total_checks} 项）。")
        
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("质控结果")
        msg_box.setIcon(QMessageBox.Information)
        msg_box.setTextFormat(Qt.RichText)
        msg_box.setText(summary)
        msg_box.setStandardButtons(QMessageBox.Ok)
        msg_box.exec_()
    
    def on_history_clicked(self):
        try:
            path = get_csv_path()
            if not os.path.exists(path) or os.path.getsize(path) == 0:
                with open(path, 'w', newline='', encoding='utf-8-sig') as f:
                    import csv
                    writer = csv.writer(f)
                    writer.writerow(['病案号', '运行日期'])
            os.startfile(path)
        except Exception as e:
            QMessageBox.critical(self, '历史', f'无法打开或创建历史文件: {e}', QMessageBox.Ok)

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def closeEvent(self, event):
        # 确保所有线程都能在关闭时被正确终止
        if self.qc_thread and self.qc_thread.isRunning():
            self.qc_thread.quit()
            self.qc_thread.wait()
        if self.scan_thread and self.scan_thread.isRunning():
            self.scan_thread.quit()
            self.scan_thread.wait()
        event.accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle(QStyleFactory.create('Fusion'))
    
    ex = QualityControlApp()
    ex.show()
    sys.exit(app.exec_())
