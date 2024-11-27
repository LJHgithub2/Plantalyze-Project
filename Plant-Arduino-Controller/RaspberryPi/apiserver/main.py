from fastapi import FastAPI, HTTPException
from typing import List, Optional
from pydantic import BaseModel
from ..SmartFarm_HD.main_control import GPIOController 
import os
from dotenv import load_dotenv

load_dotenv(verbose=True)

app = FastAPI()

# Define the controllers dictionary using environment variables
CONTROLLERS = {
    1: {"name": "LED", "PIN": int(os.getenv('LED_PIN', 17)), "DURATIONS": int(os.getenv('LED_DURATION', 1))},
    2: {"name": "워터펌프", "PIN": int(os.getenv('WATER_PIN', 18)), "DURATIONS": int(os.getenv('WATER_DURATION', 2))},
    3: {"name": "모터", "PIN": int(os.getenv('MOTOR_PIN', 19)), "DURATIONS": int(os.getenv('MOTOR_DURATION', 3))}
}

# Initialize the GPIOController with environment variables
controller = GPIOController(
    LED_PIN=CONTROLLERS[1]["PIN"],
    WATER_PIN=CONTROLLERS[2]["PIN"],
    MOTOR_PIN=CONTROLLERS[3]["PIN"],
    LED_DURATION=CONTROLLERS[1]["DURATIONS"],
    WATER_DURATION=CONTROLLERS[2]["DURATIONS"],
    MOTOR_DURATION=CONTROLLERS[3]["DURATIONS"]
)

# 구조체
class ControllerAction(BaseModel):
    controller_id: int
    duration: Optional[int] = None

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}

@app.post("/api/")
async def activate_controllers(actions: List[ControllerAction]):
    # Initialize response data
    response_data = []
    
    for action in actions:
        if action.controller_id not in CONTROLLERS:
            raise HTTPException(status_code=400, detail=f"Invalid controller ID: {action.controller_id}")
        
        controller_info = CONTROLLERS[action.controller_id]
        pin = controller_info["PIN"]
        duration = action.duration if action.duration is not None else controller_info["DURATIONS"]
        
        # Call the GPIOController's activate_control method
        success = await controller.activate_control(pin, duration)
        
        # Append the action details to response_data
        response_data.append({
            "controller_id": action.controller_id,
            "name": controller_info["name"],
            "duration": duration,
            "status": "success" if success else "failed"
        })
    
    return {"status": "success", "actions": response_data}
