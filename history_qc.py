# history_qc.py
"""
Manage historical saving of quality-control runs according to the specified format.
Simple fields are flattened, while complex lists (diagnoses, operations) are serialized
into single cells. The file is trimmed to the last 5000 records.
"""
from __future__ import annotations
import os
import csv
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple, Set

from output import info, warning, error
from extractor_qc import get_friendly_name

# ================= FIX START: 1. 同步 MAIN_FIELDS 列表 =================
# 与最新的 extractor_qc.py 保持一致，移除了其他诊断字段
MAIN_FIELDS = [
    # 基本信息
    "name", "gender", "birth_date", "marriage_status", "birth_place", "native_place",
    "nationality", "ethnicity", "occupation", "id_card_type_code", "id_card_number",
    "patient_source",
    # 地址及联系人
    "current_address", "current_address_phone", "current_address_zip", "household_address",
    "household_address_zip", "household_address_phone", "work_unit", "work_unit_address",
    "work_unit_phone", "work_unit_zip", "contact_name", "contact_relationship",
    "contact_address", "contact_phone",
    # 入/离院信息
    "treatment_type", "admission_path", "discharge_method", "readmission_plan",
    "readmission_purpose", "transferring_institution", "transferring_institution_Community",
    # 中医特色
    "tcm_preparation_usage", "clinical_pathway", "tcm_equipment_usage",
    "tcm_technique_usage", "tcm_nursing",
    # 中医诊断
    "tcm_outpatient_disease_name", "tcm_outpatient_disease_code", "tcm_outpatient_syndrome_name",
    "tcm_outpatient_syndrome_code", "tcm_outpatient_traditional_medicine_name",
    "tcm_outpatient_traditional_medicine_code", "tcm_discharge_main_disease_name",
    "tcm_discharge_main_disease_code", "tcm_discharge_main_syndrome_name",
    "tcm_discharge_main_syndrome_code", "tcm_discharge_condition", "tcm_discharge_status",
    "tcm_discharge_treatment_principle_code", "tcm_discharge_treatment_principle_name",
    "tcm_discharge_traditional_medicine_code", "tcm_discharge_traditional_medicine_name",
    # 西医诊断
    "outpatient_disease_name", "outpatient_disease_code", "admission_disease_name",
    "admission_disease_code", "discharge_disease_name", "discharge_disease_code",
    "admission_condition", "discharge_status", "discharge_tumor_name", "discharge_tumor_code",
    # 病理及损伤
    "pathology_disease_name", "pathology_disease_code", "pathology_number", "injury_poison_code",
    # 其他
    "autopsy", "drug_allergy", "allergy_drug1", "allergy_drug2", "allergy_drug3",
    "diagnosis_consistency_outpatient", "diagnosis_consistency_admission",
    "diagnosis_consistency_operation",
    # 血型、孕产
    "blood_type", "rh", "blood_transfusion_reaction", "syphilis_screening_pregnancy",
    "postpartum_hemorrhage",
    # 医护人员及质控
    "department_director", "chief_physician", "attending_physician", "resident_physician",
    "visiting_physician", "intern_physician", "responsible_nurse", "quality_control_physician",
    "quality_control_nurse", "coder", "case_quality", "quality_control_date",
    # 住院期间情况
    "critical_condition", "difficult_case", "emergency_case", "hospital_infection",
    "blood_transfusion",
    # 抢救信息
    "rescue_times", "rescue_success",
    # 费用信息
    "blood_fee", "tcm_treatment_fee", "tcm_preparation_fee", "anesthesia_fee", "admission_times",
]
# ================= FIX END: 1. 同步 MAIN_FIELDS 列表 =================


# ================= FIX START: 2. 同步 _get_qc_checked_fields 函数 =================
def _get_qc_checked_fields() -> Set[str]:
    """返回一个包含所有被 validator_qc.py 检查的字段内部键名的集合。"""
    # 与最新的 validator_qc.py 保持同步，移除了 other_diagnoses
    return {
        # 必填项
        "name", "gender", "id_card_number", "birth_date", "marriage_status",
        "nationality", "occupation", "current_address", "contact_name",
        "contact_relationship", "contact_phone", "tcm_outpatient_syndrome_code",
        "tcm_discharge_treatment_principle_code", "tcm_discharge_treatment_principle_name",
        'department_director', 'chief_physician', 'attending_physician',
        'resident_physician', 'quality_control_physician', 'responsible_nurse', 'quality_control_nurse',
        # 格式/逻辑检查
        "current_address_phone", "household_address_phone", "work_unit_phone",
        "marriage_status", "contact_relationship",
        "tcm_preparation_fee", "tcm_preparation_usage", "tcm_treatment_fee", "tcm_technique_usage",
        "discharge_method", "autopsy", "blood_fee", "blood_type", "rh",
        "current_address_zip", "household_address_zip", "work_unit_zip",
        "patient_source", "coder", "admission_condition", "tcm_discharge_condition",
        "anesthesia_fee", "admission_times", "rescue_times", "critical_condition", "emergency_case",
        "birth_place", "native_place", "work_unit",
        "transferring_institution", "transferring_institution_Community",
        # 地址字段本身也会被检查是否奇怪
        "current_address", "household_address", "contact_address", "work_unit_address",
        # 复杂字段作为整体被检查
        "operations"
    }
