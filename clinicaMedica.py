import customtkinter as ctk
from PIL import Image
from tkinter import messagebox

FONT_FAMILY = "Edwardian Script ITC"

ctk.set_appearance_mode("Light")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.update()
app.state('zoomed')
app.title("Inicio de Sesión")

#opciones del menu
def crear_ventana_agregar_paciente():
    sub = ctk.CTkToplevel(app)
    sub.title("Agregar Paciente")
    sub.state('zoomed')
    sub.configure(fg_color="white")
    # Asegurar que esté sobre la ventana principal
    sub.transient(app)
    sub.grab_set()
    sub.lift()
    sub.focus_force()

    COLOR_MORADO_CLARO = "#bd7efb"
    COLOR_MORADO_OSCURO = "#560554"
    COLOR_MORADO_BOTON = "#FFFFFF"
    COLOR_BOTON_GUARDAR = "#FDC2FE"

    sub.grid_columnconfigure(0, weight=0)
    sub.grid_columnconfigure(1, weight=1)
    sub.grid_rowconfigure(0, weight=1)

    # Panel lateral
    side_panel = ctk.CTkFrame(master=sub, corner_radius=0, fg_color=COLOR_MORADO_CLARO, width=300)
    side_panel.grid(row=0, column=0, sticky="nsew")

    header_frame = ctk.CTkFrame(master=side_panel, fg_color="#F0E8F8", corner_radius=20, width=200, height=60)
    header_frame.place(x=30, y=25)
    ctk.CTkLabel(master=header_frame, text="Dr. Maggie",
                 font=ctk.CTkFont(size=30, weight="bold"),
                 text_color=COLOR_MORADO_OSCURO).place(relx=0.5, rely=0.5, anchor="center")
    try:
        logo_path = "Logo.png"
        logo_pil_image = Image.open(logo_path)
        logo_ctk_image = ctk.CTkImage(light_image=logo_pil_image, dark_image=logo_pil_image, size=(250, 250))
        logo_label = ctk.CTkLabel(master=side_panel, image=logo_ctk_image, text="")
        logo_label.place(relx=0.5, rely=0.5, anchor="center")
    except Exception:
        ctk.CTkLabel(master=side_panel, text="[Dra. Angie Ajquill\nGinecología y Obstetricia]", font=ctk.CTkFont(size=20, weight="bold"),text_color="white",justify="center").place(relx=0.5, rely=0.5, anchor="center")


    # Contenido principal
    main_content = ctk.CTkFrame(master=sub, fg_color="white", corner_radius=0)
    main_content.grid(row=0, column=1, sticky="nsew")
    main_content.grid_columnconfigure(0, weight=0)##

    # Etiqueta "Agregar paciente"
    ctk.CTkLabel(master=main_content,text="Agregar paciente",fg_color=COLOR_MORADO_CLARO,text_color=COLOR_MORADO_OSCURO,font=ctk.CTkFont(size=30, weight="bold"),
                 corner_radius=40,
                 width=300,
                 height=60).grid(row=0, column=0, pady=(20, 40), padx=40, sticky="w")

    # Botón Cerrar a la derecha
    ctk.CTkButton(master=main_content,text="Cerrar ventana",command=sub.destroy,fg_color="#E3A5F0",text_color="white",hover_color="#C67EE7",
                  font=ctk.CTkFont(size=22, weight="bold"),
                  corner_radius=20,
                  width=220,
                  height=70).grid(row=0, column=1, sticky="e", padx=40, pady=(20, 40))

    # Formulario
    form_frame = ctk.CTkFrame(master=main_content, fg_color="transparent")
    form_frame.grid(row=1, column=0, columnspan=2, pady=(10, 50))
    form_frame.grid_columnconfigure(0, weight=1)
    form_frame.grid_columnconfigure(1, weight=2)

    try:
        image_path = "Logo.png"
        logo_pil_image = Image.open(image_path)
        logo_ctk_image = ctk.CTkImage(light_image=logo_pil_image, dark_image=logo_pil_image, size=(250, 250))
        logo_label = ctk.CTkLabel(master=form_frame, image=logo_ctk_image, text="")
        logo_label.place(relx=0.5, rely=0.5, anchor="n")
    except Exception:
        ctk.CTkLabel(master=side_panel, text="[Dra. Angie Ajquill\nGinecología y Obstetricia]", font=ctk.CTkFont(size=20, weight="bold"),text_color="white",justify="center").place(relx=0.5, rely=0.5, anchor="center")


    CAMPOS = ["Nombre:", "DPI:", "No. Tel:"]
    entries = {}

    for i, label_text in enumerate(CAMPOS):
        label_frame = ctk.CTkFrame(master=form_frame, fg_color=COLOR_MORADO_CLARO,
                                   corner_radius=20, width=200, height=60)
        label_frame.grid(row=i, column=0, padx=(150, 30), pady=30, sticky="e")
        ctk.CTkLabel(master=label_frame, text=label_text,
                     text_color=COLOR_MORADO_OSCURO,
                     font=ctk.CTkFont(size=22, weight="bold")).place(relx=0.5, rely=0.5, anchor="center")

        entry_frame = ctk.CTkFrame(master=form_frame, fg_color=COLOR_MORADO_BOTON,
                                   corner_radius=20, width=500, height=60)
        entry_frame.grid(row=i, column=1, padx=(20, 150), pady=30, sticky="w")
        entry = ctk.CTkEntry(master=entry_frame,
                             placeholder_text=f"Ingrese {label_text.replace(':', '')}",
                             fg_color=COLOR_MORADO_BOTON,
                             text_color="black",
                             font=ctk.CTkFont(size=20),
                             border_width=0,
                             width=460,
                             height=45)
        entry.place(relx=0.5, rely=0.5, anchor="center")
        entries[label_text] = entry

    # Botón Guardar
    def guardar_paciente():
        nombre = entries["Nombre:"].get()
        dpi = entries["DPI:"].get()
        tel = entries["No. Tel:"].get()
        if nombre and dpi and tel:
            messagebox.showinfo("Éxito", f"Paciente guardado: {nombre}")
            sub.destroy()
        else:
            messagebox.showwarning("Advertencia", "Todos los campos son obligatorios.")

    ctk.CTkButton(master=main_content,
                  text="Guardar",
                  command=guardar_paciente,
                  fg_color=COLOR_BOTON_GUARDAR,
                  text_color=COLOR_MORADO_OSCURO,
                  hover_color="#F0B4FB",
                  font=ctk.CTkFont(size=26, weight="bold"),
                  corner_radius=30,
                  width=250,
                  height=80).grid(row=2, column=0, columnspan=2, pady=40)


