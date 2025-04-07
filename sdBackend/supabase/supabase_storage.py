# supabase_storage.py
# tell supabase how to retrieve, write, store

from gotrue import SyncSupportedStorage 
from django.contrib.sessions.backends.base import SessionBase
from django.conf import settings

class AppSessionStorage(SyncSupportedStorage):
    def __init__(self, session: SessionBase):
        self.storage = session

    def get_item(self, key:str) -> str | None :
        return self.storage.get(key)
    
    def set_item(self, key:str, value:str) -> None:
        self.storage[key]=value

    def remove_item(self, key:str) -> None:
        self.storage.pop(key, None)

