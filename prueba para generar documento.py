from generar_documento import generar_documento_word

datos = {
    "fecha": "22/02/25",
    "unidad": "Nogales",
    "expediente": "CANNOG0042",
    "nombre": "Uriel Torres Sierras",
    "edad": "5 A",
    "fecha_nacimiento": "15/08/19",
    "diagnostico": "Trastorno del espectro autista",
    "area_intervencion": "Lenguaje",
    "periodo_intervencion": "Agosto 24 - Febrero 25",
    "terapias_recibidas": "21",
    "faltas": "3",
    "objetivos_iniciales": "Sílabas\nMandos\nPragmática del lenguaje\nIntraverbales\nFunciones\nPosesivos\nPreposiciones\nAcciones\nDescripciones\nCorrecta articulación de fonemas",
    "avance_objetivos": "Uriel se ha mostrado cada vez más cooperativo...",
    "nuevos_objetivos": "Atención\nMemoria\nFlexibilidad\nPlanificación\nFluidez verbal\nVerbos mentales",
    "observaciones": "A pesar de responder positivamente ante las actividades que se realizaron durante la intervención, son habilidades que se deben seguir trabajando en casa...",
    "tratamiento": "Se recomienda iniciar con terapia cognitiva, como también, seguir trabajando con los objetivos de la terapia de lenguaje...",
    "sugerencias_casa": "Se sugiere el uso de pictograma a la hora de trabajar con el alumno...",
    "elaborado_por": "Psic. Francisco Gabriel Pérez Carrizosa",
    "cedula": "13433362"
}

generar_documento_word(datos, 'IS_Uriel_Torres_0042_LIBERADO_Replica.docx')
