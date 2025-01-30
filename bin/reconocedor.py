import os
import csv
import tkinter as tk
from tkinter import filedialog
from tkinter.messagebox import showinfo
from dotenv import load_dotenv
import os
import requests
import PyPDF2 as pypdf
import io
import json


def credenciales():
    
    load_dotenv(override=True)
    
    url = os.getenv("URL")    
    mail = os.getenv("MAIL")
    key = os.getenv("API_KEY")
    
    return url, mail, key


def consulta_requests_restantes():
    
    url, mail, key = credenciales()
    
    endpoint = f"{url}/users/remaining-queries/"
    
    params = {
        "email": mail,
        "api_key": key
    }
    
    response = requests.get(endpoint, params=params)
    
    return response.json()


def consulta_reconocedor_pdf_individual(pdf_path):
    
    url, mail, key = credenciales()
    
    # Leer el archivo PDF completo
    with open(pdf_path, "rb") as pdf_file:
        pdf_reader = pypdf.PdfReader(pdf_file)
        first_page = pdf_reader.pages[0]

        # Crear un objeto PDF temporal solo con la primera página
        pdf_writer = pypdf.PdfWriter()
        pdf_writer.add_page(first_page)

        # Crear un archivo temporal en memoria para almacenar el PDF de la primera página
        temp_pdf_bytes = bytearray()
        with io.BytesIO() as temp_pdf_file:
            pdf_writer.write(temp_pdf_file)
            temp_pdf_file.seek(0)
            temp_pdf_bytes = temp_pdf_file.read()

    endpoint = f"{url}/analyze-invoice/"
    params = {
        "api_key": key,
        "email": mail
    }
    
    files = {
        "file": ("temp.pdf", temp_pdf_bytes, "application/pdf")
    }

    response = requests.post(endpoint, params=params, files=files)

    return response.json()


def select_folder_and_analyze_pdfs():
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        os.listdir(folder_selected)
        result_folder = os.path.join(folder_selected, "Resultado")
        pdf_files = [file for file in os.listdir(folder_selected) if file.endswith(".pdf")]
        for pdf_file in pdf_files:
            pdf_path = os.path.join(folder_selected, pdf_file)
            response = consulta_reconocedor_pdf_individual(pdf_path)
            
            os.makedirs(result_folder, exist_ok=True)
            result_file = os.path.join(result_folder, f"{pdf_file}.json")
            
            json.dump(response, open(result_file, "w"))


if __name__ == "__main__":
    #url, mail, key = credenciales()
    response = consulta_requests_restantes()
    # response = consulta_reconocedor_pdf_individual(mail, url, "/home/abp/Downloads/20374730429_011_00001_00000120.pdf")
    # response = select_folder_and_analyze_pdfs()
    print(response)