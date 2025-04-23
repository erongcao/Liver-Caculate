import sys
import numpy as np
import math
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QRadioButton, QButtonGroup, QPushButton,
    QTextEdit, QGroupBox, QSizePolicy, QMessageBox, QTabWidget
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QFont

class ASAPCalculatorApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("肝病计算器")
        self.resize(800, 600)
        self._setup_ui()
        self._setup_styles()

    def _setup_ui(self):
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout(main_widget)
        
        # 创建两个工作区
        tab_widget = QTabWidget()
        
        # ASAP/GALAD工作区
        asap_tab = QWidget()
        asap_layout = QVBoxLayout(asap_tab)
        
        # 基本信息
        basic_info_group = QGroupBox("基本信息")
        basic_info_layout = QVBoxLayout(basic_info_group)
        
        # 年龄和性别
        age_gender_row = QHBoxLayout()
        age_layout = QHBoxLayout()
        age_layout.addWidget(QLabel("年龄（岁）:"))
        self.age_entry = QLineEdit()
        self.age_entry.setPlaceholderText("18-120岁")
        age_layout.addWidget(self.age_entry)
        age_gender_row.addLayout(age_layout)
        
        gender_group = QGroupBox("性别")
        gender_layout = QHBoxLayout(gender_group)
        self.male_radio = QRadioButton("男性")
        self.female_radio = QRadioButton("女性")
        self.gender_group = QButtonGroup(self)
        self.gender_group.addButton(self.male_radio)
        self.gender_group.addButton(self.female_radio)
        self.male_radio.setChecked(True)
        gender_layout.addWidget(self.male_radio)
        gender_layout.addWidget(self.female_radio)
        age_gender_row.addWidget(gender_group)
        
        basic_info_layout.addLayout(age_gender_row)
        asap_layout.addWidget(basic_info_group)
        
        # 生物标志物
        biomarker_group = QGroupBox("肝癌标志物")
        biomarker_layout = QVBoxLayout(biomarker_group)
        
        # AFP, PIVKA-II, AFP-L3%
        biomarker_row = QHBoxLayout()
        afp_layout = QHBoxLayout()
        afp_layout.addWidget(QLabel("AFP（ng/mL）:"))
        self.afp_entry = QLineEdit()
        afp_layout.addWidget(self.afp_entry)
        biomarker_row.addLayout(afp_layout)

        pivka_layout = QHBoxLayout()
        pivka_layout.addWidget(QLabel("PIVKA-II（mAU/mL）:"))
        self.pivka_entry = QLineEdit()
        pivka_layout.addWidget(self.pivka_entry)
        biomarker_row.addLayout(pivka_layout)

        afp_l3_layout = QHBoxLayout()
        afp_l3_layout.addWidget(QLabel("AFP-L3%（可选）:"))
        self.afp_l3_entry = QLineEdit()
        self.afp_l3_entry.setPlaceholderText("0-100%")
        afp_l3_layout.addWidget(self.afp_l3_entry)
        biomarker_row.addLayout(afp_l3_layout)
        
        biomarker_layout.addLayout(biomarker_row)
        asap_layout.addWidget(biomarker_group)
        
        # ANI工作区
        ani_tab = QWidget()
        ani_layout = QVBoxLayout(ani_tab)
        
        # ANI基本信息
        ani_basic_group = QGroupBox("ANI基本信息")
        ani_basic_layout = QVBoxLayout(ani_basic_group)
        
        # 身高体重
        height_weight_row = QHBoxLayout()
        height_layout = QHBoxLayout()
        height_layout.addWidget(QLabel("身高（cm）:"))
        self.height_entry = QLineEdit()
        height_layout.addWidget(self.height_entry)
        height_weight_row.addLayout(height_layout)

        weight_layout = QHBoxLayout()
        weight_layout.addWidget(QLabel("体重（kg）:"))
        self.weight_entry = QLineEdit()
        weight_layout.addWidget(self.weight_entry)
        height_weight_row.addLayout(weight_layout)
        
        ani_basic_layout.addLayout(height_weight_row)
        
        # ANI指标
        ani_biomarker_group = QGroupBox("ANI指标")
        ani_biomarker_layout = QVBoxLayout(ani_biomarker_group)
        
        ani_row = QHBoxLayout()
        mcv_layout = QHBoxLayout()
        mcv_layout.addWidget(QLabel("MCV（fL）:"))
        self.mcv_entry = QLineEdit()
        mcv_layout.addWidget(self.mcv_entry)
        ani_row.addLayout(mcv_layout)

        ast_layout = QHBoxLayout()
        ast_layout.addWidget(QLabel("AST（U/L）:"))
        self.ast_entry = QLineEdit()
        ast_layout.addWidget(self.ast_entry)
        ani_row.addLayout(ast_layout)

        alt_layout = QHBoxLayout()
        alt_layout.addWidget(QLabel("ALT（U/L）:"))
        self.alt_entry = QLineEdit()
        alt_layout.addWidget(self.alt_entry)
        ani_row.addLayout(alt_layout)
        
        ani_biomarker_layout.addLayout(ani_row)
        ani_layout.addWidget(ani_basic_group)
        ani_layout.addWidget(ani_biomarker_group)
        
        # FLI工作区
        fli_tab = QWidget()
        fli_layout = QVBoxLayout(fli_tab)
        
        # FLI指标
        fli_biomarker_group = QGroupBox("FLI指标")
        fli_biomarker_layout = QVBoxLayout(fli_biomarker_group)
        
        # 身高体重
        height_weight_row = QHBoxLayout()
        height_layout = QHBoxLayout()
        height_layout.addWidget(QLabel("身高(cm):"))
        self.height_fli_entry = QLineEdit()
        height_layout.addWidget(self.height_fli_entry)
        height_weight_row.addLayout(height_layout)

        weight_layout = QHBoxLayout()
        weight_layout.addWidget(QLabel("体重(kg):"))
        self.weight_fli_entry = QLineEdit()
        weight_layout.addWidget(self.weight_fli_entry)
        height_weight_row.addLayout(weight_layout)
        
        fli_biomarker_layout.addLayout(height_weight_row)

        # 甘油三酯、GGT、腰围
        fli_row1 = QHBoxLayout()
        trig_layout = QHBoxLayout()
        trig_layout.addWidget(QLabel("甘油三酯(mmol/L):"))
        self.trig_entry = QLineEdit()
        trig_layout.addWidget(self.trig_entry)
        fli_row1.addLayout(trig_layout)
        
        fli_biomarker_layout.addLayout(fli_row1)
        
        fli_row2 = QHBoxLayout()
        ggt_layout = QHBoxLayout()
        ggt_layout.addWidget(QLabel("GGT(U/L):"))
        self.ggt_entry = QLineEdit()
        ggt_layout.addWidget(self.ggt_entry)
        fli_row2.addLayout(ggt_layout)

        waist_layout = QHBoxLayout()
        waist_layout.addWidget(QLabel("腰围(cm):"))
        self.waist_entry = QLineEdit()
        waist_layout.addWidget(self.waist_entry)
        fli_row2.addLayout(waist_layout)
        
        fli_biomarker_layout.addLayout(fli_row2)
        fli_layout.addWidget(fli_biomarker_group)
        
        # 按钮区域
        fli_btn_layout = QHBoxLayout()
        self.fli_btn = QPushButton("计算FLI")
        fli_btn_layout.addWidget(self.fli_btn)
        fli_layout.addLayout(fli_btn_layout)
        
        # 结果显示区域
        self.fli_result = QTextEdit()
        self.fli_result.setReadOnly(True)
        fli_layout.addWidget(self.fli_result)
        
        # 连接信号
        self.fli_btn.clicked.connect(self.calculate_fli)

        # 添加标签页
        # NFS工作区
        nfs_tab = QWidget()
        nfs_layout = QVBoxLayout(nfs_tab)
        
        # NFS基本信息
        nfs_basic_group = QGroupBox("基本信息")
        nfs_basic_layout = QVBoxLayout(nfs_basic_group)
        
        # 年龄、身高、体重
        info_row = QHBoxLayout()
        info_row.setSpacing(15)  # 增加组间距离
        
        age_layout = QHBoxLayout()
        age_layout.setSpacing(2)  # 标签与输入框间距2px
        age_label = QLabel("年龄(岁):")
        age_label.setContentsMargins(0, 0, 5, 0)  # 右间距5px
        age_layout.addWidget(age_label)
        self.nfs_age_entry = QLineEdit()
        self.nfs_age_entry.setMaximumWidth(80)
        age_layout.addWidget(self.nfs_age_entry)
        info_row.addLayout(age_layout)

        height_layout = QHBoxLayout()
        height_layout.setSpacing(2)  # 标签与输入框间距2px
        height_label = QLabel("身高(cm):")
        height_label.setContentsMargins(0, 0, 5, 0)  # 右间距5px
        height_layout.addWidget(height_label)
        self.nfs_height_entry = QLineEdit()
        self.nfs_height_entry.setMaximumWidth(80)
        height_layout.addWidget(self.nfs_height_entry)
        info_row.addLayout(height_layout)

        weight_layout = QHBoxLayout()
        weight_layout.setSpacing(2)  # 标签与输入框间距2px
        weight_label = QLabel("体重(kg):")
        weight_label.setContentsMargins(0, 0, 5, 0)  # 右间距5px
        weight_layout.addWidget(weight_label)
        self.nfs_weight_entry = QLineEdit()
        self.nfs_weight_entry.setMaximumWidth(80)
        weight_layout.addWidget(self.nfs_weight_entry)
        info_row.addLayout(weight_layout)

        # IFG/糖尿病状态
        diabetes_layout = QHBoxLayout()
        diabetes_layout.setSpacing(5)
        diabetes_layout.addWidget(QLabel("IFG/糖尿病:"))
        self.diabetes_yes = QRadioButton("是")
        self.diabetes_no = QRadioButton("否")
        self.diabetes_group = QButtonGroup(self)
        self.diabetes_group.addButton(self.diabetes_yes)
        self.diabetes_group.addButton(self.diabetes_no)
        self.diabetes_no.setChecked(True)
        diabetes_layout.addWidget(self.diabetes_yes)
        diabetes_layout.addWidget(self.diabetes_no)
        info_row.addLayout(diabetes_layout)
        
        nfs_basic_layout.addLayout(info_row)
        
        nfs_layout.addWidget(nfs_basic_group)
        
        # NFS指标
        nfs_biomarker_group = QGroupBox("NFS指标")
        nfs_biomarker_layout = QVBoxLayout(nfs_biomarker_group)
        
        # AST/ALT
        ast_alt_row = QHBoxLayout()
        ast_layout = QHBoxLayout()
        ast_layout.addWidget(QLabel("AST(U/L):"))
        self.nfs_ast_entry = QLineEdit()
        ast_layout.addWidget(self.nfs_ast_entry)
        ast_alt_row.addLayout(ast_layout)

        alt_layout = QHBoxLayout()
        alt_layout.addWidget(QLabel("ALT(U/L):"))
        self.nfs_alt_entry = QLineEdit()
        alt_layout.addWidget(self.nfs_alt_entry)
        ast_alt_row.addLayout(alt_layout)
        
        nfs_biomarker_layout.addLayout(ast_alt_row)
        
        # 血小板和血清白蛋白
        platelet_albumin_row = QHBoxLayout()
        platelet_layout = QHBoxLayout()
        platelet_layout.addWidget(QLabel("血小板(×10⁹/L):"))
        self.platelet_entry = QLineEdit()
        platelet_layout.addWidget(self.platelet_entry)
        platelet_albumin_row.addLayout(platelet_layout)

        albumin_layout = QHBoxLayout()
        albumin_layout.addWidget(QLabel("血清白蛋白(g/L):"))
        self.albumin_entry = QLineEdit()
        albumin_layout.addWidget(self.albumin_entry)
        platelet_albumin_row.addLayout(albumin_layout)
        
        nfs_biomarker_layout.addLayout(platelet_albumin_row)
        nfs_layout.addWidget(nfs_biomarker_group)
        
        # 按钮区域
        nfs_btn_layout = QHBoxLayout()
        self.nfs_btn = QPushButton("计算NFS")
        nfs_btn_layout.addWidget(self.nfs_btn)
        nfs_layout.addLayout(nfs_btn_layout)
        
        # 结果显示区域
        self.nfs_result = QTextEdit()
        self.nfs_result.setReadOnly(True)
        nfs_layout.addWidget(self.nfs_result)
        
        # 连接信号
        self.nfs_btn.clicked.connect(self.calculate_nfs)

        # 添加标签页
        tab_widget.addTab(asap_tab, "ASAP/GALAD")
        tab_widget.addTab(ani_tab, "ANI")
        tab_widget.addTab(fli_tab, "FLI")
        tab_widget.addTab(nfs_tab, "NFS")

        # FIB-4工作区
        fib4_tab = QWidget()
        fib4_layout = QVBoxLayout(fib4_tab)
        
        # FIB-4基本信息
        fib4_basic_group = QGroupBox("基本信息")
        fib4_basic_layout = QVBoxLayout(fib4_basic_group)
        
        # 年龄
        age_layout = QHBoxLayout()
        age_layout.setSpacing(2)
        age_label = QLabel("年龄(岁):")
        age_label.setContentsMargins(0, 0, 5, 0)
        age_layout.addWidget(age_label)
        self.fib4_age_entry = QLineEdit()
        self.fib4_age_entry.setMaximumWidth(80)
        age_layout.addWidget(self.fib4_age_entry)
        fib4_basic_layout.addLayout(age_layout)
        
        fib4_layout.addWidget(fib4_basic_group)
        
        # FIB-4指标
        fib4_biomarker_group = QGroupBox("FIB-4指标")
        fib4_biomarker_layout = QVBoxLayout(fib4_biomarker_group)
        
        # AST/ALT
        ast_alt_row = QHBoxLayout()
        ast_layout = QHBoxLayout()
        ast_layout.addWidget(QLabel("AST(U/L):"))
        self.fib4_ast_entry = QLineEdit()
        ast_layout.addWidget(self.fib4_ast_entry)
        ast_alt_row.addLayout(ast_layout)

        alt_layout = QHBoxLayout()
        alt_layout.addWidget(QLabel("ALT(U/L):"))
        self.fib4_alt_entry = QLineEdit()
        alt_layout.addWidget(self.fib4_alt_entry)
        ast_alt_row.addLayout(alt_layout)
        
        fib4_biomarker_layout.addLayout(ast_alt_row)
        
        # 血小板
        platelet_layout = QHBoxLayout()
        platelet_layout.addWidget(QLabel("血小板(×10⁹/L):"))
        self.fib4_platelet_entry = QLineEdit()
        platelet_layout.addWidget(self.fib4_platelet_entry)
        fib4_biomarker_layout.addLayout(platelet_layout)
        
        fib4_layout.addWidget(fib4_biomarker_group)
        
        # 按钮区域
        fib4_btn_layout = QHBoxLayout()
        self.fib4_btn = QPushButton("计算FIB-4")
        fib4_btn_layout.addWidget(self.fib4_btn)
        fib4_layout.addLayout(fib4_btn_layout)
        
        # 结果显示区域
        self.fib4_result = QTextEdit()
        self.fib4_result.setReadOnly(True)
        fib4_layout.addWidget(self.fib4_result)
        
        # 连接信号
        self.fib4_btn.clicked.connect(self.calculate_fib4)

        # 添加标签页
        tab_widget.addTab(fib4_tab, "FIB-4")
        
        main_layout.addWidget(tab_widget)
        
        # 按钮区域 - 添加到各自的工作区
        asap_btn_layout = QHBoxLayout()
        self.asap_btn = QPushButton("计算ASAP风险")
        self.galad_btn = QPushButton("计算GALAD评分")
        asap_btn_layout.addWidget(self.asap_btn)
        asap_btn_layout.addWidget(self.galad_btn)
        asap_layout.addLayout(asap_btn_layout)

        ani_btn_layout = QHBoxLayout()
        self.ani_btn = QPushButton("计算ANI")
        ani_btn_layout.addWidget(self.ani_btn)
        ani_layout.addLayout(ani_btn_layout)
        
        # 为每个工作区创建独立的结果显示区域
        self.asap_result = QTextEdit()
        self.asap_result.setReadOnly(True)
        asap_layout.addWidget(self.asap_result)
        
        self.ani_result = QTextEdit()
        self.ani_result.setReadOnly(True)
        ani_layout.addWidget(self.ani_result)
        
        # 连接信号
        self.asap_btn.clicked.connect(self.calculate_asap)
        self.galad_btn.clicked.connect(self.calculate_galad)
        self.ani_btn.clicked.connect(self.calculate_ani)

    def _create_input_field(self, layout, label, field_name):
        row = QHBoxLayout()
        row.addWidget(QLabel(label))
        field = QLineEdit()
        setattr(self, field_name, field)  # 动态设置实例变量
        row.addWidget(field)
        layout.addLayout(row)
        return field

    def _setup_styles(self):
        self.setStyleSheet("""
            QMainWindow {
                background-color: #FFF5E6;
            }
            QGroupBox {
                font-size: 14px;
                font-weight: bold;
                margin-top: 10px;
                border: 2px solid #8B5A2B;
                border-radius: 10px;
                padding-top: 15px;
                background-color: #FFEEDD;
                color: #5D3A1A;
            }
            QLabel {
                color: #5D3A1A;
                font-size: 13px;
            }
            QLineEdit, QTextEdit {
                background-color: #FFF9F0;
                border: 1px solid #B38B6D;
                border-radius: 5px;
                padding: 6px;
                color: #5D3A1A;
                selection-background-color: #B38B6D;
            }
            QPushButton {
                min-width: 120px;
                padding: 8px 12px;
                background-color: #8B5A2B;
                color: #FFF5E6;
                border-radius: 8px;
                border: 1px solid #5D3A1A;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #A67C52;
            }
            QPushButton:pressed {
                background-color: #5D3A1A;
            }
            QRadioButton {
                color: #5D3A1A;
                spacing: 5px;
            }
            QRadioButton::indicator {
                width: 16px;
                height: 16px;
                border-radius: 8px;
                border: 1px solid #5D3A1A;
            }
            QRadioButton::indicator:checked {
                background-color: #8B5A2B;
                border: 3px solid #FFEEDD;
            }
        """)

    def validate_inputs(self):
        try:
            # 验证年龄
            age_text = self.age_entry.text().strip()
            if not age_text:
                raise ValueError("请输入年龄")
            age = float(age_text)
            if age <= 0 or age > 120:
                raise ValueError("年龄必须在0-120岁之间")

            # 验证AFP
            afp_text = self.afp_entry.text().strip()
            if not afp_text:
                raise ValueError("请输入AFP值")
            afp = float(afp_text)
            if afp <= 0:
                raise ValueError("AFP值必须大于0")

            # 验证PIVKA-II
            pivka_text = self.pivka_entry.text().strip()
            if not pivka_text:
                raise ValueError("请输入PIVKA-II值")
            pivka = float(pivka_text)
            if pivka <= 0:
                raise ValueError("PIVKA-II值必须大于0")

            return age, afp, pivka
        except ValueError as e:
            QMessageBox.critical(self, "输入错误", str(e))
            return None, None, None

    def validate_ani_inputs(self):
        try:
            # 验证MCV
            mcv_text = self.mcv_entry.text().strip()
            if not mcv_text:
                raise ValueError("请输入MCV值")
            mcv = float(mcv_text)
            if mcv <= 0:
                raise ValueError("MCV值必须大于0")

            # 验证AST
            ast_text = self.ast_entry.text().strip()
            if not ast_text:
                raise ValueError("请输入AST值")
            ast = float(ast_text)
            if ast <= 0:
                raise ValueError("AST值必须大于0")

            # 验证ALT
            alt_text = self.alt_entry.text().strip()
            if not alt_text:
                raise ValueError("请输入ALT值")
            alt = float(alt_text)
            if alt <= 0:
                raise ValueError("ALT值必须大于0")

            # 验证身高体重
            height_text = self.height_entry.text().strip()
            if not height_text:
                raise ValueError("请输入身高")
            height = float(height_text)
            if height <= 0:
                raise ValueError("身高必须大于0")

            weight_text = self.weight_entry.text().strip()
            if not weight_text:
                raise ValueError("请输入体重")
            weight = float(weight_text)
            if weight <= 0:
                raise ValueError("体重必须大于0")

            # 计算BMI: 体重(kg) / (身高(m))^2
            bmi = weight / ((height / 100) ** 2)

            return mcv, ast, alt, bmi
        except ValueError as e:
            QMessageBox.critical(self, "输入错误", str(e))
            return None, None, None, None

    def calculate_ani(self):
        mcv, ast, alt, bmi = self.validate_ani_inputs()
        if mcv is None:
            return
            
        try:
            # Apply corrections
            mcv_corrected = 92 if mcv < 92 else (103 if mcv > 103 else mcv)
            ast_alt_ratio = ast / alt
            ast_alt_corrected = 3 if ast_alt_ratio > 3 else ast_alt_ratio
            gender_coeff = 6.35 if self.male_radio.isChecked() else 0
            
            # Calculate ANI score
            ani_score = -58.5 + 0.637 * mcv_corrected + 3.91 * ast_alt_corrected - 0.406 * bmi + gender_coeff
            
            # Calculate probability
            probability = math.exp(ani_score) / (1 + math.exp(ani_score))
            
            # Determine diagnosis
            if ani_score > 0:
                diagnosis = "酒精性脂肪肝(ALD)可能性高"
            elif ani_score < -0.22:
                diagnosis = "非酒精性脂肪肝(NAFLD)可能性高"
            else:
                diagnosis = "无法明确分辨，可能兼而有之"
            
            self.show_result(
                "ANI模型计算结果",
                f"ANI评分: {ani_score:.2f}\n"
                f"诊断概率: {probability:.1%}\n"
                f"诊断: {diagnosis}"
            )
            
        except Exception as e:
            QMessageBox.critical(self, "计算错误", f"ANI计算出错: {e}")

    def calculate_asap(self):
        age, afp, pivka = self.validate_inputs()
        if age is None:
            return

        gender = 0 if self.male_radio.isChecked() else 1
        ln_afp = np.log(afp)
        ln_pivka = np.log(pivka)
        asap_score = -7.57711770 + 0.04666357 * age - 0.57611693 * gender + 0.42243533 * ln_afp + 1.10518910 * ln_pivka
        risk_probability = 1 / (1 + np.exp(-asap_score))

        if risk_probability <= 0.333:
            category = "低风险"
            recommendation = "建议每6个月进行AFP+PIVKA-II和超声检查"
        elif risk_probability <= 0.666:
            category = "中风险"
            recommendation = "建议进行肝脏超声检查，有条件时进行增强CT或MRI"
        else:
            category = "高风险"
            recommendation = "建议立即进行肝脏动态CT或增强MRI检查"

        self.show_result(
            "ASAP模型计算结果",
            f"ASAP评分: {asap_score:.2f}\n"
            f"肝癌风险概率: {risk_probability:.2%}\n"
            f"风险等级: {category}\n"
            f"建议: {recommendation}"
        )

    def validate_fli_inputs(self):
        try:
            # 验证身高体重
            height_text = self.height_fli_entry.text().strip()
            if not height_text:
                raise ValueError("请输入身高")
            height = float(height_text)
            if height <= 0:
                raise ValueError("身高必须大于0")

            weight_text = self.weight_fli_entry.text().strip()
            if not weight_text:
                raise ValueError("请输入体重")
            weight = float(weight_text)
            if weight <= 0:
                raise ValueError("体重必须大于0")

            # 计算BMI
            bmi = weight / ((height / 100) ** 2)

            # 验证甘油三酯
            trig_text = self.trig_entry.text().strip()
            if not trig_text:
                raise ValueError("请输入甘油三酯值")
            trig = float(trig_text)
            if trig <= 0:
                raise ValueError("甘油三酯值必须大于0")
            # 转换为mg/dL用于计算
            trig_mgdl = trig * 88.57

            # 验证GGT
            ggt_text = self.ggt_entry.text().strip()
            if not ggt_text:
                raise ValueError("请输入GGT值")
            ggt = float(ggt_text)
            if ggt <= 0:
                raise ValueError("GGT值必须大于0")

            # 验证腰围
            waist_text = self.waist_entry.text().strip()
            if not waist_text:
                raise ValueError("请输入腰围值")
            waist = float(waist_text)
            if waist <= 0:
                raise ValueError("腰围值必须大于0")

            return trig_mgdl, bmi, ggt, waist
        except ValueError as e:
            QMessageBox.critical(self, "输入错误", str(e))
            return None, None, None, None

    def calculate_fli(self):
        trig_mgdl, bmi, ggt, waist = self.validate_fli_inputs()
        if trig_mgdl is None:
            return
            
        try:
            # 计算FLI
            log_trig = math.log(trig_mgdl)
            log_ggt = math.log(ggt)
            numerator = math.exp(0.953 * log_trig + 0.139 * bmi + 0.718 * log_ggt + 0.053 * waist - 15.745)
            fli_score = (numerator / (1 + numerator)) * 100
            
            # 解释结果
            if fli_score < 30:
                interpretation = "脂肪肝可能性低(阴性预测值15%)"
                color = "#2ecc71"  # 绿色
            elif fli_score < 60:
                interpretation = "结果不确定"
                color = "#f1c40f"  # 橙色
            else:
                interpretation = "脂肪肝可能性高(阳性预测值99%)"
                color = "#e74c3c"  # 红色
            
            self.show_result(
                "脂肪肝指数(FLI)计算结果",
                f"FLI评分: {fli_score:.1f}\n"
                f"解释: {interpretation}\n\n"
                f"计算公式:\n"
                f"FLI = (e^(0.953×ln(甘油三酯) + 0.139×BMI + 0.718×ln(GGT) + 0.053×腰围 - 15.745)) / (1 + e^(0.953×ln(甘油三酯) + 0.139×BMI + 0.718×ln(GGT) + 0.053×腰围 - 15.745)) × 100\n"
                f"= (e^(0.953×ln({trig_mgdl}) + 0.139×{bmi} + 0.718×ln({ggt}) + 0.053×{waist} - 15.745)) / (1 + e^(0.953×ln({trig_mgdl}) + 0.139×{bmi} + 0.718×ln({ggt}) + 0.053×{waist} - 15.745)) × 100"
            )
            
        except Exception as e:
            QMessageBox.critical(self, "计算错误", f"FLI计算出错: {e}")

    def calculate_galad(self):
        age, afp, pivka = self.validate_inputs()
        if age is None:
            return
            
        afp_l3 = self.afp_l3_entry.text()
        if not afp_l3:
            QMessageBox.warning(self, "参数缺失", "GALAD评分需要AFP-L3%数据")
            return
            
        try:
            afp_l3 = float(afp_l3)
            if afp_l3 < 0 or afp_l3 > 100:
                raise ValueError("AFP-L3%必须在0-100%范围内")
                
            # 统一性别编码：0=男性，1=女性（与ASAP模型保持一致）
            gender = 0 if self.male_radio.isChecked() else 1
            
            lg_afp = np.log10(afp)
            lg_pivka = np.log10(pivka)
            galad_score = -10.08 + 0.09 * age + (-1.67) * gender + 2.34 * lg_afp + 0.04 * afp_l3 + 1.33 * lg_pivka
            
            if galad_score < -0.63:
                category = "低风险"
                recommendation = "建议常规随访"
            elif galad_score < 0.88:
                category = "中风险"
                recommendation = "建议增加随访频率并进行肝脏影像检查"
            else:
                category = "高风险"
                recommendation = "建议立即进行肝脏影像检查排除肝癌"
            
            self.show_result(
                "GALAD模型计算结果",
                f"GALAD评分: {galad_score:.2f}\n"
                f"风险等级: {category}\n"
                f"建议: {recommendation}"
            )
            
        except ValueError as e:
            QMessageBox.critical(self, "输入错误", str(e))
        except Exception as e:
            QMessageBox.critical(self, "计算错误", f"GALAD计算出错: {e}")

    def validate_nfs_inputs(self):
        try:
            # 验证年龄
            age_text = self.nfs_age_entry.text().strip()
            if not age_text:
                raise ValueError("请输入年龄")
            age = float(age_text)
            if age <= 0:
                raise ValueError("年龄必须大于0")

            # 验证身高体重
            height_text = self.nfs_height_entry.text().strip()
            if not height_text:
                raise ValueError("请输入身高")
            height = float(height_text)
            if height <= 0:
                raise ValueError("身高必须大于0")

            weight_text = self.nfs_weight_entry.text().strip()
            if not weight_text:
                raise ValueError("请输入体重")
            weight = float(weight_text)
            if weight <= 0:
                raise ValueError("体重必须大于0")

            # 计算BMI
            bmi = weight / ((height / 100) ** 2)

            # 验证AST
            ast_text = self.nfs_ast_entry.text().strip()
            if not ast_text:
                raise ValueError("请输入AST值")
            ast = float(ast_text)
            if ast <= 0:
                raise ValueError("AST值必须大于0")

            # 验证ALT
            alt_text = self.nfs_alt_entry.text().strip()
            if not alt_text:
                raise ValueError("请输入ALT值")
            alt = float(alt_text)
            if alt <= 0:
                raise ValueError("ALT值必须大于0")

            # 计算AST/ALT比值
            ast_alt_ratio = ast / alt

            # 验证血小板
            platelet_text = self.platelet_entry.text().strip()
            if not platelet_text:
                raise ValueError("请输入血小板值")
            platelet = float(platelet_text)
            if platelet <= 0:
                raise ValueError("血小板值必须大于0")

            # 验证血清白蛋白
            albumin_text = self.albumin_entry.text().strip()
            if not albumin_text:
                raise ValueError("请输入血清白蛋白值")
            albumin = float(albumin_text)
            if albumin <= 0:
                raise ValueError("血清白蛋白值必须大于0")

            # 获取糖尿病状态
            diabetes = 1 if self.diabetes_yes.isChecked() else 0

            return age, bmi, diabetes, ast_alt_ratio, platelet, albumin
        except ValueError as e:
            QMessageBox.critical(self, "输入错误", str(e))
            return None, None, None, None, None, None

    def calculate_nfs(self):
        age, bmi, diabetes, ast_alt_ratio, platelet, albumin = self.validate_nfs_inputs()
        if age is None:
            return
            
        try:
            # 年龄检查
            if age <= 35:
                self.show_result(
                    "NAFLD纤维化评分(NFS)",
                    "年龄不符合模型要求，建议换用其他方法"
                )
                return
                
            # 计算NFS
            nfs_score = -1.675 + (0.037 * age) + (0.094 * bmi) + (1.13 * diabetes) + \
                       (0.99 * ast_alt_ratio) - (0.013 * platelet) - (0.66 * (albumin/10))
            
            # 解释结果 (不同年龄范围使用不同阈值)
            if age >= 65:
                # 65岁及以上使用新阈值
                if nfs_score < 0.12:
                    interpretation = "F0-F2 (无或轻度/中度纤维化)"
                    color = "#2ecc71"  # 绿色
                elif nfs_score <= 0.676:
                    interpretation = "不确定"
                    color = "#f1c40f"  # 橙色
                else:
                    interpretation = "F3-F4 (严重纤维化/肝硬化)"
                    color = "#e74c3c"  # 红色
                    
                self.show_result(
                    "NAFLD纤维化评分(NFS)",
                    f"NFS评分: {nfs_score:.2f}\n"
                    f"纤维化程度: {interpretation}\n\n"
                    f"计算公式:\n"
                    f"NFS = -1.675 + 0.037×年龄 + 0.094×BMI + 1.13×糖尿病 + 0.99×AST/ALT - 0.013×血小板 - 0.66×白蛋白/10\n"
                    f"= -1.675 + 0.037×{age} + 0.094×{bmi} + 1.13×{diabetes} + 0.99×{ast_alt_ratio} - 0.013×{platelet} - 0.66×{albumin/10}"
                )
            else:
                # 36-65岁使用原阈值
                if nfs_score < -1.455:
                    interpretation = "F0-F2 (无或轻度/中度纤维化)"
                    color = "#2ecc71"  # 绿色
                elif nfs_score <= 0.675:
                    interpretation = "不确定"
                    color = "#f1c40f"  # 橙色
                else:
                    interpretation = "F3-F4 (严重纤维化/肝硬化)"
                    color = "#e74c3c"  # 红色
                    
                self.show_result(
                    "NAFLD纤维化评分(NFS)",
                    f"NFS评分: {nfs_score:.2f}\n"
                    f"纤维化程度: {interpretation}\n\n"
                    f"计算公式:\n"
                    f"NFS = -1.675 + 0.037×年龄 + 0.094×BMI + 1.13×糖尿病 + 0.99×AST/ALT - 0.013×血小板 - 0.66×白蛋白/10\n"
                    f"= -1.675 + 0.037×{age} + 0.094×{bmi} + 1.13×{diabetes} + 0.99×{ast_alt_ratio} - 0.013×{platelet} - 0.66×{albumin/10}"
                )
            
        except Exception as e:
            QMessageBox.critical(self, "计算错误", f"NFS计算出错: {e}")

    def validate_fib4_inputs(self):
        try:
            # 验证年龄
            age_text = self.fib4_age_entry.text().strip()
            if not age_text:
                raise ValueError("请输入年龄")
            age = float(age_text)
            if age <= 0:
                raise ValueError("年龄必须大于0")

            # 验证AST
            ast_text = self.fib4_ast_entry.text().strip()
            if not ast_text:
                raise ValueError("请输入AST值")
            ast = float(ast_text)
            if ast <= 0:
                raise ValueError("AST值必须大于0")

            # 验证ALT
            alt_text = self.fib4_alt_entry.text().strip()
            if not alt_text:
                raise ValueError("请输入ALT值")
            alt = float(alt_text)
            if alt <= 0:
                raise ValueError("ALT值必须大于0")

            # 验证血小板
            platelet_text = self.fib4_platelet_entry.text().strip()
            if not platelet_text:
                raise ValueError("请输入血小板值")
            platelet = float(platelet_text)
            if platelet <= 0:
                raise ValueError("血小板值必须大于0")

            return age, ast, alt, platelet
        except ValueError as e:
            QMessageBox.critical(self, "输入错误", str(e))
            return None, None, None, None

    def calculate_fib4(self):
        age, ast, alt, platelet = self.validate_fib4_inputs()
        if age is None:
            return
            
        try:
            # 年龄检查
            if age <= 35:
                self.show_result(
                    "FIB-4评分",
                    "年龄不符合模型要求，建议换用其他方法"
                )
                return
                
            # 计算FIB-4
            fib4_score = (age * ast) / (platelet * math.sqrt(alt))
            
            # 解释结果 (不同年龄范围使用不同阈值)
            if age >= 65:
                # 65岁及以上使用新阈值
                if fib4_score < 2.0:
                    interpretation = "F0-F2 (无或轻度/中度纤维化)"
                    color = "#2ecc71"  # 绿色
                elif fib4_score <= 2.67:
                    interpretation = "不确定"
                    color = "#f1c40f"  # 橙色
                else:
                    interpretation = "F3-F4 (严重纤维化/肝硬化)"
                    color = "#e74c3c"  # 红色
                    
                self.show_result(
                    "FIB-4评分",
                    f"FIB-4评分: {fib4_score:.2f}\n"
                    f"纤维化程度: {interpretation}\n\n"
                    f"计算公式:\n"
                    f"FIB-4 = (年龄 × AST) / (血小板 × √ALT)\n"
                    f"= ({age} × {ast}) / ({platelet} × √{alt})"
                )
            else:
                # 36-65岁使用原阈值
                if fib4_score < 1.3:
                    interpretation = "F0-F2 (无或轻度/中度纤维化)"
                    color = "#2ecc71"  # 绿色
                elif fib4_score <= 2.67:
                    interpretation = "不确定"
                    color = "#f1c40f"  # 橙色
                else:
                    interpretation = "F3-F4 (严重纤维化/肝硬化)"
                    color = "#e74c3c"  # 红色
                    
                self.show_result(
                    "FIB-4评分",
                    f"FIB-4评分: {fib4_score:.2f}\n"
                    f"纤维化程度: {interpretation}\n\n"
                    f"计算公式:\n"
                    f"FIB-4 = (年龄 × AST) / (血小板 × √ALT)\n"
                    f"= ({age} × {ast}) / ({platelet} × √{alt})"
                )
            
        except Exception as e:
            QMessageBox.critical(self, "计算错误", f"FIB-4计算出错: {e}")

    def show_result(self, title, content):
        # 根据风险等级添加颜色标记
        if "低风险" in content:
            color = "#2ecc71"  # 绿色
        elif "中风险" in content:
            color = "#f1c40f"  # 橙色
        elif "高风险" in content:
            color = "#e74c3c"  # 红色
        else:
            color = "#34495e"  # 深灰色
            
        html_content = f"""
        <div style="font-family: Arial; line-height: 1.6;">
            <h3 style="color: {color}; border-bottom: 2px solid {color}; padding-bottom: 5px;">
                {title}
            </h3>
            <pre style="font-size: 14px; color: #34495e;">{content}</pre>
        </div>
        """
        
        # 根据计算类型显示到对应的结果区域
        if "ASAP" in title or "GALAD" in title:
            self.asap_result.setHtml(html_content)
        elif "FLI" in title:
            self.fli_result.setHtml(html_content)
        elif "NFS" in title:
            self.nfs_result.setHtml(html_content)
        elif "FIB-4" in title:
            self.fib4_result.setHtml(html_content)
        else:
            self.ani_result.setHtml(html_content)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ASAPCalculatorApp()
    window.show()
    sys.exit(app.exec())