#funciones principales----------------------------------------------------------------------

def crear_interfaz_principal():

    for widget in app.winfo_children():
        widget.destroy()

    #FONDO PRINCIPAL
    app.configure(fg_color="#e5d2ef")
    app.title("Menú Principal - Dr. Maggie")

    # --- CABECERA ---
    header_frame = ctk.CTkFrame(
        master=app,
        fg_color="#F0E8F8",
        corner_radius=20,
        width=200,
        height=60
    )
    header_frame.place(x=40, y=40)

    header_label = ctk.CTkLabel(
        master=header_frame,
        text="Dr. Maggie",
        font=ctk.CTkFont(size=26, weight="bold"),
        text_color="#560554"
    )
    header_label.place(relx=0.5, rely=0.5, anchor="center")

    # --- MARCO PRINCIPAL ---fcf6fb
    menu_frame = ctk.CTkFrame(
        master=app,
        fg_color="#bd7efb",
        corner_radius=40,
        width=1100,
        height=650
    )
    menu_frame.place(relx=0.5, rely=0.5, anchor="center")

    menu_frame.grid_rowconfigure((0, 1, 2), weight=1)
    menu_frame.grid_columnconfigure((0, 1, 2), weight=1)

    BUTTON_WIDTH = 280
    BUTTON_HEIGHT = 100
    BUTTON_FONT = ctk.CTkFont(size=22, weight="bold")
    BUTTON_COLOR = "#FFFFFF"

    botones = [
        ("Agregar paciente", 0, 0, crear_ventana_agregar_paciente),
        ("Crear ficha médica", 0, 1, lambda: abrir_nueva_pantalla("Crear Ficha Médica")),
        ("Agendar cita", 0, 2, lambda: abrir_nueva_pantalla("Agendar Cita")),
        ("Buscar ficha médica", 1, 0, lambda: abrir_nueva_pantalla("Buscar Ficha Médica")),
        ("Ver citas", 1, 1, lambda: abrir_nueva_pantalla("Ver Citas")),
        ("Cancelar cita", 1, 2, lambda: abrir_nueva_pantalla("Cancelar Cita")),
        ("Vender medicamento", 2, 0, lambda: abrir_nueva_pantalla("Vender Medicamento")),
        ("", 2, 1, None),
        ("Ver inventario", 2, 2, lambda: abrir_nueva_pantalla("Ver Inventario"))
    ]

    for text, row, col, command in botones:
        if text:
            button = ctk.CTkButton(master=menu_frame,text=text,command=command,width=BUTTON_WIDTH,height=BUTTON_HEIGHT,fg_color=BUTTON_COLOR,
                text_color="#560554",
                hover_color="#EEE8F8",
                font=BUTTON_FONT,
                corner_radius=25
            )
            button.grid(row=row, column=col, padx=30, pady=30, sticky="nsew")
        elif not text and command is None:
            ctk.CTkFrame(master=menu_frame, fg_color="transparent").grid(row=row, column=col, sticky="nsew")


