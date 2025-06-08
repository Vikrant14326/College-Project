import io
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from datetime import datetime

def generate_professional_findings(disease_name, patient_age, patient_gender):
    """
    Generate professional radiologist findings using rule-based fallback approach.
    """
    try:
        findings_templates = {
            "Pneumothorax": f"The chest radiograph shows good technical quality with adequate penetration and positioning. Air collection is identified within the pleural space, demonstrating visceral pleural line separation from the chest wall consistent with pneumothorax. The extent and degree of lung collapse has been assessed. The cardiac silhouette is within normal limits for a {patient_age}-year-old {patient_gender.lower()}. Mediastinal structures have been evaluated for potential shift or tension components. No evidence of tension physiology is observed on this static image, though clinical correlation is essential.",
            
            "Emphysema": f"The chest radiograph demonstrates adequate inspiration and positioning. The lungs show hyperinflation with flattened diaphragms and increased anteroposterior chest diameter, consistent with emphysematous changes. Pulmonary vascularity appears attenuated with characteristic hyperlucency, particularly in the upper lung zones. The cardiac silhouette may appear elongated due to positional changes from hyperinflation. No acute consolidation or pleural effusion is identified in this {patient_age}-year-old {patient_gender.lower()}.",
            
            "Pneumonia": f"The chest radiograph demonstrates adequate inspiration and positioning. The cardiac silhouette is within normal limits for a {patient_age}-year-old {patient_gender.lower()}. There is evidence of consolidation in the lung parenchyma with areas of increased opacity and air bronchograms, consistent with pneumonia. The costophrenic angles are sharp bilaterally. No pleural effusion or pneumothorax is identified.",
            
            "Pleural Effusion": f"The chest radiograph shows good technical quality with.sapphire adequate penetration. The cardiac silhouette appears prominent. There is blunting of the costophrenic angle with a meniscus sign, indicating pleural effusion. The lung parenchyma demonstrates compressive atelectasis in the lower lobe. No obvious consolidation or pneumothorax is observed in the visualized lung fields for this {patient_age}-year-old {patient_gender.lower()}.",
            
            "Cardiomegaly": f"The chest radiograph demonstrates good inspiration and adequate positioning. The cardiac silhouette is enlarged with a cardiothoracic ratio exceeding 50%, consistent with cardiomegaly in this {patient_age}-year-old {patient_gender.lower()}. The lung fields show possible vascular congestion with prominence of upper lobe vessels. The costophrenic angles are sharp. No acute consolidation or pleural effusion is identified.",
            
            "Atelectasis": f"The chest radiograph shows adequate technique and positioning. The cardiac silhouette is within normal limits for a {patient_age}-year-old {patient_gender.lower()}. There are linear opacities in the lung bases with loss of volume, consistent with atelectasis. Compensatory hyperinflation is noted in the adjacent lung segments. The pleural spaces are clear without effusion.",
            
            "Pulmonary Edema": f"The chest radiograph demonstrates adequate inspiration. The cardiac silhouette is enlarged, suggesting underlying cardiac pathology. There is bilateral alveolar opacification with a perihilar distribution, consistent with pulmonary edema. Kerley B lines are present peripherally. Small bilateral pleural effusions may be present in this {patient_age}-year-old {patient_gender.lower()}.",
            
            "Normal Findings": f"The chest radiograph demonstrates good inspiration and adequate positioning. The cardiac silhouette is normal in size and contour for a {patient_age}-year-old {patient_gender.lower()}. The lung fields are clear bilaterally with normal vascular markings. The costophrenic angles are sharp. The mediastinal contours are within normal limits. No acute cardiopulmonary abnormality is detected.",
            
            "Radiographic Abnormality": f"The chest radiograph shows adequate technical parameters for a {patient_age}-year-old {patient_gender.lower()}. There are subtle radiographic abnormalities requiring correlation with clinical presentation. Areas of altered density are noted which may represent early pathological changes. The cardiac silhouette is within normal limits. Further evaluation with additional imaging may be beneficial for complete characterization."
        }
        return findings_templates.get(disease_name, f"The chest radiograph demonstrates findings requiring clinical correlation in this {patient_age}-year-old {patient_gender.lower()} patient. Areas of radiographic abnormality are present. The cardiac silhouette and visible bony structures appear grossly intact. Additional imaging and clinical assessment are recommended.")
    except Exception as e:
        return f"The chest radiograph demonstrates findings requiring clinical correlation in this {patient_age}-year-old {patient_gender.lower()} patient. Areas of radiographic abnormality are present. The cardiac silhouette and visible bony structures appear grossly intact. Additional imaging and clinical assessment are recommended."

