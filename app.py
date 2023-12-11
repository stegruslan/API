from datetime import datetime

from utils import (
    write_tasks,
    read_tasks,
    filter_tasks
)
from fastapi import (
    FastAPI,
    Request,

)
from fastapi.responses import JSONResponse as Response

app = FastAPI()


@app.get('/')
def get(r: Request) -> Response:
    priority = r.query_params.get('priority')
    data = read_tasks()
    if priority:
        data = filter_tasks(data, int(priority))
    return Response(content=data, status_code=200)


@app.post('/')
async def post(r: Request) -> Response:
    data = await r.json()
    errors = []
    for item in ('title', 'description', 'priority'):
        if not data.get(item):
            errors.append(f"Нет поля {item}")
    if not isinstance (data.get('priority', ''), int):
        errors.append("Поле priority должно быть числом")
    if errors:
        return Response(content=errors, status_code=400)
    task = {
        'title': data.get('title'),
        'description': data.get('description'),
        'priority': int(data.get('priority')),
        'date': datetime.now().strftime('%Y.%m.%d %H:%M')
    }
    tasks = read_tasks()
    tasks.append(task)
    write_tasks(tasks)
    return Response(content=task, status_code=201)


@app.delete('/')
def delete(r: Request) -> Response:
    title = r.query_params.get('title')
    if not title:
        return Response(content=['Нет поля title'], status_code=400)
    tasks = read_tasks()
    new_tasks = [
        task
        for task in tasks
        if task.get('title') != title
    ]
    if len(new_tasks) == len(tasks):
        return Response(content=['Нет такой task'], status_code=404)
    write_tasks(new_tasks)
    return Response(content=None, status_code=204)
