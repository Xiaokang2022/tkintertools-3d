"""All constants for 3D"""

import platform

FONT = "Microsoft YaHei" if platform.system(
) == "Windows" else "PingFang SC" if platform.system() == "Darwin" else "Noto Sans"

SIZE = -20
