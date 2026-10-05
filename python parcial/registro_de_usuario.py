import tkinter as Ventana
from tkinter import ttk, messagebox

from inicio_sesion import Formulario


class Formulario_registro(Formulario):
    def __init__(self, ventana=None):
        super().__init__(ventana)
        self.listaCampos = ["Usuario", "Contraseña", "Confirmar contraseña", "Nombre completo",
                            "Número de documento", "Nacimiento (AAAA-MM-DD)", "Correo electrónico",
                            "Teléfono", "Dirección"]
        self.listaTipos = ["Cédula de ciudadanía", "Tarjeta de identidad", "Cédula de extranjería", "Pasaporte"]
        self.listaCiudades = ["Bogotá", "Medellín", "Cali", "Barranquilla", "Bucaramanga", "Cartagena"]
        self.listaGeneros = ["Femenino", "Masculino", "Otro"]
        self.listaServicios = ["Pesas", "Spinning", "Yoga", "Crossfit"]
        self.listaVarServicios = []
        self.listaFaltantes = []
        self.comboTipo = None
        self.varGenero = None
        self.listboxCiudad = None
        self.escala = None
        self.textObservaciones = None
        self.__clientes = []

    def iniciar_preguntas(self):
        self.marco = Ventana.Frame(self.ventana)
        self.marco.columnconfigure(0, weight=1)
        self.marco.columnconfigure(1, weight=1)

        labelTitulo = Ventana.Label(self.marco, text="Registro de clientes")
        labelTitulo.configure(font=("Arial", 18, "bold"), fg=self.colorAzul)
        labelTitulo.grid(row=0, column=0, columnspan=2, pady=(10, 0))

        labelNota = Ventana.Label(self.marco, text="Los campos con * son obligatorios")
        labelNota.grid(row=1, column=0, columnspan=2)

        izquierda = Ventana.Frame(self.marco)
        izquierda.grid(row=2, column=0, sticky="n", padx=10, pady=10)
        derecha = Ventana.Frame(self.marco)
        derecha.grid(row=2, column=1, sticky="n", padx=10, pady=10)

        # ---------- grupo 1: datos de acceso ----------
        grupoAcceso = Ventana.LabelFrame(izquierda, text="Datos de acceso")
        grupoAcceso.pack(fill="x", pady=(0, 10))
        self.crear_campos(grupoAcceso, self.listaCampos[0:3])

        # ---------- grupo 2: datos personales y contacto ----------
        grupoPersonal = Ventana.LabelFrame(izquierda, text="Datos personales y contacto")
        grupoPersonal.pack(fill="x")
        self.crear_campos(grupoPersonal, self.listaCampos[3:9])

        # ---------- grupo 3: preferencias ----------
        grupoPref = Ventana.LabelFrame(derecha, text="Preferencias")
        grupoPref.pack()

        # Combobox
        Ventana.Label(grupoPref, text="Tipo de documento *").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.comboTipo = ttk.Combobox(grupoPref, values=self.listaTipos, state="readonly", width=24)
        self.comboTipo.grid(row=0, column=1, sticky="w", padx=5)

        # Radiobutton
        Ventana.Label(grupoPref, text="Género *").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        filaGenero = Ventana.Frame(grupoPref)
        filaGenero.grid(row=1, column=1, sticky="w")
        self.varGenero = Ventana.StringVar(value="")
        for genero in self.listaGeneros:
            radio = Ventana.Radiobutton(filaGenero, text=genero, value=genero, variable=self.varGenero)
            radio.pack(side="left")

        # Listbox con Scrollbar
        Ventana.Label(grupoPref, text="Ciudad *").grid(row=2, column=0, sticky="nw", padx=5, pady=5)
        cajaCiudad = Ventana.Frame(grupoPref)
        cajaCiudad.grid(row=2, column=1, sticky="w", padx=5)
        barra = Ventana.Scrollbar(cajaCiudad)
        self.listboxCiudad = Ventana.Listbox(cajaCiudad, height=4, width=22, exportselection=False)
        self.listboxCiudad.configure(yscrollcommand=barra.set)
        barra.configure(command=self.listboxCiudad.yview)
        for ciudad in self.listaCiudades:
            self.listboxCiudad.insert(Ventana.END, ciudad)
        self.listboxCiudad.pack(side="left")
        barra.pack(side="left", fill="y")

        # Checkbutton (varios)
        Ventana.Label(grupoPref, text="Servicios de interés *").grid(row=3, column=0, sticky="nw", padx=5, pady=5)
        cajaServicios = Ventana.Frame(grupoPref)
        cajaServicios.grid(row=3, column=1, sticky="w", padx=5)
        for i in range(len(self.listaServicios)):
            variable = Ventana.BooleanVar(value=False)
            self.listaVarServicios.append(variable)
            check = Ventana.Checkbutton(cajaServicios, text=self.listaServicios[i], variable=variable)
            check.grid(row=i // 2, column=i % 2, sticky="w")

        # Scale
        Ventana.Label(grupoPref, text="Motivación (1-10)").grid(row=4, column=0, sticky="w", padx=5, pady=5)
        self.escala = Ventana.Scale(grupoPref, from_=1, to=10, orient="horizontal", length=170)
        self.escala.grid(row=4, column=1, sticky="w", padx=5)

        # Text
        Ventana.Label(grupoPref, text="Observaciones").grid(row=5, column=0, sticky="nw", padx=5, pady=5)
        self.textObservaciones = Ventana.Text(grupoPref, height=3, width=24)
        self.textObservaciones.grid(row=5, column=1, sticky="w", padx=5, pady=5)

        # ---------- resultado y botones ----------
        self.labelResultado = Ventana.Label(self.marco, text="", wraplength=700)
        self.labelResultado.configure(font=("Arial", 10, "bold"))
        self.labelResultado.grid(row=3, column=0, columnspan=2, pady=5)

        botones = Ventana.Frame(self.marco)
        botones.grid(row=4, column=0, columnspan=2, pady=5)
        botonRegistrar = Ventana.Button(botones, text="Registrar", width=15, command=self.procesar_formulario)
        botonRegistrar.configure(bg="#1f6f50", fg="white")
        botonRegistrar.grid(row=0, column=0, padx=4)
        botonLimpiar = Ventana.Button(botones, text="Limpiar", width=15, command=self.limpiar_campos)
        botonLimpiar.grid(row=0, column=1, padx=4)
        botonVolver = Ventana.Button(botones, text="Volver al login", width=15, command=self.volver_a_sesion)
        botonVolver.grid(row=0, column=2, padx=4)

    def crear_campos(self, grupo, nombres):
        for i in range(len(nombres)):
            texto = nombres[i]
            if texto != "Dirección":
                texto = texto + " *"
            labelPregunta = Ventana.Label(grupo, text=texto)
            labelPregunta.grid(row=i, column=0, sticky="w", padx=5, pady=3)

            entryCampo = Ventana.Entry(grupo, width=24)
            if "Contraseña" in texto:
                entryCampo.configure(show="*")
            entryCampo.grid(row=i, column=1, padx=5, pady=3)
            self.listaEntry.append(entryCampo)

            labelEstado = Ventana.Label(grupo, text="Sin revisar", fg="gray", width=12, anchor="w")
            labelEstado.grid(row=i, column=2, padx=5)
            self.listaEstado.append(labelEstado)

    def volver_a_sesion(self):
        self.otroFormulario.mostrar()

    def limpiar_campos(self):
        for i in range(len(self.listaEntry)):
            self.listaEntry[i].delete(0, Ventana.END)
            if i == 8:
                self.listaEstado[i].configure(text="Opcional", fg="gray")
            else:
                self.listaEstado[i].configure(text="Sin revisar", fg="gray")
        self.comboTipo.set("")
        self.varGenero.set("")
        self.listboxCiudad.selection_clear(0, Ventana.END)
        for variable in self.listaVarServicios:
            variable.set(False)
        self.escala.set(5)
        self.textObservaciones.delete("1.0", Ventana.END)
        self.labelResultado.configure(text="")

    def validar_campos(self):
        self.listaFaltantes = []
        for i in range(len(self.listaEntry)):
            vacio = self.listaEntry[i].get().strip() == ""
            if i == 8:
                if vacio:
                    self.listaEstado[i].configure(text="Opcional", fg="gray")
                else:
                    self.listaEstado[i].configure(text="Diligenciado", fg=self.colorVerde)
            elif vacio:
                self.listaEstado[i].configure(text="Vacio", fg=self.colorRojo)
                self.listaFaltantes.append(self.listaCampos[i])
            else:
                self.listaEstado[i].configure(text="Diligenciado", fg=self.colorVerde)

        if self.comboTipo.get() == "":
            self.listaFaltantes.append("Tipo de documento")
        if self.varGenero.get() == "":
            self.listaFaltantes.append("Género")
        if len(self.listboxCiudad.curselection()) == 0:
            self.listaFaltantes.append("Ciudad")
        if len(self.tomar_servicios()) == 0:
            self.listaFaltantes.append("Servicios de interés")
        return len(self.listaFaltantes) == 0

    def tomar_servicios(self):
        servicios = []
        for i in range(len(self.listaServicios)):
            if self.listaVarServicios[i].get():
                servicios.append(self.listaServicios[i])
        return servicios

    def tomar_datos(self):
        claves = ["usuario", "clave", "clave2", "nombre", "documento", "fecha", "correo", "telefono", "direccion"]
        datos = {}
        for i in range(len(claves)):
            valor = self.listaEntry[i].get()
            if i != 1 and i != 2:
                valor = valor.strip()
            datos[claves[i]] = valor
        datos["tipo_documento"] = self.comboTipo.get()
        datos["genero"] = self.varGenero.get()
        seleccion = self.listboxCiudad.curselection()
        if len(seleccion) > 0:
            datos["ciudad"] = self.listboxCiudad.get(seleccion[0])
        else:
            datos["ciudad"] = ""
        datos["servicios"] = self.tomar_servicios()
        datos["motivacion"] = self.escala.get()
        datos["observaciones"] = self.textObservaciones.get("1.0", "end-1c").strip()
        return datos

    def validar_reglas(self, d):
        if len(d["usuario"]) < 4:
            return "El usuario debe tener mínimo 4 caracteres."
        if self.existe_usuario(d["usuario"]):
            return "Ese usuario ya existe."
        if len(d["clave"]) < 6:
            return "La contraseña debe tener mínimo 6 caracteres."
        if d["clave"] != d["clave2"]:
            return "Las contraseñas no coinciden."
        if len(d["nombre"].split()) < 2:
            return "Escribe nombre y apellido."
        if not d["documento"].isdigit() or len(d["documento"]) < 6:
            return "El documento debe tener mínimo 6 números."
        partes = d["fecha"].split("-")
        if len(partes) != 3 or not (partes[0].isdigit() and partes[1].isdigit() and partes[2].isdigit()):
            return "La fecha debe tener el formato AAAA-MM-DD."
        anio = int(partes[0])
        mes = int(partes[1])
        dia = int(partes[2])
        if len(partes[0]) != 4 or mes < 1 or mes > 12 or dia < 1 or dia > 31:
            return "La fecha no es válida."
        if anio < 1900 or anio > 2026:
            return "El año de nacimiento debe estar entre 1900 y 2026."
        if "@" not in d["correo"] or "." not in d["correo"]:
            return "El correo no es válido."
        if not d["telefono"].isdigit() or len(d["telefono"]) < 7:
            return "El teléfono debe tener mínimo 7 números."
        return ""

    def existe_usuario(self, usuario):
        for cliente in self.__clientes:
            if cliente["usuario"].lower() == usuario.lower():
                return True
        return False

    def validar_acceso(self, acceso, clave):
        for cliente in self.__clientes:
            if acceso.lower() == cliente["usuario"].lower() or acceso.lower() == cliente["correo"].lower():
                if cliente["clave"] == clave:
                    return cliente
        return None

    def imprimir_datos(self, aux_dato, estaCompleto, mensaje):
        if not estaCompleto:
            texto = "Faltan por diligenciar: " + ", ".join(self.listaFaltantes)
            self.mostrar_resultado(texto, True)
        elif mensaje != "":
            texto = mensaje
            self.mostrar_resultado(texto, True)
        else:
            texto = "Cliente guardado: " + aux_dato["nombre"]
            texto = texto + "\nTotal de clientes: " + str(len(self.__clientes))
            self.mostrar_resultado(texto, False)
        print(texto)

    def procesar_formulario(self):
        estaCompleto = self.validar_campos()
        aux_dato = self.tomar_datos()
        mensaje = ""
        if estaCompleto:
            mensaje = self.validar_reglas(aux_dato)
        if estaCompleto and mensaje == "":
            aux_dato.pop("clave2")
            self.__clientes.append(aux_dato)
        self.imprimir_datos(aux_dato, estaCompleto, mensaje)
        if estaCompleto and mensaje == "":
            messagebox.showinfo("Registro exitoso", "Ya puedes iniciar sesión.")
            self.otroFormulario.mostrar()