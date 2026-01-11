# reporter_qc.py
from output import info, success, warning, error, step, add_counts

def generate_report(validation_results, case_number=None, total_checks=None):
    """
    根据校验结果生成并打印一份可读的报告。

    :param validation_results: 从 validator_qc.validate_data() 获取的问题列表
    :param case_number: 病案号
    :param total_checks: 总检查项数
    """
    if case_number:
        step(f"--- 首页质控报告 [病案号: {case_number}] ---")
    else:
        step("--- 首页质控报告 ---")
    
    info("--------------------")

    if not validation_results:
        success("未发现明显的缺漏或逻辑错误。")
        info("--------------------")
        # 即使没有问题，也要确保计数器被正确设置
        if total_checks is not None:
            add_counts(int(total_checks), 0)
        return

    level_order = {"错误": 0, "逻辑错误": 1, "警告": 2, "注意": 3}
    sorted_results = sorted(validation_results, key=lambda x: level_order.get(x['level'], 99))

    for item in sorted_results:
        level = item['level']
        field = item['field']
        message = item['message']
        
        if level in ["错误", "逻辑错误"]:
            error(f"【{level}】 {field}: {message}")
        elif level == "警告":
            warning(f"【{level}】 {field}: {message}")
        else:
            # “注意”级别也用普通info输出，不计入问题统计
            info(f"【{level}】 {field}: {message}")
    
    info("--------------------")
    # 重新统计问题数，因为"注意"级别不应算作错误
    issue_count = sum(1 for item in validation_results if item['level'] in ["错误", "逻辑错误", "警告"])
    if issue_count > 0:
        error(f"报告总结：共发现 {issue_count} 个问题（错误/警告）。")
    else:
        success("报告总结：未发现严重问题（错误/警告），但存在一些“注意”事项。")

    if total_checks is not None:
        add_counts(int(total_checks), int(issue_count))
