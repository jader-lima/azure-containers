import os
from fastapi import FastAPI, HTTPException
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
import pandas as pd
from dotenv import load_dotenv
import numpy as np

load_dotenv()

DATABASE_URL = f"postgresql+psycopg2://{os.getenv('COMPANY_PG_USER')}:{os.getenv('COMPANY_PG_PASSWORD')}@{os.getenv('COMPANY_PG_HOST')}:{os.getenv('COMPANY_PG_PORT')}/{os.getenv('COMPANY_PG_BD_NAME')}"
engine = create_engine(DATABASE_URL)

app = FastAPI()

async def insert_data_into_table(data: pd.DataFrame, table_name: str, upsert_query: str):    
    try:
        data = data.fillna(np.nan).replace([np.nan], [None])
        with engine.begin() as connection:
            for row in data.to_dict(orient="records"):
                connection.execute(text(upsert_query), row)


        return {"status": "success", "message": f"Data inserted into {table_name}"}
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=f"Data format error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

@app.post("/upload/departments/")
async def upload_departments(file_path: str):
    columns = ["id", "department"]
    upsert_query = """
                INSERT INTO departments (id, department)
                VALUES (:id, :department)
                ON CONFLICT (id)
                DO UPDATE SET department = EXCLUDED.department;
                """
    try:
        data = pd.read_csv(file_path,header=None, names=columns)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="File not found. Please check the file path.")
    except pd.errors.EmptyDataError:
        raise HTTPException(status_code=400, detail="File is empty.")
    except pd.errors.ParserError:
        raise HTTPException(status_code=400, detail="Error parsing CSV file. Check file format.")

    response = await insert_data_into_table(data, "departments", upsert_query)
    return response

@app.post("/upload/jobs/")
async def upload_jobs(file_path: str):
    columns = ["id", "jobs"]
    upsert_query = """
                    INSERT INTO jobs (id, jobs)
                    VALUES (:id, :jobs)
                    ON CONFLICT (id)
                    DO UPDATE SET jobs = EXCLUDED.jobs;
                """
    try:
        data = pd.read_csv(file_path,header=None, names=columns)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="File not found. Please check the file path.")
    except pd.errors.EmptyDataError:
        raise HTTPException(status_code=400, detail="File is empty.")
    except pd.errors.ParserError:
        raise HTTPException(status_code=400, detail="Error parsing CSV file. Check file format.")

    response = await insert_data_into_table(data, "jobs", upsert_query)
    return response

@app.post("/upload/hired_employees/")
async def upload_hired_employees(file_path: str):
    columns = ["id", "name", "datetime", "department_id", "job_id"]
    upsert_query = """
                INSERT INTO hired_employees (id, name, datetime, department_id, job_id)
                VALUES (:id, :name, :datetime, :department_id, :job_id)
                ON CONFLICT (id)
                DO UPDATE SET
                    name = EXCLUDED.name,
                    datetime = EXCLUDED.datetime,
                    department_id = EXCLUDED.department_id,
                    job_id = EXCLUDED.job_id;
                """
    try:
        data = pd.read_csv(file_path,header=None, names=columns)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="File not found. Please check the file path.")
    except pd.errors.EmptyDataError:
        raise HTTPException(status_code=400, detail="File is empty.")
    except pd.errors.ParserError:
        raise HTTPException(status_code=400, detail="Error parsing CSV file. Check file format.")

    response = await insert_data_into_table(data, "hired_employees", upsert_query)
    return response

@app.get("/departments/")
async def get_departments():
    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT * FROM departments")).mappings().all()
            departments = [dict(row) for row in result]
        return {"departments": departments}
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@app.get("/jobs/")
async def get_jobs():
    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT * FROM jobs")).mappings().all()
            jobs = [dict(row) for row in result]
        return {"jobs": jobs}
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@app.get("/employees/")
async def get_employees():
    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT * FROM hired_employees")).mappings().all()
            employees = [dict(row) for row in result]
        return {"employees": employees}
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")