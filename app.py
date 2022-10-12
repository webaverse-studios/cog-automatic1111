from typing import Union, Optional

from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel
from omegaconf import OmegaConf
import random
import os
import sys

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "stable_diffusion_webui"))
from modules.processing import StableDiffusionProcessing
#from modules.processing import StableDiffusionProcessingTxt2Img
#from modules.processing import StableDiffusionProcessingImg2Img

#os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), "stable_diffusion_webui"))

class Generation(BaseModel):
    model: Optional[str] = "sd-v1-4"
    prompt: Optional[str] = "An astronaut riding a horse."
    iterations: Optional[int] = 1
    steps: Optional[int] = 50
    seed: Optional[int] = random.randint(1, 99999)
    cfg_scale: Optional[float] = 7.5
    seamless: Optional[bool] = False
    init_img: Optional[str] = None
    init_mask: Optional[str] = None
    negative_prompt: Optional[str] = None
    restore_faces: Optional[bool] = False
    tiling: Optional[bool] = False
    strength: Optional[float] = 0.75


app = FastAPI()

"""
@app.get("/")
def run_root():
    return root()
@app.post("/")
def root():
    return "hello world"
"""
@app.post("/api")
async def root(generation: Generation = None):

    if not generation:
        generation = StableDiffusionProcessing

    arg_dict = {
        "sd_model": generation.model + ".ckpt",
        "prompt": generation.prompt,
        "iterations": generation.iterations,
        "steps": generation.steps,
        "seed": generation.seed,
        "cfg_scale": generation.cfg_scale,
        "seamless": generation.seamless,
        "init_img": generation.init_img, # For img2img
        "init_mask": generation.init_mask, # For inpainting
        "strength": generation.strength
    }

    #generation = Generate(weights=weights, config=config)
    #output = generation.prompt2png(**arg_dict, outdir="outputs/web_out")

    #return send_file(output[0][0], mimetype="image/png")
    #return "something"
    return FileResponse(output[0][0])

#async def Generate(weights: str, config: str):


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="216.153.51.112", port=8001, log_level="debug")