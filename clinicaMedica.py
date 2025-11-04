import customtkinter as ctk
from PIL import Image
from tkinter import messagebox
from tkcalendar import DateEntry
from tkinter import ttk
import sqlite3
from datetime import datetime
import os

try:
    from base_de_datos.DataBase import BaseDatos, Usuario, Doctor, Contador, Paciente, Proveedor
except ImportError:
    print("ERROR: No se pudo importar BaseDatos. Asegúrate de que DataBase.py existe.")
    raise


db = BaseDatos()
usuario_actual = None


FONT_FAMILY = "Edwardian Script ITC"

LILA = "#e9c7fb"
MAGENTA = "#560554"
MORADO_VIVO = "#bd7efb"
ROSADO = "#FDC2FE"
BOTON_USUARIO = "#F0E8F8"
MORADO_CLARO = "#C67EE7"
FONDO_CONTADOR = "#A9EAFE"
FONDO_CONTADOR_CLARO = "#D5F5E3"
GRIS_CLARO_CONTADOR = "#D1E0E8"
CAFE_PROVEEDOR = "#774d29"
CAFE_CLARO = "#9a6f49"

ctk.set_appearance_mode("Light")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.update()
app.state('zoomed')
app.title("Inicio de Sesión")


def agregar_paciente():
    sub = ctk.CTkToplevel(app)
    sub.title("Agregar Paciente")
    sub.state('zoomed')
    sub.configure(fg_color="white")

    sub.transient(app)
    sub.grab_set()
    sub.lift()
    sub.focus_force()

    sub.grid_rowconfigure(0, weight=1)
    sub.grid_columnconfigure(0, weight=0)
    sub.grid_columnconfigure(1, weight=2)
    sub.grid_columnconfigure(2, weight=1)

    side_panel = ctk.CTkFrame(master=sub, corner_radius=0, fg_color=MORADO_VIVO, width=300)
    side_panel.grid(row=0, column=0, sticky="nsew")

    header_frame = ctk.CTkFrame(master=side_panel, fg_color=BOTON_USUARIO, corner_radius=20, width=200, height=60)
    header_frame.place(x=30, y=25)
    ctk.CTkLabel(master=header_frame, text="Dr. Maggie", font=ctk.CTkFont(size=30, weight="bold"),
                 text_color=MAGENTA).place(relx=0.5, rely=0.5, anchor="center")

    try:
        logo_path = "Logo.png"
        logo_pil_image = Image.open(logo_path)
        logo_ctk_image = ctk.CTkImage(light_image=logo_pil_image, dark_image=logo_pil_image, size=(250, 250))
        logo_label = ctk.CTkLabel(master=side_panel, image=logo_ctk_image, text="")
        logo_label.place(relx=0.5, rely=0.5, anchor="center")
    except Exception:
        ctk.CTkLabel(master=side_panel, text="[Dra. Angie Ajquill\nGinecología y Obstetricia]",
                     font=ctk.CTkFont(size=20, weight="bold"), text_color="white", justify="center").place(relx=0.5,
                                                                                                           rely=0.6,
                                                                                                           anchor="center")

    main_content = ctk.CTkFrame(master=sub, fg_color="white", corner_radius=0)
    main_content.grid(row=0, column=1, sticky="nsew")

    main_content.grid_columnconfigure(0, weight=1)
    main_content.grid_columnconfigure(1, weight=2)
    main_content.grid_columnconfigure(2, weight=1)

    main_content.grid_rowconfigure(0, weight=0)
    main_content.grid_rowconfigure(1, weight=0)
    main_content.grid_rowconfigure(2, weight=1)
    main_content.grid_rowconfigure(3, weight=0)

    ctk.CTkLabel(master=main_content, text="Agregar paciente",
                 fg_color=MORADO_VIVO, text_color=MAGENTA,
                 font=ctk.CTkFont(size=30, weight="bold"),
                 corner_radius=40, width=320, height=60
                 ).grid(row=0, column=0, columnspan=2, pady=(20, 20), padx=40, sticky="w")

    ctk.CTkButton(master=main_content, text="Cerrar ventana",
                  command=sub.destroy, fg_color=MAGENTA, text_color="white",
                  hover_color=MORADO_CLARO, font=ctk.CTkFont(size=20, weight="bold"),
                  corner_radius=20, width=220, height=60
                  ).grid(row=0, column=2, sticky="e", padx=(0, 40), pady=(20, 20))

    form_frame = ctk.CTkFrame(master=main_content, fg_color="transparent")
    form_frame.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=(60, 0), pady=(100, 100))
    form_frame.grid_columnconfigure(0, weight=1)
    form_frame.grid_columnconfigure(1, weight=3)

    CAMPOS = ["Nombre:", "DPI:", "No. Tel:"]
    entries = {}

    for i, label_text in enumerate(CAMPOS):
        ctk.CTkLabel(master=form_frame, text=label_text,
                     text_color=MAGENTA, font=ctk.CTkFont(size=20, weight="bold"),
                     ).grid(row=i, column=1, sticky="e", padx=(0, 20), pady=20)

        entry = ctk.CTkEntry(master=form_frame,
                             placeholder_text=f"Ingrese {label_text.replace(':', '')}",
                             width=600, height=60,
                             fg_color="white", text_color="black",
                             font=ctk.CTkFont(size=20), border_width=0
                             )
        entry.grid(row=i, column=2, sticky="w", padx=(0, 80), pady=20)
        entries[label_text] = entry

    try:
        img_path = "paciente.jpg"
        paciente_pil = Image.open(img_path)
        paciente_img = ctk.CTkImage(light_image=paciente_pil, dark_image=paciente_pil, size=(300, 300))
        ctk.CTkLabel(master=main_content, image=paciente_img, text="").grid(row=1, column=2, padx=40, pady=(150, 10),
                                                                            sticky="n")
    except Exception as e:
        print(f"No se pudo cargar imagen del paciente: {e}")
        ctk.CTkLabel(master=main_content, text="[Imagen paciente]", text_color="gray",
                     font=ctk.CTkFont(size=20, slant="italic")).grid(row=1, column=2, padx=40, pady=10, sticky="n")

    def guardar_paciente():
        nombre = entries["Nombre:"].get()
        dpi = entries["DPI:"].get()
        tel = entries["No. Tel:"].get()

        if nombre and dpi and tel:
            try:

                nuevo_paciente = Paciente(DPI=dpi, nombre=nombre, telefonos=tel, db=db)
                nuevo_paciente.guardar()
                messagebox.showinfo("Éxito", f"Paciente guardado: {nombre}")
                sub.destroy()
            except sqlite3.IntegrityError:
                messagebox.showerror("Error", f"El DPI {dpi} ya está registrado.")
            except Exception as e:
                messagebox.showerror("Error", f"Ocurrió un error al guardar: {e}")
        else:
            messagebox.showwarning("Advertencia", "Todos los campos son obligatorios.")

    ctk.CTkButton(master=main_content, text="Guardar",
                  command=guardar_paciente, fg_color=ROSADO, text_color=MAGENTA,
                  hover_color="transparent", font=ctk.CTkFont(size=24, weight="bold"),
                  corner_radius=30, width=300, height=80
                  ).grid(row=2, column=0, columnspan=3, pady=(10, 40), sticky="n")


def buscar_paciente():
    sub = ctk.CTkToplevel(app)
    sub.title("Buscar paciente")
    sub.state('zoomed')
    sub.configure(fg_color="white")

    sub.transient(app)
    sub.grab_set()
    sub.lift()
    sub.focus_force()

    sub.grid_columnconfigure(0, weight=0)
    sub.grid_columnconfigure(1, weight=1)
    sub.grid_rowconfigure(0, weight=1)

    side_panel = ctk.CTkFrame(master=sub, corner_radius=0, fg_color=MORADO_VIVO, width=300)
    side_panel.grid(row=0, column=0, sticky="nsew")

    header_frame = ctk.CTkFrame(master=side_panel, fg_color=BOTON_USUARIO, corner_radius=20, width=200, height=60)
    header_frame.place(x=30, y=25)
    ctk.CTkLabel(master=header_frame, text="Dr. Maggie",
                 font=ctk.CTkFont(size=30, weight="bold"),
                 text_color=MAGENTA).place(relx=0.5, rely=0.5, anchor="center")
    try:
        logo_path = "Logo.png"
        logo_pil_image = Image.open(logo_path)
        logo_ctk_image = ctk.CTkImage(light_image=logo_pil_image, dark_image=logo_pil_image, size=(250, 250))
        logo_label = ctk.CTkLabel(master=side_panel, image=logo_ctk_image, text="")
        logo_label.place(relx=0.5, rely=0.5, anchor="center")
    except Exception:
        ctk.CTkLabel(master=side_panel, text="[Dra. Angie Ajquill\nGinecología y Obstetricia]",
                     font=ctk.CTkFont(size=20, weight="bold"), text_color="white", justify="center").place(relx=0.5,
                                                                                                           rely=0.5,
                                                                                                           anchor="center")

    main_content = ctk.CTkFrame(master=sub, fg_color="white", corner_radius=0)
    main_content.grid(row=0, column=1, sticky="nsew")
    main_content.grid_columnconfigure(0, weight=0)  ##

    ctk.CTkLabel(master=main_content, text="Buscar datos de paciente", fg_color=MORADO_VIVO, text_color=MAGENTA,
                 font=ctk.CTkFont(size=30, weight="bold"),
                 corner_radius=40,
                 width=300,
                 height=60).grid(row=0, column=0, pady=(20, 40), padx=40, sticky="w")

    ctk.CTkButton(master=main_content, text="Cerrar ventana", command=sub.destroy, fg_color=MAGENTA, text_color="white",
                  hover_color=MORADO_CLARO,
                  font=ctk.CTkFont(size=22, weight="bold"),
                  corner_radius=20,
                  width=220,
                  height=70).grid(row=0, column=1, sticky="e", padx=40, pady=(20, 40))

    form_frame = ctk.CTkFrame(master=main_content, fg_color="transparent")
    form_frame.grid(row=1, column=0, columnspan=2, pady=(10, 50))
    form_frame.grid_columnconfigure(0, weight=1)
    form_frame.grid_columnconfigure(1, weight=2)

    label_frame = ctk.CTkFrame(master=form_frame, fg_color=MORADO_VIVO,
                               corner_radius=20, width=200, height=60)
    label_frame.grid(row=1, column=0, padx=(150, 30), pady=30, sticky="e")
    ctk.CTkLabel(master=label_frame, text="DPI: ",
                 text_color=MAGENTA,
                 font=ctk.CTkFont(size=22, weight="bold")).place(relx=0.5, rely=0.5, anchor="center")

    entry_frame = ctk.CTkFrame(master=form_frame, fg_color="white",
                               corner_radius=20, width=500, height=60)
    entry_frame.grid(row=1, column=1, padx=(20, 150), pady=30, sticky="w")
    entry = ctk.CTkEntry(master=entry_frame,
                         placeholder_text=f"Ingrese el DPI a buscar",
                         fg_color="white",
                         text_color="black",
                         font=ctk.CTkFont(size=20),
                         border_width=0,
                         width=460,
                         height=45)
    entry.place(relx=0.5, rely=0.5, anchor="center")

    def buscar():
        dpi = entry.get()
        if not dpi:
            messagebox.showwarning("Advertencia", "El campo DPI no puede estar vacío.")
            return


        paciente_row = db.ejecutar("SELECT nombre, telefono FROM pacientes WHERE DPI=?", (dpi,), fetch=True)

        if paciente_row:
            paciente = paciente_row[0]
            nombre_paciente = paciente["nombre"]
            tel_paciente = paciente["telefono"]

            messagebox.showinfo("Éxito", f"Paciente encontrado: {nombre_paciente}")
            sub.destroy()


            crear_ventana_ficha_medica(dpi, nombre_paciente, tel_paciente)

        else:
            messagebox.showerror("Error", f"Paciente con DPI {dpi} no encontrado. Por favor, agréguelo primero.")

    ctk.CTkButton(master=main_content, text="Buscar", command=buscar, fg_color=ROSADO, text_color=MAGENTA,
                  hover_color="#F0B4FB", font=ctk.CTkFont(size=26, weight="bold"), corner_radius=30, width=250,
                  height=80).grid(row=2, column=0, columnspan=2, pady=40)


