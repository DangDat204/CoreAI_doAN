# PHẦN 1: THU THẬP VÀ CHUẨN BỊ DỮ LIỆU (DATA COLLECTION & PREPROCESSING)

## 1. Định nghĩa bài toán và Phân lớp (Classes Definition)
Để xây dựng mô hình Object Detection (Phát hiện đối tượng) nhận diện hành vi đeo dây an toàn một cách chính xác và giảm thiểu tỷ lệ báo động giả (False Positive), bài toán được cấu trúc thành 3 lớp đối tượng (Classes) rõ ràng:
- **Class 0 (`no-person` / `background`):** Khung cảnh ghế trống hoặc không có người trong vùng nhận diện. Việc train lớp này giúp mô hình không bị nhầm lẫn bối cảnh nội thất xe với con người.
- **Class 1 (`no-seatbelt`):** Có người ngồi trong xe nhưng KHÔNG đeo dây an toàn.
- **Class 2 (`with-seatbelt`):** Có người ngồi trong xe và CÓ đeo dây an toàn một cách chuẩn xác.

## 2. Nguồn dữ liệu (Data Source)
Hệ thống sử dụng nguồn dữ liệu hình ảnh thực tế được thu thập và quản lý thông qua nền tảng **Roboflow Universe**. 
- **Lý do lựa chọn:** Roboflow cung cấp các bộ dữ liệu được gán nhãn sẵn bởi cộng đồng, hỗ trợ quản lý phiên bản (Dataset Versioning) và cho phép xuất dữ liệu trực tiếp sang định dạng tương thích hoàn toàn với YOLOv8 mà không cần viết script chuyển đổi thủ công.
- **Đường dẫn nguồn dữ liệu tổng hợp:** `https://universe.roboflow.com/search?q=seatbelt+detection`
- **Các bộ dữ liệu tham khảo chính:**
  + *Seat-Belt Detection Dataset (by sidharthan):* Cung cấp các góc chụp cận cảnh người ngồi ghế trước.
  + *Seatbelt-detection (by Recommendationsystemlivecamerafeed):* Chứa cả hai nhãn `with-seatbelt` và `without-seatbelt` giúp mô hình học được đặc trưng đối nghịch.

## 3. Quy trình thu thập và Tiền xử lý dữ liệu (Data Pipeline)

### Bước 1.1: Thu thập và Chọn lọc (Data Selection)
- Tiến hành tìm kiếm và tổng hợp các hình ảnh chụp từ góc nhìn cabin xe (góc nhìn từ camera hành trình hoặc camera gắn gương chiếu hậu).
- Loại bỏ các hình ảnh bị nhòe nặng, hình ảnh hoạt họa hoặc các góc chụp không thực tế để đảm bảo chất lượng dữ liệu đầu vào.

### Bước 1.2: Tiền xử lý dữ liệu (Data Preprocessing trên Roboflow)
Để tối ưu hóa cho kiến trúc mạng siêu nhẹ của **YOLOv8n (YOLOv8 Nano)**, các bước tiền xử lý sau được áp dụng đồng nhất trên toàn bộ tập dữ liệu:
- **Auto-Orient:** Tự động xoay ảnh theo đúng chiều chuẩn của siêu dữ liệu (EXIF).
- **Resize:** Chuẩn hóa toàn bộ kích thước ảnh về dạng hình vuông **640x640 pixels**. Đây là kích thước đầu vào tối ưu (input size) mặc định của YOLOv8, giúp cân bằng giữa độ chính xác và tốc độ inference.

### Bước 1.3: Tăng cường dữ liệu (Data Augmentation)
Nhằm hạn chế hiện tượng quá khớp (Overfitting) do đặc thù không gian cabin xe khá hẹp và cố định, các kỹ thuật Augmentation sau được áp dụng để tăng tính đa dạng:
- **Thay đổi độ sáng (Brightness):** Giới hạn trong khoảng -25% đến +25% để mô hình thích nghi được với điều kiện ánh sáng thay đổi (ban ngày, ban đêm, xe đi qua hầm).
- **Nhiễu hạt (Noise):** Thêm nhiễu Gaussian (lên đến 5% số pixel) để giả lập hình ảnh từ các camera giám sát chất lượng thấp hoặc camera bị bám bụi.
- **Lật ngang (Horizontal Flip):** Giúp mô hình nhận diện tốt ở cả vị trí ghế lái lẫn ghế phụ (bên trái và bên phải).

### Bước 1.4: Chia tập dữ liệu và Xuất bản (Data Splitting & Export)
- Tập dữ liệu sau khi tăng cường được chia theo tỷ lệ chuẩn cho bài toán Deep Learning:
  + **Training set:** 70% (Dùng để mô hình học đặc trưng)
  + **Validation set:** 20% (Dùng để tối ưu và đánh giá trong quá trình train)
  + **Testing set:** 10% (Dùng để đánh giá độc lập sau khi train xong)
- Xuất dữ liệu dưới định dạng **YOLOv8 format**. Kết quả trả về cấu trúc thư mục tiêu chuẩn bao gồm file cấu hình `data.yaml` và hai thư mục con `images/`, `labels/` chứa tọa độ bounding box tương ứng cho 3 lớp đã định nghĩa.