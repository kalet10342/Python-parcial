import tkinter as Ventana


class Formulario:
    def __init__(self, ventana=None):
        self.colorRojo = "red"
        self.colorVerde = "green"
        self.colorAzul = "#1f4e79"
        self.ventana = ventana
        self.marco = None
        self.otroFormulario = None
        self.labelResultado = None
        self.listaEntry = []
        self.listaEstado = []

    # metodos abstractos: cada formulario hijo debe implementarlos
    def iniciar_preguntas(self):
        raise NotImplementedError("El formulario debe implementar iniciar_preguntas")

    def limpiar_campos(self):
        raise NotImplementedError("El formulario debe implementar limpiar_campos")

    def validar_campos(self):
        raise NotImplementedError("El formulario debe implementar validar_campos")

    def iniciar_ventana(self):
        if self.ventana is None:
            self.ventana = Ventana.Tk()
            self.ventana.title("Vitalia Gym")
            self.ventana.geometry("980x660")
            self.ventana.resizable(False, False)
        return self.ventana

    def enlazar(self, otroFormulario):
        self.otroFormulario = otroFormulario

    def ocultar(self):
        self.marco.pack_forget()

    def mostrar(self):
        self.otroFormulario.ocultar()
        self.limpiar_campos()
        self.marco.pack(fill="both", expand=True)

    def mostrar_resultado(self, texto, esError):
        if esError:
            self.labelResultado.configure(text=texto, fg=self.colorRojo)
        else:
            self.labelResultado.configure(text=texto, fg=self.colorVerde)


class Formulario_sesion(Formulario):
    def __init__(self, ventana=None):
        super().__init__(ventana)
        self.__recordado = ""
        self.varRecordar = None

    def iniciar_preguntas(self):
        self.marco = Ventana.Frame(self.ventana)

        centro = Ventana.Frame(self.marco)
        centro.place(relx=0.5, rely=0.5, anchor="center")

        labelTitulo = Ventana.Label(centro, text="Vitalia Gym")
        labelTitulo.configure(font=("Arial", 24, "bold"), fg=self.colorAzul)
        labelTitulo.pack(pady=10)

        grupo = Ventana.LabelFrame(centro, text="Acceso")
        grupo.pack(padx=10, pady=10)

        listaCampos = ["Usuario o correo", "Contraseña"]
        for i in range(len(listaCampos)):
            labelPregunta = Ventana.Label(grupo, text=listaCampos[i] + " *")
            labelPregunta.grid(row=i, column=0, sticky="w", padx=5, pady=5)

            entryCampo = Ventana.Entry(grupo, width=22)
            if i == 1:
                entryCampo.configure(show="*")
            entryCampo.grid(row=i, column=1, padx=5, pady=5)
            self.listaEntry.append(entryCampo)

            labelEstado = Ventana.Label(grupo, text="Sin revisar", fg="gray", width=12)
            labelEstado.grid(row=i, column=2, padx=5)
            self.listaEstado.append(labelEstado)

        self.varRecordar = Ventana.BooleanVar(value=False)
        checkRecordar = Ventana.Checkbutton(grupo, text="Recordar mi sesión", variable=self.varRecordar)
        checkRecordar.grid(row=2, column=1, sticky="w")

        self.labelResultado = Ventana.Label(centro, text="", wraplength=350)
        self.labelResultado.configure(font=("Arial", 10, "bold"))
        self.labelResultado.pack(pady=10)

        botonIngresar = Ventana.Button(centro, text="Ingresar", width=15, command=self.procesar_formulario)
        botonIngresar.configure(bg="#1f6f50", fg="white")
        botonIngresar.pack(pady=3)

        botonLimpiar = Ventana.Button(centro, text="Limpiar", width=15, command=self.limpiar_campos)
        botonLimpiar.pack(pady=3)

        labelPreguntaCuenta = Ventana.Label(centro, text="¿Aún no tienes cuenta?")
        labelPreguntaCuenta.pack(pady=(15, 3))

        botonRegistro = Ventana.Button(centro, text="Registrarme", width=15, command=self.ir_a_registro)
        botonRegistro.pack()

    def ir_a_registro(self):
        self.otroFormulario.mostrar()

    def limpiar_campos(self):
        for i in range(len(self.listaEntry)):
            self.listaEntry[i].delete(0, Ventana.END)
            self.listaEstado[i].configure(text="Sin revisar", fg="gray")
        self.varRecordar.set(False)
        self.labelResultado.configure(text="")
        if self.__recordado != "":
            self.listaEntry[0].insert(0, self.__recordado)
            self.varRecordar.set(True)

    def validar_campos(self):
        estaCompleto = True
        for i in range(len(self.listaEntry)):
            if self.listaEntry[i].get().strip() == "":
                self.listaEstado[i].configure(text="Vacio", fg=self.colorRojo)
                estaCompleto = False
            else:
                self.listaEstado[i].configure(text="Diligenciado", fg=self.colorVerde)
        return estaCompleto

    def tomar_datos(self):
        arreglo = []
        arreglo.append(self.listaEntry[0].get().strip())
        arreglo.append(self.listaEntry[1].get())
        return arreglo

    def imprimir_datos(self, cliente, estaCompleto):
        if not estaCompleto:
            texto = "Hay campos vacios."
            self.mostrar_resultado(texto, True)
        elif cliente is None:
            texto = "Usuario o contraseña incorrectos."
            self.mostrar_resultado(texto, True)
        else:
            if self.varRecordar.get():
                self.__recordado = cliente["usuario"]
            else:
                self.__recordado = ""
            self.listaEntry[1].delete(0, Ventana.END)
            texto = "Bienvenido " + cliente["nombre"]
            self.mostrar_resultado(texto, False)
        print(texto)

    def procesar_formulario(self):
        estaCompleto = self.validar_campos()
        aux_dato = self.tomar_datos()
        cliente = None
        if estaCompleto:
            cliente = self.otroFormulario.validar_acceso(aux_dato[0], aux_dato[1])
        self.imprimir_datos(cliente, estaCompleto)