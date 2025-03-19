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

# Роуты для ВСП
@app.post("/vsp", response_model=VSPInDB)
def create_vsp(vsp: VSP):
    vsp_data = vsp.dict()
    vsp_data["created_at"] = datetime.utcnow()
    vsp_data["updated_at"] = datetime.utcnow()
    result = vsp_collection.insert_one(vsp_data)
    vsp_data["id"] = str(result.inserted_id)
    return vsp_data

@app.get("/vsp/{vsp_id}", response_model=VSPInDB)
def get_vsp(vsp_id: str):
    vsp = vsp_collection.find_one({"_id": ObjectId(vsp_id)})
    if vsp:
        vsp["id"] = str(vsp["_id"])
        return vsp
    raise HTTPException(status_code=404, detail="VSP not found")

# Роуты для объектов
@app.post("/vsp/{vsp_id}/objects", response_model=ObjectInDB)
def create_object(vsp_id: str, obj: Object):
    obj_data = obj.dict()
    obj_data["vsp_id"] = vsp_id
    obj_data["created_at"] = datetime.utcnow()
    obj_data["updated_at"] = datetime.utcnow()
    result = object_collection.insert_one(obj_data)
    obj_data["id"] = str(result.inserted_id)
    return obj_data

@app.get("/vsp/{vsp_id}/objects", response_model=List[ObjectInDB])
def get_objects(vsp_id: str):
    objects = list(object_collection.find({"vsp_id": vsp_id}))
    for obj in objects:
        obj["id"] = str(obj["_id"])
    return objects

# Роуты для ремонтов
@app.post("/vsp/{vsp_id}/repairs", response_model=RepairInDB)
def create_repair(vsp_id: str, repair: Repair):
    repair_data = repair.dict()
    repair_data["vsp_id"] = vsp_id
    result = repair_collection.insert_one(repair_data)
    repair_data["id"] = str(result.inserted_id)
    return repair_data

@app.get("/vsp/{vsp_id}/repairs", response_model=List[RepairInDB])
def get_repairs(vsp_id: str):
    repairs = list(repair_collection.find({"vsp_id": vsp_id}))
    for repair in repairs:
        repair["id"] = str(repair["_id"])
    return repairs

# Роуты для планов обслуживания
@app.post("/vsp/{vsp_id}/maintenance_plans", response_model=MaintenancePlanInDB)
def create_maintenance_plan(vsp_id: str, plan: MaintenancePlan):
    plan_data = plan.dict()
    plan_data["vsp_id"] = vsp_id
    result = maintenance_plan_collection.insert_one(plan_data)
    plan_data["id"] = str(result.inserted_id)
    return plan_data

@app.get("/vsp/{vsp_id}/maintenance_plans", response_model=List[MaintenancePlanInDB])
def get_maintenance_plans(vsp_id: str):
    plans = list(maintenance_plan_collection.find({"vsp_id": vsp_id}))
    for plan in plans:
        plan["id"] = str(plan["_id"])
    return plans

# Роуты для выполненных работ
@app.post("/vsp/{vsp_id}/work_logs", response_model=WorkLogInDB)
def create_work_log(vsp_id: str, log: WorkLog):
    log_data = log.dict()
    log_data["vsp_id"] = vsp_id
    result = work_log_collection.insert_one(log_data)
    log_data["id"] = str(result.inserted_id)
    return log_data

@app.get("/vsp/{vsp_id}/work_logs", response_model=List[WorkLogInDB])
def get_work_logs(vsp_id: str):
    logs = list(work_log_collection.find({"vsp_id": vsp_id}))
    for log in logs:
        log["id"] = str(log["_id"])
    return logs

# Роуты для фото и схем
@app.post("/vsp/{vsp_id}/photos")
def upload_photo(vsp_id: str, file: UploadFile = File(...)):
    file_path = f"photos/{file.filename}"
    with open(file_path, "wb") as buffer:
        buffer.write(file.file.read())
    photo_data = {"vsp_id": vsp_id, "file_path": file_path, "description": file.filename}
    result = photo_collection.insert_one(photo_data)
    photo_data["id"] = str(result.inserted_id)
    return photo_data

@app.get("/vsp/{vsp_id}/photos", response_model=List[PhotoInDB])
def get_photos(vsp_id: str):
    photos = list(photo_collection.find({"vsp_id": vsp_id}))
    for photo in photos:
        photo["id"] = str(photo["_id"])
    return photos

# Роуты для карт
@app.post("/vsp/{vsp_id}/maps")
def upload_map(vsp_id: str, file: UploadFile = File(...)):
    file_path = f"maps/{file.filename}"
    with open(file_path, "wb") as buffer:
        buffer.write(file.file.read())
    map_data = {"vsp_id": vsp_id, "file_path": file_path, "description": file.filename}
    result = map_collection.insert_one(map_data)
    map_data["id"] = str(result.inserted_id)
    return map_data

@app.get("/vsp/{vsp_id}/maps", response_model=List[MapInDB])
def get_maps(vsp_id: str):
    maps = list(map_collection.find({"vsp_id": vsp_id}))
    for map in maps:
        map["id"] = str(map["_id"])
    return maps

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)