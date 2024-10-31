from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.encoders import jsonable_encoder
from fastapi import Request
from typing import List
import pandas as pd
from io import StringIO
from app.functions.interval_processing import process_intervals

app = FastAPI()

# 设置模板和静态文件目录
templates = Jinja2Templates(directory="app/templates")
app.mount("/static", StaticFiles(directory="./app/static"), name="static")

# 提供可用函数的列表
@app.get("/functions")
async def get_functions():
    return {"functions": ["process_intervals"]}

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/upload")
async def upload_file(
    files: List[UploadFile] = File(...),  # 接收多个文件
    column_names: List[str] = Form(...)  # 接收多个列名
):
    # 确保文件数量和列名数量匹配
    if len(files) != len(column_names):
        return {"error": "文件数量和列名数量不匹配。"}

    combined_data = []  # 用于存储所有文件的数据

    # 逐个处理文件
    for file, column_names_str in zip(files, column_names):
        # 读取 CSV 文件内容
        contents = await file.read()  # 读取文件内容
        string_data = contents.decode('utf-8')  # 将内容解码为字符串
        df = pd.read_csv(StringIO(string_data))  # 解析 CSV 文件
        
        # 获取列名列表
        column_names_list = column_names_str.split(",")  # 处理列名
        file_data = []  # 用于存储当前文件的数据

        # 确保所有列名存在于 DataFrame 中
        missing_columns = [col for col in column_names_list if col not in df.columns]
        if missing_columns:
            return {"error": f"缺少以下列: {', '.join(missing_columns)}"}
        
        # 将每个列的数据转换为列表，并存储在 file_data 中
        for col in column_names_list:
            # 获取列的数据并转换为列表
            col_data = df[col].dropna().tolist()  # 忽略缺失值
            file_data.append(col_data)  # 将列数据加入当前文件的数据列表
        
        combined_data.append(file_data)  # 将当前文件的数据加入到 combined_data 中

    # 调用处理函数，将汇总的数据传递给它
    result = await process_intervals(combined_data)  # 假设这是异步处理函数

    return result


