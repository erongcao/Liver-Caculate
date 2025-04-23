// Tab切换功能
document.addEventListener('DOMContentLoaded', function() {
    const tabs = document.querySelectorAll('.tab');
    const panels = document.querySelectorAll('.panel');
    
    tabs.forEach(tab => {
        tab.addEventListener('click', function() {
            // 移除所有active类
            tabs.forEach(t => t.classList.remove('active'));
            panels.forEach(p => p.classList.remove('active'));
            
            // 添加active类到当前tab和对应panel
            this.classList.add('active');
            const panelId = this.getAttribute('data-tab') + '-panel';
            document.getElementById(panelId).classList.add('active');
        });
    });

    // FLI计算功能
    document.getElementById('calculate-fli').addEventListener('click', calculateFLI);
    
    // NFS计算功能
    document.getElementById('calculate-nfs').addEventListener('click', calculateNFS);
    
    // ANI计算功能
    document.getElementById('calculate-ani').addEventListener('click', calculateANI);
    
    // ASAP计算功能
    document.getElementById('calculate-asap').addEventListener('click', calculateASAP);
    
    // GALAD计算功能
    document.getElementById('calculate-galad').addEventListener('click', calculateGALAD);
    
    // FIB-4计算功能
    document.getElementById('calculate-fib4').addEventListener('click', calculateFIB4);
});

function calculateFIB4() {
    const age = parseFloat(document.getElementById('fib4-age').value);
    const ast = parseFloat(document.getElementById('fib4-ast').value);
    const alt = parseFloat(document.getElementById('fib4-alt').value);
    const platelet = parseFloat(document.getElementById('fib4-platelet').value);

    if (!age || !ast || !alt || !platelet) {
        alert('请填写所有必填字段');
        return;
    }

    // 年龄检查
    if (age <= 35) {
        const resultDiv = document.getElementById('fib4-result');
        resultDiv.innerHTML = `
            <h3 style="color: #f1c40f; border-bottom: 2px solid #f1c40f; padding-bottom: 5px;">
                FIB-4计算结果
            </h3>
            <p>年龄不符合模型要求，建议换用其他方法</p>
        `;
        return;
    }

    // 计算FIB-4
    const fib4_score = (age * ast) / (platelet * Math.sqrt(alt));
    
    // 解释结果 (不同年龄范围使用不同阈值)
    let interpretation, color;
    if (age >= 65) {
        // 65岁及以上使用新阈值
        if (fib4_score < 2.0) {
            interpretation = "F0-F2 (无或轻度/中度纤维化)";
            color = "#2ecc71";
        } else if (fib4_score <= 2.67) {
            interpretation = "不确定";
            color = "#f1c40f";
        } else {
            interpretation = "F3-F4 (严重纤维化/肝硬化)";
            color = "#e74c3c";
        }
    } else {
        // 36-65岁使用原阈值
        if (fib4_score < 1.3) {
            interpretation = "F0-F2 (无或轻度/中度纤维化)";
            color = "#2ecc71";
        } else if (fib4_score <= 2.67) {
            interpretation = "不确定";
            color = "#f1c40f";
        } else {
            interpretation = "F3-F4 (严重纤维化/肝硬化)";
            color = "#e74c3c";
        }
    }
    
    const resultDiv = document.getElementById('fib4-result');
    resultDiv.innerHTML = `
        <h3 style="color: ${color}; border-bottom: 2px solid ${color}; padding-bottom: 5px;">
            FIB-4计算结果
        </h3>
        <p>FIB-4评分: <strong>${fib4_score.toFixed(2)}</strong></p>
        <p>纤维化程度: <strong>${interpretation}</strong></p>
        <p>计算公式:</p>
        <p>FIB-4 = (年龄 × AST) / (血小板 × √ALT)</p>
        <p>= (${age} × ${ast}) / (${platelet} × √${alt})</p>
    `;
}

function calculateFLI() {
    const height = parseFloat(document.getElementById('fli-height').value);
    const weight = parseFloat(document.getElementById('fli-weight').value);
    const trig = parseFloat(document.getElementById('fli-trig').value);
    const ggt = parseFloat(document.getElementById('fli-ggt').value);
    const waist = parseFloat(document.getElementById('fli-waist').value);

    if (!height || !weight || !trig || !ggt || !waist) {
        alert('请填写所有必填字段');
        return;
    }

    // 计算BMI
    const bmi = weight / Math.pow(height / 100, 2);
    // 转换为mg/dL
    const trig_mgdl = trig * 88.57;
    
    // 计算FLI
    const log_trig = Math.log(trig_mgdl);
    const log_ggt = Math.log(ggt);
    const numerator = Math.exp(0.953 * log_trig + 0.139 * bmi + 0.718 * log_ggt + 0.053 * waist - 15.745);
    const fli_score = (numerator / (1 + numerator)) * 100;
    
    // 解释结果
    let interpretation, color;
    if (fli_score < 30) {
        interpretation = "脂肪肝可能性低(阴性预测值15%)";
        color = "#2ecc71";
    } else if (fli_score < 60) {
        interpretation = "结果不确定";
        color = "#f1c40f";
    } else {
        interpretation = "脂肪肝可能性高(阳性预测值99%)";
        color = "#e74c3c";
    }
    
    const resultDiv = document.getElementById('fli-result');
    resultDiv.innerHTML = `
        <h3 style="color: ${color}; border-bottom: 2px solid ${color}; padding-bottom: 5px;">
            FLI计算结果
        </h3>
        <p>FLI评分: <strong>${fli_score.toFixed(1)}</strong></p>
        <p>解释: <strong>${interpretation}</strong></p>
        <p>FLI评分解释:</p>
        <ul>
            <li><30: 排除脂肪肝(阴性预测值15%)</li>
            <li>30-60: 结果不确定</li>
            <li>>=60: 存在脂肪肝(阳性预测值99%)</li>
        </ul>
    `;
}

