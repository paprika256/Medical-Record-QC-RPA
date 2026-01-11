# output.py
import logging
import sys
import traceback # Keep this for print_exception
from typing import Optional
from html import escape

# Attempt to import PyQt5 for signals. If not available, GUI logging won't work,
# but console logging will remain.
try:
    from PyQt5.QtCore import QObject, pyqtSignal
    QT_AVAILABLE = True
except ImportError:
    QT_AVAILABLE = False
    QObject = object # Dummy QObject if PyQt5 is not available
    pyqtSignal = lambda *args, **kwargs: (lambda func: func) # Dummy signal decorator

# --- Signal Emitter ---
# This class must inherit from QObject to use signals
class _OutputSignals(QObject):
    append_text_signal = pyqtSignal(str) if QT_AVAILABLE else (lambda *args: None) # type: ignore
    clear_text_signal = pyqtSignal() if QT_AVAILABLE else (lambda *args: None) # type: ignore

_signals = _OutputSignals() # Create a single instance

# --- Global Python Logger (for console) ---
logger = logging.getLogger('form_filler_logger') # Use a specific name
logger.setLevel(logging.INFO) # Default level
logger.propagate = False # Prevent logs from going to the root logger if it's configured elsewhere

# Console handler (always active for fallback/debugging)
_console_handler = logging.StreamHandler(sys.stdout)
_console_formatter = logging.Formatter('%(message)s') # Simple format for console
_console_handler.setFormatter(_console_formatter)

if not logger.hasHandlers(): # Add console handler only if not already present
    logger.addHandler(_console_handler)

# --- 简单的计数器，用于统计通过项与问题数 ---
# total_checks: 记录总检查项（由 success 或 warning/error 表示的已检测项）
# issues_count: 记录存在问题的项数（warning + error 被视为问题）
_total_checks = 0
_issues_count = 0

def reset_counters() -> None:
    """重置内部计数器。"""
    global _total_checks, _issues_count
    _total_checks = 0
    _issues_count = 0

def get_counters() -> dict:
    """返回当前计数器状态，形如 {'total': int, 'issues': int, 'passed': int}。"""
    return {
        'total': _total_checks,
        'issues': _issues_count,
        'passed': _total_checks - _issues_count
    }

def add_counts(total: int = 0, issues: int = 0) -> None:
    """静默调整计数器（不会触发 GUI 日志），用于批量设置或补偿计数。

    :param total: 要增加到 `_total_checks` 的数量（可以为负以减少）。
    :param issues: 要增加到 `_issues_count` 的数量（可以为负以减少）。
    """
    global _total_checks, _issues_count
    try:
        _total_checks += int(total)
    except Exception:
        pass
    try:
        _issues_count += int(issues)
    except Exception:
        pass

# --- Public Logging Functions ---

def _log_and_emit(log_level_func, console_message: str, gui_message: Optional[str] = None):
    """Helper to log to console and emit signal for GUI (HTML)."""
    log_level_func(console_message)
    if QT_AVAILABLE:
        if gui_message is None:
            _signals.append_text_signal.emit(escape(console_message) + '<br>')
        else:
            _signals.append_text_signal.emit(gui_message)

# 使用颜色常量，方便管理
COLOR_SUCCESS = "#16A34A"  # 成功绿（稍深）
COLOR_WARNING = "#D97706"  # 深黄色，比 #FFC107 更醒目
COLOR_ERROR = "#B91C1C"    # 深红色，更显眼
COLOR_INFO = "#111827"     # 深灰（几乎接近正文色）
COLOR_STEP = "#0B5ED7"     # 深蓝色（更沉稳的蓝）

def info(message: str) -> None:
    """输出普通信息"""
    gui_msg = f'<font color="{COLOR_INFO}">{escape(message)}</font><br>'
    _log_and_emit(logger.info, message, gui_msg)

def debug(message: str) -> None:
    """Output调试信息"""
    # Debug messages might be too verbose for GUI, so only log to console by default
    # If you want them in GUI, change it or add a flag
    logger.debug(f"DEBUG: {message}")
    # If you want debug in GUI too:
    # _log_and_emit(logger.debug, f"DEBUG: {message}")


def success(message: str) -> None:
    """输出成功信息"""
    global _total_checks
    console_msg = f"✅ {message}"
    gui_msg = f'<font color="{COLOR_SUCCESS}">✅ {escape(message)}</font><br>'
    _log_and_emit(logger.info, console_msg, gui_msg)
    try:
        _total_checks += 1
    except Exception:
        pass

def warning(message: str) -> None:
    """输出警告信息"""
    global _total_checks, _issues_count
    console_msg = f"⚠ {message}"
    gui_msg = f'<font color="{COLOR_WARNING}">⚠ {escape(message)}</font><br>'
    _log_and_emit(logger.warning, console_msg, gui_msg)
    try:
        _total_checks += 1
        _issues_count += 1
    except Exception:
        pass

