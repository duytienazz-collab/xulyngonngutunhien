import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
import json
from app.services.pipeline_service import MCQService

st.set_page_config(page_title="Text-to-MCQ Generator", page_icon="📝", layout="wide")
st.title("📝 Hệ thống Tự động tạo Câu hỏi Trắc nghiệm")
st.markdown("Hệ thống sử dụng mô hình **ViT5 Fine-tuned** và **PhoBERT MLM** để sinh câu hỏi từ tài liệu tiếng Việt.")

@st.cache_resource
def load_service():
    return MCQService()

try:
    service = load_service()
    st.success("✅ Mô hình AI đã sẵn sàng!")
except Exception as e:
    st.error(f"Lỗi khởi tạo mô hình: {e}")

st.sidebar.header("⚙️ Cấu hình")
# BỌC THÉP: Ép kiểu int() cho slider
num_questions = int(st.sidebar.slider("Số câu hỏi muốn tạo", 1, 20, 10))

uploaded_file = st.file_uploader("Tải lên tài liệu của bạn (PDF, DOCX, TXT)", type=['pdf', 'docx', 'txt'])

if uploaded_file is not None:
    temp_dir = "datasets/temp"
    os.makedirs(temp_dir, exist_ok=True)
    file_path = os.path.join(temp_dir, uploaded_file.name)
    
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
        
    st.info(f"📂 Đã tải lên: **{uploaded_file.name}**")
    
    if st.button("🚀 Bắt đầu tạo câu hỏi"):
        with st.spinner("AI đang xử lý... (Quá trình này có thể mất vài phút do chạy PhoBERT)"):
            try:
                # Gọi service xử lý
                mcqs = service.process_document(file_path, max_questions=num_questions)
                
                if not mcqs:
                    st.warning("⚠️ Không thể tạo câu hỏi đạt chuẩn từ tài liệu này. Vui lòng thử lại với tài liệu dài hơn hoặc có nhiều thông tin hơn.")
                else:
                    st.success(f"🎉 Đã tạo thành công {len(mcqs)} câu hỏi đạt tiêu chuẩn!")
                    
                    for i, mcq in enumerate(mcqs):
                        with st.container():
                            st.markdown(f"### Câu {i+1}: {mcq['question']}")
                            for key, val in mcq['options'].items():
                                st.markdown(f"**{key}.** {val}")
                            st.success(f"👉 Đáp án đúng: **{mcq['correct_answer']}** ({mcq['correct_answer_text']})")
                            
                            with st.expander("🔍 Xem đoạn văn bản gốc (Source Context)"):
                                st.info(mcq['source_context'])
                            st.divider()
                            
                    st.download_button(
                        label="📥 Tải xuống đề thi (JSON)",
                        data=json.dumps(mcqs, ensure_ascii=False, indent=4),
                        file_name="de_thi_trac_nghiem.json",
                        mime="application/json"
                    )
                    
            except Exception as e:
                st.error(f"Đã xảy ra lỗi trong quá trình xử lý: {e}")
                # In traceback ra terminal để dễ debug
                import traceback
                traceback.print_exc()
            finally:
                if os.path.exists(file_path):
                    os.remove(file_path)