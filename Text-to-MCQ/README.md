<!-- # HỆ THỐNG TỰ ĐỘNG SINH CÂU HỎI TRẮC NGHIỆM TIẾNG VIỆT (TEXT-TO-MCQ)

Đồ án môn học Xử lý Ngôn ngữ Tự nhiên (NLP).
Hệ thống chuyển đổi văn bản tiếng Việt (PDF, DOCX, TXT) thành bộ câu hỏi trắc nghiệm (MCQ) 4 lựa chọn, sử dụng mô hình ngôn ngữ **ViT5 Fine-tuned** kết hợp thư viện **Underthesea** và cơ chế **Validation** khắt khe để đảm bảo chất lượng đầu ra.

---

## 🛠️ 1. YÊU CẦU HỆ THỐNG
- **Hệ điều hành:** Windows, macOS, hoặc Linux.
- **Python:** Phiên bản `3.10` hoặc `3.11` (Khuyến nghị dùng 3.11).
- **RAM:** Tối thiểu 8GB (Chạy mô hình trên CPU).
- **Mô hình đã huấn luyện:** Bắt buộc phải có thư mục `vit5_qg` (đã được train trên Google Colab) đặt đúng vị trí.

---

## 📂 2. CẤU TRÚC THƯ MỤC QUAN TRỌNG
Trước khi chạy, hãy chắc chắn bạn đã tải mô hình từ Google Drive về và đặt đúng chỗ:
```text
Text-to-MCQ/
├── app/                  # Chứa toàn bộ source code xử lý (Backend)
│   ├── modules/          # Các module NLP (Đọc file, Chunking, Extractor, Generator...)
│   └── services/         # Pipeline Service kết nối các module
├── frontend/             # Chứa code giao diện Web
│   └── streamlit_app.py  # File chạy giao diện chính
├── models/
│   └── vit5_qg/          # <-- BẮT BUỘC: Thư mục chứa mô hình ViT5 đã train
├── datasets/             # Chứa dữ liệu test (nếu có)
└── requirements.txt      # Danh sách thư viện cần cài đặt
🚀 3. HƯỚNG DẪN CÀI ĐẶT (Lần đầu tiên)
Mở Terminal trên VS Code (Ctrl + ~ hoặc Terminal -> New Terminal), đảm bảo đang đứng ở thư mục gốc Text-to-MCQ và chạy lần lượt các lệnh sau:

Bước 3.1: Tạo môi trường ảo (Virtual Environment)

bash
python -m venv venv
Bước 3.2: Kích hoạt môi trường ảo

Nếu dùng Windows (PowerShell):

powershell
.\venv\Scripts\Activate.ps1
Nếu dùng Windows (CMD):

cmd
.\venv\Scripts\activate.bat
Nếu dùng Mac/Linux:

bash
source venv/bin/activate
(Khi kích hoạt thành công, bạn sẽ thấy chữ (venv) xuất hiện ở đầu dòng lệnh).

Bước 3.3: Cài đặt các thư viện

bash
pip install --upgrade pip
pip install -r requirements.txt
(Lưu ý: Nếu bạn chưa có file requirements.txt, hãy chạy lệnh sau để cài trực tiếp: pip install "transformers>=4.41.0,<5.0.0" "tokenizers>=0.19.0,<0.20.0" datasets evaluate sacrebleu rouge-score accelerate sentencepiece protobuf underthesea pymupdf python-docx sentence-transformers scikit-learn fastapi uvicorn streamlit)

🏃 4. HƯỚNG DẪN CHẠY CHƯƠNG TRÌNH
4.1. Chạy Giao diện Web (Dành cho Demo / Bảo vệ đồ án)
Đảm bảo Terminal đang ở trong môi trường ảo (venv) và đứng ở thư mục gốc. Chạy lệnh:

bash
streamlit run frontend/streamlit_app.py
Trình duyệt sẽ tự động mở lên tại địa chỉ http://localhost:8501.

Kéo thả file PDF/DOCX/TXT vào vùng tải lên.

Chọn số lượng câu hỏi.

Bấm "Bắt đầu tạo câu hỏi".

4.2. Chạy Test tự động bằng dòng lệnh (Dành cho Debug)
Nếu bạn muốn kiểm tra Pipeline hoạt động đúng không mà không cần mở Web, hãy chạy file test:

bash
python test_nlp.py
(Kết quả JSON của đề thi sẽ được in trực tiếp ra màn hình Terminal).

⚠️ 5. XỬ LÝ LỖI THƯỜNG GẶP (Troubleshooting)
Lỗi 1: ModuleNotFoundError: No module named 'app'

Nguyên nhân: Bạn đang chạy file Streamlit từ sai thư mục.

Khắc phục: Luôn đảm bảo bạn đang đứng ở thư mục gốc Text-to-MCQ khi gõ lệnh streamlit run ....

Lỗi 2: TypeError: 'dict' object is not an instance of 'Sequence' (Lỗi tokenizer)

Nguyên nhân: Xung đột phiên bản transformers và tokenizers.

Khắc phục: Chạy lại lệnh sau để đồng bộ phiên bản:

bash
pip install "transformers>=4.41.0,<5.0.0" "tokenizers>=0.19.0,<0.20.0"
Lỗi 3: FileNotFoundError: ./models/vit5_qg

Nguyên nhân: Chưa tải mô hình từ Google Colab về máy.

Khắc phục: Vào Google Drive, tải thư mục vit5_qg (chứa các file config.json, model.safetensors, tokenizer.json...) và ném vào thư mục 
models/
 của dự án. -->