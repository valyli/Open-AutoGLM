"""Desktop application package mappings (Windows/macOS/Linux)."""

# Desktop application paths/commands
# Users can customize these paths based on their installation
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


def list_supported_apps() -> list[str]:
    """
    Get list of supported desktop application names.

    Returns:
        List of application names.
    """
    return list(APP_PACKAGES_DESKTOP.keys())
