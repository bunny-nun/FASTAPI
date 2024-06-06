from typing import List
from fastapi import FastAPI
import logging
from models import TaskIn, TaskOut
from db import db, tasks

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()


@app.on_event('startup')
async def startup():
    await db.connect()


@app.on_event('shutdown')
async def shutdown():
    await db.disconnect()


@app.get('/tasks/', response_model=List[TaskOut])
async def read_tasks():
    logger.info('Отработал GET запрос')
    query = tasks.select()
    return await db.fetch_all(query)


@app.get('/tasks/{task_id}', response_model=TaskOut)
async def read_task_by_id(task_id: int):
    logger.info('Отработал GET запрос')
    query = tasks.select().where(tasks.c.task_id == task_id)
    return await db.fetch_one(query)


@app.post('/tasks/', response_model=TaskOut)
async def create_task(new_task: TaskIn):
    logger.info('Отработал POST запрос')
    query = tasks.insert().values(**new_task.dict())
    last_record_id = await db.execute(query)
    return {**new_task.dict(), 'task_id': last_record_id}


@app.put('/tasks/{task_id}', response_model=TaskOut)
async def update_task_by_id(task_id: int, updated_task: TaskIn):
    logger.info(f'Отработал PUT запрос для задачи с id {task_id}')
    query = (tasks.update().where(tasks.c.task_id == task_id).
             values(**updated_task.dict()))
    await db.execute(query)
    return {**updated_task.dict(), 'task_id': task_id}


@app.delete('/tasks/{task_id}')
async def delete_task_by_id(task_id: int):
    logger.info(f'Отработал DELETE запрос для задачи с id {task_id}')
    query = tasks.delete().where(tasks.c.task_id == task_id)
    await db.execute(query)
    return {'message': 'Task deleted'}
