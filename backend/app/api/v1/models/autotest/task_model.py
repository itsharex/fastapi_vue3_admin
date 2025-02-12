# -*- coding: utf-8 -*-

from datetime import datetime
from sqlalchemy import JSON, Column, String, Integer, DateTime, ForeignKey, Text, Table
from sqlalchemy.orm import relationship

from app.core.base_model import ModelBase


class TaskModel(ModelBase):
    """
    自动化测试任务表
    """
    __tablename__ = "auto_tasks"
    __table_args__ = ({'comment': '自动化测试任务表'})

    # 基础字段
    id = Column(Integer, primary_key=True, autoincrement=True, index=True, unique=True, comment='主键ID')
    name = Column(String, nullable=False, comment="任务名称")  # 新增
    status = Column(String, nullable=False, default="pending", comment="执行状态(pending/running/completed/failed)")
    
    start_time = Column(DateTime, comment="开始时间")  # 新增
    end_time = Column(DateTime, comment="结束时间")    # 新增
    
    summary = Column(JSON, comment="报告摘要")

    total_count = Column(Integer, default=0, comment="用例总数")  # 新增
    success_count = Column(Integer, default=0, comment="成功数")  # 新增
    fail_count = Column(Integer, default=0, comment="失败数")    # 新增
    skip_count = Column(Integer, default=0, comment="跳过数")
    error_count = Column(Integer, default=0, comment="错误数")   # 新增
    
    logs = Column(JSON, comment="执行日志")
    actual_response = Column(JSON, comment="实际响应（仅API测试）")
    
    # 关联关系
    project_id = Column(Integer, ForeignKey("auto_projects.id", ondelete="CASCADE"), nullable=False, comment="所属项目ID")
    project = relationship("ProjectModel", foreign_keys=project_id, lazy="joined", uselist=False)

    # 审计字段
    description = Column(Text, nullable=True, comment="备注说明")
    created_at = Column(DateTime, default=datetime.now, comment='创建时间')
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, comment='更新时间')
    creator_id = Column(
        Integer, 
        ForeignKey("system_user.id", ondelete="SET NULL", onupdate="CASCADE"), 
        nullable=True, 
        index=True, 
        comment="创建人ID"
    )
    creator = relationship(
        "UserModel", 
        foreign_keys=creator_id, 
        lazy="joined",
        post_update=True,
        uselist=False
    )

