from bs4 import BeautifulSoup
import requests
from database import supabase
from .Trabajos import Trabajo
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
        if len(self.TRABAJOS) == 0:
            #extraer de la base de datos
            response = supabase.table("trabajo").select("*").execute()
            for item in response.data:
                trabajo = Trabajo(
                    cargo=item.get("cargo"),
                    empresa=item.get("empresa"),
                    ubicacion=item.get("ubicacion"),
                    enlace=item.get("enlace"),
                    fech_finalizacion=item.get("fech_finalizacion"),
                    sueldo=item.get("sueldo"),
                    experiencia=item.get("experiencia"),
                    formacion=item.get("formacion"),
                    fuente=item.get("fuente")
                )
                self.TRABAJOS.append(trabajo)

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