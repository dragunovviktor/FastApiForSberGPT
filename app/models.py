from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class VSP(BaseModel):
    address: str
    office_number: str
    description: Optional[str] = None

class VSPInDB(VSP):
    id: str
    created_at: datetime
    updated_at: datetime

class Object(BaseModel):
    name: str
    type: str
    area_size: float
    unit: str
    characteristics: Optional[str] = None
    cleaning_frequency: Optional[str] = None

class ObjectInDB(Object):
    id: str
    created_at: datetime
    updated_at: datetime

class Repair(BaseModel):
    description: str
    date: datetime
    area_size: float
    status: str  # planned, completed, cancelled

class RepairInDB(Repair):
    id: str

class MaintenancePlan(BaseModel):
    description: str
    frequency: str
    next_maintenance: datetime

class MaintenancePlanInDB(MaintenancePlan):
    id: str

class WorkLog(BaseModel):
    description: str
    date: datetime

class WorkLogInDB(WorkLog):
    id: str

class Photo(BaseModel):
    description: str
    file_path: str

class PhotoInDB(Photo):
    id: str

class Map(BaseModel):
    description: str
    file_path: str

class MapInDB(Map):
    id: str