# ------------------------------------------------------
def abrir_nueva_pantalla(titulo):
    print(f"Abriendo ventana: {titulo}...")
    sub = ctk.CTkToplevel(app)
    sub.title(titulo)
    sub.geometry("800x600+200+100")
    sub.lift()
    sub.focus_force()
    sub.grab_set()

    ctk.CTkLabel(
        sub,
        text=f"{titulo}",
        font=ctk.CTkFont(size=30, weight="bold")
    ).pack(pady=40)

    ctk.CTkButton(
        sub,text="Cerrar ventana",command=sub.destroy,fg_color="#560554",text_color="white",width=250,height=60,font=ctk.CTkFont(size=20, weight="bold"),
        corner_radius=15
    ).pack(pady=30)

#-----------------------------------------------------------------

def intentar_login():
    usuario = user_entry.get()
    contra= pass_entry.get()

    if usuario == "admin" and contra== "1":
        crear_interfaz_principal()

    elif usuario!="admin":
        messagebox.showerror("Error", "Usuario incorrecto.")
    elif contra!="1":
        messagebox.showerror("Error", "Contraseña incorrecta.")
    else:
        messagebox.showerror("Error", "Usuario o contraseña incorrectos.")

app.grid_columnconfigure(0, weight=1)
app.grid_columnconfigure(1, weight=1)
app.grid_rowconfigure(0, weight=1)

#IZQUIERDO (Formulario) ---
left_frame = ctk.CTkFrame(master=app, corner_radius=0, fg_color="#e9c7fb")
left_frame.grid(row=0, column=0, sticky="nswe", padx=40, pady=20)

try:
    imagen_fondo = Image.open("figura.png")
    ctk_image = ctk.CTkImage(light_image=imagen_fondo, dark_image=imagen_fondo, size=(960, 800))
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
                           fg_color="white")
title_label.grid(row=1, column=1, sticky="nsew", pady=(20, 40), padx=20)

user_label = ctk.CTkLabel(master=left_frame, text="Usuario:",
                          font=ctk.CTkFont(family=FONT_FAMILY, size=30),
                          fg_color="white")
user_label.grid(row=2, column=1, sticky="w", padx=20)

user_entry = ctk.CTkEntry(master=left_frame, width=450, height=50,
                          placeholder_text="Ingrese su nombre de usuario",
                          font=ctk.CTkFont(size=18))
user_entry.grid(row=3, column=1, sticky="ew", padx=20, pady=(5, 30))

pass_label = ctk.CTkLabel(master=left_frame, text="Contraseña:",
                          font=ctk.CTkFont(family=FONT_FAMILY, size=30),
                          fg_color="white")
pass_label.grid(row=4, column=1, sticky="w", padx=20)

pass_entry = ctk.CTkEntry(master=left_frame, width=450, height=50, show="*",
                          placeholder_text="Ingrese su contraseña",
                          font=ctk.CTkFont(size=18))
pass_entry.grid(row=5, column=1, sticky="ew", padx=20, pady=(5, 30))

login_button = ctk.CTkButton(master=left_frame, text="Iniciar Sesión",
                             command=intentar_login, width=450, height=60,
                             font=ctk.CTkFont(size=22),
                             fg_color="#560554")
login_button.grid(row=6, column=1, sticky="ew", padx=20, pady=(40, 0))

#derecha IMAGEN LOGO

right_frame = ctk.CTkFrame(master=app, corner_radius=0, fg_color="#560554")
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
        text_color="#e5d2ef",
        fg_color="transparent"
    )
    logo_label.place(relx=0.5, rely=0.5, anchor="center")

# --- INICIO DEL PROGRAMA ---
app.mainloop()