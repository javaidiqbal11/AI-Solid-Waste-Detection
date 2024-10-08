import os
import uuid
import shutil
from datetime import datetime
from PIL import Image
from bson import ObjectId
from fastapi import APIRouter, UploadFile, File, HTTPException, Query, Depends
from fastapi.responses import JSONResponse
from app.crud import save_image, save_data_to_db, update_data_in_db
from app.utils import get_country_name, create_mongo_connection
from app.dependencies import get_current_user

router = APIRouter()

@router.post("/", dependencies=[Depends(get_current_user)])
async def save_data(
    image_file: UploadFile = File(...),
    latitude: float = Query(...),
    longitude: float = Query(...),
    level: str = Query(...),
    token: str = Depends(get_current_user)
):
    phone_number = token
    image_path = save_image(phone_number, image_file)
    payload = {
        "phone_number": phone_number,
        "image_path": image_path,
        "latitude": latitude,
        "longitude": longitude,
        "country": get_country_name(latitude, longitude),
        "level": level,
        "annotations": {"annotations": []},
        "cropped_paths": [],
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }
    save_data_to_db(payload)
    return JSONResponse(status_code=200, content={"message": "Data saved successfully"})

@router.patch("/", dependencies=[Depends(get_current_user)])
async def update_data(
    id: str = Query(...),
    annotations_str: str = Query(None),
    token: str = Depends(get_current_user)
):
    phone_number = token
    try:
        annotations = eval(annotations_str) if annotations_str else {"annotations": []}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid annotations format: {str(e)}")

    db = create_mongo_connection()
    waste_data = db["wastes"].find_one({"_id": ObjectId(id)})
    if not waste_data:
        raise HTTPException(status_code=404, detail="Data not found")
    image_path = waste_data["image_path"]

    cropped_dir = f"images/{phone_number}/cropped"
    if os.path.exists(cropped_dir):
        shutil.rmtree(cropped_dir)
    os.makedirs(cropped_dir, exist_ok=True)

    cropped_paths = []
    if annotations.get("annotations"):
        for annotation in annotations["annotations"]:
            x1 = annotation['x1']
            y1 = annotation['y1']
            x2 = annotation['x2']
            y2 = annotation['y2']
            image = Image.open(image_path)
            cropped_image = image.crop((x1, y1, x2, y2))
            cropped_image_filename = f"{uuid.uuid4()}_{os.path.basename(image_path)}"
            cropped_image_path = f"{cropped_dir}/{cropped_image_filename}"
            cropped_image.save(cropped_image_path)
            cropped_paths.append(cropped_image_path)

    payload = {
        "annotations": annotations,
        "cropped_paths": cropped_paths,
    }
    update_data_in_db(id, payload)
    return JSONResponse(status_code=200, content={"message": "Data updated successfully"})