def crear_ventana_ficha_medica(dpi_paciente, nombre_paciente, tel_paciente, procedencia=None, ocupacion=None,
                               fecha_nac=None, antecedentes=None, datos_consulta=None):

    ultima_ficha = db.ejecutar(
        "SELECT * FROM fichas WHERE paciente_id=? ORDER BY id DESC LIMIT 1",
        (dpi_paciente,),
        fetch=True
    )
    if ultima_ficha:
        f = ultima_ficha[0]
        procedencia = f['procedencia']
        ocupacion = f['ocupacion']
        fecha_nac = f['fecha_nacimiento']
        antecedentes = f['antecedentes']
        datos_consulta = f['datos']

    sub = ctk.CTkToplevel(app)
    sub.title("Crear Ficha Médica")
    sub.state('zoomed')
    sub.configure(fg_color="white")

    sub.transient(app)
    sub.grab_set()
    sub.lift()
    sub.focus_force()

    sub.grid_rowconfigure(0, weight=1)
    sub.grid_columnconfigure(0, weight=0)
    sub.grid_columnconfigure(1, weight=1)

    side_panel = ctk.CTkFrame(master=sub, corner_radius=0, fg_color=MORADO_VIVO, width=300)
    side_panel.grid(row=0, column=0, sticky="nsew")

    header_frame = ctk.CTkFrame(master=side_panel, fg_color=BOTON_USUARIO, corner_radius=20, width=200, height=60)
    header_frame.place(x=30, y=25)
    ctk.CTkLabel(master=header_frame, text="Dr.maggie",
                 font=ctk.CTkFont(size=30, weight="bold"),
                 text_color=MAGENTA).place(relx=0.5, rely=0.5, anchor="center")

    try:
        logo_path = "Logo.png"
        logo_pil_image = Image.open(logo_path)
        logo_ctk_image = ctk.CTkImage(light_image=logo_pil_image, dark_image=logo_pil_image, size=(250, 250))
        logo_label = ctk.CTkLabel(master=side_panel, image=logo_ctk_image, text="")
        logo_label.place(relx=0.5, rely=0.55, anchor="center")
    except Exception:
        ctk.CTkLabel(master=side_panel, text="[Dra. Angie Ajquill\nGinecología y Obstetricia]",
                     font=ctk.CTkFont(size=20, weight="bold"), text_color="white", justify="center").place(relx=0.5,
                                                                                                           rely=0.5,
                                                                                                           anchor="center")

    main_content = ctk.CTkFrame(master=sub, fg_color="white", corner_radius=0)
    main_content.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
    main_content.grid_columnconfigure(0, weight=1)
    main_content.grid_rowconfigure(3, weight=1)

    title_frame = ctk.CTkFrame(master=main_content, fg_color="transparent")
    title_frame.grid(row=0, column=0, sticky="ew", pady=(10, 0))
    title_frame.grid_columnconfigure(0, weight=1)
    title_frame.grid_columnconfigure(1, weight=0)

    ctk.CTkLabel(master=title_frame, text="Crear ficha médica",
                 fg_color=MORADO_VIVO, text_color=MAGENTA,
                 font=ctk.CTkFont(size=28, weight="bold"),
                 corner_radius=40, width=320, height=60
                 ).grid(row=0, column=0, sticky="w", padx=(30, 0))

    ctk.CTkButton(master=title_frame, text="Cerrar ventana",
                  command=sub.destroy, fg_color=MAGENTA, text_color="white",
                  hover_color=MORADO_CLARO, font=ctk.CTkFont(size=18, weight="bold"),
                  corner_radius=20, width=180, height=50
                  ).grid(row=0, column=1, sticky="e", padx=(0, 30))

    form_frame = ctk.CTkFrame(master=main_content, fg_color="transparent")
    form_frame.grid(row=1, column=0, sticky="nsew", padx=(60, 0), pady=(10, 10))
    form_frame.grid_columnconfigure((0, 1, 2), weight=1)

    entries = {}

    def campo(label_text, row, col_entry, colspan=1):

        entry = ctk.CTkEntry(master=form_frame, fg_color="white", text_color="black",
                             border_width=2, border_color=MORADO_VIVO, corner_radius=60, height=40,
                             placeholder_text=f"Ingrese la {label_text}",
                             font=ctk.CTkFont(size=16))
        entry.grid(row=row, column=col_entry, columnspan=colspan, padx=5, pady=8, sticky="ew")
        return entry

    ctk.CTkLabel(master=form_frame, text=f"Paciente: {nombre_paciente}",
                 fg_color=MORADO_VIVO, text_color="black",
                 font=ctk.CTkFont(size=16, weight="bold"),
                 corner_radius=20, anchor="center", height=40).grid(row=0, column=0, padx=5, pady=8, sticky="ew")

    ctk.CTkLabel(master=form_frame, text=f"DPI: {dpi_paciente}",
                 fg_color=MORADO_VIVO, text_color="black",
                 font=ctk.CTkFont(size=16, weight="bold"),
                 corner_radius=20, anchor="center", height=40).grid(row=0, column=1, padx=5, pady=8, sticky="ew")

    ctk.CTkLabel(master=form_frame, text=f"No. Tel: {tel_paciente}",
                 fg_color=MORADO_VIVO, text_color="black",
                 font=ctk.CTkFont(size=16, weight="bold"),
                 corner_radius=20, anchor="center", height=40).grid(row=0, column=2, padx=5, pady=8, sticky="ew")

    entries['procedencia'] = campo("Procedencia:", 1, 0)
    entries['ocupacion'] = campo("Ocupación:", 1, 1)
    entries['fecha_nac'] = ctk.CTkEntry(master=form_frame, fg_color="white", text_color="black",
                                        border_width=2, border_color=MORADO_VIVO, corner_radius=60, height=40,
                                        placeholder_text=f"Ingrese la Fecha de naciemiento (AAAA-MM-DD)",
                                        font=ctk.CTkFont(size=16))
    entries['fecha_nac'].grid(row=1, column=2, columnspan=1, padx=5, pady=8, sticky="ew")

    ctk.CTkFrame(master=form_frame, fg_color=MORADO_VIVO, corner_radius=20, height=50).grid(
        row=2, column=0, padx=5, pady=8, sticky="ew")
    ctk.CTkLabel(master=form_frame, text="Antecedentes:", font=ctk.CTkFont(size=16, weight="bold"),
                 text_color="black", anchor="w", fg_color=MORADO_VIVO, bg_color=MORADO_VIVO).grid(row=2, column=0,
                                                                                                  padx=20, pady=8,
                                                                                                  sticky="w")
    entries['antecedentes'] = ctk.CTkEntry(master=form_frame, fg_color=BOTON_USUARIO, text_color="black",
                                           border_width=0, corner_radius=20, height=50,
                                           font=ctk.CTkFont(size=16))
    entries['antecedentes'].grid(row=2, column=1, columnspan=2, padx=5, pady=8, sticky="ew")

    ctk.CTkFrame(master=form_frame, fg_color=MORADO_VIVO, corner_radius=20, height=50).grid(
        row=3, column=0, padx=5, pady=8, sticky="ew")
    ctk.CTkLabel(master=form_frame, text="Datos:", font=ctk.CTkFont(size=16, weight="bold"),
                 text_color="black", anchor="w", fg_color=MORADO_VIVO, bg_color=MORADO_VIVO).grid(row=3, column=0,
                                                                                                  padx=20, pady=8,
                                                                                                  sticky="w")

    ctk.CTkLabel(master=main_content, text="Ingrese los datos de la consulta:",
                 font=ctk.CTkFont(size=20, weight="bold"), text_color=MAGENTA
                 ).grid(row=2, column=0, padx=60, pady=(10, 5), sticky="w")

    consulta_textbox = ctk.CTkTextbox(master=main_content, height=220,
                                      corner_radius=20, border_width=2,
                                      border_color=LILA, fg_color="white",
                                      text_color="black", font=ctk.CTkFont(size=16))
    consulta_textbox.grid(row=3, column=0, sticky="nsew", padx=60, pady=(0, 10))

    if procedencia: entries['procedencia'].insert(0, procedencia)
    if ocupacion: entries['ocupacion'].insert(0, ocupacion)
    if fecha_nac: entries['fecha_nac'].insert(0, fecha_nac)
    if antecedentes: entries['antecedentes'].insert(0, antecedentes)
    if datos_consulta: consulta_textbox.insert("0.0", datos_consulta)

    def guardar_ficha():
        if usuario_actual.rol != "Doctor":
            messagebox.showerror("Error de Rol", "Solo un Doctor puede guardar una ficha médica.")
            return

        procedencia = entries['procedencia'].get()
        ocupacion = entries['ocupacion'].get()
        fecha_nac = entries['fecha_nac'].get()
        antecedentes = entries['antecedentes'].get()
        datos_consulta = consulta_textbox.get("1.0", "end-1c")

        if not procedencia or not ocupacion or not datos_consulta:
            messagebox.showwarning("Advertencia", "Debe llenar Procedencia, Ocupación y Datos de la Consulta.")
            return

        try:
            usuario_actual.crear_ficha_medica(
                paciente_id=dpi_paciente,
                datos=datos_consulta,
                procedencia=procedencia,
                ocupacion=ocupacion,
                antecedentes=antecedentes,
                fecha_nacimiento=fecha_nac
            )
            messagebox.showinfo("Éxito", "Ficha médica guardada correctamente.")
            sub.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Fallo al guardar la ficha: {e}")

    ctk.CTkButton(master=main_content, text="Guardar Ficha",
                  command=guardar_ficha, fg_color=ROSADO, text_color=MAGENTA,
                  hover_color="#F0B4FB", font=ctk.CTkFont(size=24, weight="bold"),
                  corner_radius=30, width=300, height=70
                  ).grid(row=4, column=0, pady=(20, 10))

