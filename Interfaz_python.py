import cx_Oracle
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

def validar_profesor(correo_ingresado):
    connection = cx_Oracle.connect(user="IDD", password="GRUPO", dsn="localhost:1521/xe")
    cursor = connection.cursor()

    resultado = cursor.var(cx_Oracle.STRING)
    cursor.callproc("Validar_Profesor_Login", [correo_ingresado, resultado])
    connection.close()

    return resultado.getvalue() == "Acceso Permitido"

def mostrar_trabajos(profesor_id, curso_id):
    connection = cx_Oracle.connect(user="IDD", password="GRUPO", dsn="localhost:1521/xe")
    cursor = connection.cursor()

    cursor.callproc("Mostrar_Trabajos_Curso", [profesor_id, curso_id])
    connection.close()

def login():
    correo = correo_entry.get()

    if validar_profesor(correo):
        messagebox.showinfo("Login", "Acceso Permitido")
        abrir_ventana_trabajos()
    else:
        messagebox.showerror("Login", "Acceso Denegado")

def abrir_ventana_trabajos():
    def consultar_trabajos():
        profesor_id = profesor_id_entry.get()
        curso_id = curso_id_entry.get()

        if profesor_id.isdigit() and curso_id.isdigit():
            try:
                mostrar_trabajos(int(profesor_id), int(curso_id))
                messagebox.showinfo("Consulta", "Trabajos mostrados en la consola del servidor.")
            except Exception as e:
                messagebox.showerror("Error", str(e))
        else:
            messagebox.showerror("Entrada Inválida", "Ingrese valores numéricos válidos.")

    trabajos_window = tk.Toplevel(root)
    trabajos_window.title("Trabajos de Investigación")
    trabajos_window.geometry("400x300")
    trabajos_window.configure(bg="#f4f4f4")

    ttk.Label(trabajos_window, text="ID de Profesor:").pack(pady=10)
    profesor_id_entry = ttk.Entry(trabajos_window, font=("Arial", 12))
    profesor_id_entry.pack(pady=5)

    ttk.Label(trabajos_window, text="ID del Curso:").pack(pady=10)
    curso_id_entry = ttk.Entry(trabajos_window, font=("Arial", 12))
    curso_id_entry.pack(pady=5)

    consultar_button = ttk.Button(trabajos_window, text="Consultar Trabajos", command=consultar_trabajos)
    consultar_button.pack(pady=20)

root = tk.Tk()
root.title("Login de Profesor")
root.geometry("500x300")
root.configure(bg="#e8f0fe")

frame = ttk.Frame(root, padding=20)
frame.pack(expand=True)

ttk.Label(frame, text="Correo Electrónico:", font=("Arial", 14)).pack(pady=10)
correo_entry = ttk.Entry(frame, font=("Arial", 14), width=30)
correo_entry.pack(pady=10)

login_button = ttk.Button(frame, text="Iniciar Sesión", command=login)
login_button.pack(pady=20)

root.mainloop()
