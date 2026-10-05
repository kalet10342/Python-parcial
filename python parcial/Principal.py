from inicio_sesion import Formulario_sesion
from registro_de_usuario import Formulario_registro

objSesion = Formulario_sesion()
auxVentana = objSesion.iniciar_ventana()
objRegistro = Formulario_registro(auxVentana)


objSesion.enlazar(objRegistro)
objRegistro.enlazar(objSesion)

objSesion.iniciar_preguntas()
objRegistro.iniciar_preguntas()

objSesion.mostrar()
auxVentana.mainloop()