#======================================================================
def crear_ventana_ficha_medica_actualizar(dpi_paciente, nombre_paciente, tel_paciente, procedencia=None, ocupacion=None,
                                          fecha_nac=None, antecedentes=None, datos_consulta=None):

    ficha_id_a_actualizar = None
    ultima_ficha = db.ejecutar(
        "SELECT id, procedencia, ocupacion, fecha_nacimiento, antecedentes, datos FROM fichas WHERE paciente_id=? ORDER BY id DESC LIMIT 1",
        (dpi_paciente,),
        fetch=True
    )
    if ultima_ficha:
        f = ultima_ficha[0]
        ficha_id_a_actualizar = f['id']
        procedencia = f['procedencia']
        ocupacion = f['ocupacion']
        fecha_nac = f['fecha_nacimiento']
        antecedentes = f['antecedentes']
        datos_consulta = f['datos']

    sub = ctk.CTkToplevel(app)
    sub.title("Crear Ficha Médica")
    sub.state('zoomed')
    sub.configure(fg_color="white")

    sub.transient(app)
    sub.grab_set()
    sub.lift()
    sub.focus_force()

    sub.grid_rowconfigure(0, weight=1)
    sub.grid_columnconfigure(0, weight=0)
    sub.grid_columnconfigure(1, weight=1)

    side_panel = ctk.CTkFrame(master=sub, corner_radius=0, fg_color=MORADO_VIVO, width=300)
    side_panel.grid(row=0, column=0, sticky="nsew")

    header_frame = ctk.CTkFrame(master=side_panel, fg_color=BOTON_USUARIO, corner_radius=20, width=200, height=60)
    header_frame.place(x=30, y=25)
    ctk.CTkLabel(master=header_frame, text="Dr.maggie",
                 font=ctk.CTkFont(size=30, weight="bold"),
                 text_color=MAGENTA).place(relx=0.5, rely=0.5, anchor="center")

    try:
        logo_path = "Logo.png"
        logo_pil_image = Image.open(logo_path)
        logo_ctk_image = ctk.CTkImage(light_image=logo_pil_image, dark_image=logo_pil_image, size=(250, 250))
        logo_label = ctk.CTkLabel(master=side_panel, image=logo_ctk_image, text="")
        logo_label.place(relx=0.5, rely=0.55, anchor="center")
    except Exception:
        ctk.CTkLabel(master=side_panel, text="[Dra. Angie Ajquill\nGinecología y Obstetricia]",
                     font=ctk.CTkFont(size=20, weight="bold"), text_color="white", justify="center").place(relx=0.5,
                                                                                                           rely=0.5,
                                                                                                           anchor="center")

    main_content = ctk.CTkFrame(master=sub, fg_color="white", corner_radius=0)
    main_content.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
    main_content.grid_columnconfigure(0, weight=1)
    main_content.grid_rowconfigure(3, weight=1)

    title_frame = ctk.CTkFrame(master=main_content, fg_color="transparent")
    title_frame.grid(row=0, column=0, sticky="ew", pady=(10, 0))
    title_frame.grid_columnconfigure(0, weight=1)
    title_frame.grid_columnconfigure(1, weight=0)

    title_text = "Actualizar ficha médica" if ficha_id_a_actualizar else "Crear ficha médica"

    ctk.CTkLabel(master=title_frame, text=title_text,
                 fg_color=MORADO_VIVO, text_color=MAGENTA,
                 font=ctk.CTkFont(size=28, weight="bold"),
                 corner_radius=40, width=320, height=60
                 ).grid(row=0, column=0, sticky="w", padx=(30, 0))

    ctk.CTkButton(master=title_frame, text="Cerrar ventana",
                  command=sub.destroy, fg_color=MAGENTA, text_color="white",
                  hover_color=MORADO_CLARO, font=ctk.CTkFont(size=18, weight="bold"),
                  corner_radius=20, width=180, height=50
                  ).grid(row=0, column=1, sticky="e", padx=(0, 30))

    form_frame = ctk.CTkFrame(master=main_content, fg_color="transparent")
    form_frame.grid(row=1, column=0, sticky="nsew", padx=(60, 0), pady=(10, 10))
    form_frame.grid_columnconfigure((0, 1, 2), weight=1)

    entries = {}

    def campo(label_text, row, col_entry, colspan=1):

        entry = ctk.CTkEntry(master=form_frame, fg_color="white", text_color="black",
                             border_width=2, border_color=MORADO_VIVO, corner_radius=60, height=40,
                             placeholder_text=f"Ingrese la {label_text}",
                             font=ctk.CTkFont(size=16))
        entry.grid(row=row, column=col_entry, columnspan=colspan, padx=5, pady=8, sticky="ew")
        return entry

    ctk.CTkLabel(master=form_frame, text=f"Paciente: {nombre_paciente}",
                 fg_color=MORADO_VIVO, text_color="black",
                 font=ctk.CTkFont(size=16, weight="bold"),
                 corner_radius=20, anchor="center", height=40).grid(row=0, column=0, padx=5, pady=8, sticky="ew")

    ctk.CTkLabel(master=form_frame, text=f"DPI: {dpi_paciente}",
                 fg_color=MORADO_VIVO, text_color="black",
                 font=ctk.CTkFont(size=16, weight="bold"),
                 corner_radius=20, anchor="center", height=40).grid(row=0, column=1, padx=5, pady=8, sticky="ew")

    ctk.CTkLabel(master=form_frame, text=f"No. Tel: {tel_paciente}",
                 fg_color=MORADO_VIVO, text_color="black",
                 font=ctk.CTkFont(size=16, weight="bold"),
                 corner_radius=20, anchor="center", height=40).grid(row=0, column=2, padx=5, pady=8, sticky="ew")

    entries['procedencia'] = campo("Procedencia:", 1, 0)
    entries['ocupacion'] = campo("Ocupación:", 1, 1)
    entries['fecha_nac'] = ctk.CTkEntry(master=form_frame, fg_color="white", text_color="black",
                                        border_width=2, border_color=MORADO_VIVO, corner_radius=60, height=40,
                                        placeholder_text=f"Ingrese la Fecha de naciemiento (AAAA-MM-DD)",
                                        font=ctk.CTkFont(size=16))
    entries['fecha_nac'].grid(row=1, column=2, columnspan=1, padx=5, pady=8, sticky="ew")

    ctk.CTkFrame(master=form_frame, fg_color=MORADO_VIVO, corner_radius=20, height=50).grid(
        row=2, column=0, padx=5, pady=8, sticky="ew")
    ctk.CTkLabel(master=form_frame, text="Antecedentes:", font=ctk.CTkFont(size=16, weight="bold"),
                 text_color="black", anchor="w", fg_color=MORADO_VIVO, bg_color=MORADO_VIVO).grid(row=2, column=0,
                                                                                                  padx=20, pady=8,
                                                                                                  sticky="w")
    entries['antecedentes'] = ctk.CTkEntry(master=form_frame, fg_color=BOTON_USUARIO, text_color="black",
                                           border_width=0, corner_radius=20, height=50,
                                           font=ctk.CTkFont(size=16))
    entries['antecedentes'].grid(row=2, column=1, columnspan=2, padx=5, pady=8, sticky="ew")

    ctk.CTkFrame(master=form_frame, fg_color=MORADO_VIVO, corner_radius=20, height=50).grid(
        row=3, column=0, padx=5, pady=8, sticky="ew")
    ctk.CTkLabel(master=form_frame, text="Datos:", font=ctk.CTkFont(size=16, weight="bold"),
                 text_color="black", anchor="w", fg_color=MORADO_VIVO, bg_color=MORADO_VIVO).grid(row=3, column=0,
                                                                                                  padx=20, pady=8,
                                                                                                  sticky="w")

    ctk.CTkLabel(master=main_content, text="Ingrese los datos de la consulta:",
                 font=ctk.CTkFont(size=20, weight="bold"), text_color=MAGENTA
                 ).grid(row=2, column=0, padx=60, pady=(10, 5), sticky="w")

    consulta_textbox = ctk.CTkTextbox(master=main_content, height=220,
                                      corner_radius=20, border_width=2,
                                      border_color=LILA, fg_color="white",
                                      text_color="black", font=ctk.CTkFont(size=16))
    consulta_textbox.grid(row=3, column=0, sticky="nsew", padx=60, pady=(0, 10))

    if procedencia: entries['procedencia'].insert(0, procedencia)
    if ocupacion: entries['ocupacion'].insert(0, ocupacion)
    if fecha_nac: entries['fecha_nac'].insert(0, fecha_nac)
    if antecedentes: entries['antecedentes'].insert(0, antecedentes)
    if datos_consulta: consulta_textbox.insert("0.0", datos_consulta)

    def actualizar_ficha():
        if usuario_actual.rol != "Doctor":
            messagebox.showerror("Error de Rol", "Solo un Doctor puede guardar una ficha médica.")
            return

        procedencia = entries['procedencia'].get()
        ocupacion = entries['ocupacion'].get()
        fecha_nac = entries['fecha_nac'].get()
        antecedentes = entries['antecedentes'].get()
        datos_consulta = consulta_textbox.get("1.0", "end-1c")

        if not procedencia or not ocupacion or not datos_consulta:
            messagebox.showwarning("Advertencia", "Debe llenar Procedencia, Ocupación y Datos de la Consulta.")
            return

        try:
            if ficha_id_a_actualizar:
                db.ejecutar("""
                                UPDATE fichas
                                SET datos=?, procedencia=?, ocupacion=?, antecedentes=?, fecha_nacimiento=?, 
                                    fecha=datetime('now', 'localtime')
                                WHERE id=?
                            """,
                            (datos_consulta, procedencia, ocupacion, antecedentes, fecha_nac, ficha_id_a_actualizar))

                messagebox.showinfo("Éxito", "Ficha médica actualizada correctamente.")
            else:
                usuario_actual.crear_ficha_medica(
                    paciente_id=dpi_paciente,
                    datos=datos_consulta,
                    procedencia=procedencia,
                    ocupacion=ocupacion,
                    antecedentes=antecedentes,
                    fecha_nacimiento=fecha_nac
                )
                messagebox.showinfo("Éxito", "Ficha médica guardada correctamente.")

            sub.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Fallo al guardar/actualizar la ficha: {e}")

    button_text = "Actualizar Ficha" if ficha_id_a_actualizar else "Guardar Ficha"

    ctk.CTkButton(master=main_content, text=button_text,
                  command=actualizar_ficha, fg_color=ROSADO, text_color=MAGENTA,
                  hover_color="#F0B4FB", font=ctk.CTkFont(size=24, weight="bold"),
                  corner_radius=30, width=300, height=70
                  ).grid(row=4, column=0, pady=(20, 10))
