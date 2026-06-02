# Core AI - Driver Monitoring System

Hệ thống AI giám sát tài xế xe hơi, phát hiện ngủ gật, kiểm tra đeo dây an toàn, và theo dõi các yếu tố cabin.

## Cấu trúc dự án

```
core_ai/
├── weights/              # AI models
├── data/                 # Dữ liệu test và output
├── src/                  # Source code
├── tests/                # Unit tests
├── requirements.txt      # Dependencies
├── run_webcam.py         # Chạy webcam realtime
├── run_video.py          # Chạy test video
└── README.md
```

## Cài đặt

```bash
pip install -r requirements.txt
```

## Sử dụng

### Chạy webcam realtime

```bash
python run_webcam.py
```

### Chạy test video

```bash
python run_video.py
```

## Tính năng

- **Phát hiện ngủ gật**: Sử dụng Eye Aspect Ratio (EAR)
- **Kiểm tra dây an toàn**: Detect dây an toàn bằng YOLO
- **Tracking người**: ByteTrack để gán ID cho mỗi người
- **Xác thực khuôn mặt**: InsightFace embedding extraction
- **Giám sát cabin**: Đếm số người, phân loại tuổi

## Modules chính

### Detection
- `person_detector.py`: Detect người
- `face_detector.py`: Detect khuôn mặt
- `seatbelt_detector.py`: Detect dây an toàn

### Tracking
- `tracker.py`: Gán ID cho người
- `seat_assigner.py`: Xác định tài xế

### Drowsiness
- `face_landmarks.py`: Lấy landmarks
- `ear_calculator.py`: Tính Eye Aspect Ratio
- `drowsiness_detector.py`: Logic phát hiện ngủ gật

### Cabin Monitor
- `people_counter.py`: Đếm người
- `age_classifier.py`: Phân loại tuổi
- `seatbelt_checker.py`: Kiểm tra dây an toàn

## Cấu hình

Xem [src/config/settings.py](src/config/settings.py) để điều chỉnh:
- `EAR_THRESHOLD`: Ngưỡng Eye Aspect Ratio
- `SLEEP_FRAME_LIMIT`: Số frame tối thiểu để xác định ngủ gật
- `PERSON_CONFIDENCE`: Độ tin cậy detect người

## Testing

```bash
python -m pytest tests/
```

## License

MIT License
