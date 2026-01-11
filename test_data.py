# test_data.py

def get_test_data():
    """
    返回用于测试的模拟数据。
    包含了各种场景的测试用例，包括正常数据和可能的问题数据。
    """
    return {
        # 基本信息（正常数据）
        "case_number_verify": "2025123456",
        "name": "张三",
        "gender": "男",
        "id_card_number": "110101199001011234",
        "ethnicity": "汉族",
        "native_place": "北京",
        "birth_date": "1990-01-01",
        "marriage_status": "已婚",
        "birth_place": "北京",
        "nationality": "中国",
        "occupation": "工人",
        "patient_source": "门诊",

        # 地址信息（部分缺失数据）
        "current_address": "北京市海淀区中关村大街123号",
        "current_address_phone": "",  # 缺失电话
        "current_address_zip": "100080",
        "household_address": "北京市海淀区中关村大街123号",
        "household_address_zip": "100080",
        "household_address_phone": "12345678",
        "work_unit": "北京某科技公司",
        "work_unit_phone": "010-12345678",
        "work_unit_address": "北京市海淀区",
        "work_unit_zip": "10008",  # 邮编错误
        "contact_name": "李四",
        "contact_relationship": "配偶",
        "contact_address": "北京市海淀区中关村大街123号",
        "contact_phone": "13800138000",

        # 诊疗信息（部分问题数据）
        "treatment_type": "住院",
        "admission_path": "门诊",
        "quality_control_date": "2025-09-17",
        "admission_date": "2025-09-15",
        "discharge_date": "2025-09-10",  # 出院日期早于入院日期
        "post_admission_diagnosis_date": "2025-09-16",

        # 中医诊疗（逻辑不一致）
        "tcm_preparation_usage": "1",
        "clinical_pathway": "0",
        "tcm_equipment_usage": "1",
        "tcm_technique_usage": "0",
        "tcm_nursing": "0",

        # 中医诊断
        "tcm_outpatient_disease_code": "ZY001",
        "tcm_outpatient_syndrome_code": "ZZ001",
        "tcm_discharge_main_disease_code": "ZY002",
        "tcm_discharge_main_syndrome": "肝郁气滞",
        "tcm_discharge_condition": "无",
        "tcm_discharge_status": "好转",

        # 西医诊断（诊断编码不规范）
        "outpatient_disease_code": "xyz123",  # 不规范的编码
        "admission_condition": "无",
        "discharge_tumor_code": "",
        "discharge_disease_code": "A01.1",
        "discharge_status": "好转",

        # 其他诊断 (新结构)
        "other_diagnoses": [
            {
                "other_diagnosis_disease_code": "B02.2",
                "other_diagnosis_disease_name": "带状疱疹",
                "other_diagnosis_admission_condition": "一般",
                "other_diagnosis_discharge_status": "好转",
                "other_diagnosis_tumor_name": "",
                "other_diagnosis_tumor_code": ""
            },
                        {
                "other_diagnosis_disease_code": "A01.2",
                "other_diagnosis_disease_name": "慢性胃炎",
                "other_diagnosis_admission_condition": "有",
                "other_diagnosis_discharge_status": "好转",
                "other_diagnosis_tumor_name": "",
                "other_diagnosis_tumor_code": ""
            }
        ],

        # 病理和特殊情况
        "pathology_disease_code": "P001",
        "pathology_number": "2025091701",
        "injury_poison_code": "",

        # 医疗信息
        "autopsy": "0",
        "drug_allergy": "1",
        "allergy_drug1": "青霉素",
        "allergy_drug2": "",
        "allergy_drug3": "",

        # 诊断符合情况
        "diagnosis_consistency_operation": "符合",
        "diagnosis_consistency_admission": "基本符合",
        "diagnosis_consistency_outpatient": "不符合",  # 诊断不一致

        # 血型和输血
        "blood_type": "A",
        "rh": "阴性",
        "blood_transfusion_reaction": "0",

        # 医护人员（缺失关键人员）
        "department_director": "王主任",
        "chief_physician": "",  # 缺失主任医师
        "attending_physician": "李医师",
        "resident_physician": "张医师",
        "responsible_nurse": "刘护士",
        "quality_control_physician": "",  # 缺失质控医师
        "quality_control_nurse": "陈护士",
        "case_quality": "甲",
        "visiting_physician": "",
        "intern_physician": "",
        "coder": "编码员A",

        # 手术信息 (新结构)
        "operations": [
                        {
                "operation_code": "中医操作001",
                "operation_name": "耳针",
                "operation_level": "无",
                "surgeon": "嘎嘎", # 主刀医师为空，用于测试
                "first_assistant": "",
                "second_assistant": "",
                "incision_healing": "无",
                "anesthesia_method": "",
                "anesthesiologist": "", 
                "operation_department": "消化科",
                "is_dsa": "0",
                "is_operation": "1",
                "operation_date": "2025-09-16" # 手术日期早于入院日期
            },
            {
                "operation_code": "中医操作002",
                "operation_name": "穴位贴敷",
                "operation_level": "无",
                "surgeon": "嘎嘎", # 主刀医师为空，用于测试
                "first_assistant": "",
                "second_assistant": "",
                "incision_healing": "无",
                "anesthesia_method": "静脉麻醉",
                "anesthesiologist": "1222", 
                "operation_department": "消化科",
                "is_dsa": "0",
                "is_operation": "1",
                "operation_date": "2025-09-16" # 手术日期早于入院日期
            }
        ],

        # 离院信息
        "discharge_method": "医嘱转院",
        "readmission_plan": "",  # 未填写再住院计划
        "readmission_purpose": "",  # 未填写再住院目的

        # 住院情况
        "critical_condition": "",
        "difficult_case": "0",
        "emergency_case": "",
        "hospital_infection": "0",
        "blood_transfusion": "0",

        # 抢救信息（数据不一致）
        "rescue_times": "2",
        "rescue_success": "3",  # 成功次数多于抢救次数

        # 费用信息
        "blood_fee": "0",
        "tcm_treatment_fee": "1200.50",
        "chinese_patent_medicine_fee": "586.20",
        "tcm_preparation_fee": "320.00",
        # 占位字段（ui_map 中为占位）
        "anesthesia_fee": "06.00",
        "admission_times": "10",
        # 将编码员设置为超级用户以触发警告
        "coder": "rrr",
    }