def error(message: str) -> None:
    """输出错误信息"""
    global _total_checks, _issues_count
    console_msg = f"❌ {message}"
    gui_msg = f'<font color="{COLOR_ERROR}">❌ {escape(message)}</font><br>'
    _log_and_emit(logger.error, console_msg, gui_msg)
    try:
        _total_checks += 1
        _issues_count += 1
    except Exception:
        pass

def step(message: str) -> None:
    """输出步骤信息"""
    console_msg = f"\n▶ {message}"
    gui_msg = f'<br><b style="color:{COLOR_STEP};">▶ {escape(message)}</b><br>'
    _log_and_emit(logger.info, console_msg, gui_msg)

def sub_step(message: str) -> None:
    """输出子步骤信息"""
    console_msg = f"  • {message}"
    gui_msg = f'&nbsp;&nbsp;• <font color="{COLOR_INFO}">{escape(message)}</font><br>'
    _log_and_emit(logger.info, console_msg, gui_msg)

def print_exception(e: Exception, message: Optional[str] = None) -> None:
    """输出异常信息及堆栈跟踪"""
    header = f"发生异常: {e}"
    if message:
        header = f"{message}: {e}"

    tb_str = traceback.format_exc()
    full_console_message = f"❌ {header}\n{tb_str}"

    logger.error(full_console_message) # Log full details to console

    if QT_AVAILABLE:
        gui_msg = (f'<font color="{COLOR_ERROR}">❌ <b>{escape(header)}</b></font><br>'
                   f'<pre style="color: #cdd; font-size: 9pt;">{escape(tb_str)}</pre>')
        _signals.append_text_signal.emit(gui_msg)


def clear_log() -> None:
    """清空日志输出控件 (by emitting a signal)"""
    logger.info("--- Log Cleared ---") # Log clear action to console
    if QT_AVAILABLE:
        _signals.clear_text_signal.emit()
    # 不自动重置计数器；调用方可使用 reset_counters() 在开始新的检查前重置

def setup_gui_handler(text_widget) -> None:
    """
    Connects the internal signals to the QTextEdit's slots.
    This function should be called from the GUI thread once the QTextEdit is created.
    `text_widget` is expected to be a QTextEdit instance.
    """
    if not QT_AVAILABLE:
        print("WARNING: PyQt5 not found. GUI logging will be disabled. Logs will only go to console.")
        if text_widget: # If a text_widget was passed anyway
            try:
                text_widget.append("PyQt5 not found. GUI logging disabled. Check console for logs.")
            except: # pylint: disable=bare-except
                pass # text_widget might not be a QTextEdit
        return

    # Connect signals to the QTextEdit's methods
    # QTextEdit.append and QTextEdit.clear are thread-safe when called via a signal
    # that was emitted from another thread and connected to them in the GUI thread.
    try:
        _signals.append_text_signal.connect(text_widget.append)
        _signals.clear_text_signal.connect(text_widget.clear)

        # 初始说明文本使用 HTML
        initial_message = (
            '<b style="font-size: 12pt; color: #00BFFF;">病案首页自动质控说明</b><hr>'
            "<p>本工具旨在检查并提示病案首页中的常见错误，核心检查点如下：</p>"
            '<b>1.【完整性检查】</b><ul><li>检查治则治法、医护人员等必填项是否缺漏。</li></ul>'
            '<b>2.【规范性检查】</b><ul><li>校验身份证号、电话、邮编等格式。</li></ul>'
            '<b>3.【逻辑性检查】</b><ul><li>诊断与入院病情、手术与主刀医生、麻醉信息三要素的匹配。</li><li>抢救与危急重症、输血与血型、死亡与尸检的关联。</li></ul>'
            '<b>4.【合理性检查】</b><ul><li>识别地址、联系人等字段中的无效或测试性文本。</li></ul>'
            '<hr><b style="color: #00BFFF;">使用方法</b><br>'
            '1. 在病案录入系统，打开需要质控的患者首页。<br>'
            '2. 点击本程序的<b>「开始质控」</b>按钮。<br>'
            '3. 根据生成的报告，核实问题。<br><br>'
            '<small style="color: #808080;">*本程序检查结果仅供参考，请结合专业判断进行最终核实。</small>'
            '<hr style="margin-top: 20px; margin-bottom: 10px;">'
            '<p style="font-size: 9pt; color: #808080; text-align: center;">'
            '</p>'
        )

        text_widget.setHtml(initial_message)
        logger.info("Output module connected to GUI log widget.")
    except Exception as e:
        logger.error(f"Failed to connect output signals to GUI: {e}")
        if text_widget:
            try:
                text_widget.append(f"ERROR: Failed to setup GUI logging: {e}")
            except: # pylint: disable=bare-except
                pass
