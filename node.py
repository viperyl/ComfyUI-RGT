import os
import cv2
import torch
import numpy as np
from comfy.model_management import cast_to_device, get_torch_device
from loguru import logger
from .model import RGTModel
from folder_paths import models_dir


class RGT_Upscale:
    def __init__(self):
        self.model = None


    @classmethod
    def INPUT_TYPES(cls):
        # Example structure, adjust according to your actual input requirements
        return {
            "required": {
                "model_type": (["RGT", "RGT_S"], ),
                "upscale": (["x2", "x3", "x4"], ),
                "use_chop": (["enable", "disable"], ),
                "image": ("IMAGE", )
                
            },
        }
    
    RETURN_TYPES = ("IMAGE",)
    CATEGORY = "114514"
    FUNCTION = "load_model"

    def load_model(self, model_type, upscale, use_chop, image):
        logger.debug(f"image: {image.shape}")
        model_path = os.path.join(models_dir, "RGT",f"{model_type}", f"{model_type}_{upscale}.pth")
        image = torch.permute(image, (0, 3, 1, 2))
        if self.model is None:
            self.model = RGTModel(
                name=model_type, 
                upscale=int(upscale[-1]), 
                device=get_torch_device(),
                model_path=model_path
            )
        else:
            self.model.load_model(
                model_type, 
                int(upscale[-1]), 
                get_torch_device(),
                model_path
            )
        output = self.model(image, use_chop=True if use_chop == "enable" else False)

        output = torch.permute(output, (0, 2, 3, 1))
        logger.debug(f"output: {output.shape}")

        return (output, )



NODE_CLASS_MAPPINGS = {
    "RGT_Upscale": RGT_Upscale,
}

# A dictionary that contains the friendly/humanly readable titles for the nodes
NODE_DISPLAY_NAME_MAPPINGS = {
    "RGT Upscale": "RGT Upscale"
}