#=================================================================
def buscar_ficha():
    sub = ctk.CTkToplevel(app)
    sub.title("Buscar ficha de paciente")
    sub.state('zoomed')
    sub.configure(fg_color="white")

    sub.transient(app)
    sub.grab_set()
    sub.lift()
    sub.focus_force()

    sub.grid_columnconfigure(0, weight=0)
    sub.grid_columnconfigure(1, weight=1)
    sub.grid_rowconfigure(0, weight=1)

    side_panel = ctk.CTkFrame(master=sub, corner_radius=0, fg_color=MORADO_VIVO, width=300)
    side_panel.grid(row=0, column=0, sticky="nsew")

    header_frame = ctk.CTkFrame(master=side_panel, fg_color=BOTON_USUARIO, corner_radius=20, width=200, height=60)
    header_frame.place(x=30, y=25)
    ctk.CTkLabel(master=header_frame, text="Dr. Maggie",
                 font=ctk.CTkFont(size=30, weight="bold"),
                 text_color=MAGENTA).place(relx=0.5, rely=0.5, anchor="center")
    try:
        logo_path = "Logo.png"
        logo_pil_image = Image.open(logo_path)
        logo_ctk_image = ctk.CTkImage(light_image=logo_pil_image, dark_image=logo_pil_image, size=(250, 250))
        logo_label = ctk.CTkLabel(master=side_panel, image=logo_ctk_image, text="")
        logo_label.place(relx=0.5, rely=0.5, anchor="center")
    except Exception:
        ctk.CTkLabel(master=side_panel, text="[Dra. Angie Ajquill\nGinecología y Obstetricia]",
                     font=ctk.CTkFont(size=20, weight="bold"), text_color="white", justify="center").place(relx=0.5,
                                                                                                           rely=0.5,
                                                                                                           anchor="center")

    main_content = ctk.CTkFrame(master=sub, fg_color="white", corner_radius=0)
    main_content.grid(row=0, column=1, sticky="nsew")
    main_content.grid_columnconfigure(0, weight=0)

    ctk.CTkLabel(master=main_content, text="Buscar datos de ficha", fg_color=MORADO_VIVO, text_color=MAGENTA,
                 font=ctk.CTkFont(size=30, weight="bold"),
                 corner_radius=40,
                 width=300,
                 height=60).grid(row=0, column=0, pady=(20, 40), padx=40, sticky="w")

    ctk.CTkButton(master=main_content, text="Cerrar ventana", command=sub.destroy, fg_color=MAGENTA, text_color="white",
                  hover_color=MORADO_CLARO,
                  font=ctk.CTkFont(size=22, weight="bold"),
                  corner_radius=20,
                  width=220,
                  height=70).grid(row=0, column=1, sticky="e", padx=40, pady=(20, 40))

    form_frame = ctk.CTkFrame(master=main_content, fg_color="transparent")
    form_frame.grid(row=1, column=0, columnspan=2, pady=(10, 50))
    form_frame.grid_columnconfigure(0, weight=1)
    form_frame.grid_columnconfigure(1, weight=2)

    label_frame = ctk.CTkFrame(master=form_frame, fg_color=MORADO_VIVO,
                               corner_radius=20, width=200, height=60)
    label_frame.grid(row=1, column=0, padx=(150, 30), pady=30, sticky="e")
    ctk.CTkLabel(master=label_frame, text="DPI: ",
                 text_color=MAGENTA,
                 font=ctk.CTkFont(size=22, weight="bold")).place(relx=0.5, rely=0.5, anchor="center")

    entry_frame = ctk.CTkFrame(master=form_frame, fg_color="white",
                               corner_radius=20, width=500, height=60)
    entry_frame.grid(row=1, column=1, padx=(20, 150), pady=30, sticky="w")
    entry = ctk.CTkEntry(master=entry_frame,
                         placeholder_text=f"Ingrese el DPI del paciente",
                         fg_color="white",
                         text_color="black",
                         font=ctk.CTkFont(size=20),
                         border_width=0,
                         width=460,
                         height=45)
    entry.place(relx=0.5, rely=0.5, anchor="center")

    def buscar():
        dpi_buscar = entry.get()
        if not dpi_buscar:
            messagebox.showwarning("Advertencia", "El campo DPI no puede estar vacío.")
            return

        paciente_row = db.ejecutar("SELECT nombre, telefono FROM pacientes WHERE DPI=?", (dpi_buscar,), fetch=True)
        ficha_row = db.ejecutar(
            "SELECT * FROM fichas WHERE paciente_id=? ORDER BY id DESC LIMIT 1",
            (dpi_buscar,),
            fetch=True
        )

        if paciente_row and ficha_row:
            p = paciente_row[0]
            f = ficha_row[0]

            messagebox.showinfo("Éxito", f"Ficha y paciente encontrados: {p['nombre']}")
            sub.destroy()

            crear_ventana_ficha_medica_actualizar(
                dpi_paciente=dpi_buscar,
                nombre_paciente=p['nombre'],
                tel_paciente=p['telefono'],
                procedencia=f['procedencia'],
                ocupacion=f['ocupacion'],
                fecha_nac=f['fecha_nacimiento'],
                antecedentes=f['antecedentes'],
                datos_consulta=f['datos']
            )

        else:
            messagebox.showerror("Error", f"Paciente con DPI {dpi_buscar} o ficha médica no encontrado.")

    ctk.CTkButton(master=main_content, text="Buscar", command=buscar, fg_color=ROSADO, text_color=MAGENTA,
                  hover_color="#F0B4FB", font=ctk.CTkFont(size=26, weight="bold"), corner_radius=30, width=250,
                  height=80).grid(row=2, column=0, columnspan=2, pady=40)


