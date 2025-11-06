from fastapi import FastAPI
from models.Factory import Fabricator
from database import supabase

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/check-db")
async def check_db():
    try:
        response = supabase.table("test_table").select("*").execute()
        return {"status": "success", "data": response.data}
    except Exception as e:
        return {"status": "error", "message": str(e)}

    
@app.get("/jobs/{site_name}")
async def get_jobs(site_name: str):

    try:
        job_site = Fabricator.get_job_site(site_name)
        jobs = job_site.get_jobs()
        #return {"jobs": [job.to_dict() for job in jobs]}
        return jobs
    except ValueError as e:
        return {"error": str(e)}
    
@app.on_event("startup")
async def startup_event():
    #table_name = "trabajo"
    try:
        job_site = Fabricator.get_job_site("PeruTrabajos")
        jobs = job_site.get_jobs()
    except Exception as e:
        print(e)