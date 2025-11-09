from models.Trabajos import Trabajo
from .Factory import Pagina
from concurrent.futures import ThreadPoolExecutor
class PeruTrabajos(Pagina):
    URL = "https://www.perutrabajos.com/buscar-empleo.php?"
    pages: bool = False
    
    def set_pages(self):
        paginas = self.soup.find("section", class_="pagination")
        if paginas:
            self.pages = True            
    
    #def __init__(self):
            #self.obtener_html()
            #self.set_pages()
            
        
    def obtener_trabajos(self, q: str, page: int = 1):
        temp_url = self.URL + "page="+ str(page) +"&sort=1-fechapublicacion&"+ "q=" + q + "&dep=0"
        self.obtener_html(URL = temp_url)
        #trabajos = self.soup.find_all("article", class_="puesto")
        trabajos = self.soup.find_all("div", class_="puesto__texto")
        if len(trabajos) == 0:
            return
        #return trabajos
        #self.TRABAJOS.append(Trabajo(cargo="Prueba", empresa="Empresa X", enlace=temp_url, descripcion=len(trabajos)))
        for trabajo in trabajos:
            cargo = trabajo.find("strong").text.strip()
            empresa = trabajo.find("h3").text.strip()
            ubicacion = trabajo.find("i", class_="icon-location").next_sibling.strip()
            sueldo = trabajo.find("i", class_="icon-moneda").next_sibling.strip() if trabajo.find("i", class_="icon-moneda") else "No especificado"
            fech_finalizacion = trabajo.find("i", class_="icon-calendario").next_sibling.strip() if trabajo.find("i", class_="icon-calendario") else "No especificado"
            formacion = trabajo.find("p").find("strong").next_sibling.strip()
            enlace = trabajo.find("a")["href"]
            nuevo_trabajo = Trabajo(
                cargo=cargo,    
                empresa=empresa,
                formacion= formacion,
                ubicacion=ubicacion,
                sueldo = sueldo,
                fech_finalizacion=fech_finalizacion,
                enlace=enlace,
                fuente="PeruTrabajos"
                )
            if nuevo_trabajo not in self.TRABAJOS:
                self.TRABAJOS.append(nuevo_trabajo)
        self.obtener_trabajos(q=q, page=page + 1)
    def find_jobs(self):
        #temp_url = self.URL + "q=" + "+".join(self.CLAVE[0])
        #self.obtener_trabajos(q=self.CLAVE[1])
        for clave in self.CLAVE:
            self.obtener_trabajos(q=clave)
            self.sector_privado()
        with ThreadPoolExecutor(max_workers=5) as executor:
            futuros = [executor.submit(trabajo.info_pagina) for trabajo in self.TRABAJOS]
    def sector_privado(self):
        temp_url = "https://www.perutrabajos.com/oportunidades-en-SECTOR-PRIVADO-2.html"
        self.obtener_html(URL=temp_url)
        trabajos = self.soup.find_all("div", class_="post__content")
        for trabajo in trabajos:
            formacion = trabajo.find_all("li")[-1].find("strong").text.strip()
            if True in [True if palabra.lower() in formacion.lower() else False for palabra in ["Informática", "Computación", "Sistemas", "Ingeniería"]]:
                cargo = trabajo.find("section", class_="post__header").find("p").text
                empresa = trabajo.find("i", class_="icon-business").next_sibling.next_sibling.text
                fecha_finalizacion = trabajo.find("i", class_="icon-calendario").next_sibling.next_sibling.text[-10:]
                ubicacion = trabajo.find("i", class_="icon-location").next_sibling.next_sibling.text 
                sueldo = trabajo.find("i", class_="icon-moneda").next_sibling.next_sibling.text
                enlace = trabajo.find("a")["href"]
                fuente = "PeruTrabajos-Sector Privado"
                nuevo_trabajo = Trabajo(
                    cargo=cargo,
                    empresa=empresa,
                    ubicacion=ubicacion,
                    enlace=enlace,
                    fech_finalizacion=fecha_finalizacion,
                    sueldo=sueldo,
                    formacion=formacion,
                    fuente=fuente
                )
                if nuevo_trabajo not in self.TRABAJOS:
                    self.TRABAJOS.append(nuevo_trabajo)


        

            
            
        
        