# 设计文档

## 概述

本应用程序是一个基于 Python 和 Tkinter 的轻量级桌面工具，用于快速创建和管理置顶文本显示窗口。选择 Python + Tkinter 的原因是：
- Tkinter 是 Python 标准库，无需额外安装
- 跨平台支持（Windows/macOS/Linux）
- 轻量级，启动快速
- 原生支持置顶窗口和透明度
- 适合快速开发和部署

## 架构

### 系统架构图

```
┌─────────────────────────────────────┐
│         主应用程序 (App)              │
│  - 初始化系统托盘                     │
│  - 管理全局快捷键监听                 │
│  - 协调各组件                        │
└──────────┬──────────────────────────┘
           │
           ├──────────────┬──────────────┬─────────────┐
           │              │              │             │
    ┌──────▼─────┐ ┌─────▼──────┐ ┌────▼─────┐ ┌────▼──────┐
    │ 快捷键监听器 │ │ 输入窗口    │ │ 悬浮窗口  │ │ 配置管理器 │
    │ (Hotkey)   │ │ (Input)    │ │ (Float)  │ │ (Config)  │
    └────────────┘ └────────────┘ └──────────┘ └───────────┘
```

### 组件职责

1. **主应用程序 (Application)**: 应用程序入口，管理生命周期
2. **快捷键监听器 (HotkeyListener)**: 监听全局快捷键并触发回调
3. **输入窗口 (InputWindow)**: 接收用户文本输入
4. **悬浮窗口 (FloatingWindow)**: 显示置顶文本
5. **配置管理器 (ConfigManager)**: 读取和保存配置
6. **系统托盘 (SystemTray)**: 提供托盘图标和菜单

## 组件和接口

### 1. Application (主应用类)

**职责**: 
- 初始化所有组件
- 管理应用程序生命周期
- 维护悬浮窗口列表

**接口**:
```python
class Application:
    def __init__(self)
    def run(self) -> None
    def show_input_window(self) -> None
    def create_floating_window(self, text: str) -> None
    def remove_floating_window(self, window: FloatingWindow) -> None
    def quit(self) -> None
```

### 2. HotkeyListener (快捷键监听器)

**职责**:
- 注册全局快捷键
- 监听快捷键事件
- 触发回调函数

**依赖**: `keyboard` 库（用于全局快捷键监听）

**接口**:
```python
class HotkeyListener:
    def __init__(self, hotkey: str, callback: Callable)
    def start(self) -> None
    def stop(self) -> None
```

### 3. InputWindow (输入窗口)

**职责**:
- 显示文本输入界面
- 处理用户输入
- 将输入传递给主应用

**特性**:
- 居中显示
- 自动获取焦点
- 支持 Enter 确认，Escape 取消

**接口**:
```python
class InputWindow:
    def __init__(self, parent: tk.Tk, on_submit: Callable[[str], None])
    def show(self) -> None
    def hide(self) -> None
```

### 4. FloatingWindow (悬浮窗口)

**职责**:
- 显示置顶文本
- 支持拖动
- 提供删除功能

**特性**:
- 置顶显示 (topmost)
- 半透明背景 (alpha=0.9)
- 可拖动
- 删除按钮

**接口**:
```python
class FloatingWindow:
    def __init__(self, text: str, on_close: Callable)
    def show(self) -> None
    def close(self) -> None
    def _start_drag(self, event) -> None
    def _on_drag(self, event) -> None
```

### 5. ConfigManager (配置管理器)

**职责**:
- 读取配置文件
- 保存配置
- 提供默认配置

**配置项**:
- `hotkey`: 全局快捷键（默认: "ctrl+shift+t"）
- `window_opacity`: 悬浮窗口透明度（默认: 0.9）
- `default_position`: 悬浮窗口默认位置（默认: 屏幕中央偏右）

**接口**:
```python
class ConfigManager:
    def __init__(self, config_path: str = "config.json")
    def load(self) -> dict
    def save(self, config: dict) -> None
    def get(self, key: str, default: Any = None) -> Any
```

### 6. SystemTray (系统托盘)

**职责**:
- 显示托盘图标
- 提供右键菜单
- 处理退出操作

**依赖**: `pystray` 库

**接口**:
```python
class SystemTray:
    def __init__(self, on_quit: Callable)
    def start(self) -> None
    def stop(self) -> None
```

## 数据模型

### 配置文件结构 (config.json)

```json
{
  "hotkey": "ctrl+shift+t",
  "window_opacity": 0.9,
  "default_position": {
    "x": 100,
    "y": 100
  },
  "font": {
    "family": "Arial",
    "size": 12
  }
}
```

### 窗口状态

每个悬浮窗口维护以下状态：
- `text`: 显示的文本内容
- `position`: 当前窗口位置 (x, y)
- `tk_window`: Tkinter 窗口对象引用

## 错误处理

### 1. 快捷键冲突
- **场景**: 配置的快捷键已被其他应用占用
- **处理**: 捕获异常，显示错误消息，使用默认快捷键

### 2. 配置文件错误
- **场景**: 配置文件格式错误或不存在
- **处理**: 使用默认配置，创建新的配置文件

### 3. 窗口创建失败
- **场景**: 系统资源不足或权限问题
- **处理**: 记录错误日志，向用户显示通知

### 4. 全局快捷键监听失败
- **场景**: 缺少必要权限或库未安装
- **处理**: 显示错误消息，提供手动触发选项（托盘菜单）

## 测试策略

### 单元测试
- ConfigManager 的配置读写功能
- 窗口位置计算逻辑
- 配置验证逻辑

### 集成测试
- 快捷键触发 → 输入窗口显示
- 输入确认 → 悬浮窗口创建
- 删除按钮 → 窗口关闭

### 手动测试
- 多窗口管理（创建、拖动、删除多个悬浮窗口）
- 快捷键在不同应用中的响应
- 系统托盘交互
- 配置文件修改后的行为

## 技术实现细节

### 全局快捷键实现
使用 `keyboard` 库的 `add_hotkey()` 方法注册全局快捷键。需要管理员权限（Windows）。

### 窗口置顶实现
使用 Tkinter 的 `attributes('-topmost', True)` 方法。

### 窗口透明度实现
使用 Tkinter 的 `attributes('-alpha', 0.9)` 方法。

### 窗口拖动实现
通过绑定鼠标事件实现：
1. 记录鼠标按下时的位置
2. 在拖动过程中计算偏移量
3. 更新窗口位置

### 系统托盘实现
使用 `pystray` 库创建托盘图标和菜单。

## 部署说明

### 依赖项
```
keyboard==0.13.5
pystray==0.19.4
Pillow==10.0.0
```

### 运行方式
```bash
python main.py
```

### 打包为可执行文件（可选）
使用 PyInstaller:
```bash
pyinstaller --onefile --windowed --icon=icon.ico main.py
```

## 用户界面设计

### 输入窗口
- 尺寸: 400x100 像素
- 位置: 屏幕中央
- 组件: 单行文本输入框 + 提示文字

### 悬浮窗口
- 尺寸: 根据文本内容自动调整（最小 200x50）
- 位置: 首次创建在屏幕右上角，后续窗口向下偏移
- 组件: 文本标签 + 删除按钮（右上角 X）
- 样式: 圆角边框，半透明背景，阴影效果

### 系统托盘
- 图标: 简单的文本图标（T）
- 菜单: "退出"选项
