



### Mac Battery Status App

This application is a simple macOS menu bar app that monitors the battery status of the Magic Keyboard, Magic Mouse, Magic Trackpad, and AirPods.


### System Requirements
- macOS 10.12 >
- Python 3.6 >


### install
```
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
```

### build
```
pyinstaller --onefile --icon=./AppIcon.icns --noconsole Battery.py

root/dist/Battery <<
```