def vender_medicamento():
    sub = ctk.CTkToplevel(app)
    sub.title("Vender medicamento")
    sub.state('zoomed')
    sub.configure(fg_color="white")

    sub.transient(app)
    sub.grab_set()
    sub.lift()
    sub.focus_force()

    sub.grid_rowconfigure(0, weight=1)
    sub.grid_columnconfigure(0, weight=0)
    sub.grid_columnconfigure(1, weight=2)
    sub.grid_columnconfigure(2, weight=1)

    side_panel = ctk.CTkFrame(master=sub, corner_radius=0, fg_color=MORADO_VIVO, width=300)
    side_panel.grid(row=0, column=0, sticky="nsew")

    header_frame = ctk.CTkFrame(master=side_panel, fg_color=BOTON_USUARIO, corner_radius=20, width=200, height=60)
    header_frame.place(x=30, y=25)
    ctk.CTkLabel(master=header_frame, text="Dr. Maggie", font=ctk.CTkFont(size=30, weight="bold"),
                 text_color=MAGENTA).place(relx=0.5, rely=0.5, anchor="center")

    try:
        logo_path = "Logo.png"
        logo_pil_image = Image.open(logo_path)
        logo_ctk_image = ctk.CTkImage(light_image=logo_pil_image, dark_image=logo_pil_image, size=(250, 250))
        logo_label = ctk.CTkLabel(master=side_panel, image=logo_ctk_image, text="")
        logo_label.place(relx=0.5, rely=0.5, anchor="center")
    except Exception:
        ctk.CTkLabel(master=side_panel, text="[Dra. Angie Ajquill\nGinecología y Obstetricia]",
                     font=ctk.CTkFont(size=20, weight="bold"), text_color="white", justify="center").place(relx=0.5,
                                                                                                           rely=0.6,
                                                                                                           anchor="center")

    main_content = ctk.CTkFrame(master=sub, fg_color="white", corner_radius=0)
    main_content.grid(row=0, column=1, sticky="nsew")

    main_content.grid_columnconfigure(0, weight=1)
    main_content.grid_columnconfigure(1, weight=2)
    main_content.grid_columnconfigure(2, weight=1)

    main_content.grid_rowconfigure(0, weight=0)
    main_content.grid_rowconfigure(1, weight=0)
    main_content.grid_rowconfigure(2, weight=1)
    main_content.grid_rowconfigure(3, weight=0)

    ctk.CTkLabel(master=main_content, text="Vender medicamento",
                 fg_color=MORADO_VIVO, text_color=MAGENTA,
                 font=ctk.CTkFont(size=30, weight="bold"),
                 corner_radius=40, width=320, height=60
                 ).grid(row=0, column=0, columnspan=2, pady=(20, 20), padx=40, sticky="w")

    ctk.CTkButton(master=main_content, text="Cerrar ventana",
                  command=sub.destroy, fg_color=MAGENTA, text_color="white",
                  hover_color=MORADO_CLARO, font=ctk.CTkFont(size=20, weight="bold"),
                  corner_radius=20, width=220, height=60
                  ).grid(row=0, column=2, sticky="e", padx=(0, 40), pady=(20, 20))

    form_frame = ctk.CTkFrame(master=main_content, fg_color="transparent")
    form_frame.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=(60, 0), pady=(100, 100))
    form_frame.grid_columnconfigure(0, weight=1)
    form_frame.grid_columnconfigure(1, weight=3)

    CAMPOS = ["Medicamento:", "Cantidad:", "Precio:"]
    entries = {}

    for i, label_text in enumerate(CAMPOS):
        ctk.CTkLabel(master=form_frame, text=label_text,
                     text_color=MAGENTA, font=ctk.CTkFont(size=20, weight="bold"),
                     ).grid(row=i, column=1, sticky="e", padx=(0, 20), pady=20)

        entry = ctk.CTkEntry(master=form_frame,
                             placeholder_text=f"Ingrese {label_text.replace(':', '')}",
                             width=600, height=60,
                             fg_color="white", text_color="black",
                             font=ctk.CTkFont(size=20), border_width=0
                             )
        entry.grid(row=i, column=2, sticky="w", padx=(0, 80), pady=20)
        entries[label_text] = entry

    try:
        img_path = "medicina.jpg"  ###
        paciente_pil = Image.open(img_path)
        paciente_img = ctk.CTkImage(light_image=paciente_pil, dark_image=paciente_pil, size=(300, 300))
        ctk.CTkLabel(master=main_content, image=paciente_img, text="").grid(row=1, column=2, padx=40, pady=(150, 10),
                                                                            sticky="n")
    except Exception as e:
        print(f"No se pudo cargar imagen del medicamento: {e}")
        ctk.CTkLabel(master=main_content, text="[Imagen medicina]", text_color="gray",
                     font=ctk.CTkFont(size=20, slant="italic")).grid(row=1, column=2, padx=40, pady=10, sticky="n")

    def guardar_venta():
        nombre = entries["Medicamento:"].get()
        cant = entries["Cantidad:"].get()
        precio_ingresado = entries["Precio:"].get()

        if not nombre or not cant:
            messagebox.showwarning("Advertencia", "Medicamento y Cantidad son obligatorios.")
            return

        try:
            cantidad_int = int(cant)
            if cantidad_int <= 0:
                messagebox.showwarning("Advertencia", "La cantidad debe ser un valor positivo.")
                return
        except ValueError:
            messagebox.showwarning("Advertencia", "La cantidad debe ser un número entero.")
            return

        try:
            resultado = Proveedor.vender_producto(
                db=db,
                nombre=nombre,
                cantidad=cantidad_int,
                doctor_user="docanles",
                doctor_pass="1234",
                proveedor_id=usuario_actual.id
            )

            messagebox.showinfo("Venta Realizada",
                                f"Venta registrada:\nMedicamento: {resultado['producto']}\nCantidad: {resultado['cantidad']}\nPrecio unitario: Q{resultado['precio_unitario']:.2f}\nTotal: Q{resultado['total']:.2f}")
            sub.destroy()

        except ValueError as e:
            messagebox.showerror("Error de Venta", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error inesperado: {e}")

    ctk.CTkButton(master=main_content, text="Vender",
                  command=guardar_venta, fg_color=ROSADO, text_color=MAGENTA,
                  hover_color="#transparente", font=ctk.CTkFont(size=24, weight="bold"),
                  corner_radius=30, width=300, height=80
                  ).grid(row=2, column=0, columnspan=3, pady=(10, 40), sticky="n")


def agendar_cita():
    sub = ctk.CTkToplevel(app)
    sub.title("Agendar Cita")
    sub.state('zoomed')
    sub.configure(fg_color="white")

    sub.transient(app)
    sub.grab_set()
    sub.lift()
    sub.focus_force()

    sub.grid_rowconfigure(0, weight=1)
    sub.grid_columnconfigure(0, weight=0)
    sub.grid_columnconfigure(1, weight=2)
    sub.grid_columnconfigure(2, weight=1)

    side_panel = ctk.CTkFrame(master=sub, corner_radius=0, fg_color=MORADO_VIVO, width=300)
    side_panel.grid(row=0, column=0, sticky="nsew")

    header_frame = ctk.CTkFrame(master=side_panel, fg_color=BOTON_USUARIO, corner_radius=20, width=200, height=60)
    header_frame.place(x=30, y=25)
    ctk.CTkLabel(master=header_frame, text="Dr. Maggie",
                 font=ctk.CTkFont(size=30, weight="bold"),
                 text_color=MAGENTA).place(relx=0.5, rely=0.5, anchor="center")

    try:
        logo_path = "Logo.png"
        logo_pil_image = Image.open(logo_path)
        logo_ctk_image = ctk.CTkImage(light_image=logo_pil_image, dark_image=logo_pil_image, size=(250, 250))
        logo_label = ctk.CTkLabel(master=side_panel, image=logo_ctk_image, text="")
        logo_label.place(relx=0.5, rely=0.5, anchor="center")
    except Exception:
        ctk.CTkLabel(master=side_panel, text="[Dra. Angie Ajquill\nGinecología y Obstetricia]",
                     font=ctk.CTkFont(size=20, weight="bold"), text_color="white", justify="center"
                     ).place(relx=0.5, rely=0.6, anchor="center")

    main_content = ctk.CTkFrame(master=sub, fg_color="white", corner_radius=0)
    main_content.grid(row=0, column=1, sticky="nsew")

    main_content.grid_columnconfigure(0, weight=1)
    main_content.grid_columnconfigure(1, weight=2)
    main_content.grid_columnconfigure(2, weight=1)

    main_content.grid_rowconfigure(0, weight=0)
    main_content.grid_rowconfigure(1, weight=0)
    main_content.grid_rowconfigure(2, weight=1)
    main_content.grid_rowconfigure(3, weight=0)

    ctk.CTkLabel(master=main_content, text="Agendar Cita",
                 fg_color=MORADO_VIVO, text_color=MAGENTA,
                 font=ctk.CTkFont(size=30, weight="bold"),
                 corner_radius=40, width=320, height=60
                 ).grid(row=0, column=0, columnspan=2, pady=(20, 20), padx=40, sticky="w")

    ctk.CTkButton(master=main_content, text="Cerrar ventana",
                  command=sub.destroy, fg_color=MAGENTA, text_color="white",
                  hover_color=MORADO_CLARO, font=ctk.CTkFont(size=20, weight="bold"),
                  corner_radius=20, width=220, height=60
                  ).grid(row=0, column=2, sticky="e", padx=(0, 40), pady=(20, 20))

    form_frame = ctk.CTkFrame(master=main_content, fg_color="transparent")
    form_frame.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=(60, 0), pady=(100, 100))
    form_frame.grid_columnconfigure(0, weight=1)
    form_frame.grid_columnconfigure(1, weight=3)

    ctk.CTkLabel(master=form_frame, text="DPI del paciente:",
                 text_color=MAGENTA, font=ctk.CTkFont(size=20, weight="bold")
                 ).grid(row=0, column=1, sticky="e", padx=(0, 20), pady=20)
    entry_dpi = ctk.CTkEntry(master=form_frame,
                             placeholder_text="Ingrese DPI del paciente",
                             width=600, height=60, fg_color="white",
                             text_color="black", font=ctk.CTkFont(size=20), border_width=0)
    entry_dpi.grid(row=0, column=2, sticky="w", padx=(0, 80), pady=20)

    ctk.CTkLabel(master=form_frame, text="Dirección:",
                 text_color=MAGENTA, font=ctk.CTkFont(size=20, weight="bold")
                 ).grid(row=1, column=1, sticky="e", padx=(0, 20), pady=20)
    entry_direccion = ctk.CTkEntry(master=form_frame,
                                   placeholder_text="Ingrese dirección del paciente",
                                   width=600, height=60, fg_color="white",
                                   text_color="black", font=ctk.CTkFont(size=20), border_width=0)
    entry_direccion.grid(row=1, column=2, sticky="w", padx=(0, 80), pady=20)

    ctk.CTkLabel(master=form_frame, text="Fecha de la cita:",
                 text_color=MAGENTA, font=ctk.CTkFont(size=20, weight="bold")
                 ).grid(row=2, column=1, sticky="e", padx=(0, 20), pady=20)
    date_entry = DateEntry(master=form_frame, width=18, background=MORADO_VIVO,
                           foreground="white", borderwidth=2, date_pattern="yyyy-mm-dd",
                           font=("Arial", 18))
    date_entry.grid(row=2, column=2, sticky="w", padx=(0, 80), pady=20)

    ctk.CTkLabel(master=form_frame, text="Hora:",
                 text_color=MAGENTA, font=ctk.CTkFont(size=20, weight="bold")
                 ).grid(row=3, column=1, sticky="e", padx=(0, 20), pady=20)
    horas_disponibles = [f"{h:02d}:00" for h in range(8, 18)]
    hora_combo = ctk.CTkComboBox(master=form_frame, values=horas_disponibles,
                                 fg_color="white", text_color="black",
                                 font=ctk.CTkFont(size=20),
                                 dropdown_font=ctk.CTkFont(size=18))
    hora_combo.set("Seleccione hora")
    hora_combo.grid(row=3, column=2, sticky="w", padx=(0, 80), pady=20)

    try:
        img_path = "cita.jpg"
        cita_pil = Image.open(img_path)
        cita_img = ctk.CTkImage(light_image=cita_pil, dark_image=cita_pil, size=(300, 300))
        ctk.CTkLabel(master=main_content, image=cita_img, text="").grid(row=1, column=2, padx=40, pady=(150, 10),
                                                                        sticky="n")
    except Exception as e:
        print(f"No se pudo cargar imagen de cita: {e}")
        ctk.CTkLabel(master=main_content, text="[Imagen cita]", text_color="gray",
                     font=ctk.CTkFont(size=20, slant="italic")).grid(row=1, column=2, padx=40, pady=10, sticky="n")

    def guardar_cita():
        dpi = entry_dpi.get()
        direccion = entry_direccion.get()
        fecha_date = date_entry.get_date()
        fecha = str(fecha_date)
        hora = hora_combo.get()
        registrado_en = f"{hora}:00"

        if not dpi or not direccion or hora == "Seleccione hora":
            messagebox.showwarning("Advertencia", "Todos los campos son obligatorios.")
            return


        paciente_row = db.ejecutar("SELECT DPI FROM pacientes WHERE DPI=?", (dpi,), fetch=True)
        if not paciente_row:
            messagebox.showerror("Error", f"Paciente con DPI {dpi} no encontrado. Debe registrarlo primero.")
            return

        cita_existente = db.ejecutar("SELECT id FROM citas WHERE registrado_en=?", (registrado_en,), fetch=True)
        if cita_existente:
            messagebox.showerror("Error", f"La fecha {fecha} a las {hora} ya está ocupada.")
            return

        try:
            db.ejecutar(
                """
                INSERT INTO citas (fecha, paciente_id, creado_por, registrado_en)
                VALUES (?, ?, ?, ?)
                """,
                (fecha, dpi, usuario_actual.id, registrado_en)
            )

            messagebox.showinfo("Éxito", f"Cita agendada para DPI {dpi}\nFecha: {fecha} - Hora: {hora}")
            sub.destroy()
        except Exception as e:
            messagebox.showerror("Error", f"Fallo al guardar la cita: {e}")

    ctk.CTkButton(master=main_content, text="Guardar Cita",
                  command=guardar_cita, fg_color=ROSADO, text_color=MAGENTA,
                  hover_color="#F0B4FB", font=ctk.CTkFont(size=24, weight="bold"),
                  corner_radius=30, width=300, height=80
                  ).grid(row=2, column=0, columnspan=3, pady=(10, 40), sticky="n")


def ver_citas():
    sub = ctk.CTkToplevel(app)
    sub.title("Ver citas - Historial")
    sub.state('zoomed')
    sub.configure(fg_color="white")

    sub.transient(app)
    sub.grab_set()
    sub.lift()
    sub.focus_force()

    sub.grid_rowconfigure(0, weight=1)
    sub.grid_columnconfigure(0, weight=0)
    sub.grid_columnconfigure(1, weight=2)
    sub.grid_columnconfigure(2, weight=1)

    side_panel = ctk.CTkFrame(master=sub, corner_radius=0, fg_color=MORADO_VIVO, width=300)
    side_panel.grid(row=0, column=0, sticky="nsew")

    header_frame = ctk.CTkFrame(master=side_panel, fg_color=BOTON_USUARIO, corner_radius=20, width=200, height=60)
    header_frame.place(x=30, y=25)
    ctk.CTkLabel(master=header_frame, text="Dr. Maggie", font=ctk.CTkFont(size=30, weight="bold"),
                 text_color=MAGENTA).place(relx=0.5, rely=0.5, anchor="center")

    try:
        logo_path = "Logo.png"
        logo_pil_image = Image.open(logo_path)
        logo_ctk_image = ctk.CTkImage(light_image=logo_pil_image, dark_image=logo_pil_image, size=(250, 250))
        ctk.CTkLabel(master=side_panel, image=logo_ctk_image, text="").place(relx=0.5, rely=0.5, anchor="center")
    except Exception:
        ctk.CTkLabel(master=side_panel, text="[Dra. Angie Ajquill\nGinecología y Obstetricia]",
                     font=ctk.CTkFont(size=20, weight="bold"), text_color="white", justify="center").place(relx=0.5,
                                                                                                           rely=0.6,
                                                                                                           anchor="center")

    main_content = ctk.CTkFrame(master=sub, fg_color="white", corner_radius=0)
    main_content.grid(row=0, column=1, columnspan=2, sticky="nsew")

    main_content.grid_columnconfigure(0, weight=1)
    main_content.grid_columnconfigure(1, weight=2)
    main_content.grid_columnconfigure(2, weight=1)
    main_content.grid_rowconfigure(0, weight=0)
    main_content.grid_rowconfigure(1, weight=1)

    ctk.CTkLabel(master=main_content, text="Historial de Citas",
                 fg_color=MORADO_VIVO, text_color=MAGENTA,
                 font=ctk.CTkFont(size=30, weight="bold"),
                 corner_radius=40, width=320, height=60
                 ).grid(row=0, column=0, columnspan=2, pady=(20, 20), padx=40, sticky="w")

    ctk.CTkButton(master=main_content, text="Cerrar ventana",
                  command=sub.destroy, fg_color=MAGENTA, text_color="white",
                  hover_color=MORADO_CLARO, font=ctk.CTkFont(size=20, weight="bold"),
                  corner_radius=20, width=220, height=60
                  ).grid(row=0, column=2, sticky="e", padx=(0, 40), pady=(20, 20))

    # SOLUCIÓN FINAL: Se selecciona la nueva columna 'registrado_en' y se le da el alias 'hora'.
    # ESTO REQUIERE QUE LA DB TENGA LA COLUMNA 'registrado_en' (BORRAR el archivo .db si sigue dando error).
    citas_db = db.ejecutar("""
        SELECT 
            c.fecha, 
            c.registrado_en AS hora,  
            p.nombre AS paciente_nombre, 
            p.DPI
        FROM citas c
        JOIN pacientes p ON c.paciente_id = p.DPI
        ORDER BY c.fecha DESC
    """, fetch=True)

    # --- DEBUG: Verifica qué devuelve la base de datos ---
    if citas_db:
        print("Citas encontradas en la DB:", citas_db)
    else:
        print("La consulta a la DB para citas devolvió una lista vacía.")
    # ----------------------------------------------------

    headers = ["Fecha", "Hora", "Paciente", "DPI"]
    data = []

    for fila in citas_db:
        # Leemos los valores directamente de las columnas (usando el alias 'hora').
        fecha = fila['fecha']
        hora = fila['hora']

        # Si la columna 'hora' (ahora 'registrado_en') está vacía o es None, mostramos un guion.
        hora_display = hora if hora and hora.strip() else "-"

        data.append((fecha, hora_display, fila['paciente_nombre'], fila['DPI']))

    if not data:
        ctk.CTkLabel(master=main_content, text="No hay citas agendadas.",
                     font=ctk.CTkFont(size=24, weight="bold"), text_color="gray"
                     ).grid(row=1, column=0, columnspan=3, pady=100)
    else:
        scroll_frame = ctk.CTkScrollableFrame(
            master=main_content,
            label_text="Citas Agendadas",
            fg_color="transparent",
            label_font=ctk.CTkFont(size=20, weight="bold")
        )
        scroll_frame.grid(row=1, column=0, columnspan=3, padx=40, pady=(0, 40), sticky="nsew")

        for i in range(len(headers)):
            scroll_frame.grid_columnconfigure(i, weight=1)

        header_color = MORADO_VIVO
        for i, col_name in enumerate(headers):
            ctk.CTkLabel(master=scroll_frame, text=col_name, fg_color=header_color, text_color="white",
                         font=ctk.CTkFont(size=16, weight="bold"), height=40, corner_radius=10
                         ).grid(row=0, column=i, sticky="ew", padx=5, pady=(0, 5))

        row_color_1 = LILA
        row_color_2 = "white"

        for i, row_data in enumerate(data, start=1):
            bg_color = row_color_1 if i % 2 == 0 else row_color_2
            for j, valor in enumerate(row_data):
                ctk.CTkLabel(master=scroll_frame, text=str(valor), fg_color=bg_color, text_color="black",
                             font=ctk.CTkFont(size=14), height=30, justify='left'
                             ).grid(row=i, column=j, sticky="ew", padx=5, pady=1)


