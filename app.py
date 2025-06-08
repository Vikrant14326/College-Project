import streamlit as st
import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
from PIL import Image
import io
import template
from datetime import datetime
import faiss
import pickle
import os
from pathlib import Path
import logging
import cv2

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

st.set_page_config(page_title="Medical X-ray Report Generator", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
    <style>
    .main .block-container { padding-top: 2rem; padding-bottom: 2rem; color: black; }
    h1, h2, h3 { color: #1E3A8A; }
    .stButton>button { background-color: #1E3A8A; color: white; border-radius: 5px; padding: 0.5rem 1rem; font-weight: bold; }
    .report-box { background-color: #F3F4F6; border-radius: 10px; padding: 20px; margin-bottom: 20px; color: black; }
    </style>
""", unsafe_allow_html=True)

class FastRAGSystem:
    def __init__(self, csv_path="Data\cxr_df.csv", index_path="Data/faiss_index.bin", metadata_path="Data/metadata.pkl"):
        self.csv_path = csv_path
        self.index_path = index_path
        self.metadata_path = metadata_path
        self.embedding_model = None
        self.faiss_index = None
        self.metadata = None
        self.df = None
        
    @st.cache_resource
    def load_embedding_model(_self):
        return SentenceTransformer('all-MiniLM-L6-v2')
    
    @st.cache_data
    def load_dataset(_self):
        try:
            df = pd.read_csv(_self.csv_path)
            logger.info(f"Loaded dataset with {len(df)} records")
            
            if 'text' not in df.columns and 'report' in df.columns:
                df['text'] = df['report']
            elif 'text' not in df.columns:
                text_cols = df.select_dtypes(include=['object']).columns
                if len(text_cols) > 0:
                    longest_col = max(text_cols, key=lambda x: df[x].str.len().mean())
                    df['text'] = df[longest_col]
                else:
                    df['text'] = "No report available"
            
            if 'id' not in df.columns:
                df['id'] = df.index.astype(str)
                
            return df
        except Exception as e:
            logger.error(f"Error loading dataset: {e}")
            return pd.DataFrame({'id': ['1'], 'text': ['Sample chest X-ray report showing normal findings']})
    
    def build_faiss_index(self, force_rebuild=False):
        if not force_rebuild and os.path.exists(self.index_path) and os.path.exists(self.metadata_path):
            return self.load_faiss_index()
        
        logger.info("Building FAISS index...")
        df = self.load_dataset()
        
        if self.embedding_model is None:
            self.embedding_model = self.load_embedding_model()
        
        batch_size = 100
        embeddings = []
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        for i in range(0, len(df), batch_size):
            batch = df['text'].iloc[i:i+batch_size].fillna('').tolist()
            batch_embeddings = self.embedding_model.encode(batch, show_progress_bar=False)
            embeddings.extend(batch_embeddings)
            
            progress = min((i + batch_size) / len(df), 1.0)
            progress_bar.progress(progress)
            status_text.text(f"Processing embeddings: {i+batch_size}/{len(df)}")
        
        embeddings = np.array(embeddings).astype('float32')
        dimension = embeddings.shape[1]
        index = faiss.IndexFlatIP(dimension)
        faiss.normalize_L2(embeddings)
        index.add(embeddings)
        
        os.makedirs(os.path.dirname(self.index_path), exist_ok=True)
        faiss.write_index(index, self.index_path)
        
        metadata = {
            'reports': df['text'].tolist(),
            'ids': df['id'].tolist(),
            'diseases': [self.extract_disease_name(text) for text in df['text']],
            'dimension': dimension,
            'total_records': len(df)
        }
        
        with open(self.metadata_path, 'wb') as f:
            pickle.dump(metadata, f)
        
        progress_bar.empty()
        status_text.empty()
        st.success(f"FAISS index built successfully with {len(df)} records")
        
        self.faiss_index = index
        self.metadata = metadata
        return index, metadata
    
    @st.cache_resource
    def load_faiss_index(_self):
        try:
            index = faiss.read_index(_self.index_path)
            with open(_self.metadata_path, 'rb') as f:
                metadata = pickle.load(f)
            logger.info(f"Loaded FAISS index with {metadata['total_records']} records")
            return index, metadata
        except Exception as e:
            logger.error(f"Error loading FAISS index: {e}")
            return None, None
    
    def search_similar_reports(self, query_text, k=5):
        if self.faiss_index is None or self.metadata is None:
            return []
        
        if self.embedding_model is None:
            self.embedding_model = self.load_embedding_model()
        
        query_embedding = self.embedding_model.encode([query_text]).astype('float32')
        faiss.normalize_L2(query_embedding)
        scores, indices = self.faiss_index.search(query_embedding, k)
        
        results = []
        for score, idx in zip(scores[0], indices[0]):
            if idx < len(self.metadata['reports']):
                results.append({
                    'report': self.metadata['reports'][idx],
                    'id': self.metadata['ids'][idx],
                    'disease': self.metadata['diseases'][idx],
                    'similarity_score': float(score)
                })
        return results
    
    def extract_disease_name(self, report_text: str) -> str:
        report_lower = str(report_text).lower()
        
        positive_conditions = {
            "emphysema": "Emphysema", "pneumonia": "Pneumonia", "pleural effusion": "Pleural Effusion",
            "atelectasis": "Atelectasis", "cardiomegaly": "Cardiomegaly", "pulmonary edema": "Pulmonary Edema",
            "pneumothorax": "Pneumothorax", "consolidation": "Consolidation", "fibrosis": "Fibrosis",
            "nodule": "Nodule", "mass": "Mass", "fracture": "Fracture", "tuberculosis": "Tuberculosis",
            "covid-19": "COVID-19", "bronchitis": "Bronchitis", "lung cancer": "Lung Cancer",
            "pulmonary embolism": "Pulmonary Embolism", "interstitial markings": "Interstitial Disease",
            "hyperinflated": "Emphysema", "hyperlucency": "Emphysema", "enlarged heart": "Cardiomegaly",
            "cardiac silhouette is enlarged": "Cardiomegaly"
        }
        
        for condition_key, condition_name in positive_conditions.items():
            if condition_key in report_lower:
                condition_pos = report_lower.find(condition_key)
                text_before = report_lower[max(0, condition_pos-20):condition_pos]
                negation_words = ["no ", "without ", "absence of", "rule out", "r/o"]
                is_negated = any(neg in text_before for neg in negation_words)
                if not is_negated:
                    return condition_name
        
        explicit_normal_patterns = ["normal chest", "clear lungs", "unremarkable", "no acute", "no active disease", "within normal limits"]
        has_explicit_normal = any(pattern in report_lower for pattern in explicit_normal_patterns)
        
        negative_only_patterns = ["no pneumonia", "no consolidation", "no pleural effusion", "no pneumothorax", "no mass", "no nodules", "no fracture"]
        negative_count = sum(1 for pattern in negative_only_patterns if pattern in report_lower)
        
        if has_explicit_normal or negative_count >= 2:
            return "Normal Findings"
        
        return "Radiographic Abnormality"

    def generate_professional_report(self, disease_name: str, similar_cases: list) -> str:
        """Generate professional AI report based on primary finding"""
        
        # Professional report templates based on disease
        report_templates = {
            "Normal Findings": """
            IMPRESSION: Normal chest radiographic examination.
            
            FINDINGS: The lungs demonstrate clear bilateral fields with normal pulmonary vascularity. 
            Cardiac silhouette appears within normal limits. Mediastinal contours are unremarkable. 
            No evidence of pneumothorax, pleural effusion, or focal consolidation. 
            Bony structures and soft tissues appear intact without acute abnormality.
            
            ASSESSMENT: No acute cardiopulmonary abnormalities identified on this chest radiograph.
            """,
            
            "Pneumonia": """
            IMPRESSION: Findings consistent with pneumonia.
            
            FINDINGS: Areas of increased opacity and consolidation are identified, suggesting acute inflammatory 
            process within the pulmonary parenchyma. Patchy infiltrates may be present with associated 
            air bronchograms. Cardiac silhouette and mediastinal structures evaluated within the context 
            of the inflammatory process.
            
            ASSESSMENT: Radiographic features support clinical suspicion of pneumonia. 
            Correlation with clinical symptoms and laboratory findings recommended.
            """,
            
            "Pleural Effusion": """
            IMPRESSION: Pleural effusion identified.
            
            FINDINGS: Fluid collection within the pleural space demonstrating characteristic meniscus sign 
            and blunting of costophrenic angles. The degree of effusion and impact on adjacent lung 
            expansion is noted. Cardiac and mediastinal structures assessed for displacement or compression.
            
            ASSESSMENT: Pleural effusion present. Clinical correlation recommended to determine underlying etiology 
            and guide appropriate management.
            """,
            
            "Cardiomegaly": """
            IMPRESSION: Cardiac enlargement identified.
            
            FINDINGS: Cardiac silhouette demonstrates increased size with cardiothoracic ratio suggesting 
            cardiomegaly. Pulmonary vascularity patterns evaluated for signs of congestion or redistribution. 
            Lung fields assessed for associated findings such as pulmonary edema or effusions.
            
            ASSESSMENT: Cardiomegaly noted. Clinical correlation with echocardiography and cardiac evaluation 
            recommended for further assessment.
            """,
            
            "Pneumothorax": """
            IMPRESSION: Pneumothorax identified.
            
            FINDINGS: Air collection within the pleural space demonstrating visceral pleural line separation 
            from chest wall. The extent and degree of lung collapse assessed. Mediastinal structures 
            evaluated for potential shift or tension components.
            
            ASSESSMENT: Pneumothorax present. Immediate clinical attention recommended based on size and 
            patient symptoms to determine appropriate intervention.
            """,
            
            "Atelectasis": """
            IMPRESSION: Atelectasis identified.
            
            FINDINGS: Areas of volume loss and increased opacity consistent with collapse of lung segments 
            or lobes. Compensatory changes in adjacent structures noted. Evaluation for potential 
            underlying causes such as obstruction or compression performed.
            
            ASSESSMENT: Atelectasis present. Further evaluation may be warranted to determine underlying 
            cause and guide treatment approach.
            """,
            
            "Emphysema": """
            IMPRESSION: Changes consistent with emphysema.
            
            FINDINGS: Hyperinflation of lung fields with flattened diaphragms and increased anteroposterior 
            chest diameter. Pulmonary vascularity appears attenuated with characteristic hyperlucency. 
            Cardiac silhouette may appear elongated due to positional changes.
            
            ASSESSMENT: Radiographic features consistent with emphysematous changes. 
            Pulmonary function testing and clinical correlation recommended.
            """,
            
            "Radiographic Abnormality": """
            IMPRESSION: Radiographic abnormality identified requiring further evaluation.
            
            FINDINGS: Abnormal radiographic features are present that warrant additional investigation. 
            The findings demonstrate characteristics that deviate from normal chest radiographic anatomy. 
            Further imaging or clinical correlation may be beneficial for definitive characterization.
            
            ASSESSMENT: Abnormal radiographic findings identified. Additional imaging studies or 
            clinical evaluation recommended for comprehensive assessment and diagnosis.
            """
        }
        
        # Get base template or default
        base_report = report_templates.get(disease_name, report_templates["Radiographic Abnormality"])
        
        # Enhance with similar case insights if available
        if similar_cases and len(similar_cases) > 0:
            # Extract key findings from similar cases
            similar_findings = []
            for case in similar_cases[:2]:  # Use top 2 similar cases
                case_disease = self.extract_disease_name(case['report'])
                if case_disease == disease_name and case['similarity_score'] > 0.7:
                    # Extract key phrases from similar reports
                    report_text = case['report'].lower()
                    if 'bilateral' in report_text:
                        similar_findings.append("bilateral involvement")
                    if 'acute' in report_text:
                        similar_findings.append("acute presentation")
                    if 'chronic' in report_text:
                        similar_findings.append("chronic changes")
            
            # Add clinical correlation note if similar findings found
            if similar_findings:
                additional_note = f"\n\nCLINICAL CORRELATION: Based on similar radiographic patterns, " + \
                               f"findings may demonstrate {', '.join(similar_findings)}. " + \
                               f"Correlation with patient history and clinical presentation recommended."
                base_report += additional_note
        
        return base_report.strip()

@st.cache_resource
def get_rag_system():
    return FastRAGSystem()

def process_image_with_rag(uploaded_image, rag_system):
    try:
        image = Image.open(uploaded_image).resize((224, 224)).convert('L')
        image_array = np.array(image, dtype=np.uint8)
        
        brightness = np.mean(image_array)
        contrast = np.std(image_array)
        
        edges = cv2.Canny(image_array, 100, 200)
        edge_density = np.sum(edges) / (224 * 224 * 255)
        
        h, w = image_array.shape
        mid_h, mid_w = h // 2, w // 2
        regional_means = {
            'top_left': np.mean(image_array[:mid_h, :mid_w]),
            'top_right': np.mean(image_array[:mid_h, mid_w:]),
            'bottom_left': np.mean(image_array[mid_h:, :mid_w]),
            'bottom_right': np.mean(image_array[mid_h:, mid_w:])
        }
        
        left_lung_mean = (regional_means['top_left'] + regional_means['bottom_left']) / 2
        right_lung_mean = (regional_means['top_right'] + regional_means['bottom_right']) / 2
        asymmetry = abs(left_lung_mean - right_lung_mean)
        
        query_parts = ["chest X-ray"]
        
        if brightness < 80:
            query_parts.append("dark opacity")
        elif brightness > 150:
            query_parts.append("hyperlucent")
        
        if contrast < 20:
            query_parts.append("clear lung fields")
        elif contrast > 50:
            query_parts.append("high contrast abnormality")
        
        if edge_density > 0.1:
            query_parts.append("structural abnormality")
        elif edge_density < 0.02:
            query_parts.append("smooth lung fields")
        
        if asymmetry > 30:
            query_parts.append("unilateral opacity")
        
        if "dark opacity" in query_parts and "unilateral opacity" in query_parts:
            query_parts.append("possible pneumonia or atelectasis")
        elif "hyperlucent" in query_parts:
            query_parts.append("possible pneumothorax or emphysema")
        elif "structural abnormality" in query_parts:
            query_parts.append("possible nodule or mass")
        elif "clear lung fields" in query_parts and "smooth lung fields" in query_parts:
            query_parts.append("normal findings")
        
        query = " ".join(query_parts)
        similar_cases = rag_system.search_similar_reports(query, k=5)
        
        if similar_cases:
            best_match = similar_cases[0]
            actual_disease = rag_system.extract_disease_name(best_match['report'])
            
            # Generate professional report based on disease
            professional_report = rag_system.generate_professional_report(actual_disease, similar_cases[1:3])
            
            return {
                'id': best_match['id'],
                'report': professional_report,  # Use professional report instead of raw text
                'disease': actual_disease,
                'confidence': best_match['similarity_score'],
                'similar_cases': similar_cases[1:3],
                'query_used': query
            }
        else:
            return {
                'id': 'unknown',
                'report': 'Unable to generate comprehensive report. Please consult a qualified radiologist for professional interpretation.',
                'disease': 'Unknown',
                'confidence': 0.0,
                'similar_cases': [],
                'query_used': query
            }
            
    except Exception as e:
        logger.error(f"Error processing image: {e}")
        return None

def generate_enhanced_report(base_result, rag_system):
    disease = base_result['disease']
    disease_info = rag_system.search_similar_reports(f"{disease} findings symptoms treatment", k=5)
    
    enhanced_info = {'clinical_context': [], 'differential_diagnosis': [], 'recommendations': []}
    
    for case in disease_info:
        if case['similarity_score'] > 0.7:
            enhanced_info['clinical_context'].append(case['report'][:200] + "...")
    
    return enhanced_info

def main():
    st.title("🏥 X-ray Report Generator with RAG")
    
    rag_system = get_rag_system()
    
    if not os.path.exists(rag_system.index_path):
        with st.spinner("Building FAISS index for the first time. This may take a few minutes..."):
            rag_system.build_faiss_index()
    else:
        rag_system.faiss_index, rag_system.metadata = rag_system.load_faiss_index()
        if rag_system.embedding_model is None:
            rag_system.embedding_model = rag_system.load_embedding_model()
    
    with st.sidebar:
        st.header("Patient Information")
        st.markdown("---")
        
        patient_name = st.text_input("Patient Full Name", "")
        patient_age = st.number_input("Patient Age", min_value=0, max_value=120, value=25)
        patient_gender = st.selectbox("Patient Gender", ["Male", "Female", "Other"])
        
        st.markdown("---")
        st.subheader("RAG System Status")
        if rag_system.metadata:
            st.success(f"✅ Ready with {rag_system.metadata['total_records']:,} reports")
        else:
            st.error("❌ RAG system not initialized")
        
        if st.button("🔄 Rebuild FAISS Index"):
            with st.spinner("Rebuilding FAISS index..."):
                rag_system.build_faiss_index(force_rebuild=True)
                st.rerun()
        
        st.markdown("---")
        uploaded_file = st.file_uploader("Upload a chest X-ray image", type=["jpg", "jpeg", "png"])
        show_debug = st.checkbox("Show Debug Info")
    
    if uploaded_file and patient_name.strip():
        st.markdown("## 🔍 AI Analysis Results")
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.image(uploaded_file, caption="Uploaded X-ray Image", use_container_width=True)
            process_btn = st.button("🚀 Generate AI Report with RAG", type="primary")
        
        if process_btn and rag_system.faiss_index is not None:
            with st.spinner("🧠 AI analyzing image and searching knowledge base..."):
                result = process_image_with_rag(uploaded_file, rag_system)
                
                if result:
                    with col2:
                        if show_debug:
                            with st.expander("🐞 Debug Information"):
                                st.markdown(f"**Query Generated:** {result.get('query_used', 'N/A')}")
                                st.markdown(f"**Best Match ID:** {result['id']}")
                                st.markdown(f"**Disease Extracted:** {result['disease']}")
                        
                        confidence_color = "green" if result['confidence'] > 0.8 else "orange" if result['confidence'] > 0.5 else "red"
                        st.markdown(f"""
                        ### 📋 Primary Finding: **{result['disease']}**
                        **Confidence Score:** <span style="color: {confidence_color}; font-weight: bold;">{result['confidence']:.2f}</span>
                        """, unsafe_allow_html=True)
                        
                        with st.expander("📄 AI-Generated Report", expanded=True):
                            st.markdown(f"<div class='report-box'><pre style='white-space: pre-wrap; font-family: Arial, sans-serif;'>{result['report']}</pre></div>", unsafe_allow_html=True)
                        
                        if result['similar_cases']:
                            with st.expander("🔍 Similar Cases from Database", expanded=True):
                                for i, case in enumerate(result['similar_cases'], 1):
                                    case_disease = rag_system.extract_disease_name(case['report'])
                                    st.markdown(f"""
                                    **📊 Similar Case {i}** (Relevance Score: {case['similarity_score']:.3f})
                                    - **🏥 Disease:** {case_disease}
                                    - **📝 Report Preview:** {case['report'][:400]}{'...' if len(case['report']) > 400 else ''}
                                    - **🆔 Case ID:** {case['id']}
                                    """)
                                    st.markdown("---")
                        
                        enhanced_info = generate_enhanced_report(result, rag_system)
                        
                        img_byte_arr = io.BytesIO()
                        Image.open(uploaded_file).save(img_byte_arr, format='PNG')
                        img_byte_arr = img_byte_arr.getvalue()
                        
                        try:
                            if hasattr(template, 'create_enhanced_xray_report_pdf'):
                                try:
                                    pdf_data = template.create_enhanced_xray_report_pdf(
                                        patient_name=patient_name, patient_age=patient_age,
                                        patient_gender=patient_gender, disease_name=result['disease'],
                                        image_data=img_byte_arr, confidence_score=result['confidence'],
                                        similar_cases=result['similar_cases']
                                    )
                                except TypeError:
                                    pdf_data = template.create_enhanced_xray_report_pdf(
                                        patient_name=patient_name, patient_age=patient_age,
                                        patient_gender=patient_gender, disease_name=result['disease'],
                                        image_data=img_byte_arr
                                    )
                                
                                st.download_button(
                                    label="📄 Download Complete RAG Report",
                                    data=pdf_data,
                                    file_name=f"{patient_name.replace(' ', '_')}_RAG_Report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                                    mime="application/pdf"
                                )
                            else:
                                st.info("📄 PDF template function not available. Report displayed above.")
                        except Exception as e:
                            st.warning(f"PDF generation error: {str(e)}")
            
            if 'result' in locals() and result:
                st.markdown("### 🧠 Knowledge-Enhanced Analysis")
                st.markdown("#### 🔬 Disease-Specific Knowledge")
                disease_query = f"What are the key features of {result['disease']} in chest X-rays?"
                disease_results = rag_system.search_similar_reports(disease_query, k=3)
                
                if disease_results:
                    for i, res in enumerate(disease_results, 1):
                        res_disease = rag_system.extract_disease_name(res['report'])
                        with st.expander(f"📚 Knowledge Source {i} (Relevance: {res['similarity_score']:.3f})", expanded=(i==1)):
                            st.markdown(f"**Disease Type:** {res_disease}")
                            st.markdown(f"**Case ID:** {res['id']}")
                            st.markdown("**Report Content:**")
                            st.markdown(f"<div class='report-box'>{res['report']}</div>", unsafe_allow_html=True)
                else:
                    st.info("No disease-specific knowledge found in the database.")
    
    elif uploaded_file and not patient_name.strip():
        st.warning("⚠️ Please enter patient name before generating report")

if __name__ == '__main__':
    main()