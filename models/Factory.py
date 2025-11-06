from bs4 import BeautifulSoup
import requests
from database import supabase

class Pagina:
    URL: str
    soup: BeautifulSoup
    HEADERS: dict = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36'
    }
    CLAVE: list = [
        "Sistemas",
        "Computación",
        "Informática"
    ]
    TRABAJOS: list = []
    
    def obtener_html(self, URL: str = None):
        try:
            if URL == None:
                URL = self.URL
            response = requests.get(URL, headers=self.HEADERS)
            self.soup = BeautifulSoup(response.content, 'html.parser')
        except requests.RequestException as e:
            print("Hubo un error! 😭", e)
    
    
    def find_jobs(self):
        return NotImplementedError("No implementado aun.")
    def get_jobs(self):
        if self.consulta_db() == False:
                self.find_jobs()
                trabajos_dict = [t.to_dict() for t in self.TRABAJOS]

                response = supabase.table("trabajo").insert(trabajos_dict).execute()

        return self.TRABAJOS
    def consulta_db(self) ->bool:
        response = supabase.table("trabajo").select("*").limit(1).execute()
        if len(response.data) > 0:
            return True
        return False

class Fabricator:
    @staticmethod
    def get_job_site(site_name):
        if site_name == "PeruTrabajos":
            from .PeruTrabajos import PeruTrabajos
            return PeruTrabajos()
        raise ValueError(f"Pagina desconocida: {site_name}")