def cancelar_cita():
    sub = ctk.CTkToplevel(app)
    sub.title("Cancelar cita")
    sub.state('zoomed')
    sub.configure(fg_color="white")

    sub.transient(app)
    sub.grab_set()
    sub.lift()
    sub.focus_force()

    sub.grid_columnconfigure(0, weight=0)
    sub.grid_columnconfigure(1, weight=1)
    sub.grid_rowconfigure(0, weight=1)

    side_panel = ctk.CTkFrame(master=sub, corner_radius=0, fg_color=MORADO_VIVO, width=300)
    side_panel.grid(row=0, column=0, sticky="nsew")

    header_frame = ctk.CTkFrame(master=side_panel, fg_color=BOTON_USUARIO, corner_radius=20, width=200, height=60)
    header_frame.place(x=30, y=25)
    ctk.CTkLabel(master=header_frame, text="Dr. Maggie",
                 font=ctk.CTkFont(size=30, weight="bold"),
                 text_color=MAGENTA).place(relx=0.5, rely=0.5, anchor="center")
    try:
        logo_path = "Logo.png"
        logo_pil_image = Image.open(logo_path)
        logo_ctk_image = ctk.CTkImage(light_image=logo_pil_image, dark_image=logo_pil_image, size=(250, 250))
        logo_label = ctk.CTkLabel(master=side_panel, image=logo_ctk_image, text="")
        logo_label.place(relx=0.5, rely=0.5, anchor="center")
    except Exception:
        ctk.CTkLabel(master=side_panel, text="[Dra. Angie Ajquill\nGinecología y Obstetricia]",
                     font=ctk.CTkFont(size=20, weight="bold"), text_color="white", justify="center").place(relx=0.5,
                                                                                                           rely=0.5,
                                                                                                           anchor="center")

    main_content = ctk.CTkFrame(master=sub, fg_color="white", corner_radius=0)
    main_content.grid(row=0, column=1, sticky="nsew")
    main_content.grid_columnconfigure(0, weight=0)

    ctk.CTkLabel(master=main_content, text="Buscar cita a cancelar", fg_color=MORADO_VIVO, text_color=MAGENTA,
                 font=ctk.CTkFont(size=30, weight="bold"),
                 corner_radius=40,
                 width=300,
                 height=60).grid(row=0, column=0, pady=(20, 40), padx=40, sticky="w")

    ctk.CTkButton(master=main_content, text="Cerrar ventana", command=sub.destroy, fg_color=MAGENTA, text_color="white",
                  hover_color=MORADO_CLARO,
                  font=ctk.CTkFont(size=22, weight="bold"),
                  corner_radius=20,
                  width=220,
                  height=70).grid(row=0, column=1, sticky="e", padx=40, pady=(20, 40))

    form_frame = ctk.CTkFrame(master=main_content, fg_color="transparent")
    form_frame.grid(row=1, column=0, columnspan=2, pady=(10, 50))
    form_frame.grid_columnconfigure(0, weight=1)
    form_frame.grid_columnconfigure(1, weight=2)

    label_frame = ctk.CTkFrame(master=form_frame, fg_color=MORADO_VIVO,
                               corner_radius=20, width=200, height=60)
    label_frame.grid(row=1, column=0, padx=(150, 30), pady=30, sticky="e")
    ctk.CTkLabel(master=label_frame, text="DPI: ",
                 text_color=MAGENTA,
                 font=ctk.CTkFont(size=22, weight="bold")).place(relx=0.5, rely=0.5, anchor="center")

    entry_frame = ctk.CTkFrame(master=form_frame, fg_color="white",
                               corner_radius=20, width=500, height=60)
    entry_frame.grid(row=1, column=1, padx=(20, 150), pady=30, sticky="w")
    entry = ctk.CTkEntry(master=entry_frame,
                         placeholder_text=f"Ingrese el DPI del paciente",
                         fg_color="white",
                         text_color="black",
                         font=ctk.CTkFont(size=20),
                         border_width=0,
                         width=460,
                         height=45)
    entry.place(relx=0.5, rely=0.5, anchor="center")

    def buscar():
        dpi_cancelar = entry.get()
        if not dpi_cancelar:
            messagebox.showwarning("Advertencia", "El campo DPI no puede estar vacío.")
            return

        cita = db.ejecutar(
            "SELECT id, registrado_en FROM citas WHERE paciente_id=? ORDER BY registrado_en DESC LIMIT 1",
            (dpi_cancelar,), fetch=True)

        if cita:
            cita_id = cita[0]['id']
            confirm = messagebox.askyesno("Confirmar Cancelación",
                                          f"¿Desea cancelar la cita para el DPI {dpi_cancelar} el {cita[0]['registrado_en']}?")

            if confirm:
                db.ejecutar("DELETE FROM citas WHERE id=?", (cita_id,))
                messagebox.showinfo("Éxito", f"Cita para DPI {dpi_cancelar} ha sido cancelada.")
                sub.destroy()

        else:
            messagebox.showerror("Error", f"No se encontró ninguna cita pendiente para el DPI {dpi_cancelar}.")

    ctk.CTkButton(master=main_content, text="Buscar", command=buscar, fg_color=ROSADO, text_color=MAGENTA,
                  hover_color="#F0B4FB", font=ctk.CTkFont(size=26, weight="bold"), corner_radius=30, width=250,
                  height=80).grid(row=2, column=0, columnspan=2, pady=40)


# ==========================================================================================
def crear_ventana_tabla(title, headers, data):
    sub = ctk.CTkToplevel(app)
    sub.title(title)
    sub.geometry("1000x600")
    sub.transient(app)
    sub.grab_set()
    sub.lift()
    sub.focus_force()
    sub.configure(fg_color="white")

    ctk.CTkLabel(sub, text=title,
                 fg_color=MORADO_VIVO, text_color="white",
                 font=ctk.CTkFont(size=24, weight="bold"),
                 corner_radius=15, height=40).pack(pady=20, padx=20, fill="x")

    table_frame = ctk.CTkFrame(sub, fg_color="white")
    table_frame.pack(pady=10, padx=20, fill="both", expand=True)

    style = ttk.Style()
    style.theme_use("default")
    style.configure("Treeview",
                    background="#F0F0F0",
                    foreground="black",
                    rowheight=25,
                    fieldbackground="#F0F0F0",
                    font=('Arial', 12))
    style.map('Treeview', background=[('selected', MORADO_VIVO)])
    style.configure("Treeview.Heading", font=('Arial', 12, 'bold'), background=MAGENTA, foreground="white")

    tree = ttk.Treeview(table_frame, columns=headers, show="headings")


    for col in headers:
        tree.heading(col, text=col)
        tree.column(col, anchor="center", width=int(1000 / len(headers)))

    for row in data:
        tree.insert("", "end", values=row)

    scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side="right", fill="y")
    tree.pack(side="left", fill="both", expand=True)

    ctk.CTkButton(sub, text="Cerrar", command=sub.destroy,
                  fg_color=MAGENTA, hover_color=MORADO_CLARO,
                  font=ctk.CTkFont(size=18, weight="bold"), corner_radius=15,
                  width=150, height=40).pack(pady=(10, 20))


def ver_inventario():
    productos_db = db.ejecutar("SELECT nombre, stock, precio FROM productos", fetch=True)

    headers = ["Medicamento", "Cantidad", "Precio Venta (Q)"]
    data = []

    for p in productos_db:
        data.append((p['nombre'], p['stock'], f"{p['precio']:.2f}"))

    crear_ventana_tabla("Inventario Actual de Medicamentos", headers, data)


def ver_medicamentos_comprados():
    movimientos_db  = db.ejecutar("""
        SELECT m.fecha, p.nombre AS medicamento, m.cantidad, m.precio_unitario, u.nombre AS proveedor
        FROM movimientos m
        JOIN productos p ON m.producto_id = p.id
        JOIN usuarios u ON m.usuario_id = u.id
        WHERE m.tipo='entrada' OR m.tipo='salida'
        ORDER BY m.fecha DESC
    """, fetch=True)

    headers = ["Fecha", "Medicamento", "Cantidad", "Precio Unitario (Q)", "Tipo", "Usuario/Proveedor"]
    data = []

    if not movimientos_db:
        messagebox.showwarning("No existen movimientos registrados")
    else:
        for m in movimientos_db:
            data.append((
                m['fecha'].split('T')[0],
                m['medicamento'],
                m['cantidad'],
                f"{m['precio_unitario']:.2f}",
                m['tipo'].capitalize(),
                m['proveedor']
            ))
    crear_ventana_tabla("Registro de Compras/Movimientos de Medicamentos", headers, data)


# funciones principales----------------------------------------------------------------------
# ===========================================================================================

