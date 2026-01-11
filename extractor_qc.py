# extractor_qc.py
import time
from pywinauto.findwindows import ElementNotFoundError
from pywinauto.keyboard import send_keys
from ui_map_qc import CONTROLS_QC
from output import info, warning

# 友好名称映射已根据最新的 ui_map_qc.py
FRIENDLY_CONTROL_NAMES = {
    # ================= 基本信息 =================
    #"case_number": "病案号",
    "name": "姓名",
    "gender": "性别",
    "birth_date": "出生日期",
    "marriage_status": "婚姻状况",
    "birth_place": "出生地",
    "native_place": "籍贯",
    "nationality": "国籍",
    "ethnicity": "民族",
    "occupation": "职业",
    "id_card_type_code": "身份证类别代码",
    "id_card_number": "身份证号",
    "patient_source": "病人来源",

    # ================= 地址及联系人信息 =================
    "current_address": "现住址",
    "current_address_phone": "现住址电话",
    "current_address_zip": "现住址邮编",
    "household_address": "户口地址",
    "household_address_zip": "户口地址邮编",
    "household_address_phone": "户口地址电话",
    "work_unit": "工作单位",
    "work_unit_address": "工作单位地址",
    "work_unit_phone": "工作单位电话",
    "work_unit_zip": "工作单位邮编",
    "contact_name": "联系人姓名",
    "contact_relationship": "联系人关系",
    "contact_address": "联系人地址",
    "contact_phone": "联系人电话",
    
    # ================= 入/离院信息 =================
    "treatment_type": "治疗类别",
    "admission_path": "入院途径",
    # "admission_date": "入院时间"
    # "discharge_date": "出院时间"
    # "post_admission_diagnosis_date": "入院后确诊日期"
    "discharge_method": "离院方式",
    "readmission_plan": "是否有出院31天再住院计划",
    "readmission_purpose": "再住院目的",
    "transferring_institution":"医嘱转院接收机构",
    "transferring_institution_Community": "医嘱转社区接收机构",
    
    # ================= 中医特色诊疗 =================
    "tcm_preparation_usage": "使用医疗机构中药制剂",
    "clinical_pathway": "实施临床路径",
    "tcm_equipment_usage": "使用中医诊疗设备",
    "tcm_technique_usage": "使用中医诊疗技术",
    "tcm_nursing": "辨证施护",
    
    # ================= 中医诊断 =================
    "tcm_outpatient_disease_name": "中医门诊诊断疾病名称",
    "tcm_outpatient_disease_code": "中医门诊诊断疾病编码",
    "tcm_outpatient_syndrome_name": "中医门诊诊断症候名称",
    "tcm_outpatient_syndrome_code": "中医门诊诊断症候编码",
    "tcm_outpatient_traditional_medicine_name": "门诊传统医学名称",
    "tcm_outpatient_traditional_medicine_code": "门诊传统医学编码",
    "tcm_discharge_main_disease_name": "出院中医诊断主病名称",
    "tcm_discharge_main_disease_code": "出院中医诊断主病编码",
    "tcm_discharge_main_syndrome_name": "出院中医诊断主证名称",
    "tcm_discharge_main_syndrome_code": "出院中医诊断主证编码",
    "tcm_discharge_condition": "出院中医诊断入院病情",
    "tcm_discharge_status": "出院中医诊断出院情况",
    "tcm_discharge_treatment_principle_code": "出院治则治法编码",
    "tcm_discharge_treatment_principle_name": "出院治则治法名称",
    "tcm_discharge_traditional_medicine_code": "出院传统医学编码",
    "tcm_discharge_traditional_medicine_name": "出院传统医学名称",

    # ================= 西医诊断 =================
    "outpatient_disease_name": "门诊诊断疾病名称",
    "outpatient_disease_code": "门诊诊断疾病编码",
    "admission_disease_name": "入院诊断疾病名称",
    "admission_disease_code": "入院诊断疾病编码",
    "discharge_disease_name": "出院西医主要诊断疾病名称",
    "discharge_disease_code": "出院西医主要诊断疾病编码",
    "admission_condition": "出院西医主要诊断入院病情",
    "discharge_status": "出院西医主要诊断出院情况",
    "discharge_tumor_name": "出院西医主要诊断肿瘤名称",
    "discharge_tumor_code": "出院西医主要诊断肿瘤编码",
    
    # ================= 病理及损伤中毒 =================
    "pathology_disease_name": "病理诊断疾病名称",
    "pathology_disease_code": "病理诊断疾病编码",
    "pathology_number": "病理号",
    "injury_poison_code": "损伤中毒外因疾病编码",
    
    # ================= 过敏、尸检、诊断符合情况 =================
    "autopsy": "死亡患者尸检",
    "drug_allergy": "药物过敏",
    "allergy_drug1": "过敏药物1",
    "allergy_drug2": "过敏药物2",
    "allergy_drug3": "过敏药物3",
    "diagnosis_consistency_outpatient": "诊断符合情况门诊与出院",
    "diagnosis_consistency_admission": "诊断符合情况入院与出院",
    "diagnosis_consistency_operation": "诊断符合情况术前与术后",
    
    # ================= 血型、输血、孕产 =================
    "blood_type": "血型",
    "rh": "RH",
    "blood_transfusion_reaction": "输血反应",
    "syphilis_screening_pregnancy": "妊娠梅毒筛查",
    "postpartum_hemorrhage": "产后出血",
    
    # ================= 医护人员及质控 =================
    "department_director": "科主任",
    "chief_physician": "主任医师",
    "attending_physician": "主治医师",
    "resident_physician": "住院医师",
    "visiting_physician": "进修医师",
    "intern_physician": "实习医师",
    "responsible_nurse": "责任护士",
    "quality_control_physician": "质控医师",
    "quality_control_nurse": "质控护士",
    "coder": "编码员",
    "case_quality": "病案质量",
    "quality_control_date": "质控日期",
    
    # ================= 手术信息 =================
    "operation_code": "手术及操作编码",
    "operation_name": "手术及操作名称",
    "operation_date": "手术及操作日期",
    "operation_level": "手术级别",
    "surgeon": "主刀医师",
    "first_assistant": "一助",
    "second_assistant": "二助",
    "incision_healing": "切口/愈合",
    "anesthesia_method": "麻醉方式",
    "anesthesiologist": "麻醉医师",
    "operation_department": "手术科室",
    "is_dsa": "是否DSA下造影",
    "is_operation": "操作是否算手术人次",
    
    # ================= 住院期间情况 =================
    "critical_condition": "住院期间是否出现危重",
    "difficult_case": "住院期间是否出现疑难",
    "emergency_case": "住院期间是否出现急症",
    "hospital_infection": "住院期间是否出现医院感染",
    "blood_transfusion": "住院期间是否输血",
    
    # ================= 抢救信息 =================
    "rescue_times": "抢救次数",
    "rescue_success": "成功次数",
    
    # ================= 其他信息 =================
    "blood_fee": "血费",
    "tcm_treatment_fee": "中医治疗费",
    #"chinese_patent_medicine_fee": "中成药费",
    "tcm_preparation_fee": "医疗机构中药制剂费",
    "anesthesia_fee": "麻醉费用",
    "admission_times": "住院次数",
}

