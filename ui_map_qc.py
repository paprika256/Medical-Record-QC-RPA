# ui_map_qc.py
# 定义首页质控窗口所有需要交互的UI控件的定位信息。

CONTROLS_QC = {
    # ================= 基本信息 =================
    "case_number": {"class_name": "TdxEdit", "found_index": 232},  # 病案号
    "name": {"class_name": "TdxEdit", "found_index": 138},  # 姓名
    "gender": {"class_name": "TdxEdit", "found_index": 137},  # 性别
    "birth_date": {"class_name": "TdxDateEdit", "found_index": 10},  # 出生年月日
    "marriage_status": {"class_name": "TdxEdit", "found_index": 135},  # 婚姻状况
    "birth_place": {"class_name": "TdxEdit", "found_index": 134},  # 出生地
    "native_place": {"class_name": "TdxEdit", "found_index": 126},  # 籍贯
    "nationality": {"class_name": "TdxEdit", "found_index": 132},  # 国籍
    "ethnicity": {"class_name": "TdxEdit", "found_index": 129},  # 民族
    "occupation": {"class_name": "TdxEdit", "found_index": 131},  # 职业
    "id_card_type_code": {"class_name": "TdxEdit", "found_index": 123}, # 身份证类别代码
    "id_card_number": {"class_name": "TdxEdit", "found_index": 130},  # 身份证号
    "patient_source": {"class_name": "TdxEdit", "found_index": 120},  # 病人来源

    # ================= 地址及联系人信息 =================
    "current_address": {"class_name": "TdxEdit", "found_index": 166},  # 现住址
    "current_address_phone": {"class_name": "TdxEdit", "found_index": 165},  # 现住址电话
    "current_address_zip": {"class_name": "TdxEdit", "found_index": 164},  # 现住址邮编
    "household_address": {"class_name": "TdxEdit", "found_index": 172},  # 户口地址
    "household_address_zip": {"class_name": "TdxEdit", "found_index": 173},  # 户口地址邮编
    "household_address_phone": {"class_name": "TdxEdit", "found_index": 174},  # 户口地址电话
    "work_unit": {"class_name": "TdxEdit", "found_index": 177},  # 工作单位
    "work_unit_address": {"class_name": "TdxEdit", "found_index": 167},  # 工作单位地址
    "work_unit_phone": {"class_name": "TdxEdit", "found_index": 175},  # 工作单位电话
    "work_unit_zip": {"class_name": "TdxEdit", "found_index": 176},  # 工作单位邮编
    "contact_name": {"class_name": "TdxEdit", "found_index": 168},  # 联系人姓名
    "contact_relationship": {"class_name": "TdxEdit", "found_index": 169},  # 联系人关系
    "contact_address": {"class_name": "TdxEdit", "found_index": 170},  # 联系人地址
    "contact_phone": {"class_name": "TdxEdit", "found_index": 171},  # 联系人电话
    
    # ================= 入/离院信息 =================
    "treatment_type": {"class_name": "TdxEdit", "found_index": 179},  # 治疗类别
    "admission_path": {"class_name": "TdxEdit", "found_index": 180},  # 入院途径
    #"admission_date": {"class_name": "TdxDateEdit", "found_index": 13},  # 入院时间
    #"discharge_date": {"class_name": "TdxDateEdit", "found_index": 12},  # 出院时间
    #"post_admission_diagnosis_date": {"class_name": "TdxDateEdit", "found_index": 11},  # 入院后确诊日期
    "discharge_method": {"class_name": "TdxEdit", "found_index": 74},  # 离院方式
    "readmission_plan": {"class_name": "TdxEdit", "found_index": 71},  # 是否有出院31天再住院计划
    "readmission_purpose": {"class_name": "TdxEdit", "found_index": 72},  # 目的
    "transferring_institution": {"class_name": "TdxEdit", "found_index": 75}, #医嘱转院接收机构
    "transferring_institution_Community": {"class_name": "TdxEdit", "found_index": 73}, #医嘱转社区接收机构

    # ================= 中医特色诊疗 =================
    "tcm_preparation_usage": {"class_name": "TdxEdit", "found_index": 3},  # 使用医疗机构中药制剂
    "clinical_pathway": {"class_name": "TdxEdit", "found_index": 7},  # 实施临床路径
    "tcm_equipment_usage": {"class_name": "TdxEdit", "found_index": 6},  # 使用中医诊疗设备
    "tcm_technique_usage": {"class_name": "TdxEdit", "found_index": 5},  # 使用中医诊疗技术
    "tcm_nursing": {"class_name": "TdxEdit", "found_index": 4},  # 辨证施护
    
    # ================= 中医诊断=================
    "tcm_outpatient_disease_name": {"class_name": "TdxEdit", "found_index": 83}, # 中医门诊诊断疾病名称
    "tcm_outpatient_disease_code": {"class_name": "TdxEdit", "found_index": 79},  # 中医门诊诊断疾病编码
    "tcm_outpatient_syndrome_name": {"class_name": "TdxEdit", "found_index": 76}, # 症候名称
    "tcm_outpatient_syndrome_code": {"class_name": "TdxEdit", "found_index": 82},  # 中医门诊诊断症候编码
    "tcm_outpatient_traditional_medicine_name": {"class_name": "TdxEdit", "found_index": 77}, # 门诊传统医学名称
    "tcm_outpatient_traditional_medicine_code": {"class_name": "TdxEdit", "found_index": 78}, # 门诊传统医学编码
    "tcm_discharge_main_disease_name": {"class_name": "TdxEdit", "found_index": 93}, # 出院中医诊断主病名称
    "tcm_discharge_main_disease_code": {"class_name": "TdxEdit", "found_index": 90},  # 出院中医诊断主病编码
    "tcm_discharge_main_syndrome_name": {"class_name": "TdxEdit", "found_index": 92},  # 出院中医诊断主证名称
    "tcm_discharge_main_syndrome_code": {"class_name": "TdxEdit", "found_index": 88},  # 出院中医诊断主证编码 
    "tcm_discharge_condition": {"class_name": "TdxEdit", "found_index": 89},  # 出院中医诊断入院病情
    "tcm_discharge_status": {"class_name": "TdxEdit", "found_index": 91},  # 出院中医诊断出院情况
    "tcm_discharge_treatment_principle_code": {"class_name": "TdxEdit", "found_index": 84}, # 出院治则治法编码
    "tcm_discharge_treatment_principle_name": {"class_name": "TdxEdit", "found_index": 85}, # 出院治则治法名称
    "tcm_discharge_traditional_medicine_code": {"class_name": "TdxEdit", "found_index": 86}, # 出院传统医学编码
    "tcm_discharge_traditional_medicine_name": {"class_name": "TdxEdit", "found_index": 87}, # 出院传统医学名称

    # ================= 西医诊断 ================
    "outpatient_disease_name": {"class_name": "TdxEdit", "found_index": 191}, # 门诊诊断疾病名称
    "outpatient_disease_code": {"class_name": "TdxEdit", "found_index": 190},  # 门诊诊断疾病编码
    "admission_disease_name": {"class_name": "TdxEdit", "found_index": 188}, # 入院诊断疾病名称
    "admission_disease_code": {"class_name": "TdxEdit", "found_index": 189}, # 入院诊断疾病编码
    "discharge_disease_name": {"class_name": "TdxEdit", "found_index": 195}, # 出院西医主要诊断疾病名称
    "discharge_disease_code": {"class_name": "TdxEdit", "found_index": 198},  # 出院西医主要诊断疾病编码
    "admission_condition": {"class_name": "TdxEdit", "found_index": 203},  # 出院西医主要诊断入院病情
    "discharge_status": {"class_name": "TdxEdit", "found_index": 204},  # 出院西医主要诊断出院情况
    "discharge_tumor_name": {"class_name": "TdxEdit", "found_index": 194}, # 出院西医主要诊断肿瘤名称
    "discharge_tumor_code": {"class_name": "TdxEdit", "found_index": 193},  # 出院西医主要诊断肿瘤编码

    # ================= 其他诊断 =================
    "other_diagnosis_disease_code": {"class_name": "TdxEdit", "found_index": 206},  # 其他诊断疾病编码
    "other_diagnosis_disease_name": {"class_name": "TdxEdit", "found_index": 201},  # 其他出院诊断疾病名称
    "other_diagnosis_admission_condition": {"class_name": "TdxEdit", "found_index": 203},  # 其他诊断入院病情
    "other_diagnosis_discharge_status": {"class_name": "TdxEdit", "found_index": 204},  # 其他诊断出院情况
    "other_diagnosis_tumor_name": {"class_name": "TdxEdit", "found_index": 200}, # 其他诊断肿瘤名称 
    "other_diagnosis_tumor_code": {"class_name": "TdxEdit", "found_index": 205},  # 其他诊断肿瘤编码
    
    # ================= 病理及损伤中毒 =================
    "pathology_disease_name": {"class_name": "TdxEdit", "found_index": 208}, # 病理诊断疾病名称
    "pathology_disease_code": {"class_name": "TdxEdit", "found_index": 210},  # 病理诊断疾病编码
    "pathology_number": {"class_name": "TdxEdit", "found_index": 211},  # 病理号
    "injury_poison_code": {"class_name": "TdxEdit", "found_index": 209},  # 损伤中毒外因疾病编码 
    
    # ================= 过敏、尸检、诊断符合情况 =================
    "autopsy": {"class_name": "TdxEdit", "found_index": 115},  # 死亡患者尸检
    "drug_allergy": {"class_name": "TdxEdit", "found_index": 116},  # 药物过敏
    "allergy_drug1": {"class_name": "TdxEdit", "found_index": 119},  # 过敏药物1
    "allergy_drug2": {"class_name": "TdxEdit", "found_index": 118},  # 过敏药物2
    "allergy_drug3": {"class_name": "TdxEdit", "found_index": 117},  # 过敏药物3
    "diagnosis_consistency_outpatient": {"class_name": "TdxEdit", "found_index": 114},  # 诊断符合情况门诊与出院
    "diagnosis_consistency_admission": {"class_name": "TdxEdit", "found_index": 113},  # 诊断符合情况入院与出院
    "diagnosis_consistency_operation": {"class_name": "TdxEdit", "found_index": 112},  # 诊断符合情况术前与术后
    
    # ================= 血型、输血、孕产 =================
    "blood_type": {"class_name": "TdxEdit", "found_index": 98},  # 血型
    "rh": {"class_name": "TdxEdit", "found_index": 97},  # RH
    "blood_transfusion_reaction": {"class_name": "TdxEdit", "found_index": 96},  # 输血反应
    "syphilis_screening_pregnancy": {"class_name": "TdxEdit", "found_index": 95}, # 妊娠梅毒筛查 
    "postpartum_hemorrhage": {"class_name": "TdxEdit", "found_index": 94},      # 产后出血 
    
    # ================= 医护人员及质控 =================
    "department_director": {"class_name": "TdxEdit", "found_index": 106},  # 科主任
    "chief_physician": {"class_name": "TdxEdit", "found_index": 109},  # 主任医师
    "attending_physician": {"class_name": "TdxEdit", "found_index": 108},  # 主治医师
    "resident_physician": {"class_name": "TdxEdit", "found_index": 107},  # 住院医师
    "visiting_physician": {"class_name": "TdxEdit", "found_index": 105},  # 进修医师
    "intern_physician": {"class_name": "TdxEdit", "found_index": 104},  # 实习医师
    "responsible_nurse": {"class_name": "TdxEdit", "found_index": 100},  # 责任护士
    "quality_control_physician": {"class_name": "TdxEdit", "found_index": 102},  # 质控医师
    "quality_control_nurse": {"class_name": "TdxEdit", "found_index": 101},  # 质控护士
    "coder": {"class_name": "TdxEdit", "found_index": 103},  # 编码员
    "case_quality": {"class_name": "TdxEdit", "found_index": 99},  # 病案质量
    "quality_control_date": {"class_name": "TdxDateEdit", "found_index": 9},  # 质控日期
    
    # ================= 手术信息 =================
    "operation_code": {"class_name": "TdxEdit", "found_index": 218},  # 手术及操作编码
    "operation_name": {"class_name": "TdxEdit", "found_index": 217},  # 手术及操作名称
    "operation_date": {"class_name": "TdxDateEdit", "found_index": 14},  # 手术及操作日期
    "operation_level": {"class_name": "TdxEdit", "found_index": 219},  # 手术级别
    "surgeon": {"class_name": "TdxEdit", "found_index": 223},  # 主刀医师
    "first_assistant": {"class_name": "TdxEdit", "found_index": 222},  # 一助
    "second_assistant": {"class_name": "TdxEdit", "found_index": 221},  # 二助
    "incision_healing": {"class_name": "TdxEdit", "found_index": 220},  # 切口/愈合
    "anesthesia_method": {"class_name": "TdxEdit", "found_index": 226},  # 麻醉方式
    "anesthesiologist": {"class_name": "TdxEdit", "found_index": 225},  # 麻醉医师
    "operation_department": {"class_name": "TdxEdit", "found_index": 216},  # 手术科室
    "is_dsa": {"class_name": "TdxEdit", "found_index": 215},  # 是否DSA下造影
    "is_operation": {"class_name": "TdxEdit", "found_index": 214},  # 操作是否算手术人次
    
    # ================= 住院期间情况 =================
    "critical_condition": {"class_name": "TdxEdit", "found_index": 54},  # 住院期间是否出现危重
    "difficult_case": {"class_name": "TdxEdit", "found_index": 53},  # 住院期间是否出现疑难
    "emergency_case": {"class_name": "TdxEdit", "found_index": 52},  # 住院期间是否出现急症
    "hospital_infection": {"class_name": "TdxEdit", "found_index": 51},  # 住院期间是否出现医院感染
    "blood_transfusion": {"class_name": "TdxEdit", "found_index": 46},  # 住院期间是否输血
    
    # ================= 抢救信息 =================
    "rescue_times": {"class_name": "TdxCurrencyEdit", "found_index": 1},  # 抢救次数
    "rescue_success": {"class_name": "TdxCurrencyEdit", "found_index": 0},  # 成功次数
    
    # ================= 其他信息 =================
    "blood_fee": {"class_name": "TdxCurrencyEdit", "found_index": 42},  # 血费
    "tcm_treatment_fee": {"class_name": "TdxCurrencyEdit", "found_index": 25},  # 中医治疗费
   # "chinese_patent_medicine_fee": {"class_name": "TdxCurrencyEdit", "found_index": 40},  # 中成药费
    "tcm_preparation_fee": {"class_name": "TdxCurrencyEdit", "found_index": 14},  # 医疗机构中药制剂费
    "anesthesia_fee": {"class_name": "TdxCurrencyEdit", "found_index": 41},  # 麻醉费用
    "admission_times": {"class_name": "TdxCurrencyEdit", "found_index": 48},  # 住院次数
}
