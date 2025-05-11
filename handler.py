from runpod.serverless.modules.rp_handler import RunPodHandler
import torch
from diffusers import StableDiffusionPipeline
import os

pipe = None

def init_pipeline():
    global pipe
    if pipe is None:
        print("Loading Stable Diffusion v1.5 pipeline...")

        pipe = StableDiffusionPipeline.from_pretrained(
            "runwayml/stable-diffusion-v1-5",
            torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
            use_safetensors=True,
        )
        pipe.to("cuda" if torch.cuda.is_available() else "cpu")

def handler(event):
    init_pipeline()

    prompt = event.get("input", {}).get("prompt", "A futuristic cityscape")
    negative_prompt = event.get("input", {}).get("negative_prompt", "")
    width = event.get("input", {}).get("width", 512)
    height = event.get("input", {}).get("height", 512)
    guidance = event.get("input", {}).get("guidance_scale", 7.5)
    steps = event.get("input", {}).get("num_inference_steps", 20)

    print(f"Generating image: {prompt}")

    result = pipe(
        prompt,
        negative_prompt=negative_prompt,
        width=width,
        height=height,
        guidance_scale=guidance,
        num_inference_steps=steps
    )

    image_path = "/tmp/generated_image.png"
    result.images[0].save(image_path)

    return {
        "image_path": image_path,
        "prompt": prompt
    }

handler = RunPodHandler(handler)