def crear_interfaz_principal():
    for widget in app.winfo_children():
        widget.destroy()

    app.title("Menú Principal - Dr. Maggie")
    app.state('zoomed')
    app.configure(fg_color="white")

    app.grid_rowconfigure(0, weight=1)
    app.grid_columnconfigure(0, weight=0)
    app.grid_columnconfigure(1, weight=2)
    app.grid_columnconfigure(2, weight=1)

    side_panel = ctk.CTkFrame(master=app, corner_radius=0, fg_color=MORADO_VIVO, width=300)
    side_panel.grid(row=0, column=0, sticky="nsew")

    header_frame = ctk.CTkFrame(master=side_panel, fg_color=BOTON_USUARIO, corner_radius=20, width=200, height=60)
    header_frame.place(x=30, y=25)
    ctk.CTkLabel(master=header_frame, text="Dr. Maggie",
                 font=ctk.CTkFont(size=30, weight="bold"),
                 text_color=MAGENTA).place(relx=0.5, rely=0.5, anchor="center")

    try:
        logo_path = "Logo.png"
        logo_pil_image = Image.open(logo_path)
        logo_ctk_image = ctk.CTkImage(light_image=logo_pil_image, dark_image=logo_pil_image, size=(250, 250))
        logo_label = ctk.CTkLabel(master=side_panel, image=logo_ctk_image, text="")
        logo_label.place(relx=0.5, rely=0.5, anchor="center")
    except Exception:
        ctk.CTkLabel(master=side_panel, text="[Dra. Angie Ajquill\nGinecología y Obstetricia]",
                     font=ctk.CTkFont(size=20, weight="bold"),
                     text_color="white", justify="center").place(relx=0.5, rely=0.6, anchor="center")

    main_content = ctk.CTkFrame(master=app, fg_color=ROSADO, corner_radius=0)
    main_content.grid(row=0, column=1, columnspan=2, sticky="nsew")

    main_content.grid_columnconfigure(0, weight=1)
    main_content.grid_columnconfigure(1, weight=2)
    main_content.grid_columnconfigure(2, weight=1)
    main_content.grid_rowconfigure(0, weight=0)
    main_content.grid_rowconfigure(1, weight=1)
    main_content.grid_rowconfigure(2, weight=0)

    ctk.CTkLabel(master=main_content, text="Opciones clínica",
                 fg_color=MORADO_VIVO, text_color=MAGENTA,
                 font=ctk.CTkFont(size=30, weight="bold"),
                 corner_radius=40, width=320, height=60
                 ).grid(row=0, column=0, columnspan=2, pady=(20, 20), padx=40, sticky="w")

    def cerrar_sesion():
        for widget in app.winfo_children():
            widget.destroy()
        app.update_idletasks()
        interfaz_login()

    ctk.CTkButton(master=main_content, text="Cerrar sesión",
                  command=cerrar_sesion,
                  fg_color=MAGENTA, text_color="white",
                  hover_color=MORADO_CLARO,
                  font=ctk.CTkFont(size=20, weight="bold"),
                  corner_radius=20, width=220, height=60
                  ).grid(row=0, column=2, sticky="e", padx=(0, 40), pady=(20, 20))

    botones_frame = ctk.CTkFrame(master=main_content, fg_color="transparent")
    botones_frame.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=(60, 0), pady=(60, 60))
    botones_frame.grid_columnconfigure(0, weight=1)
    botones_frame.grid_columnconfigure(1, weight=1)
    botones_frame.grid_columnconfigure(2, weight=1)

    botones = [
        ("Agregar paciente", agregar_paciente),
        ("Crear ficha médica", buscar_paciente),
        ("Buscar ficha médica", buscar_ficha),
        ("Vender medicamento", vender_medicamento),
        ("Agendar cita", agendar_cita),
        ("Ver citas", ver_citas),
        ("Cancelar cita", cancelar_cita)
    ]

    for i, (texto, comando) in enumerate(botones[:4]):
        ctk.CTkButton(master=botones_frame, text=texto, command=comando,
                      fg_color="white", text_color="black",
                      hover_color=MORADO_CLARO,
                      font=ctk.CTkFont(size=20, weight="bold"),
                      corner_radius=30, width=300, height=70
                      ).grid(row=i, column=0, sticky="w", padx=(40, 20), pady=15)

    for i, (texto, comando) in enumerate(botones[4:]):
        ctk.CTkButton(master=botones_frame, text=texto, command=comando,
                      fg_color="white", text_color="black",
                      hover_color=MORADO_CLARO,
                      font=ctk.CTkFont(size=20, weight="bold"),
                      corner_radius=30, width=260, height=70
                      ).grid(row=4, column=i, padx=30, pady=(100, 0))

    try:
        img_path = "consulta.png"
        img_pil = Image.open(img_path)
        img_ctk = ctk.CTkImage(light_image=img_pil, dark_image=img_pil, size=(400, 300))
        ctk.CTkLabel(master=main_content, image=img_ctk, text="").grid(row=1, column=2, padx=40, pady=(80, 0),
                                                                       sticky="n")
    except Exception:
        ctk.CTkLabel(master=main_content, text="[Imagen consulta]",
                     text_color="gray", font=ctk.CTkFont(size=20, slant="italic")
                     ).grid(row=1, column=2, padx=40, pady=(80, 0), sticky="n")


def menu_contador():
    for widget in app.winfo_children():
        widget.destroy()

    app.title("Contador - Inventario y Compras")
    app.state('zoomed')
    app.configure(fg_color="white")

    app.grid_columnconfigure(0, weight=0)
    app.grid_columnconfigure(1, weight=1)
    app.grid_rowconfigure(0, weight=1)

    side_panel = ctk.CTkFrame(master=app, corner_radius=0, fg_color=FONDO_CONTADOR, width=300)
    side_panel.grid(row=0, column=0, sticky="nsew")

    title_side = ctk.CTkFrame(master=side_panel, fg_color=ROSADO, corner_radius=20, width=200, height=60)
    title_side.place(x=30, y=25)
    ctk.CTkLabel(master=title_side, text="Contador",
                 font=ctk.CTkFont(size=30, weight="bold"),
                 text_color=MAGENTA).place(relx=0.5, rely=0.5, anchor="center")

    try:
        logo_path = "Logo.png"
        logo_pil_image = Image.open(logo_path)
        logo_ctk_image = ctk.CTkImage(light_image=logo_pil_image, dark_image=logo_pil_image, size=(250, 250))
        ctk.CTkLabel(master=side_panel, image=logo_ctk_image, text="").place(relx=0.5, rely=0.55, anchor="center")
    except Exception:
        ctk.CTkLabel(master=side_panel, text="[Dra. Angie Ajquill\nGinecología y Obstetricia]",
                     font=ctk.CTkFont(size=20, weight="bold"),
                     text_color="gray", justify="center").place(relx=0.5, rely=0.55, anchor="center")

    main_content = ctk.CTkFrame(master=app, fg_color="white", corner_radius=0)
    main_content.grid(row=0, column=1, sticky="nsew")
    main_content.grid_rowconfigure((0, 1), weight=1)
    main_content.grid_columnconfigure((0, 1), weight=1)

    title_main = ctk.CTkLabel(master=main_content, text="Módulo Financiero",
                              fg_color=FONDO_CONTADOR_CLARO,
                              text_color=MAGENTA,
                              font=ctk.CTkFont(size=30, weight="bold"),
                              corner_radius=20, width=250, height=60
                              )
    title_main.place(x=20, y=20)

    btn_inventario = ctk.CTkButton(master=main_content, text="Ver inventario",
                                   command=ver_inventario,
                                   fg_color=GRIS_CLARO_CONTADOR,
                                   text_color="black",
                                   hover_color="#BFC8CE",
                                   font=ctk.CTkFont(size=22, weight="bold"),
                                   corner_radius=40, width=250, height=80)
    btn_inventario.grid(row=0, column=0, padx=50, pady=(150, 0), sticky="n")

    try:
        inventario_path = "image_cac7fb.png"
        inventario_pil_image = Image.open(inventario_path)
        inventario_ctk_image = ctk.CTkImage(light_image=inventario_pil_image, dark_image=inventario_pil_image,
                                            size=(250, 250))
        ctk.CTkLabel(master=main_content, image=inventario_ctk_image, text="").grid(row=1, column=0, padx=50,
                                                                                    pady=(10, 50), sticky="n")
    except Exception:
        ctk.CTkLabel(master=main_content, text="[Imagen Inventario]", text_color="gray",
                     font=ctk.CTkFont(size=20, slant="italic")).grid(row=1, column=0, padx=50, pady=(10, 50),
                                                                     sticky="n")

    btn_compras = ctk.CTkButton(master=main_content, text="Ver medicamentos comprados",
                                command=ver_medicamentos_comprados,
                                fg_color=GRIS_CLARO_CONTADOR,
                                text_color="black",
                                hover_color="#BFC8CE",
                                font=ctk.CTkFont(size=22, weight="bold"),
                                corner_radius=40, width=350, height=80)
    btn_compras.grid(row=0, column=1, padx=50, pady=(150, 0), sticky="n")

    try:
        compras_path = "image_cb4e88.png"
        compras_pil_image = Image.open(compras_path)
        compras_ctk_image = ctk.CTkImage(light_image=compras_pil_image, dark_image=compras_pil_image, size=(250, 250))
        ctk.CTkLabel(master=main_content, image=compras_ctk_image, text="").grid(row=1, column=1, padx=50,
                                                                                 pady=(10, 50), sticky="n")
    except Exception:
        ctk.CTkLabel(master=main_content, text="[Imagen Compras]", text_color="gray",
                     font=ctk.CTkFont(size=20, slant="italic")).grid(row=1, column=1, padx=50, pady=(10, 50),
                                                                     sticky="n")

    def cerrar_sesion():
        for widget in app.winfo_children():
            widget.destroy()
        app.update_idletasks()
        interfaz_login()

    ctk.CTkButton(master=main_content, text="Cerrar Sesión",
                  command=cerrar_sesion,
                  fg_color=MAGENTA, text_color="white",
                  hover_color=MORADO_CLARO, font=ctk.CTkFont(size=20, weight="bold"),
                  corner_radius=20, width=150, height=50
                  ).place(relx=1.0, rely=1.0, anchor="se", x=-20, y=-20)


