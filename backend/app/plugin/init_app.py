# -*- coding: utf-8 -*-

from typing import Any, AsyncGenerator
from starlette.staticfiles import StaticFiles
from fastapi import FastAPI
from fastapi.concurrency import asynccontextmanager
from fastapi.openapi.docs import (
    get_redoc_html,
    get_swagger_ui_html,
    get_swagger_ui_oauth2_redirect_html
)

from app.config.setting import settings
from app.api.v1.urls.system_url import SystemApiRouter
from app.api.v1.urls.common_url import CommonApiRouter
from app.api.v1.urls.monitor_url import MonitorApiRouter
from app.core.logger import logger
from app.utils.common_util import import_module, import_modules_async
from app.core.exceptions import (
    CustomException,
    CustomExceptionHandler,
    HTTPException,
    HttpExceptionHandler,
    ValidationExceptionHandler,
    RequestValidationError,
    SQLAlchemyError,
    SQLAlchemyExceptionHandler,
    ValueExceptionHandler,
    FieldValidationError,
    FieldValidationExceptionHandler,
    AllExceptionHandler,
    ResponseValidationHandle,
    ResponseValidationError
)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[Any, Any]:
    """
    自定义生命周期
    """
    logger.info(settings.BANNER + '\n' + f'{settings.TITLE} 服务开始启动...')
    await import_modules_async(modules=settings.get_events, desc="全局事件", app=app, status=True)
    logger.info(f'{settings.TITLE} 服务成功启动...')

    yield

    await import_modules_async(modules=settings.get_events, desc="全局事件", app=app, status=False)
    logger.info(f'{settings.TITLE} 服务关闭...')

def register_middlewares(app: FastAPI) -> None:
    """
    注册中间件
    """
    for middleware in settings.get_middlewares[::-1]:
        if not middleware:
            continue
        middleware = import_module(middleware, desc="中间件")
        app.add_middleware(middleware)

def register_exceptions(app: FastAPI) -> None:
    """
    异常捕捉
    """
    app.add_exception_handler(CustomException, CustomExceptionHandler)
    app.add_exception_handler(HTTPException, HttpExceptionHandler)
    app.add_exception_handler(RequestValidationError,ValidationExceptionHandler)
    app.add_exception_handler(SQLAlchemyError, SQLAlchemyExceptionHandler)
    app.add_exception_handler(ValueError, ValueExceptionHandler)
    app.add_exception_handler(Exception, AllExceptionHandler)
    app.add_exception_handler(FieldValidationError,FieldValidationExceptionHandler)
    app.add_exception_handler(ResponseValidationError,ResponseValidationHandle)

def register_routers(app: FastAPI) -> None:
    """
    注册根路由
    """
    app.include_router(router=SystemApiRouter)
    app.include_router(router=MonitorApiRouter)
    app.include_router(router=CommonApiRouter)

def register_files(app: FastAPI) -> None:
    """
    注册文件相关配置
    """
    # 挂载静态文件目录
    if settings.STATIC_ENABLE:
        # 确保日志目录存在
        settings.STATIC_ROOT.mkdir(parents=True, exist_ok=True)
        app.mount(path=settings.STATIC_URL, app=StaticFiles(directory=settings.STATIC_ROOT), name=settings.STATIC_DIR)
    # 挂载模版文件目录
    if settings.PROFILES_ENABLE:
        # 确保日志目录存在
        settings.PROFILES_ROOT.mkdir(parents=True, exist_ok=True)
        app.mount(path=settings.PROFILES_URL, app=StaticFiles(directory=settings.PROFILES_ROOT), name=settings.PROFILES_DIR)

def reset_api_docs(app: FastAPI) -> None:
    """
    自定义配置接口本地静态文档
    """

    @app.get(settings.DOCS_URL, include_in_schema=False)
    async def custom_swagger_ui_html():
        return get_swagger_ui_html(
            openapi_url=app.root_path + app.openapi_url,
            title=app.title + " - Swagger UI",
            oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
            swagger_js_url=settings.SWAGGER_JS_URL,
            swagger_css_url=settings.SWAGGER_CSS_URL,
            swagger_favicon_url=settings.FAVICON_URL,
        )

    @app.get(app.swagger_ui_oauth2_redirect_url, include_in_schema=False)
    async def swagger_ui_redirect():
        return get_swagger_ui_oauth2_redirect_html()

    @app.get(settings.REDOC_URL, include_in_schema=False)
    async def custom_redoc_html():
        return get_redoc_html(
            openapi_url=app.root_path + app.openapi_url,
            title=app.title + " - ReDoc",
            redoc_js_url=settings.REDOC_JS_URL,
            redoc_favicon_url=settings.FAVICON_URL,
        )
