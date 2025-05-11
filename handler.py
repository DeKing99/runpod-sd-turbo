
from runpod.serverless.modules.rp_handler import RunPodHandler
from diffusers import DiffusionPipeline
import torch

pipe = DiffusionPipeline.from_pretrained(
    "stabilityai/stable-diffusion-3.5-large-turbo",
    torch_dtype=torch.float16,
    variant="fp16"
).to("cuda")

def handler(event):
    prompt = event["input"].get("prompt", "an astronaut cat")
    width = event["input"].get("width", 1024)
    height = event["input"].get("height", 1024)
    steps = event["input"].get("num_inference_steps", 25)
    guidance = event["input"].get("guidance_scale", 7.5)

    image = pipe(prompt=prompt, width=width, height=height, num_inference_steps=steps, guidance_scale=guidance).images[0]
    output_path = "/tmp/output.png"
    image.save(output_path)

    return {"image": output_path}
