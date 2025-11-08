from fastapi import FastAPI
from models.Factory import Fabricator
from database import supabase
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime    
app = FastAPI()
        
valores = {
    "actualizaciones": [],
    "paginas_consultadas": {
        "PeruTrabajos": 0,
    }
}
scheduler = BackgroundScheduler()

def obtener_trabajos():
    supabase.table("trabajo").delete().neq("id", 0).execute()
    for pagina in valores["paginas_consultadas"]:
        job_site = Fabricator.get_job_site(pagina)
        jobs = job_site.get_jobs()
        valores["paginas_consultadas"][pagina] += len(job_site.TRABAJOS)
        



def tarea_diaria():
    valores["actualizaciones"].append(datetime.now())
    #reset table trabajo (delete all rows ) and eject  the functino on startup to refill it
    obtener_trabajos()    
    
scheduler.add_job(tarea_diaria, 'interval', hours=8)

scheduler.start()

@app.on_event("shutdown")
def shutdown_event():
    scheduler.shutdown()
    
    
    
@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/check-db")
async def check_db():
    try:
        response = supabase.table("test_table").select("*").    execute()
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
        #valor.append(datetime.now())
        #job_site = Fabricator.get_job_site("PeruTrabajos")
        #jobs = job_site.get_jobs()
        tarea_diaria()
    except Exception as e:
        print(e)
    

# Endpoint to get the actualizaciones          
@app.get("/actualizacion")
async def get_actualizaciones():
    return valores