"""窗口组件模块"""
import tkinter as tk
from tkinter import ttk
from typing import Callable


class InputWindow:
    """输入窗口类，用于接收用户文本输入"""
    
    def __init__(self, parent: tk.Tk, on_submit: Callable[[str], None]):
        """初始化输入窗口
        
        Args:
            parent: 父窗口（Tkinter主窗口）
            on_submit: 提交回调函数，接收输入的文本
        """
        self.parent = parent
        self.on_submit = on_submit
        self.window = None
        self.entry = None
    
    def show(self) -> None:
        """显示输入窗口"""
        if self.window is not None:
            self.window.lift()
            self.entry.focus_set()
            return
        
        # 创建Toplevel窗口
        self.window = tk.Toplevel(self.parent)
        self.window.title("")
        
        # 移除窗口装饰，使用自定义设计
        self.window.overrideredirect(True)
        
        # 设置窗口置顶
        self.window.attributes('-topmost', True)
        
        # 设置窗口背景色（深色主题）
        bg_color = '#2c3e50'
        self.window.configure(bg=bg_color)
        
        # 创建主容器框架（带圆角效果的视觉）
        main_frame = tk.Frame(
            self.window,
            bg=bg_color,
            relief=tk.FLAT,
            borderwidth=0
        )
        main_frame.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)
        
        # 创建标题栏
        title_bar = tk.Frame(main_frame, bg='#34495e', height=35)
        title_bar.pack(fill=tk.X)
        title_bar.pack_propagate(False)
        
        # 标题文字
        title_label = tk.Label(
            title_bar,
            text="✨ 输入文本",
            font=("Microsoft YaHei UI", 11, "bold"),
            bg='#34495e',
            fg='#ecf0f1'
        )
        title_label.pack(side=tk.LEFT, padx=15, pady=8)
        
        # 关闭按钮
        close_btn = tk.Label(
            title_bar,
            text="✕",
            font=("Arial", 12, "bold"),
            bg='#34495e',
            fg='#95a5a6',
            cursor='hand2',
            padx=10
        )
        close_btn.pack(side=tk.RIGHT, padx=5)
        close_btn.bind('<Button-1>', self._on_cancel)
        close_btn.bind('<Enter>', lambda e: close_btn.config(fg='#e74c3c', bg='#2c3e50'))
        close_btn.bind('<Leave>', lambda e: close_btn.config(fg='#95a5a6', bg='#34495e'))
        
        # 内容区域
        content_frame = tk.Frame(main_frame, bg=bg_color)
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # 创建提示标签（现代化设计）
        label = tk.Label(
            content_frame,
            text="请输入要显示的文本内容",
            font=("Microsoft YaHei UI", 10),
            bg=bg_color,
            fg='#bdc3c7'
        )
        label.pack(anchor=tk.W, pady=(0, 10))
        
        # 创建输入框容器（带边框效果）
        entry_frame = tk.Frame(
            content_frame,
            bg='#34495e',
            relief=tk.FLAT,
            borderwidth=1
        )
        entry_frame.pack(fill=tk.X, pady=(0, 15))
        
        # 创建文本输入框（现代化样式）
        self.entry = tk.Entry(
            entry_frame,
            font=("Microsoft YaHei UI", 12),
            bg='#34495e',
            fg='#ecf0f1',
            insertbackground='#3498db',  # 光标颜色
            relief=tk.FLAT,
            borderwidth=0
        )
        self.entry.pack(fill=tk.X, padx=2, pady=2, ipady=8)
        
        # 提示信息
        hint_label = tk.Label(
            content_frame,
            text="按 Enter 确认 | 按 Esc 取消",
            font=("Microsoft YaHei UI", 9),
            bg=bg_color,
            fg='#7f8c8d'
        )
        hint_label.pack(anchor=tk.W)
        
        # 绑定Enter键提交
        self.entry.bind('<Return>', self._on_submit)
        
        # 绑定Escape键取消
        self.entry.bind('<Escape>', self._on_cancel)
        
        # 绑定窗口关闭事件
        self.window.protocol("WM_DELETE_WINDOW", self._on_cancel)
        
        # 设置窗口大小
        self.window.geometry("450x180")
        
        # 居中显示窗口
        self._center_window()
        
        # 自动获取焦点
        self.entry.focus_set()
    
    def hide(self) -> None:
        """隐藏并销毁输入窗口"""
        if self.window is not None:
            self.window.destroy()
            self.window = None
            self.entry = None
    
    def _center_window(self) -> None:
        """将窗口居中显示在屏幕上"""
        self.window.update_idletasks()
        
        # 获取窗口尺寸
        window_width = self.window.winfo_width()
        window_height = self.window.winfo_height()
        
        # 获取屏幕尺寸
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        
        # 计算居中位置
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        
        # 设置窗口位置
        self.window.geometry(f"{window_width}x{window_height}+{x}+{y}")
    
    def _on_submit(self, event=None) -> None:
        """处理提交事件（Enter键）
        
        Args:
            event: 事件对象
        """
        text = self.entry.get().strip()
        if text:  # 只有在有文本时才提交
            self.on_submit(text)
            self.hide()
    
    def _on_cancel(self, event=None) -> None:
        """处理取消事件（Escape键或关闭窗口）
        
        Args:
            event: 事件对象
        """
        self.hide()


