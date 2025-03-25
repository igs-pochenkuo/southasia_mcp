from typing import Dict, List, Optional
from datetime import datetime

from ..models.note import Note

class NoteService:
    """
    筆記服務類別，處理所有筆記相關的業務邏輯
    """
    def __init__(self):
        self._notes: Dict[str, Note] = {}

    def add_note(self, name: str, content: str) -> Note:
        """
        新增筆記
        
        參數:
            name: 筆記名稱
            content: 筆記內容
            
        返回:
            新建的筆記對象
            
        異常:
            ValueError: 當筆記名稱已存在時
        """
        if name in self._notes:
            raise ValueError(f"筆記 '{name}' 已存在")
        
        note = Note(name=name, content=content)
        self._notes[name] = note
        return note

    def get_note(self, name: str) -> Note:
        """
        獲取指定筆記
        
        參數:
            name: 筆記名稱
            
        返回:
            筆記對象
            
        異常:
            ValueError: 當筆記不存在時
        """
        if name not in self._notes:
            raise ValueError(f"找不到筆記 '{name}'")
        return self._notes[name]

    def update_note(self, name: str, content: str) -> Note:
        """
        更新筆記內容
        
        參數:
            name: 筆記名稱
            content: 新的筆記內容
            
        返回:
            更新後的筆記對象
            
        異常:
            ValueError: 當筆記不存在時
        """
        note = self.get_note(name)
        note.update_content(content)
        return note

    def delete_note(self, name: str) -> None:
        """
        刪除筆記
        
        參數:
            name: 筆記名稱
            
        異常:
            ValueError: 當筆記不存在時
        """
        if name not in self._notes:
            raise ValueError(f"找不到筆記 '{name}'")
        del self._notes[name]

    def search_notes(self, keyword: str) -> List[Note]:
        """
        搜尋筆記
        
        參數:
            keyword: 搜尋關鍵字
            
        返回:
            符合關鍵字的筆記列表
        """
        return [
            note for note in self._notes.values()
            if keyword.lower() in note.content.lower()
        ]

    def list_notes(self) -> List[Note]:
        """
        列出所有筆記
        
        返回:
            所有筆記的列表
        """
        return list(self._notes.values()) 