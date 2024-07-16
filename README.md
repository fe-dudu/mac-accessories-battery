



### BatteryStatus 애플리케이션

이 애플리케이션은 매직 키보드, 매직 마우스, 매직 트랙패드, 에어팟의 배터리 상태를 모니터링하는 간단한 macOS 메뉴 바 앱입니다.

### 시작하기

### 시스템 요구 사항

- macOS 10.12 이상
- Python 3.6 이상 설치 필요

### 설치
```
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
```

### 빌드
```
pyinstaller --onefile --icon=./AppIcon.icns --noconsole Battery.py
```
