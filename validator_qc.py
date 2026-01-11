# validator_qc.py
import re
from output import info
from extractor_qc import get_friendly_name

# 正则表达式常量
ID_CARD_REGEX = re.compile(r'^\d{17}(\d|X)$', re.IGNORECASE)
PHONE_REGEX = re.compile(r'^((1[3-9]\d{9})|((0\d{2,3}-?)?\d{7,8}))$')
ZIP_CODE_REGEX = re.compile(r'^\d{6}$')

def is_simple_sequence(phone_str: str, threshold: int = 6) -> bool:
    """
    检查电话号码字符串是否包含简单的数字序列。

    :param phone_str: 要检查的电话号码字符串。
    :param threshold: 判断为序列的最小连续数字长度，默认为6。
    :return: 如果包含简单序列，返回 True，否则返回 False。
    """
    if not phone_str:
        return False

    # 只提取数字进行判断
    digits_only = re.sub(r'\D', '', phone_str)
    
    if len(digits_only) < threshold:
        return False

    for i in range(len(digits_only) - threshold + 1):
        sub_seq = digits_only[i:i+threshold]

        # 1. 检查是否为重复数字 (e.g., "888888")
        if len(set(sub_seq)) == 1:
            return True

        # 2. 检查是否为连续升序数字 (e.g., "123456")
        is_ascending = True
        for j in range(len(sub_seq) - 1):
            if int(sub_seq[j+1]) != int(sub_seq[j]) + 1:
                is_ascending = False
                break
        if is_ascending:
            return True

        # 3. 检查是否为连续降序数字 (e.g., "765432")
        is_descending = True
        for j in range(len(sub_seq) - 1):
            if int(sub_seq[j+1]) != int(sub_seq[j]) - 1:
                is_descending = False
                break
        if is_descending:
            return True

    return False

def is_strange_text(text: str, min_len: int = 2, placeholders: list = None) -> bool:
    """
    检查文本是否“奇怪”（过短、是占位符、或高度重复）。
    :param text: 要检查的字符串。
    :param min_len: 最小可接受长度。
    :param placeholders: 常见的占位符列表。
    :return: 如果文本奇怪，返回True，否则False。
    """
    if not text:
        return False
    if placeholders is None:
        placeholders = ["测试", "未知"]
    
    # 1. 检查是否为占位符
    if text in placeholders:
        return True
    # 2. 检查长度是否过短
    if len(text) < min_len:
        return True
    # 3. 检查字符是否高度重复 (例如 "xxxxxx", "ababab")
    if len(set(text)) <= 2 and len(text) > 3:
        return True
    return False

def is_strange_zip(zip_code: str) -> bool:
    """
    检查邮编是否“奇怪”（格式不正确或为简单序列）。
    :param zip_code: 要检查的邮政编码字符串。
    :return: 如果邮编奇怪，返回True，否则False。
    """
    if not zip_code:
        return False
    # 1. 检查格式是否为6位数字
    if not ZIP_CODE_REGEX.match(zip_code):
        return True
    # 2. 检查是否为简单序列
    if is_simple_sequence(zip_code):
        return True
    return False