# ================= FIX END: 2. 同步 _get_qc_checked_fields 函数 =================


def get_csv_path() -> str:
    """Return the full path to the records.csv inside %AppData%\Roaming\autoqc."""
    appdata = os.environ.get('APPDATA') or os.path.join(os.path.expanduser('~'), 'AppData', 'Roaming')
    base = os.path.join(appdata, 'autoqc')
    if not os.path.exists(base):
        try:
            os.makedirs(base, exist_ok=True)
        except Exception as e:
            error(f"无法创建历史记录目录 {base}: {e}")
    return os.path.join(base, 'records.csv')

def _serialize_list_of_dicts(items: List[Dict[str, Any]]) -> str:
    """将字典列表序列化为紧凑的字符串，例如：'[(名称:xx,编码:yy),...]'"""
    if not items:
        return ''
    
    serialized_items = []
    for item_dict in items:
        if not isinstance(item_dict, dict):
            continue
        
        parts = [f"{get_friendly_name(k)}:{v}" for k, v in item_dict.items()]
        serialized_items.append(f"({','.join(parts)})")
        
    return f"[{','.join(serialized_items)}]"

def build_header() -> List[str]:
    """根据 MAIN_FIELDS 列表构建固定的表头。"""
    header = ['病案号', '运行日期']
    for key in MAIN_FIELDS:
        friendly_name = get_friendly_name(key)
        header.append(friendly_name)
        header.append(f"{friendly_name}质控")
    
    header.extend(['手术操作', '手术操作质控'])
    return header

def format_row(extracted_data: Dict[str, Any], validation_results: List[Dict[str, Any]], case_number: Optional[str] = None) -> Tuple[List[str], List[str]]:
    """根据新的固定结构格式化表头和数据行。"""
    header = build_header()
    qc_checked_fields = _get_qc_checked_fields()

    field_status_map = {}
    for item in validation_results or []:
        field_name = item.get('field')
        if field_name:
            for sub_field in field_name.split('/'):
                field_status_map[sub_field] = item.get('level')

    row = []
    row.append(case_number or extracted_data.get('case_number_verify', ''))
    row.append(datetime.now().strftime('%d-%m-%Y %H:%M:%S'))

    for key in MAIN_FIELDS:
        value = extracted_data.get(key, '')
        row.append(value)
        
        friendly_name = get_friendly_name(key)
        status = '未质控'
        if friendly_name in field_status_map:
            status = '未通过'
        elif key in qc_checked_fields:
            status = '通过'
        row.append(status)

    operations_data = extracted_data.get('operations', [])
    row.append(_serialize_list_of_dicts(operations_data))

    op_status = '未质控'
    if any('手术' in f or '操作' in f for f in field_status_map):
        op_status = '未通过'
    elif 'operations' in qc_checked_fields:
        op_status = '通过'
    row.append(op_status)

    return header, row

def save_run_snapshot(extracted_data: Dict[str, Any], validation_results: List[Dict[str, Any]], case_number: Optional[str] = None, max_records: int = 5000) -> bool:
    """
    将运行快照保存到 records.csv，并确保文件只保留最新的 max_records 条记录。
    """
    try:
        path = get_csv_path()
        header, new_row = format_row(extracted_data, validation_results, case_number)
        
        records = []
        if os.path.exists(path) and os.path.getsize(path) > 0:
            with open(path, 'r', newline='', encoding='utf-8-sig') as f:
                reader = csv.reader(f)
                try:
                    next(reader) 
                    for row in reader:
                        records.append(row)
                except StopIteration:
                    pass
        
        records.append(new_row)
        
        if len(records) > max_records:
            records = records[-max_records:]
            info(f"历史记录超过 {max_records} 条，已截断为最新的 {len(records)} 条。")

        with open(path, 'w', newline='', encoding='utf-8-sig') as f:
            writer = csv.writer(f)
            writer.writerow(header)
            writer.writerows(records)
            
        global _LAST_SNAPSHOT
        _LAST_SNAPSHOT = {'extracted': extracted_data, 'validation': validation_results, 'case_number': case_number}
        return True

    except Exception as e:
        error(f"保存或截断质控历史失败: {e}")
        return False

_LAST_SNAPSHOT = None

def get_last_snapshot() -> Optional[Dict[str, Any]]:
    """返回最后一次保存的快照。"""
    return _LAST_SNAPSHOT
