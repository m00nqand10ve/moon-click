"""配置管理模块"""
import json
import os
from typing import Any, Dict


class ConfigManager:
    """配置管理器类，负责读取和保存配置文件"""
    
    DEFAULT_CONFIG = {
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
    
    def __init__(self, config_path: str = "config.json"):
        """初始化配置管理器
        
        Args:
            config_path: 配置文件路径
        """
        self.config_path = config_path
        self.config = self._load_or_create_config()
    
    def _load_or_create_config(self) -> Dict[str, Any]:
        """加载配置文件，如果不存在则创建默认配置
        
        Returns:
            配置字典
        """
        if os.path.exists(self.config_path):
            try:
                return self.load()
            except (json.JSONDecodeError, IOError) as e:
                print(f"配置文件加载失败: {e}，使用默认配置")
                return self.DEFAULT_CONFIG.copy()
        else:
            # 创建默认配置文件
            self.save(self.DEFAULT_CONFIG)
            return self.DEFAULT_CONFIG.copy()
    
    def load(self) -> Dict[str, Any]:
        """从文件加载配置
        
        Returns:
            配置字典
        """
        with open(self.config_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def save(self, config: Dict[str, Any]) -> None:
        """保存配置到文件
        
        Args:
            config: 要保存的配置字典
        """
        with open(self.config_path, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        self.config = config
    
    def get(self, key: str, default: Any = None) -> Any:
        """获取配置项
        
        Args:
            key: 配置键，支持点号分隔的嵌套键（如 "font.size"）
            default: 默认值
            
        Returns:
            配置值
        """
        keys = key.split('.')
        value = self.config
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        
        return value