class FloatingWindow:
    """悬浮窗口类，用于显示置顶文本"""
    
    def __init__(self, parent: tk.Tk, text: str, on_close: Callable, opacity: float = 0.9):
        """初始化悬浮窗口
        
        Args:
            parent: 父窗口（Tkinter主窗口）
            text: 要显示的文本内容
            on_close: 关闭回调函数
            opacity: 窗口透明度（0.0-1.0）
        """
        self.parent = parent
        self.text = text
        self.on_close = on_close
        self.opacity = opacity
        self.window = None
        self.text_widget = None
        self._drag_start_x = 0
        self._drag_start_y = 0
        self._resize_start_x = 0
        self._resize_start_y = 0
        self._resize_start_width = 0
        self._resize_start_height = 0
        self._is_editing = False
        self._base_font_size = 16
        self._click_count = 0
        self._last_click_time = 0
        
        # 创建窗口
        self._create_window()
    
    def _create_window(self) -> None:
        """创建悬浮窗口"""
        # 创建Toplevel窗口
        self.window = tk.Toplevel(self.parent)
        self.window.title("")
        
        # 设置窗口置顶
        self.window.attributes('-topmost', True)
        
        # 移除窗口标题栏
        self.window.overrideredirect(True)
        
        # 设置透明色键（使背景完全透明）
        transparent_color = '#000001'
        self.window.attributes('-transparentcolor', transparent_color)
        self.window.configure(bg=transparent_color)
        
        # 创建主容器框架（透明背景）
        main_frame = tk.Frame(
            self.window,
            bg=transparent_color
        )
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 创建可编辑的文本框（初始为只读）
        self.text_widget = tk.Text(
            main_frame,
            font=("Microsoft YaHei UI", self._base_font_size, "bold"),
            bg=transparent_color,
            fg='#ffffff',
            insertbackground='#3498db',
            relief=tk.FLAT,
            borderwidth=0,
            wrap=tk.WORD,
            padx=15,
            pady=10
        )
        # 先插入文本
        self.text_widget.insert('1.0', self.text)
        # 然后设置为只读
        self.text_widget.config(state='disabled')
        self.text_widget.pack(fill=tk.BOTH, expand=True)
        
        # 绑定文本区域的鼠标事件
        # 左键：单击移动，连续三击进入编辑模式
        self.text_widget.bind('<Button-1>', self._on_left_click)
        self.text_widget.bind('<B1-Motion>', self._on_left_drag)
        self.text_widget.bind('<ButtonRelease-1>', self._on_left_release)
        
        # 右键：单击删除，长按缩放
        self.text_widget.bind('<Button-3>', self._on_right_click)
        self.text_widget.bind('<B3-Motion>', self._on_right_drag)
        self.text_widget.bind('<ButtonRelease-3>', self._on_right_release)
        
        # 更新窗口以获取正确的尺寸
        self.window.update_idletasks()
        
        # 设置初始窗口大小（更大的默认尺寸）
        self.window.geometry("500x200")
    
    def _on_left_click(self, event) -> None:
        """处理左键点击事件 - 检测三连击进入编辑模式"""
        import time
        current_time = time.time()
        
        # 检测连续点击（500ms内）
        if current_time - self._last_click_time < 0.5:
            self._click_count += 1
        else:
            self._click_count = 1
        
        self._last_click_time = current_time
        
        # 三连击进入编辑模式
        if self._click_count >= 3:
            self._enter_edit_mode()
            self._click_count = 0
        elif not self._is_editing:
            # 非编辑模式下，准备移动
            self._drag_start_x = event.x_root
            self._drag_start_y = event.y_root
    
    def _on_left_drag(self, event) -> None:
        """处理左键拖动事件（移动窗口）"""
        if not self._is_editing:
            delta_x = event.x_root - self._drag_start_x
            delta_y = event.y_root - self._drag_start_y
            
            # 只有移动距离超过5像素才认为是拖动
            if abs(delta_x) > 5 or abs(delta_y) > 5:
                self._click_count = 0  # 拖动时重置点击计数
                
                current_x = self.window.winfo_x()
                current_y = self.window.winfo_y()
                
                new_x = current_x + delta_x
                new_y = current_y + delta_y
                
                self.window.geometry(f"+{new_x}+{new_y}")
                
                self._drag_start_x = event.x_root
                self._drag_start_y = event.y_root
                
                self.window.attributes('-topmost', True)
                self.text_widget.config(cursor='fleur')
    
    def _on_left_release(self, event) -> None:
        """处理左键释放事件"""
        if not self._is_editing:
            self.text_widget.config(cursor='')
    
    def _on_right_click(self, event) -> None:
        """处理右键点击事件 - 单击删除"""
        if not self._is_editing:
            # 记录右键按下的位置
            self._resize_start_x = event.x_root
            self._resize_start_y = event.y_root
            self._resize_start_width = self.window.winfo_width()
            self._resize_start_height = self.window.winfo_height()
    
    def _on_right_drag(self, event) -> None:
        """处理右键拖动事件（缩放窗口）"""
        if not self._is_editing:
            delta_x = event.x_root - self._resize_start_x
            delta_y = event.y_root - self._resize_start_y
            
            # 只有移动距离超过5像素才认为是缩放
            if abs(delta_x) > 5 or abs(delta_y) > 5:
                new_width = max(self._resize_start_width + delta_x, 200)
                new_height = max(self._resize_start_height + delta_y, 100)
                
                current_x = self.window.winfo_x()
                current_y = self.window.winfo_y()
                self.window.geometry(f"{new_width}x{new_height}+{current_x}+{current_y}")
                
                self._update_font_size()
                self.window.attributes('-topmost', True)
                self.text_widget.config(cursor='sizing')
    
    def _on_right_release(self, event) -> None:
        """处理右键释放事件 - 如果没有拖动则删除"""
        if not self._is_editing:
            delta_x = event.x_root - self._resize_start_x
            delta_y = event.y_root - self._resize_start_y
            
            # 如果移动距离小于5像素，认为是单击，执行删除
            if abs(delta_x) <= 5 and abs(delta_y) <= 5:
                self._confirm_delete()
            
            self.text_widget.config(cursor='')
    
    def _enter_edit_mode(self) -> None:
        """进入编辑模式"""
        self._is_editing = True
        self.text_widget.config(state='normal', cursor='xterm')
        self.text_widget.focus_set()
        # 选中所有文本
        self.text_widget.tag_add('sel', '1.0', 'end')
        
        # 绑定Escape键和Enter键退出编辑模式
        self.text_widget.bind('<Escape>', lambda e: self._exit_edit_mode())
        self.text_widget.bind('<Return>', lambda e: self._exit_edit_mode())
    
    def _exit_edit_mode(self) -> None:
        """退出编辑模式"""
        self._is_editing = False
        self.text_widget.config(state='disabled', cursor='')
        self.text_widget.unbind('<Escape>')
        self.text_widget.unbind('<Return>')
    
    def _confirm_delete(self) -> None:
        """确认删除窗口"""
        # 创建确认对话框
        confirm_window = tk.Toplevel(self.window)
        confirm_window.title("确认删除")
        confirm_window.geometry("250x100")
        confirm_window.attributes('-topmost', True)
        confirm_window.overrideredirect(True)
        
        # 居中显示
        x = self.window.winfo_x() + (self.window.winfo_width() - 250) // 2
        y = self.window.winfo_y() + (self.window.winfo_height() - 100) // 2
        confirm_window.geometry(f"250x100+{x}+{y}")
        
        # 设置背景
        confirm_window.configure(bg='#2c3e50')
        
        # 提示文字
        label = tk.Label(
            confirm_window,
            text="确定要删除这个窗口吗？",
            font=("Microsoft YaHei UI", 11),
            bg='#2c3e50',
            fg='#ecf0f1'
        )
        label.pack(pady=15)
        
        # 按钮容器
        button_frame = tk.Frame(confirm_window, bg='#2c3e50')
        button_frame.pack(pady=10)
        
        # 确认按钮
        yes_btn = tk.Label(
            button_frame,
            text="确定",
            font=("Microsoft YaHei UI", 10, "bold"),
            bg='#e74c3c',
            fg='white',
            padx=20,
            pady=5,
            cursor='hand2'
        )
        yes_btn.pack(side=tk.LEFT, padx=10)
        yes_btn.bind('<Button-1>', lambda e: [confirm_window.destroy(), self.close()])
        yes_btn.bind('<Enter>', lambda e: yes_btn.config(bg='#c0392b'))
        yes_btn.bind('<Leave>', lambda e: yes_btn.config(bg='#e74c3c'))
        
        # 取消按钮
        no_btn = tk.Label(
            button_frame,
            text="取消",
            font=("Microsoft YaHei UI", 10, "bold"),
            bg='#95a5a6',
            fg='white',
            padx=20,
            pady=5,
            cursor='hand2'
        )
        no_btn.pack(side=tk.LEFT, padx=10)
        no_btn.bind('<Button-1>', lambda e: confirm_window.destroy())
        no_btn.bind('<Enter>', lambda e: no_btn.config(bg='#7f8c8d'))
        no_btn.bind('<Leave>', lambda e: no_btn.config(bg='#95a5a6'))
    
    def _update_font_size(self) -> None:
        """根据窗口大小更新字体大小"""
        window_width = self.window.winfo_width()
        window_height = self.window.winfo_height()
        
        # 根据窗口面积计算字体大小
        area = window_width * window_height
        base_area = 500 * 200  # 初始窗口面积
        
        # 字体大小随面积变化，但有上下限
        font_size = int(self._base_font_size * (area / base_area) ** 0.3)
        font_size = max(10, min(font_size, 32))  # 限制在10-32之间
        
        # 更新字体
        current_font = self.text_widget.cget("font")
        if isinstance(current_font, str):
            self.text_widget.config(font=("Microsoft YaHei UI", font_size, "bold"))
        else:
            self.text_widget.config(font=("Microsoft YaHei UI", font_size, "bold"))
    

    
    def show(self, x: int = None, y: int = None) -> None:
        """显示悬浮窗口
        
        Args:
            x: 窗口X坐标（可选）
            y: 窗口Y坐标（可选）
        """
        if x is not None and y is not None:
            self.window.geometry(f"+{x}+{y}")
        
        self.window.deiconify()
    
    def close(self) -> None:
        """关闭悬浮窗口"""
        if self.window is not None:
            self.window.destroy()
            self.window = None
            # 调用关闭回调
            if self.on_close:
                self.on_close(self)
