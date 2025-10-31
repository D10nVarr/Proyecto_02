import customtkinter as ctk
from PIL import Image
from tkinter import messagebox

FONT_FAMILY = "Edwardian Script ITC"

LILA="#e9c7fb"
MAGENTA="#560554"
MORADO_VIVO="#bd7efb"
ROSADO="#FDC2FE"
BOTON_USUARIO="#F0E8F8"
MORADO_CLARO="#C67EE7"

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

    # Mantener la ventana encima de la principal y modal
    sub.transient(app)
    sub.grab_set()
    sub.lift()
    sub.focus_force()

    # Grid principal de la subventana
    sub.grid_rowconfigure(0, weight=1)
    sub.grid_columnconfigure(0, weight=0)   # panel lateral fijo
    sub.grid_columnconfigure(1, weight=2)   # formulario (más ancho)
    sub.grid_columnconfigure(2, weight=1)   # columna imagen (menos ancho)

    # PANEL LATERAL
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
        logo_label=ctk.CTkLabel(master=side_panel, image=logo_ctk_image, text="")
        logo_label.place(relx=0.5, rely=0.5, anchor="center")
    except Exception:
        ctk.CTkLabel(master=side_panel, text="[Dra. Angie Ajquill\nGinecología y Obstetricia]",
                     font=ctk.CTkFont(size=20, weight="bold"), text_color="white", justify="center"
                     ).place(relx=0.5, rely=0.6, anchor="center")

    # CONTENIDO PRINCIPAL (formulario + imagen)
    main_content = ctk.CTkFrame(master=sub, fg_color="white", corner_radius=0)
    main_content.grid(row=0, column=1, sticky="nsew")
    # Configurar columnas internas: 0 etiquetas, 1 entradas (form), 2 imagen (columna externa pero aquí la reservamos)
    main_content.grid_columnconfigure(0, weight=1)
    main_content.grid_columnconfigure(1, weight=2)
    main_content.grid_columnconfigure(2, weight=1)

    # Filas: 0 título, 1 formulario, 2 espacio flexible, 3 boton guardar
    main_content.grid_rowconfigure(0, weight=0)
    main_content.grid_rowconfigure(1, weight=0)
    main_content.grid_rowconfigure(2, weight=1)
    main_content.grid_rowconfigure(3, weight=0)

    # --- Título ---
    ctk.CTkLabel(master=main_content, text="Agregar paciente",
                 fg_color=MORADO_VIVO, text_color=MAGENTA,
                 font=ctk.CTkFont(size=30, weight="bold"),
                 corner_radius=40, width=320, height=60
                 ).grid(row=0, column=0, columnspan=2, pady=(20, 20), padx=40, sticky="w")

    # --- Botón Cerrar (misma Y que el título) colocado sobre la columna de la imagen ---
    ctk.CTkButton(master=main_content, text="Cerrar ventana",
                  command=sub.destroy, fg_color=MAGENTA, text_color="white",
                  hover_color=MORADO_CLARO, font=ctk.CTkFont(size=20, weight="bold"),
                  corner_radius=20, width=220, height=60
                  ).grid(row=0, column=2, sticky="e", padx=(0, 40), pady=(20, 20))

    # --- Formulario (etiquetas / entradas) ---
    form_frame = ctk.CTkFrame(master=main_content, fg_color="transparent")
    form_frame.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=(60, 0), pady=(100, 100))
    form_frame.grid_columnconfigure(0, weight=1)
    form_frame.grid_columnconfigure(1, weight=3)

    CAMPOS = ["Nombre:", "DPI:", "No. Tel:"]
    entries = {}

    for i, label_text in enumerate(CAMPOS):
        # Etiqueta (col 0)
        ctk.CTkLabel(master=form_frame, text=label_text,
                     text_color=MAGENTA, font=ctk.CTkFont(size=20, weight="bold"),
                     ).grid(row=i, column=1, sticky="e", padx=(0, 20), pady=20)

        # Entrada (col 1) — suficiente ancho y sticky para mostrar texto completo
        entry = ctk.CTkEntry(master=form_frame,
                             placeholder_text=f"Ingrese {label_text.replace(':', '')}",
                             width=600, height=60,
                             fg_color="white", text_color="black",
                             font=ctk.CTkFont(size=20), border_width=0
                             )
        entry.grid(row=i, column=2, sticky="w", padx=(0, 80), pady=20)
        entries[label_text] = entry

    # --- Imagen a la derecha (col 2 de main_content) ---
    try:
        img_path = "paciente.jpg"
        paciente_pil = Image.open(img_path)
        paciente_img = ctk.CTkImage(light_image=paciente_pil, dark_image=paciente_pil, size=(300, 300))
        ctk.CTkLabel(master=main_content, image=paciente_img, text="").grid(row=1, column=2, padx=40, pady=(150,10), sticky="n")
    except Exception as e:
        print(f"No se pudo cargar imagen del paciente: {e}")
        ctk.CTkLabel(master=main_content, text="[Imagen paciente]", text_color="gray",
                     font=ctk.CTkFont(size=20, slant="italic")).grid(row=1, column=2, padx=40, pady=10, sticky="n")

    # --- Botón Guardar centrado abajo ---
    def guardar_paciente():
        nombre = entries["Nombre:"].get()
        dpi = entries["DPI:"].get()
        tel = entries["No. Tel:"].get()
        if nombre and dpi and tel:
            messagebox.showinfo("Éxito", f"Paciente guardado: {nombre}")
            sub.destroy()
        else:
            messagebox.showwarning("Advertencia", "Todos los campos son obligatorios.")

    ctk.CTkButton(master=main_content, text="Guardar",
                  command=guardar_paciente, fg_color=ROSADO, text_color=MAGENTA,
                  hover_color="#transparente", font=ctk.CTkFont(size=24, weight="bold"),
                  corner_radius=30, width=300, height=80
                  ).grid(row=2, column=0, columnspan=3, pady=(10, 40), sticky="n")


