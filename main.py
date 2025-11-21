"""主应用程序入口"""
import keyboard
from typing import Callable
import threading


class HotkeyListener:
    """全局快捷键监听器类"""
    
    def __init__(self, hotkey: str, callback: Callable):
        """初始化快捷键监听器
        
        Args:
            hotkey: 快捷键字符串（如 "ctrl+shift+t"）
            callback: 快捷键触发时的回调函数
        """
        self.hotkey = hotkey
        self.callback = callback
        self._is_running = False
        self._listener_thread = None
    
    def start(self) -> None:
        """启动快捷键监听
        
        Raises:
            Exception: 当快捷键注册失败时抛出异常
        """
        if self._is_running:
            print(f"快捷键监听器已在运行: {self.hotkey}")
            return
        
        try:
            # 验证快捷键格式
            if not self._validate_hotkey(self.hotkey):
                raise ValueError(f"无效的快捷键格式: {self.hotkey}")
            
            # 注册全局快捷键
            keyboard.add_hotkey(self.hotkey, self._on_hotkey_pressed)
            self._is_running = True
            print(f"快捷键监听器已启动: {self.hotkey}")
            
        except Exception as e:
            error_msg = f"快捷键注册失败: {e}"
            print(error_msg)
            # 尝试使用默认快捷键
            if self.hotkey != "ctrl+shift+t":
                print("尝试使用默认快捷键: ctrl+shift+t")
                self.hotkey = "ctrl+shift+t"
                try:
                    keyboard.add_hotkey(self.hotkey, self._on_hotkey_pressed)
                    self._is_running = True
                    print(f"使用默认快捷键成功: {self.hotkey}")
                except Exception as fallback_error:
                    raise Exception(f"快捷键注册失败，包括默认快捷键: {fallback_error}")
            else:
                raise Exception(error_msg)
    
    def stop(self) -> None:
        """停止快捷键监听"""
        if not self._is_running:
            return
        
        try:
            keyboard.remove_hotkey(self.hotkey)
            self._is_running = False
            print(f"快捷键监听器已停止: {self.hotkey}")
        except Exception as e:
            print(f"停止快捷键监听时出错: {e}")
    
    def _validate_hotkey(self, hotkey: str) -> bool:
        """验证快捷键格式是否有效
        
        Args:
            hotkey: 快捷键字符串
            
        Returns:
            bool: 格式是否有效
        """
        if not hotkey or not isinstance(hotkey, str):
            return False
        
        # 基本格式检查：至少包含一个字符
        if len(hotkey.strip()) == 0:
            return False
        
        # 检查是否包含有效的按键组合
        # keyboard库支持的格式如: "ctrl+shift+t", "alt+f4" 等
        parts = hotkey.lower().split('+')
        if len(parts) == 0:
            return False
        
        # 常见的修饰键
        valid_modifiers = {'ctrl', 'shift', 'alt', 'win', 'cmd', 'control'}
        
        # 至少应该有一个按键
        return True
    
    def _on_hotkey_pressed(self) -> None:
        """快捷键按下时的内部处理函数"""
        try:
            # 在新线程中执行回调，避免阻塞快捷键监听
            if self.callback:
                # 使用线程执行回调，确保不阻塞keyboard库的事件循环
                callback_thread = threading.Thread(target=self.callback, daemon=True)
                callback_thread.start()
        except Exception as e:
            print(f"快捷键回调执行失败: {e}")


