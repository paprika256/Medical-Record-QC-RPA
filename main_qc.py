# main_qc.py
import sys
from output import info, success, warning, error, step, print_exception
from validator_qc import validate_data
from reporter_qc import generate_report
from history_qc import save_run_snapshot

# 仅在非测试模式下导入 pywinauto 相关模块
TEST_MODE = 0  # 切换测试模式

if not TEST_MODE:
    from pywinauto import Application
    from pywinauto.findwindows import ElementNotFoundError, ElementAmbiguousError
    import time
    from extractor_qc import extract_all_data
else:
    from test_data import get_test_data, get_additional_test_cases

def activate_window(app, window_title):
    """
    连接并激活目标窗口。
    """
    try:
        info(f"正在连接窗口: '{window_title}'")
        dlg = app.connect(title=window_title, timeout=10).window(title=window_title)
        success("窗口连接成功。")
        
        if dlg.is_minimized():
            info("窗口已最小化，正在恢复...")
            dlg.restore()
        
        dlg.set_focus()
        dlg.wait('active', timeout=5)
        success("窗口已激活。")
        
        return dlg

    except ElementAmbiguousError:
        error(f"检测到多个标题为 '{window_title}' 的窗口。请只保留一个目标窗口后重试。")
        return None
    except ElementNotFoundError:
        error(f"找不到窗口标题为 '{window_title}' 的应用。请确保程序正在运行且标题匹配。")
        return None
    except Exception as e:
        print_exception(e, "连接或激活窗口时发生未知错误")
        return None

def run_quality_control(test_case_index=None, progress_callback=None):
    """
    执行首页质控的主流程。

    :param test_case_index: 在测试模式下，指定要使用的测试用例索引。
    :param progress_callback: 用于传递进度的回调或 PyQt 信号。
    :return: (case_number, total_checks, num_issues) on success, None on failure.
    """
    import time

    def report_progress(percent, message):
        if not progress_callback:
            return
        try:
            progress_callback.emit(int(percent), str(message))
        except Exception:
            try:
                progress_callback(int(percent), str(message))
            except Exception:
                pass
        time.sleep(0.18)

    try:
        report_progress(5, "正在初始化...")
        step("初始化质控程序")

        if TEST_MODE:
            info("▶ 运行测试模式")
            report_progress(20, "正在加载测试数据...")
            if test_case_index is not None:
                extracted_data = get_additional_test_cases()[test_case_index]
                info(f"使用测试用例 {test_case_index + 1}")
            else:
                extracted_data = get_test_data()
                info("使用主测试数据集")
        else:
            report_progress(15, "正在连接目标窗口...")
            window_title = "首页录入"
            app = Application(backend="win32")
            dlg = activate_window(app, window_title)
            if not dlg:
                error("未能获取到目标窗口，程序退出。")
                report_progress(100, "错误：未找到目标窗口")
                return None

            report_progress(40, "正在提取界面数据...")
            extracted_data = extract_all_data(dlg)
            if not extracted_data:
                warning("未能从界面提取到任何数据，无法进行校验。")
                report_progress(100, "警告：未提取到数据")
                return None

        report_progress(70, "正在校验数据逻辑...")
        validation_results, case_number, total_checks = validate_data(extracted_data)

        report_progress(90, "正在生成质控报告...")
        generate_report(validation_results, case_number, total_checks)

        try:
            save_run_snapshot(extracted_data, validation_results, case_number)
        except Exception as e:
            print_exception(e, "保存质控历史时发生错误")

        report_progress(100, "质控完成！")
        return (case_number, total_checks, len(validation_results))

    except Exception as e:
        print_exception(e, "质控程序运行时发生严重错误")
        report_progress(100, f"错误: {e}")
        return None

def test_all_cases():
    """
    运行所有测试用例
    """
    if not TEST_MODE:
        error("请先启用测试模式")
        return

    step("\n=== 运行主测试数据集 ===")
    run_quality_control()

    test_cases = get_additional_test_cases()
    for i in range(len(test_cases)):
        step(f"\n=== 运行测试用例 {i + 1} ===")
        run_quality_control(i)

if __name__ == '__main__':
    if TEST_MODE:
        test_all_cases()
    else:
        run_quality_control()
    
    input("\n质控流程结束，按回车键退出...")
