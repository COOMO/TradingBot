from enum import Enum
from typing import Optional
from fastapi import FastAPI

# 在 https://9dbe-114-43-155-82.ngrok-free.app/docs 中可以看到 API 文件幫忙建立了下拉選單
class Gender(str, Enum):
    male = "male"
    female = "female"

app = FastAPI()


@app.get("/users/{user_id}")
async def get_current_user(user_id: int):
    return {"user_id": user_id}

@app.get("/student/{gender}")
async def get_gender(gender: Gender):
    return {"student" : f'This is a {gender.value} student'}

# 這邊的 page_index 和 page_size 是 query parameter, url 使用 ?
# https://9dbe-114-43-155-82.ngrok-free.app/users?page_index=3&page_size=20
# 會回傳 {'page info': 'index: 3, size : 20'}

#Optional 代表 page_size 可以不給值, 要 from typing import Optional
@app.get("/users")
async def get_user(page_index: int = 0, page_size: Optional[int] = 30):
    return {'page info' : f'index: {page_index}, size : {page_size}'}

# user_id 是路徑參數，必須提供在 URL 中
# limit 是 query parameter, url 使用 ? 因為沒有提供預設值，所以 URL 中必須提供
# page_size 是 Optional, 可以不提供
@app.get("/users/{user_id}/friends")
async def get_user_friends(user_id: int, limit: int, page_size: Optional[int] = 10):
    return {'user friends': f'_user_id: {user_id}, page_size: {page_size}, limit: {limit}'}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app="test:app", host="0.0.0.0", port=80, reload=True)