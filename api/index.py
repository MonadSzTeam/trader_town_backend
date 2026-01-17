"""
Vercel Serverless Function 入口文件
将 FastAPI 应用包装为 Vercel 函数
"""
from mangum import Mangum
from app.main import app

# 使用 Mangum 将 FastAPI 应用适配为 ASGI 应用
handler = Mangum(app, lifespan="off")

