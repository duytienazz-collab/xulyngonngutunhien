<!-- HƯỚNG DẪN CÀI ĐẶT VÀ CHẠY HỆ THỐNG TEXT-TO-MCQ
1. YÊU CẦU HỆ THỐNG (Prerequisites)
Trước khi bắt đầu, máy tính của bạn cần đáp ứng các điều kiện sau:

Hệ điều hành: Windows 10/11, macOS, hoặc Ubuntu.

Python: Phiên bản 3.10 hoặc 3.11 (Khuyến nghị dùng 3.11). Tuyệt đối không dùng Python 3.12+ vì dễ lỗi thư viện AI.

RAM: Tối thiểu 8GB (Khuyến nghị 16GB nếu chạy mô hình PhoBERT).

Dung lượng ổ cứng: Cần trống ít nhất 5GB để tải các mô hình (ViT5, PhoBERT, SBERT).

Kết nối Internet: Cần thiết cho lần chạy đầu tiên để tải các mô hình từ Hugging Face.

2. CÀI ĐẶT MÔI TRƯỜNG
Bước 2.1: Mở Terminal / Command Prompt
Mở cửa sổ dòng lệnh và di chuyển đến thư mục chứa source code của dự án (thư mục Text-to-MCQ).

bash
cd đường_dẫn_đến_thư_mục/Text-to-MCQ
Bước 2.2: Tạo môi trường ảo (Virtual Environment)
Việc này giúp cô lập các thư viện của dự án, tránh làm hỏng môi trường Python chung của máy.

bash
python -m venv venv
Bước 2.3: Kích hoạt môi trường ảo
Nếu dùng Windows (PowerShell):

powershell
.\venv\Scripts\Activate.ps1
(Nếu bị lỗi Execution Policy, hãy chạy lệnh Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass trước).

Nếu dùng Windows (CMD):

cmd
.\venv\Scripts\activate.bat
Nếu dùng macOS / Linux:

bash
source venv/bin/activate
(Khi kích hoạt thành công, bạn sẽ thấy chữ (venv) xuất hiện ở đầu dòng lệnh).

3. CÀI ĐẶT THƯ VIỆN (Dependencies)

Bước 3: Tiến hành cài đặt
Chạy lệnh sau để cài toàn bộ thư viện (Quá trình này mất khoảng 3-5 phút):

bash
pip install --upgrade pip
pip install -r requirements.txt
⚠️ CẢNH BÁO LỖI THƯỜNG GẶP:
Nếu bạn thấy lỗi liên quan đến tokenizers (như lỗi link.exe trên Windows), hãy chạy lệnh sau để ép pip tải bản đã biên dịch sẵn:
pip install tokenizers==0.19.1 --only-binary :all:

5. CHẠY CHƯƠNG TRÌNH
Có 2 cách để chạy hệ thống, tùy thuộc vào mục đích của bạn:

Cách 1: Chạy Giao diện Web (Dành cho Demo / Bảo vệ đồ án)
Đây là cách chạy đẹp mắt nhất để thầy cô xem sản phẩm. Đảm bảo Terminal đang ở trong môi trường (venv) và đứng ở thư mục gốc, chạy lệnh:

bash
streamlit run frontend/streamlit_app.py
Trình duyệt web sẽ tự động mở lên tại địa chỉ http://localhost:8501.

Lần chạy đầu tiên: Hệ thống sẽ mất khoảng 2-5 phút để tải các mô hình ngôn ngữ (ViT5, PhoBERT, SBERT) về máy. Các lần sau sẽ chạy ngay lập tức.

Bạn chỉ cần kéo thả file PDF/DOCX/TXT vào và bấm "Bắt đầu tạo câu hỏi".

Cách 2: Chạy Test tự động bằng dòng lệnh (Dành cho Debug)
Nếu bạn muốn kiểm tra xem Pipeline có hoạt động đúng không mà không cần mở Web, hãy chạy file test:

bash
python test_nlp.py
(Kết quả JSON của đề thi sẽ được in trực tiếp ra màn hình Terminal, kèm theo các log thông báo quá trình lọc dữ liệu).

6. XỬ LÝ LỖI THƯỜNG GẶP (Troubleshooting)
Lỗi	Nguyên nhân	Cách khắc phục
ModuleNotFoundError: No module named 'app'	Đang đứng sai thư mục khi chạy Streamlit.	Đảm bảo Terminal đang ở thư mục gốc Text-to-MCQ trước khi gõ lệnh streamlit run ....
TypeError: 'dict' object is not an instance of 'Sequence'	Xung đột phiên bản transformers và tokenizers.	Chạy lại: pip install "transformers>=4.41.0,<5.0.0" "tokenizers>=0.19.0,<0.20.0"
FileNotFoundError: ./models/vit5_qg	Chưa tải mô hình ViT5 từ Google Drive về.	Xem lại Mục 4 để tải và đặt mô hình đúng vị trí.
Web báo: "Không thể tạo câu hỏi đạt chuẩn"	Bộ lọc Validation quá khắt khe hoặc văn bản quá ngắn/ít thực thể.	Đây không phải lỗi, hệ thống đang ưu tiên chất lượng. Hãy thử upload một file PDF dài hơn (bài báo, giáo trình) có nhiều tên riêng/địa danh/số liệu.
Web bị "đơ" ở lần chạy đầu tiên	Hệ thống đang ngầm tải mô hình PhoBERT và SBERT (dung lượng lớn).	Đợi khoảng 2-5 phút tùy tốc độ mạng. Lần sau sẽ chạy rất nhanh.
 -->
