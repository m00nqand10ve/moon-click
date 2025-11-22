"""系统托盘模块"""
import pystray
from PIL import Image, ImageDraw, ImageFont
from typing import Callable
import threading


class SystemTray:
    """系统托盘类，提供托盘图标和菜单功能"""
    
    def __init__(self, on_quit: Callable):
        """
        初始化系统托盘
        
        Args:
            on_quit: 退出回调函数
        """
        self.on_quit = on_quit
        self.icon = None
        self.thread = None
        
    def _create_icon_image(self) -> Image.Image:
        """
        创建托盘图标（从文件加载图标）
        
        Returns:
            PIL Image 对象
        """
        try:
            # 尝试加载指定的图标文件
            icon_path = "20251122004844.ico"
            return Image.open(icon_path)
        except FileNotFoundError:
            # 如果图标文件不存在，使用原来的生成方式
            return self._create_default_icon_image()
    
    def _create_default_icon_image(self) -> Image.Image:
        """
        创建默认托盘图标（简单的文本图标 'T'）
        
        Returns:
            PIL Image 对象
        """
        # 创建 64x64 的图标
        width = 64
        height = 64
        image = Image.new('RGB', (width, height), color='white')
        draw = ImageDraw.Draw(image)
        
        # 绘制蓝色背景
        draw.rectangle([0, 0, width, height], fill='#4A90E2')
        
        # 绘制白色文字 'T'
        try:
            # 尝试使用系统字体
            font = ImageFont.truetype("arial.ttf", 40)
        except:
            # 如果失败，使用默认字体
            font = ImageFont.load_default()
        
        # 计算文字位置使其居中
        text = "T"
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        position = ((width - text_width) // 2, (height - text_height) // 2 - 5)
        
        draw.text(position, text, fill='white', font=font)
        
        return image
    
    def _create_menu(self) -> pystray.Menu:
        """
        创建托盘菜单
        
        Returns:
            pystray.Menu 对象
        """
        return pystray.Menu(
            pystray.MenuItem('退出', self._on_quit_clicked)
        )
    
    def _on_quit_clicked(self, icon, item):
        """
        处理退出菜单点击事件
        
        Args:
            icon: pystray.Icon 对象
            item: 菜单项
        """
        # 停止托盘图标
        icon.stop()
        # 调用退出回调
        if self.on_quit:
            self.on_quit()
    
    def start(self) -> None:
        """启动系统托盘（在新线程中运行）"""
        # 创建图标
        icon_image = self._create_icon_image()
        menu = self._create_menu()
        
        self.icon = pystray.Icon(
            name="FloatingTextDisplay",
            icon=icon_image,
            title="置顶文本显示工具",
            menu=menu
        )
        
        # 在新线程中运行托盘图标
        self.thread = threading.Thread(target=self.icon.run, daemon=True)
        self.thread.start()
    
    def stop(self) -> None:
        """停止系统托盘"""
        if self.icon:
            self.icon.stop()
