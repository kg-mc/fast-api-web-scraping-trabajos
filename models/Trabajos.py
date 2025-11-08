from bs4 import BeautifulSoup
import requests


class Trabajo:
    cargo: str = None
    empresa: str = None
    ubicacion: str = None
    enlace: str = None
    fech_finalizacion: str = None
    sueldo: str = None
    experiencia: str = None
    formacion: str = None
    fuente: str = "Desconocido"
    def to_dict(self):
        return {
            "cargo": self.cargo,
            "empresa": self.empresa,
            "ubicacion": self.ubicacion,
            "enlace": self.enlace,
            "fech_finalizacion": self.fech_finalizacion,
            "sueldo": self.sueldo,
            "experiencia": self.experiencia,
            "formacion": self.formacion,
            "fuente": self.fuente,
        }

    def __repr__(self):
        return f"Trabajo(cargo={self.cargo}, empresa={self.empresa}, ubicacion={self.ubicacion}, enlace={self.enlace}, fech_finalizacion={self.fech_finalizacion}, sueldo={self.sueldo}, descripcion={self.descripcion})"
    
    def __str__(self):
        return f"{self.cargo} at {self.empresa} in {self.ubicacion}. More info: {self.enlace}"
    def __init__(self, cargo=None, empresa=None, ubicacion=None, enlace=None, fech_finalizacion=None, sueldo=None, experiencia=None, formacion = None, fuente = "Desconocido"):
        self.cargo = cargo
        self.empresa = empresa
        self.ubicacion = ubicacion
        self.enlace = enlace
        self.fech_finalizacion = fech_finalizacion[-10:]
        self.sueldo = sueldo
        self.experiencia = experiencia   
        self.formacion = formacion
        self.fuente = fuente
        
    def __eq__(self, other) -> bool:
        if not isinstance(other, Trabajo):
            return NotImplemented
        return (self.cargo == other.cargo and
                self.empresa == other.empresa and
                self.ubicacion == other.ubicacion and
                self.fech_finalizacion == other.fech_finalizacion)
    def info_pagina(self):
        if self.fuente == "PeruTrabajos":
            #print("Hola mundo")
            response = requests.get(self.enlace, headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36'
            })
            soup = BeautifulSoup(response.content, 'html.parser')
            self.experiencia = soup.find("div", class_="requisitos").find("ul").text.strip()
        else:
            return   