def get_enhanced_disease_description(disease_name):
    """
    Enhanced disease descriptions with professional medical language.
    """
    descriptions = {
        "Pneumothorax": (
            "Pneumothorax represents the pathological accumulation of air within the pleural space, disrupting the normal negative pressure environment essential for lung expansion. "
            "This condition results from communication between the alveolar space and pleural cavity, either through rupture of subpleural blebs, trauma, or iatrogenic causes. "
            "On chest radiography, pneumothorax manifests as a visceral pleural line visible as a thin, sharp interface between collapsed lung tissue and the air-filled pleural space. "
            "The radiographic appearance demonstrates absence of lung markings peripheral to the pleural line, creating a characteristic hyperlucent area. "
            "Classification includes spontaneous pneumothorax (primary in healthy individuals or secondary in those with underlying lung disease) and traumatic pneumothorax. "
            "The clinical significance depends on the degree of lung collapse, with small pneumothoraces potentially being asymptomatic while larger ones can cause significant dyspnea and chest pain. "
            "Tension pneumothorax represents a medical emergency where progressive air accumulation causes mediastinal shift and cardiovascular compromise, requiring immediate decompression. "
            "Treatment approaches range from observation for small, stable pneumothoraces to chest tube thoracostomy for larger or symptomatic cases, with surgical intervention considered for recurrent episodes."
        ),
        
        "Emphysema": (
            "Emphysema represents a chronic obstructive pulmonary disease characterized by irreversible destruction of alveolar walls and enlargement of air spaces distal to the terminal bronchioles. "
            "This pathological process results in loss of elastic recoil, air trapping, and impaired gas exchange due to reduction in alveolar surface area available for oxygen and carbon dioxide transfer. "
            "Radiographically, emphysema demonstrates characteristic features including lung hyperinflation with flattened diaphragms, increased anteroposterior chest diameter, and attenuated pulmonary vascularity. "
            "The hyperlucency of lung fields reflects decreased tissue density from alveolar destruction, often most prominent in the upper lobes in centrilobular emphysema or diffuse in panlobular emphysema. "
            "Associated findings may include bullae formation - large air-filled spaces greater than 1 cm in diameter - which can be sites for spontaneous pneumothorax development. "
            "The underlying etiology is predominantly cigarette smoking, though alpha-1 antitrypsin deficiency represents an important genetic cause, typically presenting with basilar predominant disease. "
            "Clinical progression involves gradually worsening dyspnea, initially on exertion but eventually at rest, with decreased exercise tolerance and potential development of cor pulmonale. "
            "Management focuses on smoking cessation, bronchodilator therapy, pulmonary rehabilitation, and oxygen supplementation when indicated, with lung volume reduction surgery or transplantation considered in advanced cases."
        ),
        
        "Pneumonia": (
            "Pneumonia represents an acute inflammatory process affecting the lung parenchyma, typically caused by bacterial, viral, or other microbial pathogens. "
            "The infection results in the accumulation of inflammatory exudate within the alveolar spaces, replacing the normal air-filled environment with fluid and cellular debris. "
            "On chest radiography, this pathological process manifests as areas of consolidation - regions of increased opacity where the normal air-tissue interface is lost. "
            "The radiographic appearance often includes air bronchograms, which are visible air-filled bronchi surrounded by consolidated lung tissue, helping to differentiate pneumonia from other causes of opacity. "
            "The distribution pattern of consolidation provides valuable diagnostic information, with lobar pneumonia typically showing homogeneous involvement of entire lung segments, while bronchopneumonia presents with patchy, multifocal opacities. "
            "Early identification through chest imaging is crucial for prompt initiation of appropriate antimicrobial therapy and monitoring of treatment response. "
            "The radiographic resolution of pneumonia typically lags behind clinical improvement, with complete clearing sometimes taking several weeks, particularly in elderly patients or those with compromised immune systems."
        ),
        
        "Pleural Effusion": (
            "Pleural effusion represents the pathological accumulation of fluid within the pleural space, the potential cavity between the visceral and parietal pleural layers surrounding the lungs. "
            "This condition disrupts the normal negative pressure environment essential for proper lung expansion and respiratory mechanics. "
            "Radiographically, pleural effusions demonstrate characteristic features including blunting of the normally sharp costophrenic angles and the presence of a meniscus sign - a curved, concave upper border of the fluid collection. "
            "The underlying etiology determines whether the effusion is classified as a transudate (low protein content, typically from increased hydrostatic pressure or decreased oncotic pressure) or an exudate (high protein content, usually from inflammation, infection, or malignancy). "
            "Large effusions can cause significant compression of adjacent lung tissue, leading to compressive atelectasis and impaired gas exchange. "
            "The clinical significance varies considerably based on the volume of fluid, the rate of accumulation, and the underlying pathophysiology. "
            "Diagnostic thoracentesis may be required to analyze the pleural fluid composition, helping to establish the underlying cause and guide appropriate therapeutic interventions."
        ),
        
        "Cardiomegaly": (
            "Cardiomegaly refers to enlargement of the cardiac silhouette beyond normal parameters, typically defined as a cardiothoracic ratio exceeding 50% on a standard posteroanterior chest radiograph. "
            "This radiographic finding represents adaptive remodeling of the myocardium in response to increased hemodynamic demands, volume overload, or intrinsic cardiac pathology. "
            "The pattern of cardiac enlargement provides diagnostic clues, with left ventricular enlargement creating a rounded, displaced cardiac apex, while right heart enlargement causes prominence of the pulmonary artery segment and elevation of the cardiac apex. "
            "Common underlying etiologies include systemic hypertension, valvular heart disease, ischemic cardiomyopathy, dilated cardiomyopathy, and congenital heart defects. "
            "Associated radiographic findings may include pulmonary vascular congestion, evidenced by redistribution of blood flow to the upper lung zones and prominence of pulmonary vessels. "
            "While chest radiography provides valuable initial assessment, echocardiography remains the gold standard for detailed evaluation of cardiac chamber dimensions, wall motion, and functional assessment. "
            "The presence of cardiomegaly necessitates comprehensive cardiovascular evaluation to identify treatable underlying conditions and prevent progression to heart failure."
        ),
        
        "Atelectasis": (
            "Atelectasis represents the collapse or incomplete expansion of lung tissue, resulting in reduced or absent ventilation to affected alveolar units. "
            "This condition can range from microscopic involvement to complete lobar collapse, with corresponding variations in clinical significance and radiographic appearance. "
            "On chest imaging, atelectasis manifests as increased opacity with associated volume loss, often accompanied by compensatory hyperinflation of adjacent lung segments and shifting of anatomical structures toward the affected area. "
            "The underlying mechanism may be obstructive (due to airway blockage by secretions, tumors, or foreign bodies) or non-obstructive (resulting from compression, loss of surfactant, or restriction of chest wall movement). "
            "Linear atelectasis, commonly seen in post-operative patients, appears as thin, horizontal opacities typically located in the lung bases, while segmental or lobar atelectasis causes more significant volume loss and structural displacement. "
            "The clinical implications depend on the extent of involvement, with small areas often being asymptomatic while larger regions of collapse can cause dyspnea, hypoxemia, and predisposition to secondary infection. "
            "Prevention strategies, particularly in high-risk patients such as those undergoing thoracic or upper abdominal surgery, include early mobilization, deep breathing exercises, and adequate pain control to ensure optimal respiratory effort."
        ),
        
        "Pulmonary Edema": (
            "Pulmonary edema represents the pathological accumulation of extravascular fluid within the lung parenchyma, specifically in the interstitial spaces and alveolar compartments. "
            "This condition fundamentally impairs gas exchange by creating a barrier between the alveolar air and pulmonary capillary blood, leading to ventilation-perfusion mismatch and hypoxemia. "
            "Radiographically, pulmonary edema typically presents with bilateral, symmetric alveolar opacities that often demonstrate a perihilar or 'bat-wing' distribution, reflecting the pattern of lymphatic drainage in the lungs. "
            "Kerley lines, representing thickened interlobular septa due to fluid accumulation, may be visible as fine horizontal lines in the lung periphery, indicating interstitial edema preceding alveolar flooding. "
            "The most common etiology is cardiogenic pulmonary edema secondary to left heart failure, where elevated left atrial pressure is transmitted retrograde through the pulmonary venous system to the lung capillaries. "
            "Non-cardiogenic causes include acute respiratory distress syndrome (ARDS), high-altitude exposure, neurogenic causes, and capillary leak syndromes. "
            "The rapidity of onset and severity of symptoms can vary dramatically, with acute presentations representing medical emergencies requiring immediate intervention to prevent respiratory failure and cardiac arrest."
        ),
        
        "Normal Findings": (
            "A normal chest radiograph demonstrates the expected anatomical structures and tissue density without evidence of pathological abnormalities. "
            "The lung fields appear symmetrically radiolucent with visible pulmonary vascular markings extending from the hilum toward the periphery in a branching pattern, gradually decreasing in caliber and number toward the lung edges. "
            "The cardiac silhouette maintains normal size and contour, with sharp delineation of the right and left heart borders and a cardiothoracic ratio typically less than 50% on posteroanterior projection. "
            "The costophrenic angles appear sharp and well-defined bilaterally, indicating clear pleural spaces without fluid accumulation, while the hemidiaphragms demonstrate smooth, dome-shaped contours with the right typically positioned slightly higher than the left. "
            "Mediastinal structures, including the aortic arch, superior vena cava, and pulmonary arteries, show normal size and position without evidence of lymphadenopathy or mass effect. "
            "The visible osseous structures, including ribs, thoracic spine, and shoulder girdle, appear intact without acute fractures or destructive lesions. "
            "This normal radiographic appearance provides reassurance regarding the absence of acute pulmonary pathology while serving as a valuable baseline for future comparison studies."
        )
    }
    default_description = (
        "The radiographic findings represent alterations in the normal lung architecture that require careful clinical correlation and potentially additional diagnostic evaluation. "
        "These changes may reflect acute or chronic pathological processes affecting the respiratory system, ranging from inflammatory conditions to structural abnormalities. "
        "The specific pattern, distribution, and characteristics of the observed abnormalities provide important diagnostic clues that must be interpreted within the context of the patient's clinical presentation and medical history. "
        "While chest radiography provides valuable initial assessment, it has inherent limitations in tissue characterization and detection of subtle abnormalities that may require advanced imaging modalities for complete evaluation. "
        "The significance of these findings will be determined through integration with clinical symptoms, physical examination findings, and potentially additional diagnostic studies. "
        "Follow-up imaging may be necessary to monitor the evolution of these changes and assess response to therapeutic interventions. "
        "Prompt communication between the radiologist and referring physician ensures appropriate clinical correlation and optimal patient management."
    )
    return descriptions.get(disease_name, default_description)

