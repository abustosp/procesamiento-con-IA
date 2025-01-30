import tkinter as tk
import tkinter.ttk as ttk
from bin.reconocedor import credenciales, consulta_requests_restantes, select_folder_and_analyze_pdfs
from tkinter import messagebox
import webbrowser

def consulta_requests_restantes_valor():
    
    response = consulta_requests_restantes()
    keys_values = "\n".join([f"{key}: {value}" for key, value in response.items()])
    messagebox.showinfo("Consultas Restantes", f"Response:\n{keys_values}")


def donaciones():
    webbrowser.open("https://cafecito.app/abustos")


class AppIA:
    def __init__(self, master=None):
        # build ui
        Toplevel_1 = tk.Tk() if master is None else tk.Toplevel(master)
        Toplevel_1.configure(background="#2e2e2e", height=250, width=325)
        try:
            Toplevel_1.iconbitmap("bin/ABP-blanco-en-fondo-negro.ico")
        except:
            pass
        Toplevel_1.minsize(325, 320)
        Toplevel_1.resizable(False, False)
        Toplevel_1.title("Procesador IA")
        Label_3 = ttk.Label(Toplevel_1)
        self.img_ABPblancosinfondo = tk.PhotoImage(
            file="bin/ABP-blanco-sin-fondo.png")
        Label_3.configure(
            background="#2e2e2e",
            image=self.img_ABPblancosinfondo)
        Label_3.pack(side="top")
        Label_1 = ttk.Label(Toplevel_1)
        Label_1.configure(
            background="#2e2e2e",
            foreground="#ffffff",
            justify="center",
            takefocus=False,
            text='Reconocedor y extractor de Facturas con\nInteligencia Artificial\n',
            wraplength=325
            )
        Label_1.pack(expand=True, side="top")
        Label_2 = ttk.Label(Toplevel_1)
        Label_2.configure(
            background="#2e2e2e",
            foreground="#ffffff",
            justify="center",
            text='por Agustín Bustos Piasentini\nhttps://www.Agustin-Bustos-Piasentini.com.ar/')
        Label_2.pack(expand=True, side="top")
        
        # crear función para abrir archivos de texto en una ventana emergente, con un botón de guardar
        def abrir_archivo_de_texto(archivo):
            with open(archivo, "r") as file:
                text = file.read()
            Toplevel_2 = tk.Toplevel()
            Toplevel_2.title(archivo)
            Text_1 = tk.Text(Toplevel_2)
            Text_1.insert(tk.END, text)
            Text_1.pack(expand=True, fill="both")
            
            def guardar_cambios():
                with open(archivo, "w") as file:
                    file.write(Text_1.get("1.0", tk.END))
                messagebox.showinfo("Guardado", "El archivo ha sido guardado exitosamente.")
            
            Button_1 = ttk.Button(Toplevel_2)
            Button_1.configure(text='Guardar', command=guardar_cambios)
            Button_1.pack(expand=True, side="top")
            Toplevel_2.mainloop()
            
        self.Configuraciones = ttk.Button(Toplevel_1, name="configuraciones")
        self.Configuraciones.configure(text='Editar configuraciones', command=lambda: abrir_archivo_de_texto(".env"))
        self.Configuraciones.pack(expand=True, pady=4, side="top")
        
        self.EditarPromptGeneral = ttk.Button(Toplevel_1, name="editarPromptGeneral")
        self.EditarPromptGeneral.configure(text='Editar Prompt General', command=lambda: abrir_archivo_de_texto("promt-general.txt"))
        self.EditarPromptGeneral.pack(expand=True, pady=4, side="top")
        
        self.Consultas_restantes = ttk.Button(Toplevel_1, name="consultas_restantes")
        self.Consultas_restantes.configure(text='Consultas Restantes', command=consulta_requests_restantes_valor)
        self.Consultas_restantes.pack(expand=True, pady=4, side="top")
        
        self.Seleccionar_Carpeta_Procesar = ttk.Button(Toplevel_1, name="seleccionar_Carpeta_Procesar")
        self.Seleccionar_Carpeta_Procesar.configure(text='Seleccionar Carpeta a Procesar' , command=select_folder_and_analyze_pdfs)
        self.Seleccionar_Carpeta_Procesar.pack(expand=True, pady=4, side="top")
        
        self.Donaciones = ttk.Button(Toplevel_1, name="donaciones")
        self.Donaciones.configure(text='Donaciones', command=donaciones)
        self.Donaciones.pack(expand=True, pady=4, side="top")

        # Main widget
        self.mainwindow = Toplevel_1

    def run(self):
        self.mainwindow.mainloop()


if __name__ == "__main__":
    app = AppIA()
    app.run()