def buscar_paciente():
    sub = ctk.CTkToplevel(app)
    sub.title("Buscar paciente")
    sub.state('zoomed')
    sub.configure(fg_color="white")
    # Asegurar que esté sobre la ventana principal
    sub.transient(app)
    sub.grab_set()
    sub.lift()
    sub.focus_force()

    sub.grid_columnconfigure(0, weight=0)
    sub.grid_columnconfigure(1, weight=1)
    sub.grid_rowconfigure(0, weight=1)

    # Panel lateral
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
        ctk.CTkLabel(master=side_panel, text="[Dra. Angie Ajquill\nGinecología y Obstetricia]", font=ctk.CTkFont(size=20, weight="bold"),text_color="white",justify="center").place(relx=0.5, rely=0.5, anchor="center")


    # Contenido principal
    main_content = ctk.CTkFrame(master=sub, fg_color="white", corner_radius=0)
    main_content.grid(row=0, column=1, sticky="nsew")
    main_content.grid_columnconfigure(0, weight=0)##

    # Etiqueta "Agregar paciente"
    ctk.CTkLabel(master=main_content,text="Buscar datos de paciente",fg_color=MORADO_VIVO,text_color=MAGENTA,font=ctk.CTkFont(size=30, weight="bold"),
                 corner_radius=40,
                 width=300,
                 height=60).grid(row=0, column=0, pady=(20, 40), padx=40, sticky="w")

    # Botón Cerrar a la derecha
    ctk.CTkButton(master=main_content,text="Cerrar ventana",command=sub.destroy,fg_color=MAGENTA,text_color="white",hover_color=MORADO_CLARO,
                  font=ctk.CTkFont(size=22, weight="bold"),
                  corner_radius=20,
                  width=220,
                  height=70).grid(row=0, column=1, sticky="e", padx=40, pady=(20, 40))

    # Formulario
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

    dpi_paprueba="1234567890"

    def buscar():
        dpi = entry.get()
        if dpi == dpi_paprueba:
            # 1. Simular datos (en un futuro, esto vendría de una BD)
            # (Usaré datos de ejemplo)
            nombre_simulado = "Nombre Paciente de Prueba"
            tel_simulado = "5555-1234"

            # 2. Mostrar éxito y cerrar la ventana de búsqueda
            messagebox.showinfo("Éxito", f"Paciente encontrado: {nombre_simulado}")
            sub.destroy()

            # 3. Abrir la nueva ventana de "Crear Ficha Médica"
            #    pasándole los datos encontrados.
            crear_ventana_ficha_medica(dpi, nombre_simulado, tel_simulado)

        elif not dpi:
            messagebox.showwarning("Advertencia", "El campo DPI no puede estar vacío.")
        else:
            messagebox.showerror("Error", f"Paciente con DPI {dpi} no encontrado.")

    ctk.CTkButton(master=main_content,
                  text="Buscar",
                  command=buscar,
                  fg_color=ROSADO,
                  text_color=MAGENTA,
                  hover_color="#F0B4FB",
                  font=ctk.CTkFont(size=26, weight="bold"),
                  corner_radius=30,
                  width=250,
                  height=80).grid(row=2, column=0, columnspan=2, pady=40)