def validate_data(data):
    """
    校验提取出的数据，检查缺失和逻辑错误。

    :param data: 从 extractor_qc.extract_all_data() 获取的字典
    :return: tuple (validation_results, case_number)
        - validation_results: 一个包含所有发现问题的列表，每个问题是一个字典
        - case_number: 病案号
    """
    info("▶ 开始数据校验...")
    report_items = []
    # 统计已执行的检查项数量（用于总检查数统计）
    check_count = 0

    # --- 1. 必填项检查 ---
    # 定义哪些字段是必须填写的
    required_staff = [
    "name", "gender", "id_card_number", "birth_date", "marriage_status",
    "nationality", "occupation", "current_address", "contact_name",
    "contact_relationship", "contact_phone",
    "tcm_outpatient_syndrome_code", "tcm_discharge_treatment_principle_code", "tcm_discharge_treatment_principle_name",
    'department_director', 'chief_physician', 'attending_physician',
    'resident_physician', 'quality_control_physician', 'responsible_nurse', 'quality_control_nurse'
    ]
    for staff_key in required_staff:
        # 每个必填项视为一项检查
        check_count += 1
        val = data.get(staff_key)
        if not val or val in (None, '', '-', '无'):
            report_items.append({
                'level': '错误',
                'field': get_friendly_name(staff_key),
                'message': f"{get_friendly_name(staff_key)} 不能为空，请补充。"
            })

    # 国籍检查
    nationality = data.get("nationality")
    if nationality and nationality not in ["中国", "156"]: # 156是中国国籍代码
        check_count += 1
        report_items.append({
            "level": "警告",
            "field": get_friendly_name("nationality"),
            "message": f"国籍为 '{nationality}'，不是'中国'，请核实。"
        })

    # 身份证号格式检查
    id_card = data.get("id_card_number")
    if id_card and not ID_CARD_REGEX.match(id_card):
        check_count += 1
        report_items.append({
            "level": "错误",
            "field": get_friendly_name("id_card_number"),
            "message": f"身份证号 '{id_card}' 格式不正确，应为18位。"
        })

    # 手机号格式检查
    if data.get("work_unit_phone") == "不详" or data.get("work_unit_phone") == "无":
        phone_fields = ["current_address_phone", "contact_phone", "household_address_phone"]
    else:
        phone_fields = ["current_address_phone", "contact_phone", "household_address_phone", "work_unit_phone"]
    for field_key in phone_fields:
        phone = data.get(field_key)
        # 只有当字段有值时才进行校验；将该字段视为一项检查
        if phone:
            check_count += 1
            # 检查1: 基本格式校验
            if not PHONE_REGEX.match(phone):
                report_items.append({
                    "level": "警告",
                    "field": get_friendly_name(field_key),
                    "message": f"电话号码 '{phone}' 格式似乎不正确，请核实。"
                })
            # 检查2: 简单序列校验 (如连续、重复数字)
            if is_simple_sequence(phone):
                report_items.append({
                    "level": "警告",
                    "field": get_friendly_name(field_key),
                    "message": f"电话号码 '{phone}' 包含连续或重复数字，请核实其有效性。"
                })

    # 婚姻状况与联系人关系逻辑检查
    # 假设：婚姻状况代码 '1'=未婚, '2'=已婚。 联系人关系代码 '2'=配偶
    relationship = data.get("contact_relationship")
    marriage_status = data.get("marriage_status")
    if relationship in ["配偶", "2"]:
        check_count += 1
        if marriage_status and marriage_status not in ["已婚", "2"]:
            report_items.append({
                "level": "逻辑错误",
                "field": f"{get_friendly_name('marriage_status')}/{get_friendly_name('contact_relationship')}",
                "message": "联系人关系为'配偶'，但患者婚姻状况不是'已婚'，请核实。"
            })
    
    if marriage_status in ["未婚", "1"]:
        check_count += 1
        if relationship and relationship in ["配偶", "2"]:
            report_items.append({
                "level": "逻辑错误",
                "field": f"{get_friendly_name('marriage_status')}/{get_friendly_name('contact_relationship')}",
                "message": "患者婚姻状况为'未婚'，但联系人关系为'配偶'，请核实。"
            })           

    # 是否使用医疗机构中药制剂
    tcm_prep_fee_str = data.get("tcm_preparation_fee")
    tcm_prep_usage = data.get("tcm_preparation_usage")
    if tcm_prep_fee_str:
        try:
            # 视为一项检查
            check_count += 1
            fee = float(tcm_prep_fee_str)
            # 假设"是"的代码为"1"
            if fee > 0 and tcm_prep_usage not in ["是", "1"]:
                report_items.append({
                    "level": "逻辑错误",
                    "field": f"{get_friendly_name('tcm_preparation_fee')}/{get_friendly_name('tcm_preparation_usage')}",
                    "message": f"有'{get_friendly_name('tcm_preparation_fee')}'({fee})，但'{get_friendly_name('tcm_preparation_usage')}'不为'是'。"
                })
        except ValueError:
            # 如果费用不是有效数字，则忽略此项检查
            pass

    # 是否使用中医诊疗技术
    tcm_treat_fee_str = data.get("tcm_treatment_fee")
    tcm_tech_usage = data.get("tcm_technique_usage")
    if tcm_treat_fee_str:
        try:
            # 视为一项检查
            check_count += 1
            fee = float(tcm_treat_fee_str)
            # 假设"是"的代码为"1"
            if fee > 0 and tcm_tech_usage not in ["是", "1"]:
                report_items.append({
                    "level": "逻辑错误",
                    "field": f"{get_friendly_name('tcm_treatment_fee')}/{get_friendly_name('tcm_technique_usage')}",
                    "message": f"有'{get_friendly_name('tcm_treatment_fee')}'({fee})，但'{get_friendly_name('tcm_technique_usage')}'不为'是'。"
                })
        except ValueError:
            pass

    # 是否死亡患者尸检
    discharge_method = data.get("discharge_method")
    autopsy = data.get("autopsy")
    # 离院方式: 5-死亡; 尸检: 1-是, 2-否, 3/- 为空
    if discharge_method in ["死亡", "5"]:
        check_count += 1
        if autopsy in [None, "", "-", "3"]:
            report_items.append({
                "level": "逻辑错误",
                "field": f"{get_friendly_name('discharge_method')}/{get_friendly_name('autopsy')}",
                "message": "离院方式为'死亡'，但'死亡患者尸检'状态未明确填写为'是'或'否'。"
            })

    # 血型
    blood_fee_str = data.get("blood_fee")
    if blood_fee_str:
        try:
            check_count += 1
            fee = float(blood_fee_str)
            if fee > 0:
                blood_type = data.get("blood_type")
                rh = data.get("rh")
                # 血型: 6-未查; RH: 4-未查
                blood_type_invalid = blood_type in [None, "", "-", "未查", "6"]
                rh_invalid = rh in [None, "", "-", "未查", "4"]
                
                if blood_type_invalid or rh_invalid:
                    invalid_fields = []
                    if blood_type_invalid:
                        invalid_fields.append(get_friendly_name('blood_type'))
                    if rh_invalid:
                        invalid_fields.append(get_friendly_name('rh'))
                    
                    report_items.append({
                        "level": "逻辑错误",
                        "field": f"{get_friendly_name('blood_fee')}/{'/'.join(invalid_fields)}",
                        "message": f"有'血费'产生，但 { ' 和 '.join(invalid_fields) } 信息为'未查'或空。"
                    })
        except ValueError:
            pass
    
    # 检查地址和邮编是否“奇怪”
    address_fields = {
        "current_address": "current_address_zip",
        "household_address": "household_address_zip",
        "contact_address": None, # 联系人地址没有独立的邮编字段
        "work_unit_address": "work_unit_zip"
    }
    for addr_key, zip_key in address_fields.items():
        address = data.get(addr_key)
        # 每个地址字段视为一项检查（存在时）
        if address:
            check_count += 1
        if address and is_strange_text(address, min_len=5, placeholders=["测试", "地址", "同上"]) and address != "不详" and address != "无":
            report_items.append({
                "level": "注意",
                "field": get_friendly_name(addr_key),
                "message": f"地址 '{address}' 看起来过短或为通用占位符，请核实。"
            })
        
        if zip_key:
            zip_code = data.get(zip_key)
            if zip_code:
                check_count += 1
            if zip_code and is_strange_zip(zip_code) and zip_code != "不详" and zip_code != "无":
                report_items.append({
                    "level": "警告",
                    "field": get_friendly_name(zip_key),
                    "message": f"邮编 '{zip_code}' 格式不正确或为简单序列，请核实。"
                })
    # "病人来源" 是否和 "现住址" 匹配
    patient_source = data.get("patient_source")
    current_address = data.get("current_address")
    if patient_source and current_address:
        # 病人来源: 1-本区, 2-本市, 3-外地
        # 假设医院在上海市徐汇区或浦东新区
        check_count += 1
        is_shanghai = "上海" in current_address
        is_district = "徐汇" in current_address or "浦东" in current_address
        
        if patient_source in ["本区", "1"] and not is_district:
            report_items.append({
                "level": "注意",
                "field": f"{get_friendly_name('patient_source')}/{get_friendly_name('current_address')}",
                "message": f"病人来源为'本区'，但现住址'{current_address}'中未找到'徐汇'或'浦东'，请核实。"
            })
        elif patient_source in ["本市", "2"] and not is_shanghai:
            report_items.append({
                "level": "注意",
                "field": f"{get_friendly_name('patient_source')}/{get_friendly_name('current_address')}",
                "message": f"病人来源为'本市'，但现住址'{current_address}'中未找到'上海'，请核实。"
            })
        elif patient_source in ["外地", "3"] and is_shanghai:
            report_items.append({
                "level": "注意",
                "field": f"{get_friendly_name('patient_source')}/{get_friendly_name('current_address')}",
                "message": f"病人来源为'外地'，但现住址'{current_address}'似乎是上海地址，请核实。"
            })
    # "联系人姓名" 是否“奇怪”或与患者同名
    contact_name = data.get("contact_name")
    patient_name = data.get("name")
    
    if contact_name:
        # 检查是否为奇怪的文本
        # 联系人姓名检查计为一项
        check_count += 1
        if is_strange_text(contact_name, min_len=2, placeholders=["无", "不详", "测试", "联系人", "家属"]):
             report_items.append({
                "level": "注意",
                "field": get_friendly_name('contact_name'),
                "message": f"联系人姓名 '{contact_name}' 看起来像占位符或过短，请核实。"
            })
        # 检查是否与患者同名
        elif patient_name and contact_name == patient_name:
            report_items.append({
                "level": "注意",
                "field": f"{get_friendly_name('contact_name')}/{get_friendly_name('name')}",
                "message": "联系人姓名与患者本人姓名相同，请核实。"
            })

    # 出生地 and 籍贯: 如为占位符或过短则提示（不强制为必填）
    birth_place = data.get('birth_place')
    native_place = data.get('native_place')
    if birth_place:
        check_count += 1
        if is_strange_text(birth_place, min_len=2, placeholders=["无", "不详", "测试"]):
            report_items.append({
                'level': '注意',
                'field': get_friendly_name('birth_place'),
                'message': f"出生地 '{birth_place}' 看起来像占位符或过短，请核实。"
            })

    if native_place:
        check_count += 1
        if is_strange_text(native_place, min_len=2, placeholders=["无", "不详", "测试"]):
            report_items.append({
                'level': '注意',
                'field': get_friendly_name('native_place'),
                'message': f"籍贯 '{native_place}' 看起来像占位符或过短，请核实。"
            })

    # 工作单位: 允许为空或为'无'/'不详'，但若有内容也检查是否为占位符或过短
    work_unit = data.get('work_unit')
    if work_unit:
        check_count += 1
        if work_unit not in ["无", "不详"] and is_strange_text(work_unit, min_len=2, placeholders=["无", "不详", "测试"]):
            report_items.append({
                'level': '注意',
                'field': get_friendly_name('work_unit'),
                'message': f"工作单位 '{work_unit}' 看起来像占位符或过短，请核实。"
            })

    coder = data.get('coder')
    if coder:
        # 假设系统中“超级用户”会被标注为字符串 '超级用户' 
        check_count += 1
        try:
            if coder in ['超级用户', 'admin']:
                report_items.append({
                    'level': '警告',
                    'field': get_friendly_name('coder'),
                    'message': f"编码员不应是'{coder}'"
                })
        except Exception:
            # 如果 coder 非字符串则忽略该特定警告，但已计入检查数
            pass

    # 出院西医主要诊断入院病情 (admission_condition) 不应为 '无'
    adm_cond = data.get('admission_condition')
    tcm_adm_cond = data.get('tcm_discharge_condition')
    if adm_cond and adm_cond == '无':
        report_items.append({
            'level': '错误',
            'field': get_friendly_name('admission_condition'),
            'message': "出院西医主要诊断入院病情不应为'无'，请核实"
        })
    if tcm_adm_cond and tcm_adm_cond == '无':
        report_items.append({
            'level': '错误',
            'field': get_friendly_name('tcm_discharge_condition'),
            'message': "出院中医诊断入院病情不应为'无'，请核实"
        })

    # ================== CODE MODIFICATION START ==================
    # --- 手术和麻醉相关校验 (重构逻辑) ---

    # 1. 初始化状态变量，用于在遍历所有操作后进行全局判断
    any_op_has_anesthesia_info = False
    any_op_has_incomplete_anesthesia_info = False
    ops_with_incomplete_info = []

    if data.get('operations'):
        for i, op in enumerate(data['operations']):
            # 校验1：有手术编码但无主刀医生
            operation_code = op.get('operation_code')
            surgeon = op.get('surgeon')
            if operation_code and operation_code not in (None, '', '-', '无'):
                check_count += 1
                if not surgeon or surgeon in (None, '', '-', '无'):
                    report_items.append({
                        'level': '警告',
                        'field': f"手术及操作 {i+1} - {get_friendly_name('surgeon')}",
                        'message': "存在手术或操作编码，但主刀医师为空，请核实。"
                    })

            # 2. 收集每个操作的麻醉信息状态
            method_present = op.get('anesthesia_method') not in (None, '', '-', '无')
            anesthetist_present = op.get('anesthesiologist') not in (None, '', '-', '无')

            # 如果方式或医师任一存在，则标记为“有麻醉信息”
            if method_present or anesthetist_present:
                any_op_has_anesthesia_info = True

            # 如果两者中只有一个存在 (XOR)，则标记为“信息不完整”
            if method_present != anesthetist_present:
                any_op_has_incomplete_anesthesia_info = True
                ops_with_incomplete_info.append(str(i + 1))

    # 3. 全局麻醉逻辑判断 (在遍历所有操作之后)
    # 整个麻醉逻辑作为一个检查项
    check_count += 1
    
    # 首先，安全地解析麻醉费用
    anesthesia_fee_str = data.get('anesthesia_fee', '0')
    try:
        # 移除可能的逗号分隔符并转换为浮点数
        fee_val = float(anesthesia_fee_str.replace(',', ''))
        fee_present = fee_val > 0
    except (ValueError, TypeError):
        fee_present = False

    # 场景一：信息不完整 (最高优先级错误)
    # 无论费用如何，只要有任何一个操作的麻醉信息不完整，就必须报告错误。
    if any_op_has_incomplete_anesthesia_info:
        op_list_str = ', '.join(ops_with_incomplete_info)
        report_items.append({
            'level': '错误',
            'field': f"手术及操作 {op_list_str}",
            'message': f"有填写不完整的麻醉信息，请核实。"
        })
    
    # 场景二：费用与信息有无的逻辑矛盾
    # (此分支仅在信息完整或全无时进入)
    elif fee_present and not any_op_has_anesthesia_info:
        # 有费用，但没有任何操作填写麻醉信息 -> 确定性漏填
        report_items.append({
            'level': '错误',
            'field': f"{get_friendly_name('anesthesia_fee')}/手术操作",
            'message': "存在麻醉费用，但所有手术/操作均未填写麻醉方式或麻醉医师。"
        })
    elif not fee_present and any_op_has_anesthesia_info:
        # 没有费用，但有操作填写了麻醉信息 -> 逻辑冲突
        report_items.append({
            'level': '逻辑错误',
            'field': f"{get_friendly_name('anesthesia_fee')}/手术操作",
            'message': "没有麻醉费用，但有手术/操作填写了麻醉信息，请核实。"
        })
        
    # 场景三：逻辑上一致，但需要人工核实（您提到的难点）
    # (有费用，且有完整的麻醉信息)
    elif fee_present and any_op_has_anesthesia_info:
        report_items.append({
            'level': '注意',
            'field': f"{get_friendly_name('anesthesia_fee')}/手术操作",
            'message': "检测到麻醉费用和对应的麻醉信息。请人工核实，确保麻醉信息填写在正确的手术/操作条目下。"
        })
    # 最后一种情况 (not fee_present and not any_op_has_anesthesia_info) 是正确的，无需报告。

    # ================== CODE MODIFICATION END ==================

    #住院次数
    admission_times = data.get('admission_times')
    try:
        if admission_times not in (None, '', '-', '无'):
            atimes_val = float(admission_times)
            if atimes_val > 100:
                report_items.append({
                    'level': '注意',
                    'field': get_friendly_name('admission_times'),
                    'message': f'住院次数为 {admission_times} 次，超过 100 次，请注意。'
                })
    except Exception:
        # 如果不是数字则忽略该检查
        pass

    discharge_method = data.get('discharge_method')
    if discharge_method in ['医嘱转院', '2', '医嘱转社区']:
        # 检查是否有相关填写（例如转院去向之类字段），此处没有明确字段，查看 readmission_purpose 和 readmission_plan
        if not data.get('transferring_institution') and not data.get('transferring_institution_Community'):
            report_items.append({
                'level': '警告',
                'field': get_friendly_name('discharge_method'),
                'message': "离院方式为'医嘱转院'，但无填写内容，请核实。"
            })

    #抢救次数和“是否危重”与“是否急症”匹配
    rescue_times = data.get('rescue_times')
    critical = data.get('critical_condition')
    emergency = data.get('emergency_case')
    try:
        rescue_num = float(rescue_times) if rescue_times not in (None, '', '-', '无') else 0
    except Exception:
        rescue_num = 0
    if rescue_num > 0:
        # 判断 critical/emergency 是否存在 '是' 或 对应代码 '1'
        # 抢救相关检查视为一项
        check_count += 1
        critical_yes = str(critical).strip() in ['是', '1', 'true', 'True'] if critical is not None else False
        emergency_yes = str(emergency).strip() in ['是', '1', 'true', 'True'] if emergency is not None else False
        if not (critical_yes or emergency_yes):
            report_items.append({
                'level': '逻辑错误',
                'field': f"{get_friendly_name('rescue_times')}/{get_friendly_name('critical_condition')}/{get_friendly_name('emergency_case')}",
                'message': '记录有抢救次数，但“是否危重”与“是否急症”均未标识为是，请核实。'
            })


    info("✔ 数据校验完成。")
    case_number = data.get("case_number_verify", "")
    return report_items, case_number, check_count