function calculateNFS() {
    const age = parseFloat(document.getElementById('nfs-age').value);
    const height = parseFloat(document.getElementById('nfs-height').value);
    const weight = parseFloat(document.getElementById('nfs-weight').value);
    const ast = parseFloat(document.getElementById('nfs-ast').value);
    const alt = parseFloat(document.getElementById('nfs-alt').value);
    const platelet = parseFloat(document.getElementById('nfs-platelet').value);
    const albumin = parseFloat(document.getElementById('nfs-albumin').value);
    const diabetes = document.getElementById('diabetes-yes').checked ? 1 : 0;

    if (!age || !height || !weight || !ast || !alt || !platelet || !albumin) {
        alert('请填写所有必填字段');
        return;
    }

    // 计算BMI
    const bmi = weight / Math.pow(height / 100, 2);
    // 计算AST/ALT比值
    const ast_alt_ratio = ast / alt;
    
    // 年龄检查
    if (age <= 35) {
        const resultDiv = document.getElementById('nfs-result');
        resultDiv.innerHTML = `
            <h3 style="color: #f1c40f; border-bottom: 2px solid #f1c40f; padding-bottom: 5px;">
                NFS计算结果
            </h3>
            <p>年龄不符合模型要求，建议换用其他方法</p>
        `;
        return;
    }

    // 计算NFS
    const nfs_score = -1.675 + (0.037 * age) + (0.094 * bmi) + (1.13 * diabetes) +
                     (0.99 * ast_alt_ratio) - (0.013 * platelet) - (0.66 * (albumin/10));
    
    // 解释结果 (不同年龄范围使用不同阈值)
    let interpretation, color;
    if (age >= 65) {
        // 65岁及以上使用新阈值
        if (nfs_score < 0.12) {
            interpretation = "F0-F2 (无或轻度/中度纤维化)";
            color = "#2ecc71";
        } else if (nfs_score <= 0.676) {
            interpretation = "不确定";
            color = "#f1c40f";
        } else {
            interpretation = "F3-F4 (严重纤维化/肝硬化)";
            color = "#e74c3c";
        }
    } else {
        // 36-65岁使用原阈值
        if (nfs_score < -1.455) {
            interpretation = "F0-F2 (无或轻度/中度纤维化)";
            color = "#2ecc71";
        } else if (nfs_score <= 0.675) {
            interpretation = "不确定";
            color = "#f1c40f";
        } else {
            interpretation = "F3-F4 (严重纤维化/肝硬化)";
            color = "#e74c3c";
        }
    }
    
    const resultDiv = document.getElementById('nfs-result');
    resultDiv.innerHTML = `
        <h3 style="color: ${color}; border-bottom: 2px solid ${color}; padding-bottom: 5px;">
            NFS计算结果
        </h3>
        <p>NFS评分: <strong>${nfs_score.toFixed(2)}</strong></p>
        <p>纤维化程度: <strong>${interpretation}</strong></p>
        <p>计算公式:</p>
        <p>NFS = -1.675 + 0.037×年龄 + 0.094×BMI + 1.13×糖尿病 + 0.99×AST/ALT - 0.013×血小板 - 0.66×白蛋白/10</p>
        <p>= -1.675 + 0.037×${age} + 0.094×${bmi} + 1.13×${diabetes} + 0.99×${ast_alt_ratio} - 0.013×${platelet} - 0.66×${albumin/10}</p>
    `;
}

