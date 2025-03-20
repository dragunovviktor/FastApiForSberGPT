from fastapi import FastAPI, HTTPException, UploadFile, File
from pymongo import MongoClient
from typing import List
from bson.objectid import ObjectId
from datetime import datetime
from .models import (
    VSP, VSPInDB, Object, ObjectInDB, Repair, RepairInDB,
    MaintenancePlan, MaintenancePlanInDB, WorkLog, WorkLogInDB,
    Photo, PhotoInDB, Map, MapInDB
)
from .database import (
    vsp_collection, object_collection, repair_collection,
    maintenance_plan_collection, work_log_collection,
    photo_collection, map_collection
)

app = FastAPI()
def generate_id(collection):
    last_document = collection.find_one(sort=[("id", -1)])
    if last_document:
        return last_document["id"] + 1
    return 1

def validate_vsp_id(vsp_id: int):
    """Проверяет, существует ли ВСП с указанным id."""
    vsp = vsp_collection.find_one({"id": vsp_id})
    if not vsp:
        raise HTTPException(status_code=404, detail="VSP not found")
    return vsp

@app.post("/vsp", response_model=VSPInDB)
def create_vsp(vsp: VSP):
    """Создает новый ВСП."""
    vsp_data = vsp.dict()
    vsp_data["id"] = generate_id(vsp_collection)  # Генерация числового ID
    vsp_data["created_at"] = datetime.utcnow()
    vsp_data["updated_at"] = datetime.utcnow()
    vsp_collection.insert_one(vsp_data)
    return vsp_data

@app.get("/vsp", response_model=List[VSPInDB])
def get_all_vsp():
    """Возвращает список всех ВСП."""
    vsp_list = list(vsp_collection.find())
    return vsp_list

@app.get("/vsp/{vsp_id}", response_model=VSPInDB)
def get_vsp(vsp_id: int):
    """Возвращает ВСП по его id."""
    vsp = validate_vsp_id(vsp_id)
    return vsp

# Роуты для объектов
@app.post("/objects", response_model=ObjectInDB)
def create_object(obj: Object):
    """Создает новый объект, привязанный к ВСП."""
    validate_vsp_id(obj.vsp_id)  # Проверяем, что ВСП существует
    obj_data = obj.dict()
    obj_data["id"] = generate_id(object_collection)  # Генерация числового ID
    obj_data["created_at"] = datetime.utcnow()
    obj_data["updated_at"] = datetime.utcnow()
    object_collection.insert_one(obj_data)
    return obj_data

@app.get("/vsp/{vsp_id}/objects", response_model=List[ObjectInDB])
def get_objects(vsp_id: int):
    """Возвращает все объекты, привязанные к ВСП."""
    validate_vsp_id(vsp_id)  # Проверяем, что ВСП существует
    objects = list(object_collection.find({"vsp_id": vsp_id}))
    return objects

# Роуты для ремонтов
@app.post("/repairs", response_model=RepairInDB)
def create_repair(repair: Repair):
    """Создает новую запись о ремонте, привязанную к ВСП."""
    validate_vsp_id(repair.vsp_id)  # Проверяем, что ВСП существует
    repair_data = repair.dict()
    repair_data["id"] = generate_id(repair_collection)  # Генерация числового ID
    repair_collection.insert_one(repair_data)
    return repair_data

@app.get("/vsp/{vsp_id}/repairs", response_model=List[RepairInDB])
def get_repairs(vsp_id: int):
    """Возвращает все ремонты, привязанные к ВСП."""
    validate_vsp_id(vsp_id)  # Проверяем, что ВСП существует
    repairs = list(repair_collection.find({"vsp_id": vsp_id}))
    return repairs

# Роуты для планов обслуживания
@app.post("/maintenance_plans", response_model=MaintenancePlanInDB)
def create_maintenance_plan(plan: MaintenancePlan):
    """Создает новый план обслуживания, привязанный к ВСП."""
    validate_vsp_id(plan.vsp_id)  # Проверяем, что ВСП существует
    plan_data = plan.dict()
    plan_data["id"] = generate_id(maintenance_plan_collection)  # Генерация числового ID
    maintenance_plan_collection.insert_one(plan_data)
    return plan_data

@app.get("/vsp/{vsp_id}/maintenance_plans", response_model=List[MaintenancePlanInDB])
def get_maintenance_plans(vsp_id: int):
    """Возвращает все планы обслуживания, привязанные к ВСП."""
    validate_vsp_id(vsp_id)  # Проверяем, что ВСП существует
    plans = list(maintenance_plan_collection.find({"vsp_id": vsp_id}))
    return plans

# Роуты для выполненных работ
@app.post("/work_logs", response_model=WorkLogInDB)
def create_work_log(log: WorkLog):
    """Создает новую запись о выполненной работе, привязанную к ВСП."""
    validate_vsp_id(log.vsp_id)  # Проверяем, что ВСП существует
    log_data = log.dict()
    log_data["id"] = generate_id(work_log_collection)  # Генерация числового ID
    work_log_collection.insert_one(log_data)
    return log_data

@app.get("/vsp/{vsp_id}/work_logs", response_model=List[WorkLogInDB])
def get_work_logs(vsp_id: int):
    """Возвращает все записи о выполненной работе, привязанные к ВСП."""
    validate_vsp_id(vsp_id)  # Проверяем, что ВСП существует
    logs = list(work_log_collection.find({"vsp_id": vsp_id}))
    return logs

# Роуты для фото
@app.post("/photos", response_model=PhotoInDB)
def upload_photo(file: UploadFile = File(...), vsp_id: int = None):
    """Загружает фото, привязанное к ВСП."""
    if vsp_id:
        validate_vsp_id(vsp_id)  # Проверяем, что ВСП существует
    file_path = f"photos/{file.filename}"
    with open(file_path, "wb") as buffer:
        buffer.write(file.file.read())
    photo_data = {
        "id": generate_id(photo_collection),  # Генерация числового ID
        "vsp_id": vsp_id,
        "file_path": file_path,
        "description": file.filename
    }
    photo_collection.insert_one(photo_data)
    return photo_data

@app.get("/vsp/{vsp_id}/photos", response_model=List[PhotoInDB])
def get_photos(vsp_id: int):
    """Возвращает все фото, привязанные к ВСП."""
    validate_vsp_id(vsp_id)  # Проверяем, что ВСП существует
    photos = list(photo_collection.find({"vsp_id": vsp_id}))
    return photos

# Роуты для карт
@app.post("/maps", response_model=MapInDB)
def upload_map(file: UploadFile = File(...), vsp_id: int = None):
    """Загружает карту, привязанную к ВСП."""
    if vsp_id:
        validate_vsp_id(vsp_id)  # Проверяем, что ВСП существует
    file_path = f"maps/{file.filename}"
    with open(file_path, "wb") as buffer:
        buffer.write(file.file.read())
    map_data = {
        "id": generate_id(map_collection),  # Генерация числового ID
        "vsp_id": vsp_id,
        "file_path": file_path,
        "description": file.filename
    }
    map_collection.insert_one(map_data)
    return map_data

@app.get("/vsp/{vsp_id}/maps", response_model=List[MapInDB])
def get_maps(vsp_id: int):
    """Возвращает все карты, привязанные к ВСП."""
    validate_vsp_id(vsp_id)  # Проверяем, что ВСП существует
    maps = list(map_collection.find({"vsp_id": vsp_id}))
    return maps


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)