def menu_proveedor():
    for widget in app.winfo_children():
        widget.destroy()

    app.title("Vender Medicamento")
    app.state('zoomed')
    app.configure(fg_color="white")

    app.grid_columnconfigure(0, weight=0)
    app.grid_columnconfigure(1, weight=1)
    app.grid_rowconfigure(0, weight=1)

    side_panel = ctk.CTkFrame(master=app, corner_radius=0, fg_color=CAFE_PROVEEDOR, width=300)
    side_panel.grid(row=0, column=0, sticky="nsew")

    title_side = ctk.CTkFrame(master=side_panel, fg_color="white", corner_radius=20, width=200, height=60)
    title_side.place(x=30, y=25)
    ctk.CTkLabel(master=title_side, text="Farmacia",
                 font=ctk.CTkFont(size=30, weight="bold"),
                 text_color=MAGENTA).place(relx=0.5, rely=0.5, anchor="center")

    try:
        logo_path = "Logo.png"
        logo_pil_image = Image.open(logo_path)
        logo_ctk_image = ctk.CTkImage(light_image=logo_pil_image, dark_image=logo_pil_image, size=(250, 250))
        ctk.CTkLabel(master=side_panel, image=logo_ctk_image, text="").place(relx=0.5, rely=0.55, anchor="center")
    except Exception:
        ctk.CTkLabel(master=side_panel, text="[Dra. Angie Ajquill\nGinecología y Obstetricia]",
                     font=ctk.CTkFont(size=20, weight="bold"),
                     text_color="gray", justify="center").place(relx=0.5, rely=0.55, anchor="center")

    main_content = ctk.CTkFrame(master=app, fg_color="white", corner_radius=0)
    main_content.grid(row=0, column=1, sticky="nsew")
    main_content.grid_rowconfigure(1, weight=1)
    main_content.grid_columnconfigure(0, weight=1)

    title_main = ctk.CTkLabel(master=main_content, text="Vender Medicamento",
                              fg_color=CAFE_CLARO,
                              font=ctk.CTkFont(size=30, weight="bold"),
                              text_color="black",
                              corner_radius=20, width=350, height=60
                              )
    title_main.grid(row=0, column=0, padx=20, pady=20, sticky="w")

    form_frame = ctk.CTkFrame(master=main_content, fg_color="transparent")
    form_frame.grid(row=1, column=0, sticky="nsew", padx=50, pady=(50, 20))
    form_frame.grid_columnconfigure(0, weight=1)
    form_frame.grid_columnconfigure(1, weight=2)

    nombre_var = ctk.StringVar()
    cantidad_var = ctk.StringVar()
    precio_var = ctk.StringVar()

    def crear_etiqueta_estilizada(master, row, text):
        label_frame = ctk.CTkFrame(master=master, fg_color=MORADO_VIVO, corner_radius=20, width=280, height=60)
        label_frame.grid(row=row, column=0, padx=(150, 30), pady=25, sticky="e")
        ctk.CTkLabel(master=label_frame, text=text, text_color=MAGENTA,
                     font=ctk.CTkFont(size=22, weight="bold")).place(relx=0.5, rely=0.5, anchor="center")

    crear_etiqueta_estilizada(form_frame, 0, "Nombre del medicamento:")

    entry_nombre = ctk.CTkEntry(master=form_frame, textvariable=nombre_var, placeholder_text="Ej. Ampicilina 500mg",
                                font=ctk.CTkFont(size=18), width=350, height=50, border_width=2, corner_radius=10)
    entry_nombre.grid(row=0, column=1, padx=(20, 150), pady=25, sticky="w")

    crear_etiqueta_estilizada(form_frame, 1, "Cantidad a vender:")

    entry_cantidad = ctk.CTkEntry(master=form_frame, textvariable=cantidad_var, placeholder_text="Ej. 10",
                                  font=ctk.CTkFont(size=18), width=350, height=50, border_width=2, corner_radius=10)
    entry_cantidad.grid(row=1, column=1, padx=(20, 150), pady=25, sticky="w")

    crear_etiqueta_estilizada(form_frame, 2, "Precio de Venta (Q):")

    entry_precio = ctk.CTkEntry(master=form_frame, textvariable=precio_var, placeholder_text="Ej. 45.00",
                                font=ctk.CTkFont(size=18), width=350, height=50, border_width=2, corner_radius=10)
    entry_precio.grid(row=2, column=1, padx=(20, 150), pady=25, sticky="w")

    def realizar_venta_proveedor():
        nombre = nombre_var.get().strip()
        cantidad = cantidad_var.get().strip()
        precio = precio_var.get().strip()

        if not nombre or not cantidad or not precio:
            messagebox.showwarning("Advertencia", "Nombre, Cantidad (Stock) y Precio son obligatorios.")
            return

        try:
            # Validar y convertir la Cantidad a entero (Stock)
            cantidad_int = int(cantidad)
            if cantidad_int <= 0:
                messagebox.showwarning("Advertencia", "La Cantidad (Stock) debe ser un valor positivo.")
                return
        except ValueError:
            messagebox.showwarning("Advertencia",
                                   "La Cantidad (Stock) tiene un formato incorrecto (debe ser un número entero).")
            return

        try:
            precio_float = float(precio)
            if precio_float <= 0:
                messagebox.showwarning("Advertencia", "El Precio de Venta debe ser mayor que cero.")
                return
        except ValueError:
            messagebox.showwarning("Advertencia",
                                   "El Precio de Venta tiene un formato incorrecto (debe ser un número decimal).")
            return

        try:
            proveedor = Proveedor(nombre=usuario_actual.nombre, rol=usuario_actual.rol, db=db)
            proveedor.id = usuario_actual.id
            resultado = proveedor.agregar_producto(
                nombre=nombre,
                precio=precio_float,
                stock=cantidad_int
            )
            messagebox.showinfo("Registro Exitoso",
                                f"Producto '{nombre}' registrado/actualizado en el inventario.\nStock Añadido: {cantidad_int}\nPrecio de Venta: Q{precio_float:.2f}")

            nombre_var.set("")
            cantidad_var.set("")
            precio_var.set("")

        except Exception as e:
            messagebox.showerror("Error de Registro", f"Ocurrió un error inesperado al registrar el producto: {e}")


    ctk.CTkButton(master=form_frame, text="Vender Medicamento",
                  command=realizar_venta_proveedor,
                  fg_color=MAGENTA, text_color="white",
                  hover_color=MORADO_CLARO, font=ctk.CTkFont(size=20, weight="bold"),
                  corner_radius=20, width=300, height=60
                  ).grid(row=3, column=0, columnspan=2, pady=50)

    def cerrar_sesion():
        for widget in app.winfo_children():
            widget.destroy()
        app.update_idletasks()
        interfaz_login()

    ctk.CTkButton(master=main_content, text="Cerrar Sesión",
                  command=cerrar_sesion,
                  fg_color=CAFE_PROVEEDOR, text_color="white",
                  hover_color=CAFE_CLARO, font=ctk.CTkFont(size=20, weight="bold"),
                  corner_radius=20, width=150, height=50
                  ).place(relx=1.0, rely=1.0, anchor="se", x=-20, y=-20)
def interfaz_login():
    global usuario_actual
    app.state('zoomed')

    for i in range(3):
        app.grid_columnconfigure(i, weight=0)
        app.grid_rowconfigure(i, weight=0)

    app.grid_columnconfigure(0, weight=1)
    app.grid_columnconfigure(1, weight=1)
    app.grid_rowconfigure(0, weight=1)

    left_frame = ctk.CTkFrame(master=app, corner_radius=0, fg_color=LILA)
    left_frame.grid(row=0, column=0, sticky="nswe", padx=40, pady=20)

    try:
        imagen_fondo = Image.open("figura.png")
        ctk_image = ctk.CTkImage(light_image=imagen_fondo, dark_image=imagen_fondo, size=(800, 800))
        logo_etiqueta = ctk.CTkLabel(master=left_frame, image=ctk_image, text="")
        logo_etiqueta.place(relx=0.5, rely=0.5, anchor="center")
    except Exception as e:
        print(f"Error al cargar fondo: {e}")

    left_frame.grid_rowconfigure(0, weight=1)
    left_frame.grid_rowconfigure(7, weight=1)
    left_frame.grid_columnconfigure(0, weight=1)
    left_frame.grid_columnconfigure(2, weight=1)

    title_label = ctk.CTkLabel(master=left_frame, text="Iniciar sesión",
                               font=ctk.CTkFont(family=FONT_FAMILY, size=100),
                               fg_color="white",
                               bg_color="white")
    title_label.grid(row=1, column=1, sticky="nsew", pady=(20, 40), padx=20)

    user_label = ctk.CTkLabel(master=left_frame, text="Usuario:",
                              font=ctk.CTkFont(family=FONT_FAMILY, size=30),
                              fg_color="white")
    user_label.grid(row=2, column=1, sticky="w", padx=20)

    user_entry = ctk.CTkEntry(master=left_frame, width=450, height=50,
                              placeholder_text="Ingrese su nombre de usuario",
                              font=ctk.CTkFont(size=18),
                              corner_radius=15,
                              bg_color="white",
                              fg_color="white", border_width=0
                              )
    user_entry.grid(row=3, column=1, sticky="ew", padx=20, pady=(5, 30))

    pass_label = ctk.CTkLabel(master=left_frame, text="Contraseña:",
                              font=ctk.CTkFont(family=FONT_FAMILY, size=30),
                              fg_color="white")
    pass_label.grid(row=4, column=1, sticky="w", padx=20)

    pass_entry = ctk.CTkEntry(master=left_frame, width=450, height=50, show="*",
                              placeholder_text="Ingrese su contraseña",
                              font=ctk.CTkFont(size=18),
                              corner_radius=15,
                              bg_color="white",
                              fg_color="white", border_width=0
                              )
    pass_entry.grid(row=5, column=1, sticky="ew", padx=20, pady=(5, 30))

    right_frame = ctk.CTkFrame(master=app, corner_radius=0, fg_color=MAGENTA)
    right_frame.grid(row=0, column=1, sticky="nswe")

    try:
        logo_path = "Logo.png"
        logo_pil_image = Image.open(logo_path)
        logo_ctk_image = ctk.CTkImage(light_image=logo_pil_image, dark_image=logo_pil_image, size=(550, 550))
        logo_label = ctk.CTkLabel(master=right_frame, image=logo_ctk_image, text="")
        logo_label.place(relx=0.5, rely=0.5, anchor="center")
    except FileNotFoundError:
        print("No se encontró la imagen del logo. Mostrando texto alternativo.")
        logo_label = ctk.CTkLabel(
            master=right_frame,
            text="[ LOGO DE MUESTRA ]",
            font=ctk.CTkFont(size=30, weight="bold"),
            text_color="white",
            fg_color="transparent"
        )
        logo_label.place(relx=0.5, rely=0.5, anchor="center")

    def intentar_login():
        global usuario_actual
        usuario = user_entry.get()

        contra = pass_entry.get()

        if not usuario or not contra:
            messagebox.showwarning("Advertencia", "Por favor, ingrese usuario y contraseña.")
            return


        temp_user = Usuario(nombre="", rol="", db=db)
        datos_usuario = temp_user.iniciar_sesion(usuario, contra)

        if datos_usuario:
            rol = datos_usuario["rol"]
            messagebox.showinfo("Éxito", f"Bienvenido(a) {rol}")


            if rol == "Doctor":
                usuario_actual = Doctor(datos_usuario["nombre"], rol, db=db)
            elif rol == "Contador":
                usuario_actual = Contador(datos_usuario["nombre"], rol, db=db)
            elif rol == "Proveedor":
                usuario_actual = Proveedor(datos_usuario["nombre"], rol, db=db)
            else:
                usuario_actual = Usuario(datos_usuario["nombre"], rol, db=db)


            usuario_actual.id = datos_usuario["id"]


            if rol == "Doctor":
                crear_interfaz_principal()
            elif rol == "Contador":
                menu_contador()
            elif rol == "Proveedor":
                menu_proveedor()

        else:
            messagebox.showerror("Error", "Credenciales incorrectas.")

    login_button = ctk.CTkButton(master=left_frame, text="Iniciar Sesión",
                                 command=intentar_login, width=450, height=60,
                                 font=ctk.CTkFont(size=22),
                                 fg_color=MAGENTA, hover_color=MORADO_CLARO,
                                 corner_radius=100,
                                 bg_color="white")
    login_button.grid(row=6, column=1, sticky="ew", padx=20, pady=(40, 0))


# --- INICIO DEL PROGRAMA ---

interfaz_login()
app.mainloop()