from fastapi import FastAPI
import uvicorn
import urm
from .urm_dec import build_urm_program_from_data, serialize_urm_program
import json
from fastapi import Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from .load_programs import load_programs
import os
import click

current_dir = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(current_dir, "urm-visualization/build_latest")
# STATIC_DIR = "urm-visualization/build"

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.mount("/static", StaticFiles(directory=f"{STATIC_DIR}/static"), name="static")

@app.get("/")
def read_root():
    return HTMLResponse(content=open(f"{STATIC_DIR}/index.html", "r").read())

@app.post("/get_max_register")
async def get_haddr(request: Request):
    try:
        data = await request.json()
        urm_program, _ = build_urm_program_from_data(data)
        return {"haddr": urm.haddr(urm_program) + 1}
    except Exception as e:
        return {"error": str(e)}

@app.post("/run_urm_program")
async def run_urm_program(request: Request):
    try:
        data = await request.json()
        print(f"Data: {data}")
        urm_program, safety_count = build_urm_program_from_data(data['program'])
        initialization_registers = data['initialRegisters']
        initialization_registers = urm.Registers(initialization_registers)
        print(urm_program)
        result = urm.forward(None, initialization_registers, urm_program, safety_count=safety_count)
        wrapped_result = {}
        wrapped_result['registers_from_steps'] = []
        wrapped_result['ops_from_steps'] = []
        wrapped_result['serialized_program'] = serialize_urm_program(urm_program, safety_count=safety_count)
        for item in result.registers_from_steps:
            wrapped_result['registers_from_steps'].append(item.registers)
        for item in result.ops_from_steps:
            wrapped_result['ops_from_steps'].append(item)
        print(wrapped_result)
        return {"result": wrapped_result}
    except Exception as e:
        print(f"Error: {e}")
        return {"error": str(e)}

@app.get("/index")
async def serve_react_app(request: Request):
    return HTMLResponse(content=open(f"{STATIC_DIR}/index.html", "r").read())


@app.get("/get_programs")
async def get_programs():
    return {"programs": load_programs(os.path.join(current_dir, "programs"))}


@click.command()
@click.option("--host", default="localhost", help="Host to run the server on")
@click.option("--port", default=8975, help="Port to run the server on")
def gui(host, port):
    print(f"Visit page at http://{host}:{port}/index")
    uvicorn.run("urm.gui.server:app", host=host, port=port, reload=False)

if __name__ == "__main__":
    gui()
