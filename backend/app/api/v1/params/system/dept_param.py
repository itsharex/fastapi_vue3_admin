# -*- coding: utf-8 -*-

from typing import Optional
from fastapi import Query
from datetime import datetime

from app.core.validator import DateTimeStr

class DeptQueryParams:
    """部门管理查询参数"""

    def __init__(
            self,
            name: Optional[str] = Query(None, description="部门名称", min_length=2, max_length=50),
            available: Optional[bool] = Query(None, description="部门状态(True正常 False停用)"),
            
    ) -> None:
        super().__init__()
        
        # 模糊查询字段
        self.name = ("like", name)

        # 精确查询字段
        self.available = available