def crear_ventana_ficha_medica(dpi_paciente, nombre_paciente, tel_paciente):
    """
    Crea la ventana para llenar la ficha médica con diseño igual al mostrado en la imagen.
    """
    sub = ctk.CTkToplevel(app)
    sub.title("Crear Ficha Médica")
    sub.state('zoomed')
    sub.configure(fg_color="white")

    # Modal sobre la ventana principal
    sub.transient(app)
    sub.grab_set()
    sub.lift()
    sub.focus_force()

    # ============= ESTRUCTURA GENERAL (Panel lateral + Contenido principal) =============
    sub.grid_rowconfigure(0, weight=1)
    sub.grid_columnconfigure(0, weight=0)
    sub.grid_columnconfigure(1, weight=1)

    # Panel lateral igual a las otras ventanas
    side_panel = ctk.CTkFrame(master=sub, corner_radius=0, fg_color=MORADO_VIVO, width=300)
    side_panel.grid(row=0, column=0, sticky="nsew")

    header_frame = ctk.CTkFrame(master=side_panel, fg_color=BOTON_USUARIO, corner_radius=20, width=200, height=60)
    header_frame.place(x=30, y=25)
    ctk.CTkLabel(master=header_frame, text="Dr.maggie",
                 font=ctk.CTkFont(size=30, weight="bold"),
                 text_color=MAGENTA).place(relx=0.5, rely=0.5, anchor="center")

    # Logo
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

    # ====================== CONTENIDO PRINCIPAL ======================
    main_content = ctk.CTkFrame(master=sub, fg_color="white", corner_radius=0)
    main_content.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
    main_content.grid_columnconfigure(0, weight=1)
    main_content.grid_rowconfigure(3, weight=1)

    # ----- Título y botón cerrar -----
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

    # ----- FRAME DEL FORMULARIO -----
    form_frame = ctk.CTkFrame(master=main_content, fg_color="transparent")
    form_frame.grid(row=1, column=0, sticky="nsew", padx=(60, 0), pady=(10, 10))
    form_frame.grid_columnconfigure((0, 1, 2), weight=1)

    entries = {}

    def campo(label_text, row, col_label, col_entry, colspan=1):
        """Función auxiliar para crear un campo morado + entrada."""

        entry = ctk.CTkEntry(master=form_frame, fg_color="white", text_color="black",
                             border_width=2,border_color=MORADO_VIVO, corner_radius=60, height=40,placeholder_text=f"Ingrese la {label_text}",
                             font=ctk.CTkFont(size=16))
        entry.grid(row=row, column=col_entry, columnspan=colspan, padx=5, pady=8, sticky="ew")
        return entry

    # -------- Fila 1: Paciente, DPI, Teléfono --------
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

    # -------- Fila 2: Procedencia, Ocupación, Fecha --------
    entries['procedencia'] = campo("Procedencia:", 1, 0, 0)
    entries['ocupacion'] = campo("Ocupación:", 1, 1, 1)
    entries['fecha_nac'] = campo("Fecha de nacimiento:", 1, 2, 2)

    # -------- Fila 3: Antecedentes (larga) --------
    ctk.CTkFrame(master=form_frame, fg_color=MORADO_VIVO, corner_radius=20, height=50).grid(
        row=2, column=0, padx=5, pady=8, sticky="ew")
    ctk.CTkLabel(master=form_frame, text="Antecedentes:", font=ctk.CTkFont(size=16, weight="bold"),
                 text_color="black", anchor="w", fg_color=MORADO_VIVO, bg_color=MORADO_VIVO).grid(row=2, column=0, padx=20, pady=8, sticky="w")
    entries['antecedentes'] =ctk.CTkEntry(master=form_frame, fg_color=BOTON_USUARIO, text_color="black",
                                           border_width=0, corner_radius=20, height=50,
                                           font=ctk.CTkFont(size=16))
    entries['antecedentes'].grid(row=2, column=1, columnspan=2, padx=5, pady=8, sticky="ew")

    # -------- Fila 4: Datos (larga) --------
    ctk.CTkFrame(master=form_frame, fg_color=MORADO_VIVO, corner_radius=20, height=50).grid(
        row=3, column=0, padx=5, pady=8, sticky="ew")
    ctk.CTkLabel(master=form_frame, text="Datos:", font=ctk.CTkFont(size=16, weight="bold"),
                 text_color="black", anchor="w", fg_color=MORADO_VIVO, bg_color=MORADO_VIVO).grid(row=3, column=0, padx=20, pady=8, sticky="w")

    # ----- Textbox de consulta -----
    ctk.CTkLabel(master=main_content, text="Ingrese los datos de la consulta:",
                 font=ctk.CTkFont(size=20, weight="bold"), text_color=MAGENTA
                 ).grid(row=2, column=0, padx=60, pady=(10, 5), sticky="w")

    consulta_textbox = ctk.CTkTextbox(master=main_content, height=220,
                                      corner_radius=20, border_width=2,
                                      border_color=LILA, fg_color="white",
                                      text_color="black", font=ctk.CTkFont(size=16))
    consulta_textbox.grid(row=3, column=0, sticky="nsew", padx=60, pady=(0, 10))

    # ----- Botón Guardar(con diccionario mientras se carga DB) -----
    def guardar_ficha():
        procedencia = entries['procedencia'].get()
        ocupacion = entries['ocupacion'].get()
        datos_consulta = consulta_textbox.get("1.0", "end-1c")
        if not procedencia or not ocupacion or not datos_consulta:
            messagebox.showwarning("Advertencia", "Debe llenar Procedencia, Ocupación y Datos de la Consulta.")
            return
        messagebox.showinfo("Éxito", "Ficha médica guardada correctamente.")
        sub.destroy()

    ctk.CTkButton(master=main_content, text="Guardar Ficha",
                  command=guardar_ficha, fg_color=ROSADO, text_color=MAGENTA,
                  hover_color="#F0B4FB", font=ctk.CTkFont(size=24, weight="bold"),
                  corner_radius=30, width=300, height=70
                  ).grid(row=4, column=0, pady=(20, 10))