function calculateANI() {
    const height = parseFloat(document.getElementById('ani-height').value);
    const weight = parseFloat(document.getElementById('ani-weight').value);
    const mcv = parseFloat(document.getElementById('ani-mcv').value);
    const ast = parseFloat(document.getElementById('ani-ast').value);
    const alt = parseFloat(document.getElementById('ani-alt').value);
    const gender = document.getElementById('gender-male').checked ? 'male' : 'female';

    if (!height || !weight || !mcv || !ast || !alt) {
        alert('请填写所有必填字段');
        return;
    }

    // 计算BMI
    const bmi = weight / Math.pow(height / 100, 2);
    // 应用修正
    const mcv_corrected = mcv < 92 ? 92 : (mcv > 103 ? 103 : mcv);
    const ast_alt_ratio = ast / alt;
    const ast_alt_corrected = ast_alt_ratio > 3 ? 3 : ast_alt_ratio;
    const gender_coeff = gender === 'male' ? 6.35 : 0;
    
    // 计算ANI评分
    const ani_score = -58.5 + 0.637 * mcv_corrected + 3.91 * ast_alt_corrected - 0.406 * bmi + gender_coeff;
    
    // 计算概率
    const probability = Math.exp(ani_score) / (1 + Math.exp(ani_score));
    
    // 确定诊断
    let diagnosis, color;
    if (ani_score > 0) {
        diagnosis = "酒精性脂肪肝(ALD)可能性高";
        color = "#e74c3c";
    } else if (ani_score < -0.22) {
        diagnosis = "非酒精性脂肪肝(NAFLD)可能性高";
        color = "#2ecc71";
    } else {
        diagnosis = "无法明确分辨，可能兼而有之";
        color = "#f1c40f";
    }
    
    const resultDiv = document.getElementById('ani-result');
    resultDiv.innerHTML = `
        <h3 style="color: ${color}; border-bottom: 2px solid ${color}; padding-bottom: 5px;">
            ANI计算结果
        </h3>
        <p>ANI评分: <strong>${ani_score.toFixed(2)}</strong></p>
        <p>诊断概率: <strong>${(probability * 100).toFixed(1)}%</strong></p>
        <p>诊断: <strong>${diagnosis}</strong></p>
    `;
}

function calculateASAP() {
    const age = parseFloat(document.getElementById('asap-age').value);
    const afp = parseFloat(document.getElementById('asap-afp').value);
    const pivka = parseFloat(document.getElementById('asap-pivka').value);
    const gender = document.getElementById('asap-gender-male').checked ? 0 : 1;

    if (!age || !afp || !pivka) {
        alert('请填写所有必填字段');
        return;
    }

    const ln_afp = Math.log(afp);
    const ln_pivka = Math.log(pivka);
    const asap_score = -7.57711770 + 0.04666357 * age - 0.57611693 * gender + 0.42243533 * ln_afp + 1.10518910 * ln_pivka;
    const risk_probability = 1 / (1 + Math.exp(-asap_score));

    let category, color, recommendation;
    if (risk_probability <= 0.333) {
        category = "低风险";
        color = "#2ecc71";
        recommendation = "建议每6个月进行AFP+PIVKA-II和超声检查";
    } else if (risk_probability <= 0.666) {
        category = "中风险";
        color = "#f1c40f";
        recommendation = "建议进行肝脏超声检查，有条件时进行增强CT或MRI";
    } else {
        category = "高风险";
        color = "#e74c3c";
        recommendation = "建议立即进行肝脏动态CT或增强MRI检查";
    }

    const resultDiv = document.getElementById('asap-result');
    resultDiv.innerHTML = `
        <h3 style="color: ${color}; border-bottom: 2px solid ${color}; padding-bottom: 5px;">
            ASAP计算结果
        </h3>
        <p>ASAP评分: <strong>${asap_score.toFixed(2)}</strong></p>
        <p>肝癌风险概率: <strong>${(risk_probability * 100).toFixed(2)}%</strong></p>
        <p>风险等级: <strong>${category}</strong></p>
        <p>建议: <strong>${recommendation}</strong></p>
    `;
}

function calculateGALAD() {
    const age = parseFloat(document.getElementById('asap-age').value);
    const afp = parseFloat(document.getElementById('asap-afp').value);
    const pivka = parseFloat(document.getElementById('asap-pivka').value);
    const afpl3 = parseFloat(document.getElementById('asap-afpl3').value);
    const gender = document.getElementById('asap-gender-male').checked ? 0 : 1;

    if (!age || !afp || !pivka || !afpl3) {
        alert('请填写所有必填字段');
        return;
    }

    const lg_afp = Math.log10(afp);
    const lg_pivka = Math.log10(pivka);
    const galad_score = -10.08 + 0.09 * age + (-1.67) * gender + 2.34 * lg_afp + 0.04 * afpl3 + 1.33 * lg_pivka;

    let category, color, recommendation;
    if (galad_score < -0.63) {
        category = "低风险";
        color = "#2ecc71";
        recommendation = "建议常规随访";
    } else if (galad_score < 0.88) {
        category = "中风险";
        color = "#f1c40f";
        recommendation = "建议增加随访频率并进行肝脏影像检查";
    } else {
        category = "高风险";
        color = "#e74c3c";
        recommendation = "建议立即进行肝脏影像检查排除肝癌";
    }

    const resultDiv = document.getElementById('asap-result');
    resultDiv.innerHTML = `
        <h3 style="color: ${color}; border-bottom: 2px solid ${color}; padding-bottom: 5px;">
            GALAD计算结果
        </h3>
        <p>GALAD评分: <strong>${galad_score.toFixed(2)}</strong></p>
        <p>风险等级: <strong>${category}</strong></p>
        <p>建议: <strong>${recommendation}</strong></p>
    `;
}
