from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from wallpaper import WallPreview
import json
import base64
import cv2
import os
import numpy as np

# Define constants
CONSTANTS = {
    'IMAGE_FOLDER_PATH': './uploads/',
    'WALLPAPER_FOLDER_PATH': './wallpapers/',
    'ALLOWED_ORIGINS': [
        # 'http://localhost:8080',
        'https://wallpreviews.vercel.app',
        'https://wallpreviews.com',
        'https://www.wallpreviews.com'
    ],
    'CUSTOM_WALLPAPER_NAME': 'wallpaperCustom.jpg'
}

CUSTOM_WALLPAPER_PATH = f"{CONSTANTS['WALLPAPER_FOLDER_PATH']}{CONSTANTS['CUSTOM_WALLPAPER_NAME']}"

# Create upload directories if they don't exist
os.makedirs(CONSTANTS['IMAGE_FOLDER_PATH'], exist_ok=True)
os.makedirs(CONSTANTS['WALLPAPER_FOLDER_PATH'], exist_ok=True)

# Initialize FastAPI app
app = FastAPI(title="WallPreviews Backend API")
user_wall = None

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=CONSTANTS['ALLOWED_ORIGINS'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

class ImageUpload(BaseModel):
    image: str

@app.post("/upload")
async def upload_file(image_upload: ImageUpload):
    image_data = image_upload.image
    try:
        header, base64_data = image_data.split(',')
        image_bytes = base64.b64decode(base64_data)
        image_path = f"{CONSTANTS['IMAGE_FOLDER_PATH']}cropped_image.jpg"
        with open(image_path, 'wb') as buffer:
            buffer.write(image_bytes)
        global user_wall
        user_wall = WallPreview()
        return True
    except Exception as e:
        print(f"Error in upload: {str(e)}")
        return JSONResponse(content={"error": str(e)}, status_code=500)

@app.post("/wallpaper-upload")
async def upload_file(image_upload: ImageUpload):
    image_data = image_upload.image
    try:
        header, base64_data = image_data.split(',')
        image_bytes = base64.b64decode(base64_data)
        image_path = CUSTOM_WALLPAPER_PATH
        with open(image_path, 'wb') as buffer:
            buffer.write(image_bytes)
        return True
    except Exception as e:
        print(f"Error in wallpaper upload: {str(e)}")
        return JSONResponse(content={"error": str(e)}, status_code=500)

class InitializePreviewInput(BaseModel):
    image_path: str

@app.post("/initialize")
async def initialize_program(user_input: InitializePreviewInput):
    try:
        response = user_wall.generate_wall_mask(f"{CONSTANTS['IMAGE_FOLDER_PATH']}{user_input.image_path}")
        if not response:
            response = user_wall.generate_wall_mask(f"{CONSTANTS['IMAGE_FOLDER_PATH']}{user_input.image_path}")
        return response
    except Exception as e:
        print(f"Error in initialize: {str(e)}")
        return JSONResponse(content={"error": str(e)}, status_code=500)

class ApplyWallpaperInput(BaseModel):
    image_path: str
    wallpaper_path: str
    wall_width: int
    roll_width: float
    best_shift: int

@app.post("/apply")
async def apply_file(choices: ApplyWallpaperInput):
    global user_wall
    try:
        if user_wall is None:
            return JSONResponse(content={"error": "Wall preview not initialized"}, status_code=400)
        
        result_image = user_wall.apply_wallpaper(
            f"{CONSTANTS['IMAGE_FOLDER_PATH']}{choices.image_path}", 
            f"{CONSTANTS['WALLPAPER_FOLDER_PATH']}{choices.wallpaper_path}", 
            choices.wall_width,
            choices.roll_width,
            choices.best_shift
        )
        if result_image is not None:
            _, encoded_img = cv2.imencode('.jpg', result_image)
            base64_img = base64.b64encode(encoded_img.tobytes())
            return JSONResponse(content={"image": base64_img.decode('utf-8')})
        else:
            return False
    except Exception as e:
        print(f"Error in apply: {str(e)}")
        return JSONResponse(content={"error": str(e)}, status_code=500)


########## For wallpaper shifting

@app.post("/wallpaper-preview-initialize")
async def initialize_preview():
    try:
        wallpaper = cv2.imread(CUSTOM_WALLPAPER_PATH, cv2.IMREAD_COLOR)
        height, width, _ = wallpaper.shape
        
        # Create the combined image
        first_image = wallpaper
        second_image = np.zeros_like(wallpaper)
        second_image[:height, :] = wallpaper
        
        combined_image = np.hstack((first_image, second_image))
        _, encoded_img = cv2.imencode('.jpg', combined_image)
        base64_img = base64.b64encode(encoded_img.tobytes()).decode('utf-8')

        return JSONResponse(content={"image": base64_img, "height": height})
    except Exception as e:
        return JSONResponse(content={"error": str(e)})

class ShiftAdjustment(BaseModel):
    shift: int

@app.post("/wallpaper-preview-adjust")
async def adjust_preview(adjustment: ShiftAdjustment):
    try:
        image_path = CUSTOM_WALLPAPER_PATH
        wallpaper = cv2.imread(image_path, cv2.IMREAD_COLOR)
        height, width, _ = wallpaper.shape
        shift = adjustment.shift
        if abs(shift) >= height:
            shift = 0

        black_space_top = np.zeros((abs(shift), width, 3), dtype=np.uint8)
        black_space_bottom = np.zeros((abs(shift), width, 3), dtype=np.uint8)

        # Adjust second image and add black spaces as needed
        if shift > 0:
            # Shift down
            second_image_with_space = np.vstack((black_space_top, wallpaper))
            first_image_with_space = np.vstack((wallpaper, black_space_bottom))
        else:
            # Shift up
            second_image_with_space = np.vstack((wallpaper, black_space_bottom))
            first_image_with_space = np.vstack((black_space_top, wallpaper))

        combined_image = np.hstack((first_image_with_space, second_image_with_space))
        _, encoded_img = cv2.imencode('.jpg', combined_image)
        base64_img = base64.b64encode(encoded_img.tobytes()).decode('utf-8')

        return JSONResponse(content={"image": base64_img})
    except Exception as e:
        return JSONResponse(content={"error": str(e)})


if __name__ == "__main__":
    import uvicorn
    # Start the server
    uvicorn.run(app, host="0.0.0.0", port=8000)
