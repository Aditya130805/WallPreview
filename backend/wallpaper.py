import base64
import numpy as np
import cv2
import os
import torch
from PIL import Image
from transformers import AutoImageProcessor, SegformerForSemanticSegmentation
from dotenv import load_dotenv


load_dotenv()

class WallPreview:
    MODEL_NAME = "badmatr11x/semantic-image-segmentation"
    ROLL_WIDTH = 21  # Constant fixed by supplier
    # Initialize model and processor once at class level
    processor = None
    model = None

    @classmethod
    def initialize_model(cls):
        if cls.processor is None or cls.model is None:
            cls.processor = AutoImageProcessor.from_pretrained(cls.MODEL_NAME)
            cls.model = SegformerForSemanticSegmentation.from_pretrained(cls.MODEL_NAME)

    def __init__(self):
        self.mask = None
        self.current_image_path = None
        # Initialize the model when creating an instance
        WallPreview.initialize_model()

    @staticmethod
    def query(filename):
        # Ensure model is loaded
        WallPreview.initialize_model()
        
        # Load image
        image = Image.open(filename)
        
        # Process image for model input
        inputs = WallPreview.processor(images=image, return_tensors="pt")
        
        # Run inference
        with torch.no_grad():
            outputs = WallPreview.model(**inputs)
            logits = outputs.logits
        
        # Get the id2label mapping if available
        id2label = getattr(WallPreview.model.config, 'id2label', None)
        wall_class_idx = 0
        
        # Try to find wall class in the model's class mapping
        if id2label:
            for idx, label in id2label.items():
                if 'wall' in label.lower():
                    wall_class_idx = int(idx)
                    break

        # Resize logits to match original image size
        upsampled_logits = torch.nn.functional.interpolate(
            logits,
            size=image.size[::-1],  # (height, width)
            mode="bilinear",
            align_corners=False,
        )
        
        # Get class predictions
        pred_seg = upsampled_logits.argmax(dim=1)[0].cpu().numpy()
        unique_classes = np.unique(pred_seg)
        
        # Create a binary mask for the wall class
        wall_mask = (pred_seg == wall_class_idx).astype(np.uint8) * 255
        
        # Convert to base64 for compatibility with existing code
        _, buffer = cv2.imencode('.png', wall_mask)
        wall_mask_base64 = base64.b64encode(buffer).decode('utf-8')
        
        # Return in a format similar to the original API response
        return [{"label": "wall", "mask": wall_mask_base64}]

    def generate_wall_mask(self, filename) -> bool:
        self.current_image_path = filename
        try:
            output = WallPreview.query(filename)
            
            base64_string = None
            for i in range(len(output)):
                if output[i]['label'] == 'wall':
                    base64_string = output[i]['mask']
                    break
                    
            if base64_string:
                image_data = base64.b64decode(base64_string)
                np_array = np.frombuffer(image_data, np.uint8)
                image = cv2.imdecode(np_array, cv2.IMREAD_GRAYSCALE)
                if image is not None:
                    _, self.mask = cv2.threshold(image, 127, 255, cv2.THRESH_BINARY)
                    return True
        except Exception as e:
            print(f"Error generating wall mask: {e}")
            return False
            
        self.mask = None
        return False

    @staticmethod
    def get_original_image(filename):
        return cv2.imread(filename, cv2.IMREAD_COLOR)

    # .shape gives [height, width, channels]
    def apply_wallpaper(self, img_path, wallpaper_path, wall_width, roll_width, best_shift):

        image = self.get_original_image(img_path)
        if image is None or self.mask is None:
            return False
        mask = self.mask
        
        wallpaper = self.get_original_image(wallpaper_path)
        
        # Forming the accurate horizontal layer
        num_horizontal_repeats = wall_width / roll_width
        int_horizontal_repeats = int(num_horizontal_repeats)
        fractional_width = int((num_horizontal_repeats % 1) * wallpaper.shape[1])
        horizontal_layers = [wallpaper]
        for i in range(1, int_horizontal_repeats):
            shifted_layer = np.roll(wallpaper, i * best_shift, axis=0)
            horizontal_layers.append(shifted_layer)
        final_horizontal = np.hstack(horizontal_layers)
        if fractional_width > 0:
            fractional_horizontal = np.roll(wallpaper[:, :fractional_width], int_horizontal_repeats * best_shift, axis=0)
            final_horizontal = np.hstack((final_horizontal, fractional_horizontal))

        # Forming the accurate vertical layer using the wallpaper height
        ##### ASSUMPTION: The entire image is cropped to show only the wall
        aspect_ratio = image.shape[1] / image.shape[0]
        in_accordance_height = final_horizontal.shape[1] / aspect_ratio
        num_vertical_repeats = in_accordance_height / wallpaper.shape[0]
        int_vertical_repeats = int(num_vertical_repeats)
        if int_vertical_repeats > 0:
            whole_vertical = np.vstack([final_horizontal] * int(num_vertical_repeats))
        else:
            whole_vertical = np.empty((0, final_horizontal.shape[1], final_horizontal.shape[2]), dtype=final_horizontal.dtype)
        fractional_vertical = final_horizontal[:int((num_vertical_repeats % 1) * final_horizontal.shape[0]), :]
        final_both = np.vstack((whole_vertical, fractional_vertical))
        
        # Resizing to form the correctly-sized final wallpaper
        final_wallpaper = cv2.resize(final_both, (image.shape[1], image.shape[0]), 
                                        interpolation=cv2.INTER_LINEAR)
        
        # Applying the wallpaper onto the image
        image_plus_one = np.clip(image.astype(np.int32) + 1, 0, 255).astype(np.uint8)
        wall_image = np.zeros_like(image)
        wall_image[mask == 0] = image_plus_one[mask == 0]
        wall_image[mask == 255] = final_wallpaper[mask == 255]
        
        return wall_image

if __name__ == '__main__':
    user_wall = WallPreview()
    user_wall.generate_wall_mask('../../../../TestWall.jpg')
    result = user_wall.apply_wallpaper('../../../../TestWall.jpg', '../../../../Test1.png', 86, 20.34, 21, 20.34, -1)
    
    scaling_factor = 0.2
    width = int(result.shape[1] * scaling_factor)
    height = int(result.shape[0] * scaling_factor)
    new_dimensions = (width, height)
    resized_image = cv2.resize(result, new_dimensions, interpolation=cv2.INTER_AREA)
    cv2.imshow('Result', resized_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