def get_additional_test_cases():
    """
    返回额外的测试用例，用于测试特定场景
    """
    return [
        {
            # 测试用例1：缺少必填项
            "case_number_verify": "",
            "name": "",
            "gender": "",
            "id_card_number": "",
            "operations": [], # 确保新字段存在
            "other_diagnoses": [], # 确保新字段存在
        },
        {
            # 测试用例2：数据格式错误
            "case_number_verify": "ABC123",
            "id_card_number": "12345",
            "current_address_phone": "12345",
            "birth_date": "2025-13-45",
            "operations": [],
            "other_diagnoses": [],
        },
        {
            # 测试用例3：全部正常数据
            "case_number_verify": "2025123457",
            "name": "李四",
            "gender": "女",
            "id_card_number": "110101199001011235",
            "operations": [],
            "other_diagnoses": [],
            # ... 其他字段都填写正确
        }
        ,
        {
            # 测试用例4：麻醉信息不完整（触发麻醉三项不全警告）
            "case_number_verify": "2025123460",
            "name": "王五",
            "gender": "男",
            "id_card_number": "110101199001011236",
            "operations": [
                {
                    "operation_code": "手术003",
                    "operation_name": "膝关节置换",
                    "anesthesia_method": "局麻",
                    "anesthesiologist": "", # 麻醉医师为空
                    # ... 其他手术字段
                }
            ],
            "anesthesia_fee": "", # 麻醉费用为空
            "coder": "编码员B",
            # 补足必填医护人员，避免其他干扰
            "department_director": "王主任",
            "chief_physician": "赵主任",
            "attending_physician": "孙医师",
            "resident_physician": "周医师",
            "quality_control_physician": "吴医师",
            "responsible_nurse": "刘护士",
            "quality_control_nurse": "陈护士",
        },
        {
            # 测试用例5：离院方式为医嘱转院但未填写转院目的/计划
            "case_number_verify": "2025123461",
            "name": "赵六",
            "gender": "女",
            "id_card_number": "110101199001011237",
            "discharge_method": "医嘱转院",
            "readmission_plan": "",
            "readmission_purpose": "",
            "coder": "编码员C",
            "operations": [],
            "other_diagnoses": [],
            # 补足医护人员
            "department_director": "王主任",
            "chief_physician": "赵主任",
            "attending_physician": "孙医师",
            "resident_physician": "周医师",
            "quality_control_physician": "吴医师",
            "responsible_nurse": "刘护士",
            "quality_control_nurse": "陈护士",
        }
    ]