class Application:
    """主应用程序类，管理应用程序生命周期和所有组件"""
    
    def __init__(self):
        """初始化应用程序"""
        # 初始化Tkinter主窗口（隐藏）
        self.root = None
        self.config_manager = None
        self.hotkey_listener = None
        self.system_tray = None
        self.input_window = None
        self.floating_windows = []  # 悬浮窗口列表
        
        # 窗口位置偏移量（用于多窗口布局）
        self.window_offset = 0
        self.window_offset_step = 60  # 每个新窗口向下偏移的像素
    
    def run(self) -> None:
        """运行应用程序"""
        try:
            # 创建隐藏的Tkinter主窗口
            import tkinter as tk
            self.root = tk.Tk()
            self.root.withdraw()  # 隐藏主窗口
            print("✓ Tkinter主窗口已创建")
            
            # 初始化配置管理器并加载配置
            from config import ConfigManager
            self.config_manager = ConfigManager()
            print("✓ 配置已加载")
            
            # 获取快捷键配置
            hotkey = self.config_manager.get('hotkey', 'ctrl+shift+t')
            
            # 初始化快捷键监听器
            self.hotkey_listener = HotkeyListener(hotkey, self.show_input_window)
            self.hotkey_listener.start()
            print("✓ 快捷键监听器已启动")
            
            # 初始化系统托盘
            from tray import SystemTray
            self.system_tray = SystemTray(self.quit)
            self.system_tray.start()
            print("✓ 系统托盘已启动")
            
            print("\n" + "=" * 50)
            print(f"应用程序已就绪！")
            print(f"快捷键: {hotkey}")
            print("使用说明:")
            print(f"  - 按 {hotkey} 打开输入窗口")
            print("  - 右键点击托盘图标退出应用")
            print("=" * 50 + "\n")
            
            # 启动Tkinter主循环
            self.root.mainloop()
            
        except Exception as e:
            print(f"应用程序启动失败: {e}")
            import traceback
            traceback.print_exc()
            self.quit()
            raise
    
    def show_input_window(self) -> None:
        """显示输入窗口"""
        try:
            # 确保在主线程中执行UI操作
            if self.root:
                self.root.after(0, self._show_input_window_impl)
        except Exception as e:
            print(f"显示输入窗口失败: {e}")
    
    def _show_input_window_impl(self) -> None:
        """显示输入窗口的实际实现（在主线程中执行）"""
        try:
            from windows import InputWindow
            if self.input_window is None:
                self.input_window = InputWindow(self.root, self.create_floating_window)
            self.input_window.show()
        except Exception as e:
            print(f"创建输入窗口失败: {e}")
    
    def create_floating_window(self, text: str) -> None:
        """创建新的悬浮窗口并计算位置
        
        Args:
            text: 要显示的文本内容
        """
        try:
            from windows import FloatingWindow
            
            # 获取窗口透明度配置
            opacity = self.config_manager.get('window_opacity', 0.9)
            
            # 创建悬浮窗口
            floating_window = FloatingWindow(
                self.root,
                text,
                self.remove_floating_window,
                opacity
            )
            
            # 计算窗口位置
            x, y = self._calculate_window_position()
            
            # 显示窗口
            floating_window.show(x, y)
            
            # 添加到窗口列表
            self.floating_windows.append(floating_window)
            
            print(f"创建悬浮窗口: {text[:20]}...")
            
        except Exception as e:
            print(f"创建悬浮窗口失败: {e}")
    
    def _calculate_window_position(self) -> tuple:
        """计算悬浮窗口的默认位置（屏幕右上角，多窗口向下偏移）
        
        Returns:
            (x, y) 坐标元组
        """
        # 获取屏幕尺寸
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        # 默认窗口尺寸估算
        window_width = 250
        window_height = 100
        
        # 计算右上角位置（留出一些边距）
        margin = 20
        x = screen_width - window_width - margin
        y = margin + self.window_offset
        
        # 更新偏移量，为下一个窗口做准备
        self.window_offset += self.window_offset_step
        
        # 如果偏移量太大，重置（避免窗口超出屏幕）
        if y + window_height > screen_height - margin:
            self.window_offset = 0
            y = margin
        
        return (x, y)
    
    def remove_floating_window(self, window) -> None:
        """从列表中移除悬浮窗口
        
        Args:
            window: 要移除的FloatingWindow对象
        """
        try:
            if window in self.floating_windows:
                self.floating_windows.remove(window)
                print(f"移除悬浮窗口，剩余窗口数: {len(self.floating_windows)}")
        except Exception as e:
            print(f"移除悬浮窗口失败: {e}")
    
    def quit(self) -> None:
        """清理资源并退出应用程序"""
        print("正在退出应用程序...")
        
        try:
            # 停止快捷键监听
            if self.hotkey_listener:
                self.hotkey_listener.stop()
            
            # 停止系统托盘
            if self.system_tray:
                self.system_tray.stop()
            
            # 关闭所有悬浮窗口
            for window in self.floating_windows[:]:  # 使用副本避免迭代时修改列表
                try:
                    window.close()
                except:
                    pass
            
            # 关闭输入窗口
            if self.input_window:
                try:
                    self.input_window.hide()
                except:
                    pass
            
            # 退出Tkinter主循环
            if self.root:
                self.root.quit()
                self.root.destroy()
            
            print("应用程序已退出")
            
        except Exception as e:
            print(f"退出时出错: {e}")


if __name__ == "__main__":
    import time
    import sys
    
    print("=" * 50)
    print("悬浮文本显示应用程序")
    print("=" * 50)
    print("正在启动...")
    
    start_time = time.time()
    
    try:
        # 创建并运行应用程序
        app = Application()
        
        # 计算初始化时间
        init_time = time.time() - start_time
        print(f"初始化完成，耗时: {init_time:.2f} 秒")
        
        # 检查是否在3秒内完成初始化（需求5.5）
        if init_time > 3.0:
            print(f"警告: 初始化时间超过3秒 ({init_time:.2f}秒)")
        
        # 运行应用程序
        app.run()
        
    except KeyboardInterrupt:
        print("\n收到中断信号，正在退出...")
        sys.exit(0)
    except Exception as e:
        print(f"\n应用程序发生错误: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