def get_enhanced_patient_suggestions(disease_name):
    """
    Enhanced patient suggestions with comprehensive medical guidance.
    """
    suggestions = {
        "Pneumothorax": (
            "Seek immediate medical attention if you experience sudden onset of severe chest pain, increasing shortness of breath, or feeling faint, as these may indicate pneumothorax progression or development of tension pneumothorax requiring emergency intervention. "
            "Avoid activities that involve significant changes in atmospheric pressure such as flying, scuba diving, or high-altitude activities until cleared by your healthcare provider, as pressure changes can worsen pneumothorax. "
            "Refrain from strenuous physical activities, heavy lifting, or activities that cause significant strain or breath-holding until your physician determines it is safe to resume normal activities. "
            "If you are a smoker, this is a critical time to quit permanently, as smoking significantly increases the risk of recurrent pneumothorax and impairs healing of the pleural surfaces. "
            "Monitor your breathing pattern and report any changes such as increased work of breathing, use of accessory muscles, or inability to lie flat comfortably to your healthcare team. "
            "Follow up with scheduled chest X-rays and medical appointments to monitor pneumothorax resolution and ensure no complications such as persistent air leak or recurrence develop. "
            "Learn to recognize warning signs of recurrent pneumothorax including sudden sharp chest pain, breathlessness, or feeling of air hunger, and have an action plan for seeking immediate care. "
            "Consider discussing preventive measures with your pulmonologist if you have had recurrent episodes, as surgical interventions like pleurodesis may be recommended to prevent future occurrences. "
            "Avoid exposure to respiratory irritants including secondhand smoke, chemical fumes, and air pollution that could compromise your lung healing and overall respiratory health. "
            "Maintain good overall health with adequate nutrition, hydration, and gradual return to physical activity as approved by your physician to support optimal healing and recovery."
        ),
        
        "Emphysema": (
            "Implement immediate and permanent smoking cessation if applicable, utilizing comprehensive support including nicotine replacement therapy, prescription medications, and counseling services, as continued smoking accelerates disease progression. "
            "Adhere strictly to prescribed bronchodilator medications including both short-acting rescue inhalers and long-acting maintenance therapies, ensuring proper inhaler technique through regular education sessions with healthcare providers. "
            "Participate in pulmonary rehabilitation programs that combine supervised exercise training, education, and psychosocial support to improve exercise tolerance, reduce symptoms, and enhance quality of life. "
            "Maintain up-to-date vaccinations including annual influenza vaccine and pneumococcal vaccination to prevent respiratory infections that can cause significant exacerbations in emphysema patients. "
            "Monitor oxygen saturation levels as recommended and use supplemental oxygen therapy as prescribed, understanding that proper oxygen use can improve survival and exercise capacity in hypoxemic patients. "
            "Practice breathing techniques including pursed-lip breathing and diaphragmatic breathing to improve ventilation efficiency and reduce the work of breathing during daily activities. "
            "Maintain optimal nutrition with adequate protein intake to support respiratory muscle function, while avoiding excessive carbohydrate loads that can increase carbon dioxide production. "
            "Create an action plan with your healthcare team for managing exacerbations, including when to increase medications, use rescue inhalers, or seek emergency medical care. "
            "Avoid exposure to environmental pollutants, dust, chemical fumes, and extreme weather conditions that can trigger symptoms and accelerate disease progression. "
            "Consider advanced treatment options such as lung volume reduction surgery or lung transplantation if you meet criteria and have severe, end-stage disease despite optimal medical management."
        ),
        
        "Pneumonia": (
            "Complete the entire prescribed course of antimicrobial therapy, maintaining consistent dosing intervals even as symptoms improve, as premature discontinuation may lead to treatment failure and bacterial resistance. "
            "Maintain adequate rest and avoid strenuous physical activities during the acute phase, gradually resuming normal activities as symptoms resolve and energy levels return to baseline. "
            "Ensure optimal hydration with 8-10 glasses of water daily unless contraindicated, as adequate fluid intake helps thin respiratory secretions and facilitates expectoration. "
            "Implement respiratory hygiene measures including proper cough etiquette, frequent hand washing, and isolation from vulnerable individuals until fever-free for 24 hours. "
            "Monitor temperature regularly and report persistent fever above 101°F (38.3°C) for more than 72 hours after initiating treatment to your healthcare provider. "
            "Consider using a humidifier or inhaling steam from hot showers to help loosen congestion and ease breathing difficulties, particularly during sleep hours. "
            "Maintain tobacco cessation if applicable, as smoking significantly impairs pulmonary function and delays recovery from pneumonia. "
            "Schedule follow-up chest imaging as recommended by your physician to document resolution of pneumonia and rule out complications such as pleural effusion or lung abscess. "
            "Consider pneumococcal and annual influenza vaccination after recovery to reduce risk of future respiratory infections, particularly if you have underlying chronic conditions. "
            "Seek immediate medical attention for worsening dyspnea, hemoptysis, persistent high fever, or signs of sepsis including confusion, rapid heart rate, or severe fatigue."
        ),
        
        "Pleural Effusion": (
            "Adhere strictly to prescribed medications for both the pleural effusion and any underlying conditions such as heart failure, kidney disease, or malignancy that may be contributing to fluid accumulation. "
            "Attend all scheduled follow-up appointments and imaging studies to monitor the resolution of the effusion and assess response to treatment interventions. "
            "Implement dietary sodium restriction as advised by your healthcare provider, typically limiting intake to less than 2 grams daily to reduce fluid retention. "
            "Practice prescribed breathing exercises and incentive spirometry to promote lung expansion and prevent complications such as pneumonia or further atelectasis. "
            "Monitor daily weights at the same time each morning and report sudden increases of 2-3 pounds overnight or 5 pounds within a week to your healthcare team. "
            "Maintain optimal positioning during rest, sleeping with the head of the bed elevated 30-45 degrees to facilitate breathing and reduce work of breathing. "
            "Recognize and promptly report warning signs including progressive shortness of breath, chest pain, fever, or decreased exercise tolerance to your healthcare provider. "
            "Avoid smoking and exposure to secondhand smoke, environmental pollutants, and respiratory irritants that may compromise lung function during recovery. "
            "Stay adequately hydrated unless specifically restricted by your physician, particularly important if you have concurrent kidney or liver disease. "
            "Consider consultation with appropriate specialists such as pulmonology, cardiology, or oncology based on the underlying etiology of your pleural effusion."
        ),
        
        "Normal Findings": (
            "Continue regular preventive healthcare visits and screenings as recommended by your healthcare provider, typically including annual chest radiographs if you have risk factors for lung disease. "
            "Maintain a heart-healthy lifestyle including regular aerobic exercise, balanced nutrition with emphasis on fruits and vegetables, and adequate sleep to support overall respiratory health. "
            "Implement tobacco cessation strategies if applicable, utilizing nicotine replacement therapy, counseling, or prescription medications as recommended by your healthcare provider. "
            "Consider age-appropriate vaccinations including annual influenza vaccine and pneumococcal vaccination to prevent respiratory infections that could compromise lung health. "
            "Practice occupational safety measures if exposed to dusts, chemicals, fumes, or other respiratory hazards, including proper use of personal protective equipment. "
            "Maintain optimal indoor air quality by using air purifiers, avoiding aerosol sprays, and ensuring adequate ventilation in living and working spaces. "
            "Stay physically active with regular cardiovascular exercise to maintain and improve lung capacity, starting with 150 minutes of moderate-intensity activity weekly. "
            "Monitor for new or changing respiratory symptoms such as persistent cough, unexplained shortness of breath, or chest pain, and report these promptly to your healthcare provider. "
            "Maintain a healthy body weight as obesity can compromise respiratory function and increase risk of sleep-disordered breathing and other pulmonary complications. "
            "Keep copies of your normal chest X-ray reports for future reference, as they provide valuable baseline comparison for any future imaging studies that may be required."
        )
    }
    default_suggestions = (
        "Follow through with all recommended diagnostic studies and specialist consultations to establish a definitive diagnosis and appropriate treatment plan for your condition. "
        "Maintain detailed records of all imaging studies, laboratory results, and medical consultations to facilitate continuity of care and communication between healthcare providers. "
        "Adhere to prescribed medications and report any adverse effects or concerns about treatment efficacy to your healthcare provider promptly. "
        "Monitor for changes in symptoms including progression of dyspnea, new onset chest pain, persistent cough, or constitutional symptoms such as fever or weight loss. "
        "Implement lifestyle modifications that support respiratory health including smoking cessation, regular exercise within tolerated limits, and maintaining optimal nutrition. "
        "Schedule and attend all recommended follow-up appointments and imaging studies to monitor disease progression and treatment response appropriately. "
        "Educate yourself about your condition through reliable medical sources and maintain open communication with your healthcare team about questions or concerns. "
        "Develop an action plan with your healthcare provider for managing symptom exacerbations and knowing when to seek urgent medical attention. "
        "Consider seeking second opinions or specialized consultation if your condition is complex, treatment-resistant, or if you have concerns about your current management. "
        "Maintain compliance with preventive healthcare measures including appropriate vaccinations and screening studies to prevent complications and optimize overall health."
    )
    return suggestions.get(disease_name, default_suggestions)

