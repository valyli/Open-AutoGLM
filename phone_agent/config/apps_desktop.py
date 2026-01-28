"""Desktop application package mappings (Windows/macOS/Linux)."""

import platform

# Get current operating system
_system = platform.system().lower()

# Desktop application paths/commands
# Users can customize these paths based on their installation
if _system == "darwin":  # macOS
    APP_PACKAGES_DESKTOP = {
        # Browsers
        "Chrome": "open -a 'Google Chrome'",
        "谷歌浏览器": "open -a 'Google Chrome'",
        "Safari": "open -a Safari",
        "浏览器": "open -a Safari",
        "Firefox": "open -a Firefox",
        "火狐浏览器": "open -a Firefox",
        "Edge": "open -a 'Microsoft Edge'",
        
        # Office
        "Word": "open -a 'Microsoft Word'",
        "Excel": "open -a 'Microsoft Excel'",
        "PowerPoint": "open -a 'Microsoft PowerPoint'",
        "Outlook": "open -a 'Microsoft Outlook'",
        
        # System Apps
        "TextEdit": "open -a TextEdit",
        "文本编辑": "open -a TextEdit",
        "记事本": "open -a TextEdit",
        "Calculator": "open -a Calculator",
        "计算器": "open -a Calculator",
        "Finder": "open -a Finder",
        "访达": "open -a Finder",
        "资源管理器": "open -a Finder",
        "Terminal": "open -a Terminal",
        "终端": "open -a Terminal",
        "命令行": "open -a Terminal",
        
        # Communication
        "WeChat": "open -a WeChat",
        "微信": "open -a WeChat",
        "QQ": "open -a QQ",
        "Telegram": "open -a Telegram",
        "Slack": "open -a Slack",
        
        # Media
        "Music": "open -a Music",
        "音乐": "open -a Music",
        "Photos": "open -a Photos",
        "照片": "open -a Photos",
        "QuickTime Player": "open -a 'QuickTime Player'",
        
        # Development
        "VS Code": "open -a 'Visual Studio Code'",
        "Visual Studio Code": "open -a 'Visual Studio Code'",
        "Xcode": "open -a Xcode",
        "iTerm": "open -a iTerm",
        
        # Productivity
        "Notes": "open -a Notes",
        "备忘录": "open -a Notes",
        "Calendar": "open -a Calendar",
        "日历": "open -a Calendar",
        "Mail": "open -a Mail",
        "邮件": "open -a Mail",
    }
elif _system == "windows":
    APP_PACKAGES_DESKTOP = {
        # Browsers
        "Chrome": "chrome.exe",
        "谷歌浏览器": "chrome.exe",
        "Edge": "msedge.exe",
        "浏览器": "msedge.exe",
        "Firefox": "firefox.exe",
        "火狐浏览器": "firefox.exe",
        
        # Office
        "Word": "winword.exe",
        "Excel": "excel.exe",
        "PowerPoint": "powerpnt.exe",
        "Outlook": "outlook.exe",
        
        # System Apps
        "记事本": "notepad.exe",
        "Notepad": "notepad.exe",
        "计算器": "calc.exe",
        "Calculator": "calc.exe",
        "画图": "mspaint.exe",
        "Paint": "mspaint.exe",
        "资源管理器": "explorer.exe",
        "Explorer": "explorer.exe",
        
        # Communication
        "微信": r"C:\Program Files\Tencent\WeChat\WeChat.exe",
        "WeChat": r"C:\Program Files\Tencent\WeChat\WeChat.exe",
        "QQ": r"C:\Program Files\Tencent\QQ\Bin\QQ.exe",
        
        # Media
        "Windows Media Player": "wmplayer.exe",
        
        # Development
        "VS Code": "code.exe",
        "Visual Studio Code": "code.exe",
        "命令提示符": "cmd.exe",
        "CMD": "cmd.exe",
        "PowerShell": "powershell.exe",
    }
else:  # Linux
    APP_PACKAGES_DESKTOP = {
        # Browsers
        "Chrome": "google-chrome",
        "谷歌浏览器": "google-chrome",
        "Firefox": "firefox",
        "火狐浏览器": "firefox",
        "Edge": "microsoft-edge",
        "浏览器": "firefox",
        
        # Office
        "LibreOffice Writer": "libreoffice --writer",
        "Writer": "libreoffice --writer",
        "LibreOffice Calc": "libreoffice --calc",
        "Calc": "libreoffice --calc",
        
        # System Apps
        "Text Editor": "gedit",
        "记事本": "gedit",
        "Calculator": "gnome-calculator",
        "计算器": "gnome-calculator",
        "File Manager": "nautilus",
        "资源管理器": "nautilus",
        "Terminal": "gnome-terminal",
        "终端": "gnome-terminal",
        
        # Development
        "VS Code": "code",
        "Visual Studio Code": "code",
    }


def list_supported_apps() -> list[str]:
    """
    Get list of supported desktop application names.

    Returns:
        List of application names.
    """
    return list(APP_PACKAGES_DESKTOP.keys())
