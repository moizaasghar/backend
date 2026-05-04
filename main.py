from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

app = FastAPI() # create FastAPI instance

class Task(BaseModel):
    id: int
    task: str
    description: str
    completed: bool = False

to_do_list: List[Task] = []

to_do_list.append(Task(id=1, task="Buy groceries", description="Milk, Bread, Eggs", completed=False))
to_do_list.append(Task(id=2, task="Read a book", description="Finish reading 'The Great Gatsby'", completed=False))
to_do_list.append(Task(id=3, task="Exercise", description="Go for a 30-minute run", completed=False))

@app.get("/tasks", response_model=List[Task])
def get_tasks():
    return to_do_list

@app.post("/addTask", response_model=Task)
def add_task(task: Task):
    to_do_list.append(task)
    return task

@app.delete("/deleteTask/{task_id}")
def delete_task(task_id: int):
    global to_do_list
    to_do_list = [t for t in to_do_list if t.id != task_id]
    return {"message": f"Task with id {task_id} deleted"}

@app.put("/updateTask/{task_id}")
def update_task(task_id: int, updated_task: Task):
    for idx, t in enumerate(to_do_list):
        if t.id == task_id:
            to_do_list[idx] = updated_task
            return updated_task
    return {"error": "Task not found"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)