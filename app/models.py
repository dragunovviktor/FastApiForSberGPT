from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class VSP(BaseModel):
    address: str
    office_number: str
    description: Optional[str] = None

class VSPInDB(VSP):
    id: int  # Числовой ID
    created_at: str  # Строка вместо datetime
    updated_at: str  # Строка вместо datetime

class Object(BaseModel):
    name: str
    type: str
    area_size: str  # Строка вместо float
    unit: str
    characteristics: Optional[str] = None
    cleaning_frequency: Optional[str] = None

class ObjectInDB(Object):
    id: int  # Числовой ID
    created_at: str  # Строка вместо datetime
    updated_at: str  # Строка вместо datetime

class Repair(BaseModel):
    description: str
    date: str  # Строка вместо datetime
    area_size: str  # Строка вместо float
    status: str  # planned, completed, cancelled

class RepairInDB(Repair):
    id: int  # Числовой ID

class MaintenancePlan(BaseModel):
    description: str
    frequency: str
    next_maintenance: str  # Строка вместо datetime

class MaintenancePlanInDB(MaintenancePlan):
    id: int  # Числовой ID

class WorkLog(BaseModel):
    description: str
    date: str  # Строка вместо datetime

class WorkLogInDB(WorkLog):
    id: int  # Числовой ID

class Photo(BaseModel):
    description: str
    file_path: str

class PhotoInDB(Photo):
    id: int  # Числовой ID

class Map(BaseModel):
    description: str
    file_path: str

class MapInDB(Map):
    id: int  # Числовой ID