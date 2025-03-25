from pydantic import BaseModel
from datetime import datetime

class Note(BaseModel):
    """
    筆記模型類別
    
    屬性:
        name: 筆記名稱
        content: 筆記內容
        created_at: 創建時間
        updated_at: 最後更新時間
    """
    name: str
    content: str
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()

    def update_content(self, new_content: str) -> None:
        """更新筆記內容並更新時間戳"""
        self.content = new_content
        self.updated_at = datetime.now() 