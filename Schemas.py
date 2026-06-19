from typing import Optional
from pydantic import BaseModel


class crawler_req(BaseModel):
    url : str
    depth : Optional[int] = 1