def get_friendly_name(control_key):
    """获取控件的友好名称，如果未定义则返回原始键名"""
    return FRIENDLY_CONTROL_NAMES.get(control_key, control_key)

def _extract_operations_by_keyboard(dlg, item_keys):
    """
    通过键盘操作提取手术信息。
    方法：点击“离院方式”，按“上”键进入表格，然后重复按“上”键遍历记录。
    """
    results = []
    last_data_signature = None

    try:
        # 1. 点击“离院方式”以设置焦点，然后按“上”键进入表格
        info("  定位到手术列表...")
        discharge_method_control = dlg.child_window(**CONTROLS_QC['discharge_method'])
        discharge_method_control.click_input()
        discharge_method_control.set_focus()
        time.sleep(0.1)
        send_keys('{UP}')
        time.sleep(0.2)  # 等待UI响应

        # 2. 循环提取数据
        info("  开始循环提取手术信息...")
        for _ in range(25):  # 设置最多25次循环，防止意外的无限循环
            current_item = {}
            is_empty_row = True
            for key in item_keys:
                spec = CONTROLS_QC[key]
                control = dlg.child_window(**spec)
                text_value = control.window_text().strip()
                current_item[key] = text_value
                if text_value:
                    is_empty_row = False
            
            # 如果整行都是空的，说明已超出列表范围
            if is_empty_row:
                info("  检测到空行，停止提取手术信息。")
                break

            current_signature = tuple(current_item.values())
            
            # 如果当前数据与上一条完全相同，说明已到达列表末尾
            if current_signature == last_data_signature:
                info("  检测到重复数据，已到达列表末尾。")
                break
            
            results.append(current_item)
            last_data_signature = current_signature
            
            # 按“上”键以移动到下一条记录，为下一次循环做准备
            send_keys('{UP}')
            time.sleep(0.1)

    except ElementNotFoundError as e:
        warning(f"  提取手术数据时定位控件失败: {e}。将跳过手术信息提取。")
    except Exception as e:
        warning(f"  提取手术数据时发生未知错误: {e}")
        
    return results

def extract_all_data(dlg):
    """
    从指定的对话框(dlg)中提取所有在CONTROLS_QC中定义的控件的文本值。
    包括对“手术”列表数据的循环提取。

    :param dlg: pywinauto 的窗口对象
    :return: 一个字典，键为控件的逻辑名称，值为从UI读取到的文本
    """
    info("▶ 开始从界面提取数据...")
    extracted_data = {}

    # 定义需要循环提取的字段
    operation_keys = [
        "operation_code", "operation_name", "operation_date", "operation_level", "surgeon", 
        "first_assistant", "second_assistant", "incision_healing", "anesthesia_method", 
        "anesthesiologist", "operation_department", "is_dsa", "is_operation"
    ]
    
    # 将循环提取的字段放入一个集合，以便在主循环中跳过
    skipped_keys = set(operation_keys)

    # 1. 提取所有非循环的静态字段
    for control_key, spec in CONTROLS_QC.items():
        if control_key in skipped_keys:
            continue
        try:
            control = dlg.child_window(**spec)
            control.wait('exists', timeout=2)
            text_value = control.window_text()
            extracted_data[control_key] = text_value.strip()
        except ElementNotFoundError:
            warning(f"  未找到控件 '{get_friendly_name(control_key)}' (key: {control_key})，跳过。")
            extracted_data[control_key] = None
        except Exception as e:
            warning(f"  提取控件 '{get_friendly_name(control_key)}' (key: {control_key}) 时出错: {e}")
            extracted_data[control_key] = None

    # 2. 提取“手术及操作”列表
    info("  正在提取手术及操作信息...")
    extracted_data['operations'] = _extract_operations_by_keyboard(
        dlg, operation_keys
    )

    # 3. 单独获取用于校验的病案号
    try:
        case_number_control = dlg.child_window(**CONTROLS_QC["case_number"])
        extracted_data['case_number_verify'] = case_number_control.window_text().strip()
    except Exception:
        extracted_data['case_number_verify'] = ""

    info("✔ 数据提取完成。")
    return extracted_data
