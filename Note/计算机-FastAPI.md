# FastAPI

> [黑马程序员PythonWeb开发：FastAPI从入门到实战视频教程](https://www.bilibili.com/video/BV1zV2QBtE39)

## 1. 优点

- 原生支持异步
- 适配 Pydantic
- 自动生成可交互的API文档

## 2. 运行

```shell
# uvicorn: web服务器
# --reload 热更新，修改代码后自动重启服务器
uvicorn main:app --reload
```

## 3. 交互式文档

`http://127.0.0.1:8000/docs`

## 4. 定义请求路由

请求路由：url 和 处理函数 的映射关系

```python
from fastapi import FastAPI

# 创建 FastAPI 实例
app = FastAPI()


# 装饰器：FastAPI 实例，请求方法，请求路径
@app.get("/")
async def root():
    return {"message": "Hello World"}
```

### 4.1. 不同入参类型校验

#### 4.1.1. url参数

```python
@app.get("/book/{id}")
async def get_book(id: int = Path(..., description = "书籍id")):
    return ""
```

可以用 python 原生的类型声明 `int` 校验入参类型
也可以用 `Path` 来进行进一步的限制，如数据范围，description

#### 4.1.2. 普通get参数

直接在方法上加入参即可。

类型校验也有两种，python 原生 和 `Query`

```python
@app.get("/book/query")
async def query_books(
    skip: int = Query(0, lt = 100),
    limit: int = 10
    ):
    return ""
```

#### 4.1.3. 请求体

```python
from pydantic import BaseModel

class User(BaseModel):
    username: str
    password: str

@app.post("/register")
async def register(user: User)
    return user
```

类型校验：

```python
from pydantic import BaseModel, Field

class User(BaseModel):
    username: str = Field(default="john", min_length = 2)

```

### 4.2. 响应

FastAPI会自动将 python 对象转为 JSON，包装为 JSONResponse

还支持：HTMLResponse, PlainTextResponse, FileResponse, StreamingResponse, RedirectResponse

方式一：装饰器里指定

方式二：返回响应对象

```python
@app.get("/html", response_class=HTMLResponse)
async def get_html():
    return "<h1>标题</h1>"

@app.get("/file")
async def get_file():
    file_path = "./image.png"
    return FileResponse(file_path)
```

### 4.3. 自定义响应数据格式，用 response_model

```python
from pydantic import BaseModel

class News(BaseModel):
    id: int
    title: str

@app.get("news/{id}", response_model=News)
async def get_news(id: int):
    return {
        "id": id,
        "title": f"第{id}本书"
    }

```

## 5. http异常

```python
from fastapi import HTTPException

@app.get("")
def method():
    raise HTTPException(status_code=404, detail="资源不存在")

```

## 6. 中间件 Middleware

每次请求进入 FastAPI 应用都会被执行的函数

```python
# 声明这个方法是 中间件
@app.middleware("http")
async def middleware(request, call_next):
    # ...
    response = await call_next(request)
    # ...
    return response

```

多个中间件的执行顺序：在代码里，最下面的，位于调用链的最前面。

例如 mw1, mw2 的顺序定义了2个，然后发送请求

mw2 入参 -> mw1 入参 -> mw1 响应 -> mw2 响应

```

mw2  -->   mw1   -->   app
     <--         <--
```

## 7. 依赖注入，复用代码

```python
from fastapi import Depends

async def common_part(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, le=60)
):
    return {"skip": skip, "limit": limit}

@app.get("/news/query")
async def query_news(commons=Depends(common_part)):
    return commons

@app.get("/users/query")
async def query_users(commons=Depends(common_part)):
    return commons

```

之前是请求响应

## 8. ORM

SQLAlchemy ORM

安装依赖

sqlalchemy[asyncio]
aiomysql

面向对象，操作数据库

创建数据库引擎

create_async_engine

定义模型类，需要继承 DeclarativeBase

```python
from datetime import datetime
from sqlalchemy import DateTime

class Base(DeclarativeBase):
    create_time: Mapped[datetime] = mapped_column(DateTime, insert_default=func.now(), default=func.now, comment="创建时间")

class Book(Base):
    # 表名
    __tablename__="book"

    # 右边是数据库表的列信息
    id: Mapped[int] = mapped_column(primary_key=True)
```

创建表

从连接池获取连接，开启事务，执行ORM操作
可以在应用启动的时候，建表

```python
async def create_tables():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.on_event("startup")
async def startup_event():
    await create_tables()
```
