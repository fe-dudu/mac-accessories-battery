import rumps
import subprocess
import re

class PeripheralBatteryStatus(rumps.App):
    def __init__(self):
        super(PeripheralBatteryStatus, self).__init__("BatteryStatus")
        self.menu = ["Update"]
        self.previous_bluetooth_info = None
        self.timer = rumps.Timer(self.update_status, 10)
        self.timer.start()

    def get_device_battery(self, device_name):
        cmd = f"ioreg -c AppleDeviceManagementHIDEventService -r -l | grep -i '{device_name}' -A 20 | grep -i 'batterypercent' | cut -d '=' -f2 | cut -d ' ' -f2"
        try:
            result = subprocess.check_output(cmd, shell=True).decode('utf-8').strip()
            return int(result) if result else None
        except Exception as e:
            print(f"Error getting battery info for {device_name}: {e}")
            return None

    def get_airpods_battery(self):
        cmd = "system_profiler SPBluetoothDataType"
        try:
            result = subprocess.check_output(cmd, shell=True).decode('utf-8')
            left_battery = re.search(r"Left Battery Level: (\d+)%", result)
            right_battery = re.search(r"Right Battery Level: (\d+)%", result)
            case_battery = re.search(r"Case Battery Level: (\d+)%", result)
            left_battery = int(left_battery.group(1)) if left_battery else None
            right_battery = int(right_battery.group(1)) if right_battery else None
            case_battery = int(case_battery.group(1)) if case_battery else None
            return left_battery, right_battery, case_battery
        except Exception as e:
            print(f"Error getting AirPods battery info: {e}")
            return None, None, None

    def get_bluetooth_info(self):
        cmd = "system_profiler SPBluetoothDataType"
        try:
            result = subprocess.check_output(cmd, shell=True).decode('utf-8')
            return result
        except Exception as e:
            print(f"Error getting Bluetooth info: {e}")
            return None

    def bluetooth_info_changed(self, current_info):
        if self.previous_bluetooth_info is None:
            return True
        return current_info != self.previous_bluetooth_info

    @rumps.clicked("Update")
    def update_status(self, _=None):
        current_bluetooth_info = self.get_bluetooth_info()
        if current_bluetooth_info is None:
            return
        
        if self.bluetooth_info_changed(current_bluetooth_info):
            self.previous_bluetooth_info = current_bluetooth_info

            keyboard_battery = self.get_device_battery("Magic Keyboard")
            mouse_battery = self.get_device_battery("Magic Mouse")
            trackpad_battery = self.get_device_battery("Magic Trackpad")
            airpods_battery = self.get_airpods_battery()

            status = []
            if keyboard_battery is not None:
                status.append(f"⌨ {keyboard_battery}%")
            if mouse_battery is not None:
                status.append(f"🖱️ {mouse_battery}%")
            if trackpad_battery is not None:
                status.append(f"🖐️ {trackpad_battery}%")
            if airpods_battery[0] is not None:
                status.append(f"🎧L: {airpods_battery[0]}%")
            if airpods_battery[1] is not None:
                status.append(f"🎧R: {airpods_battery[1]}%")
            if airpods_battery[2] is not None:
                status.append(f"🎧C: {airpods_battery[2]}%")

            self.title = " | ".join(status) if status else "No devices"

if __name__ == "__main__":
    PeripheralBatteryStatus().run()
