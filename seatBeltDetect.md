

// file seatbetl_detector.py

1. __init__(model_path, confidence)
Input: Đường dẫn file model .pt, ngưỡng confidence (mặc định 0.5)
Output: Không có, chỉ khởi tạo
Làm gì: Load cục model YOLO lên bộ nhớ. Chạy 1 lần duy nhất khi tạo object.

2. detect(frame, person_bbox) ⭐ Hàm chính
Input: Ảnh/frame gốc + tọa độ vùng của 1 người [x1, y1, x2, y2]
Output: dict gồm: có dây không (True/False), tên class, confidence, tọa độ bbox
Làm gì: Cắt ảnh ra chỉ còn vùng người đó → đưa vào YOLO → trả lời "người này có đeo dây không"

3. detect_raw(frame)
Input: Ảnh/frame nguyên (không cần biết người ở đâu)
Output: Danh sách tất cả các vật detect được trong ảnh
Làm gì: Quét toàn bộ ảnh, tìm tất cả dây an toàn/không dây. Dùng để test nhanh một ảnh xem model hoạt động không.

4. _pick_best(results) (hàm nội bộ, có dấu _)
Input: Kết quả thô từ YOLO
Output: Detection có confidence cao nhất
Làm gì: Trong trường hợp YOLO tìm ra nhiều kết quả cùng lúc, hàm này chọn ra 1 kết quả tin cậy nhất để trả về.

-----------------------------------------------------------------------------

seatbelt_checker.py — Đây là lớp trung gian, nó gọi SeatbeltDetector và "đóng gói" kết quả lại cho Pipeline dùng. Bạn cần viết file này.    
pipeline.py → detect_seatbelt() — Bạn sẽ nối hàm detect_seatbelt() trong pipeline vào SeatbeltChecker. Cái này 2 bạn còn lại cũng sẽ làm phần của họ, nên cả nhóm sẽ làm chung.
Các file còn lại (core/, utils/, modules/tracking/, v.v.) → Cả nhóm làm chung

-----------------------------------------------------------------------------
// seatbelt_checker.py 

1. __init__()
Input: Không có
Output: Không có
Làm gì: Tạo ra 1 object SeatbeltDetector bên trong và giữ nó. Pipeline chỉ cần SeatbeltChecker, không cần biết bên trong dùng cái gì.

2. check(frame, person_bbox) ⭐
Input: Ảnh gốc + bbox 1 người
Output: dict (có dây, tên class, confidence, bbox)
Làm gì: Chuyển tiếp thẳng xuống SeatbeltDetector.detect(). Đây là hàm pipeline sẽ gọi.

3. check_all(frame, person_bboxes)
Input: Ảnh gốc + danh sách nhiều bbox người
Output: Danh sách dict tương ứng
Làm gì: Gọi check() cho từng người trong danh sách. Tiện khi xe có nhiều người.

----------------------------------------------------------------------------