#funciones principales----------------------------------------------------------------------
#===========================================================================================
def crear_interfaz_principal():
    for widget in app.winfo_children():
        widget.destroy()

    #FONDO PRINCIPAL
    app.configure(fg_color=LILA)
    app.title("Menú Principal - Dr. Maggie")

    # --- CABECERA ---
    header_frame = ctk.CTkFrame(
        master=app,
        fg_color=BOTON_USUARIO,
        corner_radius=20,
        width=200,
        height=60
    )
    header_frame.place(x=40, y=40)

    header_label = ctk.CTkLabel(
        master=header_frame,
        text="Dr. Maggie",
        font=ctk.CTkFont(size=26, weight="bold"),
        text_color=MAGENTA
    )
    header_label.place(relx=0.5, rely=0.5, anchor="center")

    # --- MARCO PRINCIPAL ---fcf6fb
    menu_frame = ctk.CTkFrame(
        master=app,
        fg_color=MORADO_VIVO,
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

    botones = [
        ("Agregar paciente", 0, 0, crear_ventana_agregar_paciente),
        ("Crear ficha médica", 0, 1, buscar_paciente),
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
            button = ctk.CTkButton(master=menu_frame,text=text,command=command,width=BUTTON_WIDTH,height=BUTTON_HEIGHT,fg_color="white",
                text_color=MAGENTA,
                hover_color="white",
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
        sub,text="Cerrar ventana",command=sub.destroy,fg_color=MAGENTA,text_color="white",width=250,height=60,font=ctk.CTkFont(size=20, weight="bold"),
        corner_radius=15
    ).pack(pady=30)

#-----------------------------------------------------------------

def intentar_login():
    usuario = user_entry.get()
    contra= pass_entry.get()

    if usuario == "1" and contra== "1":
        crear_interfaz_principal()

    elif usuario!="1":
        messagebox.showerror("Error", "Usuario incorrecto.")
    elif contra!="1":
        messagebox.showerror("Error", "Contraseña incorrecta.")
    else:
        messagebox.showerror("Error", "Usuario o contraseña incorrectos.")

app.grid_columnconfigure(0, weight=1)
app.grid_columnconfigure(1, weight=1)
app.grid_rowconfigure(0, weight=1)

#IZQUIERDO (Formulario) ---
left_frame = ctk.CTkFrame(master=app, corner_radius=0, fg_color=LILA)
left_frame.grid(row=0, column=0, sticky="nswe", padx=40, pady=20)

try:
    imagen_fondo = Image.open("figura.png")
    ctk_image = ctk.CTkImage(light_image=imagen_fondo, dark_image=imagen_fondo, size=(800,800))
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
                          fg_color="white",border_width=0
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

login_button = ctk.CTkButton(master=left_frame, text="Iniciar Sesión",
                             command=intentar_login, width=450, height=60,
                             font=ctk.CTkFont(size=22),
                             fg_color=MAGENTA,hover_color=MORADO_CLARO,
                             corner_radius=100,
                             bg_color="white")
login_button.grid(row=6, column=1, sticky="ew", padx=20, pady=(40, 0))

#derecha IMAGEN LOGO

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

# --- INICIO DEL PROGRAMA ---
app.mainloop()