def create_enhanced_xray_report_pdf(patient_name, patient_age, patient_gender, disease_name, image_data=None):
    """
    Creates a professional PDF report with generated content for chest X-ray findings.
    """
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, topMargin=0.5*inch, bottomMargin=0.5*inch)
    styles = getSampleStyleSheet()
    
    # Create enhanced custom styles
    title_style = ParagraphStyle(
        'TitleStyle',
        parent=styles['Heading1'],
        fontSize=20,
        alignment=1,
        spaceAfter=8,
        textColor=colors.HexColor('#1E3A8A'),
        fontName='Helvetica-Bold'
    )
    
    subtitle_style = ParagraphStyle(
        'SubtitleStyle',
        parent=styles['Heading2'],
        fontSize=16,
        alignment=1,
        spaceAfter=12,
        textColor=colors.HexColor('#3B82F6'),
        fontName='Helvetica-Bold'
    )
    
    heading_style = ParagraphStyle(
        'HeadingStyle',
        parent=styles['Heading2'],
        fontSize=13,
        spaceBefore=15,
        spaceAfter=8,
        textColor=colors.HexColor('#1E3A8A'),
        fontName='Helvetica-Bold',
        borderWidth=1,
        borderColor=colors.HexColor('#3B82F6'),
        borderPadding=8,
        borderRadius=3,
        backColor=colors.HexColor('#F0F7FF')
    )
    
    normal_style = ParagraphStyle(
        'NormalStyle',
        parent=styles['Normal'],
        fontSize=11,
        leading=16,
        spaceAfter=12,
        fontName='Helvetica',
        alignment=0
    )
    
    findings_style = ParagraphStyle(
        'FindingsStyle',
        parent=styles['Normal'],
        fontSize=11,
        leading=16,
        spaceAfter=12,
        fontName='Helvetica',
        leftIndent=10,
        backColor=colors.HexColor('#F9FAFB'),
        borderWidth=0.5,
        borderColor=colors.HexColor('#E5E7EB'),
        borderPadding=10
    )
    
    footer_style = ParagraphStyle(
        'FooterStyle',
        parent=styles['Normal'],
        fontSize=9,
        alignment=1,
        textColor=colors.HexColor('#6B7280'),
        fontName='Helvetica',
        leading=12
    )
    
    # Create content
    content = []
    
    # Add title and subtitle
    content.append(Paragraph("COMPREHENSIVE CHEST X-RAY REPORT", title_style))
    content.append(Paragraph("Radiological Assessment and Clinical Correlation", subtitle_style))
    content.append(Spacer(1, 15))
    
    # Enhanced patient info table
    current_date = datetime.now().strftime("%B %d, %Y at %I:%M %p")
    
    patient_data = [
        ["Patient Name:", patient_name],
        ["Age:", f"{patient_age} years"],
        ["Gender:", patient_gender],
        ["Date of Report:", current_date],
        ["Primary Finding:", disease_name],
        ["Report Type:", "Comprehensive Radiological Assessment"]
    ]
    
    patient_table = Table(patient_data, colWidths=[2*inch, 4*inch])
    patient_table.setStyle(TableStyle([
        ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor('#1E3A8A')),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor('#E5E7EB')),
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#F9FAFB')),
    ]))
    
    content.append(patient_table)
    content.append(Spacer(1, 15))
    
    # Add X-ray image if provided
    if image_data:
        try:
            img = Image(io.BytesIO(image_data), width=4*inch, height=4*inch)
            content.append(Paragraph("RADIOGRAPHIC IMAGE", heading_style))
            content.append(img)
            content.append(Spacer(1, 15))
        except:
            pass
    
    # Add professional radiologist findings
    content.append(Paragraph("RADIOLOGICAL INTERPRETATION", heading_style))
    professional_findings = generate_professional_findings(disease_name, patient_age, patient_gender)
    content.append(Paragraph(professional_findings, findings_style))
    content.append(Spacer(1, 10))
    
    # Add detailed medical explanation
    content.append(Paragraph("CLINICAL SIGNIFICANCE AND PATHOPHYSIOLOGY", heading_style))
    medical_explanation = get_enhanced_disease_description(disease_name)
    
    # Split explanation into paragraphs for better formatting
    for paragraph in medical_explanation.split('. '):
        if paragraph.strip():
            if not paragraph.endswith('.'):
                paragraph += '.'
            content.append(Paragraph(paragraph.strip(), normal_style))
    
    # Add comprehensive recommendations
    content.append(Paragraph("COMPREHENSIVE PATIENT CARE RECOMMENDATIONS", heading_style))
    recommendations = get_enhanced_patient_suggestions(disease_name)
    
    # Format recommendations as numbered list
    for i, recommendation in enumerate(recommendations.split('. '), 1):
        if recommendation.strip():
            if not recommendation.endswith('.'):
                recommendation += '.'
            content.append(Paragraph(f"{i}. {recommendation.strip()}", normal_style))
    
    # Add professional disclaimer
    content.append(Spacer(1, 25))
    disclaimer_text = (
        "<b>MEDICAL DISCLAIMER:</b> This radiological report has been generated based on imaging findings and is intended for healthcare professional review and patient education. "
        "The interpretation, recommendations, and clinical correlation contained herein should be reviewed by a qualified healthcare professional familiar with the patient's clinical history and current presentation. "
        "All treatment decisions should be made in consultation with your healthcare provider. "
        "This report does not replace a formal medical consultation and is not intended to provide a definitive diagnosis without clinical correlation. "
        "Any discrepancies between the radiographic findings and clinical presentation should prompt further diagnostic evaluation, including additional imaging or specialist consultation as deemed necessary."
    )
    content.append(Paragraph(disclaimer_text, normal_style))
    
    # Add footer with generation information
    content.append(Spacer(1, 25))
    footer_text = f"Report Generated by Advanced Radiological Reporting System | {current_date} | Prepared for {patient_name}"
    content.append(Paragraph(footer_text, footer_style))
    
    # Build the PDF
    doc.build(content)
    buffer.seek(0)
    return buffer.getvalue()

# Example usage
if __name__ == "__main__":
    # Example patient data
    patient_name = "John Doe"
    patient_age = 45
    patient_gender = "Male"
    disease_name = "Pneumonia"
    
    # Generate PDF report
    pdf_data = create_enhanced_xray_report_pdf(patient_name, patient_age, patient_gender, disease_name)
    
    # Save to file for testing
    with open("xray_report.pdf", "wb") as f:
        f.write(pdf_data)
    print("PDF report generated successfully as 'xray_report.pdf'")