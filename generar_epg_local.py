import xml.etree.ElementTree as ET
from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo
from xml.dom import minidom

# Zona horaria de Argentina
ARG_TZ = ZoneInfo("America/Argentina/Buenos_Aires")

# Programación base según el día
programas_lunes = [
    {"canal": "Sol", "inicio": "00:00", "fin": "06:00", "titulo": "Sin programación", "cat": "Otros"},
    {"canal": "Sol", "inicio": "06:00", "fin": "06:30", "titulo": "El club de la Sol", "cat": "Otros"},
    {"canal": "Sol", "inicio": "06:30", "fin": "08:30", "titulo": "La primera de Sol", "cat": "Otros"},
    {"canal": "Sol", "inicio": "08:30", "fin": "13:30", "titulo": "Malas constumbres", "cat": "Radio"},
    {"canal": "Sol", "inicio": "13:30", "fin": "14:30", "titulo": "La segunda de Sol", "cat": "Radio"},
    {"canal": "Sol", "inicio": "14:30", "fin": "17:00", "titulo": "Silencio que hay ruido", "cat": "Radio"},
    {"canal": "Sol", "inicio": "17:00", "fin": "18:00", "titulo": "Clave de Sol", "cat": "Radio"},
    {"canal": "Sol", "inicio": "18:00", "fin": "19:00", "titulo": "La tercera de Sol", "cat": "Radio"},
    {"canal": "Sol", "inicio": "19:00", "fin": "00:00", "titulo": "Programación de noche", "cat": "Radio"},

    {"canal": "PowerMax", "inicio": "00:00", "fin": "05:00", "titulo": "Sin programación", "cat": "Otros"},
    {"canal": "PowerMax", "inicio": "05:00", "fin": "07:00", "titulo": "Amanecer con JR", "cat": "Radio"},
    {"canal": "PowerMax", "inicio": "07:00", "fin": "09:30", "titulo": "El mundo y la región", "cat": "Radio"},
    {"canal": "PowerMax", "inicio": "09:30", "fin": "11:00", "titulo": "Página 104", "cat": "Radio"},
    {"canal": "PowerMax", "inicio": "11:00", "fin": "13:00", "titulo": "Asi son las mañanas", "cat": "Radio"},
    {"canal": "PowerMax", "inicio": "13:00", "fin": "14:00", "titulo": "Sin programación", "cat": "Otros"},
    {"canal": "PowerMax", "inicio": "14:00", "fin": "16:00", "titulo": "El show debe continuar", "cat": "Música"},
    {"canal": "PowerMax", "inicio": "16:00", "fin": "18:00", "titulo": "Radio City", "cat": "Radio"},
    {"canal": "PowerMax", "inicio": "18:00", "fin": "20:00", "titulo": "Todos para uno", "cat": "Radio"},
    {"canal": "PowerMax", "inicio": "20:00", "fin": "21:00", "titulo": "Frecuencia retro", "cat": "Radio"},
    {"canal": "PowerMax", "inicio": "21:00", "fin": "00:00", "titulo": "Sin programación", "cat": "Otros"},

    {"canal": "Next", "inicio": "00:00", "fin": "07:00", "titulo": "Programación de madrugada", "cat": "Otros"},
    {"canal": "Next", "inicio": "07:00", "fin": "10:00", "titulo": "Red Urbana", "cat": "Radio"},
    {"canal": "Next", "inicio": "10:00", "fin": "12:00", "titulo": "Diario Castellanos", "cat": "Radio"},
    {"canal": "Next", "inicio": "12:00", "fin": "14:00", "titulo": "Next Noticias", "cat": "Noticiero"},
    {"canal": "Next", "inicio": "14:00", "fin": "15:00", "titulo": "El Espectador Deportes", "cat": "Deportes"},
    {"canal": "Next", "inicio": "15:00", "fin": "19:00", "titulo": "Programación de tarde", "cat": "Otros"},
    {"canal": "Next", "inicio": "19:00", "fin": "20:00", "titulo": "Sin Rebajes", "cat": "Deportes"},
    {"canal": "Next", "inicio": "20:00", "fin": "22:00", "titulo": "+ Noticias", "cat": "Noticiero"},
    {"canal": "Next", "inicio": "22:00", "fin": "00:00", "titulo": "Programación de noche", "cat": "Otros"},

    {"canal": "Chacra", "inicio": "00:00", "fin": "06:00", "titulo": "La red del campo", "cat": "Agro"},
    {"canal": "Chacra", "inicio": "06:00", "fin": "07:00", "titulo": "Chacra Agro Continental", "cat": "Noticiero"},
    {"canal": "Chacra", "inicio": "07:00", "fin": "12:00", "titulo": "La red del campo", "cat": "Agro"},
    {"canal": "Chacra", "inicio": "12:00", "fin": "13:00", "titulo": "ChacraTV Noticias", "cat": "Noticiero"},
    {"canal": "Chacra", "inicio": "13:00", "fin": "18:00", "titulo": "La red del campo", "cat": "Agro"},
    {"canal": "Chacra", "inicio": "18:00", "fin": "00:00", "titulo": "La red del campo", "cat": "Agro"},

    {"canal": "Taste", "inicio": "00:00", "fin": "06:00", "titulo": "Comida y viajes", "cat": "Cocina"},
    {"canal": "Taste", "inicio": "06:00", "fin": "12:00", "titulo": "Comida y viajes", "cat": "Cocina"},
    {"canal": "Taste", "inicio": "12:00", "fin": "18:00", "titulo": "Comida y viajes", "cat": "Cocina"},
    {"canal": "Taste", "inicio": "18:00", "fin": "00:00", "titulo": "Comida y viajes", "cat": "Cocina"},

    {"canal": "F10", "inicio": "00:00", "fin": "07:00", "titulo": "Programación de madrugada", "cat": "Otros"},
    {"canal": "F10", "inicio": "07:00", "fin": "09:30", "titulo": "F10 Noticias - Primera edición", "cat": "Noticiero"},
    {"canal": "F10", "inicio": "09:30", "fin": "12:30", "titulo": "El show de las mañanas", "cat": "Entretenimiento"},
    {"canal": "F10", "inicio": "12:30", "fin": "13:20", "titulo": "Programación de tarde", "cat": "Otros"},
    {"canal": "F10", "inicio": "13:20", "fin": "15:00", "titulo": "F10 Noticias - Segunda edición", "cat": "Noticiero"},
    {"canal": "F10", "inicio": "15:00", "fin": "18:00", "titulo": "Así es aquí con la aplanadora", "cat": "Cultural"},
    {"canal": "F10", "inicio": "18:00", "fin": "20:00", "titulo": "Programación de tarde", "cat": "Otros"},
    {"canal": "F10", "inicio": "20:00", "fin": "22:00", "titulo": "F10 Noticias - Edición central", "cat": "Noticiero"},
    {"canal": "F10", "inicio": "22:00", "fin": "23:30", "titulo": "Titanes", "cat": "Entretenimiento"},
    {"canal": "F10", "inicio": "23:30", "fin": "00:00", "titulo": "Programación de noche", "cat": "Otros"},

    {"canal": "Litus", "inicio": "00:00", "fin": "05:00", "titulo": "Programación de madrugada", "cat": "Otros"},
    {"canal": "Litus", "inicio": "05:00", "fin": "06:00", "titulo": "Hora cinco", "cat": "Radio"},
    {"canal": "Litus", "inicio": "06:00", "fin": "09:00", "titulo": "Que quede claro", "cat": "Radio"},
    {"canal": "Litus", "inicio": "09:00", "fin": "13:00", "titulo": "Radiosapiens", "cat": "Radio"},
    {"canal": "Litus", "inicio": "13:00", "fin": "13:15", "titulo": "Panorama informativo", "cat": "Radio"},
    {"canal": "Litus", "inicio": "13:15", "fin": "14:00", "titulo": "10 en deportes", "cat": "Deportes"},
    {"canal": "Litus", "inicio": "14:00", "fin": "16:00", "titulo": "Ahí vamos", "cat": "Radio"},
    {"canal": "Litus", "inicio": "16:00", "fin": "18:00", "titulo": "Al derecho y al revés", "cat": "Radio"},
    {"canal": "Litus", "inicio": "18:00", "fin": "19:00", "titulo": "10 en deportes", "cat": "Deportes"},
    {"canal": "Litus", "inicio": "19:00", "fin": "20:00", "titulo": "Algo pasó", "cat": "Radio"},
    {"canal": "Litus", "inicio": "20:00", "fin": "20:15", "titulo": "Panorama informativo", "cat": "Radio"},
    {"canal": "Litus", "inicio": "20:15", "fin": "00:00", "titulo": "Programación de noche", "cat": "Radio"},

    {"canal": "Rafaela", "inicio": "00:00", "fin": "06:00", "titulo": "Sin programación", "cat": "Otros"},
    {"canal": "Rafaela", "inicio": "06:00", "fin": "08:00", "titulo": "Amanece la Región", "cat": "Radio"},
    {"canal": "Rafaela", "inicio": "08:00", "fin": "12:00", "titulo": "Arriba la Mañana", "cat": "Radio"},
    {"canal": "Rafaela", "inicio": "12:00", "fin": "16:00", "titulo": "Nada de Siesta", "cat": "Radio"},
    {"canal": "Rafaela", "inicio": "16:00", "fin": "18:00", "titulo": "Entre Mates", "cat": "Radio"},
    {"canal": "Rafaela", "inicio": "18:00", "fin": "20:00", "titulo": "Nunca es Tarde", "cat": "Radio"},
    {"canal": "Rafaela", "inicio": "20:00", "fin": "00:00", "titulo": "Música de Radio", "cat": "Música"},

    {"canal": "Aire", "inicio": "00:00", "fin": "05:00", "titulo": "Sin programación", "cat": "Otros"},
    {"canal": "Aire", "inicio": "05:00", "fin": "06:00", "titulo": "Anticipos", "cat": "Radio"},
    {"canal": "Aire", "inicio": "06:00", "fin": "08:00", "titulo": "CREO", "cat": "Radio"},
    {"canal": "Aire", "inicio": "08:00", "fin": "14:00", "titulo": "Ahora vengo", "cat": "Radio"},
    {"canal": "Aire", "inicio": "14:00", "fin": "14:30", "titulo": "Dale, dale deportivo", "cat": "Deportes"},
    {"canal": "Aire", "inicio": "14:30", "fin": "17:30", "titulo": "Santa siesta", "cat": "Radio"},
    {"canal": "Aire", "inicio": "17:30", "fin": "20:00", "titulo": "Una tarde a la vez", "cat": "Radio"},
    {"canal": "Aire", "inicio": "20:00", "fin": "21:00", "titulo": "Dale, dale deportivo", "cat": "Deportes"},
    {"canal": "Aire", "inicio": "21:00", "fin": "00:00", "titulo": "VIVO AIRE", "cat": "Radio"},

    {"canal": "22Web", "inicio": "00:00", "fin": "00:30", "titulo": "Algo que contar", "cat": "Periodístico"},
    {"canal": "22Web", "inicio": "00:30", "fin": "06:00", "titulo": "Repetición", "cat": "Otros"},
    {"canal": "22Web", "inicio": "06:00", "fin": "09:00", "titulo": "Repetición", "cat": "Otros"},
    {"canal": "22Web", "inicio": "09:00", "fin": "11:00", "titulo": "La mañana de Juan Domingo", "cat": "Periodístico"},
    {"canal": "22Web", "inicio": "11:00", "fin": "12:00", "titulo": "Infoshow", "cat": "Magazine"},
    {"canal": "22Web", "inicio": "12:00", "fin": "14:00", "titulo": "GreKo", "cat": "Periodístico"},
    {"canal": "22Web", "inicio": "14:00", "fin": "16:00", "titulo": "Uno más uno tres", "cat": "Periodístico"},
    {"canal": "22Web", "inicio": "16:00", "fin": "17:00", "titulo": "Intimamente", "cat": "Espectáculo"},
    {"canal": "22Web", "inicio": "17:00", "fin": "19:00", "titulo": "Estamos de vuelta", "cat": "Periodístico"},
    {"canal": "22Web", "inicio": "19:00", "fin": "20:00", "titulo": "22 Noticias", "cat": "Noticiero"},
    {"canal": "22Web", "inicio": "20:00", "fin": "22:00", "titulo": "La revancha del 1", "cat": "Periodístico"},
    {"canal": "22Web", "inicio": "22:00", "fin": "00:00", "titulo": "Moranza", "cat": "Periodístico"},

    {"canal": "Perfil", "inicio": "00:00", "fin": "08:00", "titulo": "Repetición", "cat": "Otros"},
    {"canal": "Perfil", "inicio": "08:00", "fin": "10:00", "titulo": "Longobardi", "cat": "Periodístico"},
    {"canal": "Perfil", "inicio": "10:00", "fin": "13:00", "titulo": "Modo Fontevecchia", "cat": "Periodístico"},
    {"canal": "Perfil", "inicio": "13:00", "fin": "14:30", "titulo": "Ronda de investigación", "cat": "Periodístico"},
    {"canal": "Perfil", "inicio": "14:30", "fin": "16:30", "titulo": "Ronda de corresponsales", "cat": "Periodístico"},
    {"canal": "Perfil", "inicio": "16:30", "fin": "18:00", "titulo": "Ronda de economistas", "cat": "Periodístico"},
    {"canal": "Perfil", "inicio": "18:00", "fin": "19:00", "titulo": "Ronda de escritores", "cat": "Periodístico"},
    {"canal": "Perfil", "inicio": "19:00", "fin": "21:00", "titulo": "Ronda de editores", "cat": "Periodístico"},
    {"canal": "Perfil", "inicio": "21:00", "fin": "23:00", "titulo": "QR!", "cat": "Periodístico"},
    {"canal": "Perfil", "inicio": "23:00", "fin": "00:00", "titulo": "Periodismo puro", "cat": "Entrevistas"},
]

programas_martes = [
    {"canal": "Sol", "inicio": "00:00", "fin": "06:00", "titulo": "Sin programación", "cat": "Otros"},
    {"canal": "Sol", "inicio": "06:00", "fin": "06:30", "titulo": "El club de la Sol", "cat": "Otros"},
    {"canal": "Sol", "inicio": "06:30", "fin": "08:30", "titulo": "La primera de Sol", "cat": "Otros"},
    {"canal": "Sol", "inicio": "08:30", "fin": "13:30", "titulo": "Malas constumbres", "cat": "Radio"},
    {"canal": "Sol", "inicio": "13:30", "fin": "14:30", "titulo": "La segunda de Sol", "cat": "Radio"},
    {"canal": "Sol", "inicio": "14:30", "fin": "17:00", "titulo": "Silencio que hay ruido", "cat": "Radio"},
    {"canal": "Sol", "inicio": "17:00", "fin": "18:00", "titulo": "Clave de Sol", "cat": "Radio"},
    {"canal": "Sol", "inicio": "18:00", "fin": "19:00", "titulo": "La tercera de Sol", "cat": "Radio"},
    {"canal": "Sol", "inicio": "19:00", "fin": "00:00", "titulo": "Programación de noche", "cat": "Radio"},

    {"canal": "PowerMax", "inicio": "00:00", "fin": "05:00", "titulo": "Sin programación", "cat": "Otros"},
    {"canal": "PowerMax", "inicio": "05:00", "fin": "07:00", "titulo": "Amanecer con JR", "cat": "Radio"},
    {"canal": "PowerMax", "inicio": "07:00", "fin": "09:30", "titulo": "El mundo y la región", "cat": "Radio"},
    {"canal": "PowerMax", "inicio": "09:30", "fin": "11:00", "titulo": "Página 104", "cat": "Radio"},
    {"canal": "PowerMax", "inicio": "11:00", "fin": "13:00", "titulo": "Asi son las mañanas", "cat": "Radio"},
    {"canal": "PowerMax", "inicio": "13:00", "fin": "14:00", "titulo": "Sin programación", "cat": "Otros"},
    {"canal": "PowerMax", "inicio": "14:00", "fin": "16:00", "titulo": "El show debe continuar", "cat": "Música"},
    {"canal": "PowerMax", "inicio": "16:00", "fin": "18:00", "titulo": "Radio City", "cat": "Radio"},
    {"canal": "PowerMax", "inicio": "18:00", "fin": "20:00", "titulo": "Todos para uno", "cat": "Radio"},
    {"canal": "PowerMax", "inicio": "20:00", "fin": "21:00", "titulo": "Frecuencia retro", "cat": "Radio"},
    {"canal": "PowerMax", "inicio": "21:00", "fin": "00:00", "titulo": "Sin programación", "cat": "Otros"},

    {"canal": "Next", "inicio": "00:00", "fin": "07:00", "titulo": "Programación de madrugada", "cat": "Otros"},
    {"canal": "Next", "inicio": "07:00", "fin": "10:00", "titulo": "Red Urbana", "cat": "Radio"},
    {"canal": "Next", "inicio": "10:00", "fin": "12:00", "titulo": "Diario Castellanos", "cat": "Radio"},
    {"canal": "Next", "inicio": "12:00", "fin": "14:00", "titulo": "Next Noticias", "cat": "Noticiero"},
    {"canal": "Next", "inicio": "14:00", "fin": "15:00", "titulo": "El Espectador Deportes", "cat": "Deportes"},
    {"canal": "Next", "inicio": "15:00", "fin": "19:00", "titulo": "Programación de tarde", "cat": "Otros"},
    {"canal": "Next", "inicio": "19:00", "fin": "20:00", "titulo": "Sin Rebajes", "cat": "Deportes"},
    {"canal": "Next", "inicio": "20:00", "fin": "22:00", "titulo": "+ Noticias", "cat": "Noticiero"},
    {"canal": "Next", "inicio": "22:00", "fin": "00:00", "titulo": "Programación de noche", "cat": "Otros"},

    {"canal": "Chacra", "inicio": "00:00", "fin": "06:00", "titulo": "La red del campo", "cat": "Agro"},
    {"canal": "Chacra", "inicio": "06:00", "fin": "07:00", "titulo": "Chacra Agro Continental", "cat": "Noticiero"},
    {"canal": "Chacra", "inicio": "07:00", "fin": "12:00", "titulo": "La red del campo", "cat": "Agro"},
    {"canal": "Chacra", "inicio": "12:00", "fin": "13:00", "titulo": "ChacraTV Noticias", "cat": "Noticiero"},
    {"canal": "Chacra", "inicio": "13:00", "fin": "18:00", "titulo": "La red del campo", "cat": "Agro"},
    {"canal": "Chacra", "inicio": "18:00", "fin": "00:00", "titulo": "La red del campo", "cat": "Agro"},

    {"canal": "Taste", "inicio": "00:00", "fin": "06:00", "titulo": "Comida y viajes", "cat": "Cocina"},
    {"canal": "Taste", "inicio": "06:00", "fin": "12:00", "titulo": "Comida y viajes", "cat": "Cocina"},
    {"canal": "Taste", "inicio": "12:00", "fin": "18:00", "titulo": "Comida y viajes", "cat": "Cocina"},
    {"canal": "Taste", "inicio": "18:00", "fin": "00:00", "titulo": "Comida y viajes", "cat": "Cocina"},

    {"canal": "F10", "inicio": "00:00", "fin": "07:00", "titulo": "Programación de madrugada", "cat": "Otros"},
    {"canal": "F10", "inicio": "07:00", "fin": "09:30", "titulo": "F10 Noticias - Primera edición", "cat": "Noticiero"},
    {"canal": "F10", "inicio": "09:30", "fin": "12:30", "titulo": "El show de las mañanas", "cat": "Entretenimiento"},
    {"canal": "F10", "inicio": "12:30", "fin": "13:20", "titulo": "Programación de tarde", "cat": "Otros"},
    {"canal": "F10", "inicio": "13:20", "fin": "15:00", "titulo": "F10 Noticias - Segunda edición", "cat": "Noticiero"},
    {"canal": "F10", "inicio": "15:00", "fin": "18:00", "titulo": "Así es aquí con la aplanadora", "cat": "Cultural"},
    {"canal": "F10", "inicio": "18:00", "fin": "20:00", "titulo": "Programación de tarde", "cat": "Otros"},
    {"canal": "F10", "inicio": "20:00", "fin": "22:00", "titulo": "F10 Noticias - Edición central", "cat": "Noticiero"},
    {"canal": "F10", "inicio": "22:00", "fin": "23:30", "titulo": "Titanes", "cat": "Entretenimiento"},
    {"canal": "F10", "inicio": "23:30", "fin": "00:00", "titulo": "Programación de noche", "cat": "Otros"},

    {"canal": "Litus", "inicio": "00:00", "fin": "05:00", "titulo": "Programación de madrugada", "cat": "Otros"},
    {"canal": "Litus", "inicio": "05:00", "fin": "06:00", "titulo": "Hora cinco", "cat": "Radio"},
    {"canal": "Litus", "inicio": "06:00", "fin": "09:00", "titulo": "Que quede claro", "cat": "Radio"},
    {"canal": "Litus", "inicio": "09:00", "fin": "13:00", "titulo": "Radiosapiens", "cat": "Radio"},
    {"canal": "Litus", "inicio": "13:00", "fin": "13:15", "titulo": "Panorama informativo", "cat": "Radio"},
    {"canal": "Litus", "inicio": "13:15", "fin": "14:00", "titulo": "10 en deportes", "cat": "Deportes"},
    {"canal": "Litus", "inicio": "14:00", "fin": "16:00", "titulo": "Ahí vamos", "cat": "Radio"},
    {"canal": "Litus", "inicio": "16:00", "fin": "18:00", "titulo": "Al derecho y al revés", "cat": "Radio"},
    {"canal": "Litus", "inicio": "18:00", "fin": "19:00", "titulo": "10 en deportes", "cat": "Deportes"},
    {"canal": "Litus", "inicio": "19:00", "fin": "20:00", "titulo": "Algo pasó", "cat": "Radio"},
    {"canal": "Litus", "inicio": "20:00", "fin": "20:15", "titulo": "Panorama informativo", "cat": "Radio"},
    {"canal": "Litus", "inicio": "20:15", "fin": "00:00", "titulo": "Programación de noche", "cat": "Radio"},

    {"canal": "Rafaela", "inicio": "00:00", "fin": "06:00", "titulo": "Sin programación", "cat": "Otros"},
    {"canal": "Rafaela", "inicio": "06:00", "fin": "08:00", "titulo": "Amanece la Región", "cat": "Radio"},
    {"canal": "Rafaela", "inicio": "08:00", "fin": "12:00", "titulo": "Arriba la Mañana", "cat": "Radio"},
    {"canal": "Rafaela", "inicio": "12:00", "fin": "16:00", "titulo": "Nada de Siesta", "cat": "Radio"},
    {"canal": "Rafaela", "inicio": "16:00", "fin": "18:00", "titulo": "Entre Mates", "cat": "Radio"},
    {"canal": "Rafaela", "inicio": "18:00", "fin": "20:00", "titulo": "Nunca es Tarde", "cat": "Radio"},
    {"canal": "Rafaela", "inicio": "20:00", "fin": "00:00", "titulo": "Música de Radio", "cat": "Música"},

    {"canal": "Aire", "inicio": "00:00", "fin": "05:00", "titulo": "La noche al Aire", "cat": "Radio"},
    {"canal": "Aire", "inicio": "05:00", "fin": "06:00", "titulo": "Anticipos", "cat": "Radio"},
    {"canal": "Aire", "inicio": "06:00", "fin": "08:00", "titulo": "CREO", "cat": "Radio"},
    {"canal": "Aire", "inicio": "08:00", "fin": "14:00", "titulo": "Ahora vengo", "cat": "Radio"},
    {"canal": "Aire", "inicio": "14:00", "fin": "14:30", "titulo": "Dale, dale deportivo", "cat": "Deportes"},
    {"canal": "Aire", "inicio": "14:30", "fin": "17:30", "titulo": "Santa siesta", "cat": "Radio"},
    {"canal": "Aire", "inicio": "17:30", "fin": "20:00", "titulo": "Una tarde a la vez", "cat": "Radio"},
    {"canal": "Aire", "inicio": "20:00", "fin": "21:00", "titulo": "Dale, dale deportivo", "cat": "Deportes"},
    {"canal": "Aire", "inicio": "21:00", "fin": "00:00", "titulo": "VIVO AIRE", "cat": "Radio"},

    {"canal": "22Web", "inicio": "00:00", "fin": "00:30", "titulo": "Algo que contar", "cat": "Periodístico"},
    {"canal": "22Web", "inicio": "00:30", "fin": "06:00", "titulo": "Repetición", "cat": "Otros"},
    {"canal": "22Web", "inicio": "06:00", "fin": "11:00", "titulo": "Repetición", "cat": "Otros"},
    {"canal": "22Web", "inicio": "11:00", "fin": "12:00", "titulo": "Infoshow", "cat": "Magazine"},
    {"canal": "22Web", "inicio": "12:00", "fin": "14:00", "titulo": "GreKo", "cat": "Periodístico"},
    {"canal": "22Web", "inicio": "14:00", "fin": "16:00", "titulo": "Uno más uno tres", "cat": "Periodístico"},
    {"canal": "22Web", "inicio": "16:00", "fin": "17:00", "titulo": "Intimamente", "cat": "Espectáculo"},
    {"canal": "22Web", "inicio": "17:00", "fin": "19:00", "titulo": "Estamos de vuelta", "cat": "Periodístico"},
    {"canal": "22Web", "inicio": "19:00", "fin": "20:00", "titulo": "22 Noticias", "cat": "Noticiero"},
    {"canal": "22Web", "inicio": "20:00", "fin": "22:00", "titulo": "La revancha del 1", "cat": "Periodístico"},
    {"canal": "22Web", "inicio": "22:00", "fin": "00:00", "titulo": "Moranza", "cat": "Periodístico"},

    {"canal": "Perfil", "inicio": "00:00", "fin": "08:00", "titulo": "Repetición", "cat": "Otros"},
    {"canal": "Perfil", "inicio": "08:00", "fin": "10:00", "titulo": "Longobardi", "cat": "Periodístico"},
    {"canal": "Perfil", "inicio": "10:00", "fin": "13:00", "titulo": "Modo Fontevecchia", "cat": "Periodístico"},
    {"canal": "Perfil", "inicio": "13:00", "fin": "14:30", "titulo": "Ronda de investigación", "cat": "Periodístico"},
    {"canal": "Perfil", "inicio": "14:30", "fin": "16:30", "titulo": "Ronda de corresponsales", "cat": "Periodístico"},
    {"canal": "Perfil", "inicio": "16:30", "fin": "18:00", "titulo": "Ronda de economistas", "cat": "Periodístico"},
    {"canal": "Perfil", "inicio": "18:00", "fin": "19:00", "titulo": "Ronda de escritores", "cat": "Periodístico"},
    {"canal": "Perfil", "inicio": "19:00", "fin": "21:00", "titulo": "Ronda de editores", "cat": "Periodístico"},
    {"canal": "Perfil", "inicio": "21:00", "fin": "23:00", "titulo": "QR!", "cat": "Periodístico"},
    {"canal": "Perfil", "inicio": "23:00", "fin": "00:00", "titulo": "Periodismo puro", "cat": "Entrevistas"},
]

programas_miercoles = [
    {"canal": "Sol", "inicio": "00:00", "fin": "06:00", "titulo": "Sin programación", "cat": "Otros"},
    {"canal": "Sol", "inicio": "06:00", "fin": "06:30", "titulo": "El club de la Sol", "cat": "Otros"},
    {"canal": "Sol", "inicio": "06:30", "fin": "08:30", "titulo": "La primera de Sol", "cat": "Otros"},
    {"canal": "Sol", "inicio": "08:30", "fin": "13:30", "titulo": "Malas constumbres", "cat": "Radio"},
    {"canal": "Sol", "inicio": "13:30", "fin": "14:30", "titulo": "La segunda de Sol", "cat": "Radio"},
    {"canal": "Sol", "inicio": "14:30", "fin": "17:00", "titulo": "Silencio que hay ruido", "cat": "Radio"},
    {"canal": "Sol", "inicio": "17:00", "fin": "18:00", "titulo": "Clave de Sol", "cat": "Radio"},
    {"canal": "Sol", "inicio": "18:00", "fin": "19:00", "titulo": "La tercera de Sol", "cat": "Radio"},
    {"canal": "Sol", "inicio": "19:00", "fin": "00:00", "titulo": "Programación de noche", "cat": "Radio"},

    {"canal": "PowerMax", "inicio": "00:00", "fin": "05:00", "titulo": "Sin programación", "cat": "Otros"},
    {"canal": "PowerMax", "inicio": "05:00", "fin": "07:00", "titulo": "Amanecer con JR", "cat": "Radio"},
    {"canal": "PowerMax", "inicio": "07:00", "fin": "09:30", "titulo": "El mundo y la región", "cat": "Radio"},
    {"canal": "PowerMax", "inicio": "09:30", "fin": "11:00", "titulo": "Página 104", "cat": "Radio"},
    {"canal": "PowerMax", "inicio": "11:00", "fin": "13:00", "titulo": "Asi son las mañanas", "cat": "Radio"},
    {"canal": "PowerMax", "inicio": "13:00", "fin": "14:00", "titulo": "Sin programación", "cat": "Otros"},
    {"canal": "PowerMax", "inicio": "14:00", "fin": "16:00", "titulo": "El show debe continuar", "cat": "Música"},
    {"canal": "PowerMax", "inicio": "16:00", "fin": "18:00", "titulo": "Radio City", "cat": "Radio"},
    {"canal": "PowerMax", "inicio": "18:00", "fin": "20:00", "titulo": "Todos para uno", "cat": "Radio"},
    {"canal": "PowerMax", "inicio": "20:00", "fin": "21:00", "titulo": "Frecuencia retro", "cat": "Radio"},
    {"canal": "PowerMax", "inicio": "21:00", "fin": "00:00", "titulo": "Sin programación", "cat": "Otros"},

    {"canal": "Next", "inicio": "00:00", "fin": "07:00", "titulo": "Programación de madrugada", "cat": "Otros"},
    {"canal": "Next", "inicio": "07:00", "fin": "10:00", "titulo": "Red Urbana", "cat": "Radio"},
    {"canal": "Next", "inicio": "10:00", "fin": "12:00", "titulo": "Diario Castellanos", "cat": "Radio"},
    {"canal": "Next", "inicio": "12:00", "fin": "14:00", "titulo": "Next Noticias", "cat": "Noticiero"},
    {"canal": "Next", "inicio": "14:00", "fin": "15:00", "titulo": "El Espectador Deportes", "cat": "Deportes"},
    {"canal": "Next", "inicio": "15:00", "fin": "19:00", "titulo": "Programación de tarde", "cat": "Otros"},
    {"canal": "Next", "inicio": "19:00", "fin": "20:00", "titulo": "Sin Rebajes", "cat": "Deportes"},
    {"canal": "Next", "inicio": "20:00", "fin": "22:00", "titulo": "+ Noticias", "cat": "Noticiero"},
    {"canal": "Next", "inicio": "22:00", "fin": "00:00", "titulo": "Programación de noche", "cat": "Otros"},

    {"canal": "Chacra", "inicio": "00:00", "fin": "06:00", "titulo": "La red del campo", "cat": "Agro"},
    {"canal": "Chacra", "inicio": "06:00", "fin": "07:00", "titulo": "Chacra Agro Continental", "cat": "Noticiero"},
    {"canal": "Chacra", "inicio": "07:00", "fin": "12:00", "titulo": "La red del campo", "cat": "Agro"},
    {"canal": "Chacra", "inicio": "12:00", "fin": "13:00", "titulo": "ChacraTV Noticias", "cat": "Noticiero"},
    {"canal": "Chacra", "inicio": "13:00", "fin": "18:00", "titulo": "La red del campo", "cat": "Agro"},
    {"canal": "Chacra", "inicio": "18:00", "fin": "00:00", "titulo": "La red del campo", "cat": "Agro"},

    {"canal": "Taste", "inicio": "00:00", "fin": "06:00", "titulo": "Comida y viajes", "cat": "Cocina"},
    {"canal": "Taste", "inicio": "06:00", "fin": "12:00", "titulo": "Comida y viajes", "cat": "Cocina"},
    {"canal": "Taste", "inicio": "12:00", "fin": "18:00", "titulo": "Comida y viajes", "cat": "Cocina"},
    {"canal": "Taste", "inicio": "18:00", "fin": "00:00", "titulo": "Comida y viajes", "cat": "Cocina"},

    {"canal": "F10", "inicio": "00:00", "fin": "07:00", "titulo": "Programación de madrugada", "cat": "Otros"},
    {"canal": "F10", "inicio": "07:00", "fin": "09:30", "titulo": "F10 Noticias - Primera edición", "cat": "Noticiero"},
    {"canal": "F10", "inicio": "09:30", "fin": "12:30", "titulo": "El show de las mañanas", "cat": "Entretenimiento"},
    {"canal": "F10", "inicio": "12:30", "fin": "13:20", "titulo": "Programación de tarde", "cat": "Otros"},
    {"canal": "F10", "inicio": "13:20", "fin": "15:00", "titulo": "F10 Noticias - Segunda edición", "cat": "Noticiero"},
    {"canal": "F10", "inicio": "15:00", "fin": "18:00", "titulo": "Así es aquí con la aplanadora", "cat": "Cultural"},
    {"canal": "F10", "inicio": "18:00", "fin": "20:00", "titulo": "Programación de tarde", "cat": "Otros"},
    {"canal": "F10", "inicio": "20:00", "fin": "22:00", "titulo": "F10 Noticias - Edición central", "cat": "Noticiero"},
    {"canal": "F10", "inicio": "22:00", "fin": "23:30", "titulo": "Titanes", "cat": "Entretenimiento"},
    {"canal": "F10", "inicio": "23:30", "fin": "00:00", "titulo": "Programación de noche", "cat": "Otros"},

    {"canal": "Litus", "inicio": "00:00", "fin": "05:00", "titulo": "Programación de madrugada", "cat": "Otros"},
    {"canal": "Litus", "inicio": "05:00", "fin": "06:00", "titulo": "Hora cinco", "cat": "Radio"},
    {"canal": "Litus", "inicio": "06:00", "fin": "09:00", "titulo": "Que quede claro", "cat": "Radio"},
    {"canal": "Litus", "inicio": "09:00", "fin": "13:00", "titulo": "Radiosapiens", "cat": "Radio"},
    {"canal": "Litus", "inicio": "13:00", "fin": "13:15", "titulo": "Panorama informativo", "cat": "Radio"},
    {"canal": "Litus", "inicio": "13:15", "fin": "14:00", "titulo": "10 en deportes", "cat": "Deportes"},
    {"canal": "Litus", "inicio": "14:00", "fin": "16:00", "titulo": "Ahí vamos", "cat": "Radio"},
    {"canal": "Litus", "inicio": "16:00", "fin": "18:00", "titulo": "Al derecho y al revés", "cat": "Radio"},
    {"canal": "Litus", "inicio": "18:00", "fin": "19:00", "titulo": "10 en deportes", "cat": "Deportes"},
    {"canal": "Litus", "inicio": "19:00", "fin": "20:00", "titulo": "Algo pasó", "cat": "Radio"},
    {"canal": "Litus", "inicio": "20:00", "fin": "20:15", "titulo": "Panorama informativo", "cat": "Radio"},
    {"canal": "Litus", "inicio": "20:15", "fin": "00:00", "titulo": "Programación de noche", "cat": "Radio"},

    {"canal": "Rafaela", "inicio": "00:00", "fin": "06:00", "titulo": "Sin programación", "cat": "Otros"},
    {"canal": "Rafaela", "inicio": "06:00", "fin": "08:00", "titulo": "Amanece la Región", "cat": "Radio"},
    {"canal": "Rafaela", "inicio": "08:00", "fin": "12:00", "titulo": "Arriba la Mañana", "cat": "Radio"},
    {"canal": "Rafaela", "inicio": "12:00", "fin": "16:00", "titulo": "Nada de Siesta", "cat": "Radio"},
    {"canal": "Rafaela", "inicio": "16:00", "fin": "18:00", "titulo": "Entre Mates", "cat": "Radio"},
    {"canal": "Rafaela", "inicio": "18:00", "fin": "20:00", "titulo": "Nunca es Tarde", "cat": "Radio"},
    {"canal": "Rafaela", "inicio": "20:00", "fin": "00:00", "titulo": "Música de Radio", "cat": "Música"},

    {"canal": "Aire", "inicio": "00:00", "fin": "05:00", "titulo": "La noche al Aire", "cat": "Radio"},
    {"canal": "Aire", "inicio": "05:00", "fin": "06:00", "titulo": "Anticipos", "cat": "Radio"},
    {"canal": "Aire", "inicio": "06:00", "fin": "08:00", "titulo": "CREO", "cat": "Radio"},
    {"canal": "Aire", "inicio": "08:00", "fin": "14:00", "titulo": "Ahora vengo", "cat": "Radio"},
    {"canal": "Aire", "inicio": "14:00", "fin": "14:30", "titulo": "Dale, dale deportivo", "cat": "Deportes"},
    {"canal": "Aire", "inicio": "14:30", "fin": "17:30", "titulo": "Santa siesta", "cat": "Radio"},
    {"canal": "Aire", "inicio": "17:30", "fin": "20:00", "titulo": "Una tarde a la vez", "cat": "Radio"},
    {"canal": "Aire", "inicio": "20:00", "fin": "21:00", "titulo": "Dale, dale deportivo", "cat": "Deportes"},
    {"canal": "Aire", "inicio": "21:00", "fin": "00:00", "titulo": "VIVO AIRE", "cat": "Radio"},

    {"canal": "22Web", "inicio": "00:00", "fin": "00:30", "titulo": "Algo que contar", "cat": "Periodístico"},
    {"canal": "22Web", "inicio": "00:30", "fin": "06:00", "titulo": "Repetición", "cat": "Otros"},
    {"canal": "22Web", "inicio": "06:00", "fin": "09:00", "titulo": "Repetición", "cat": "Otros"},
    {"canal": "22Web", "inicio": "09:00", "fin": "11:00", "titulo": "La mañana de Juan Domingo", "cat": "Periodístico"},
    {"canal": "22Web", "inicio": "11:00", "fin": "12:00", "titulo": "Infoshow", "cat": "Magazine"},
    {"canal": "22Web", "inicio": "12:00", "fin": "14:00", "titulo": "GreKo", "cat": "Periodístico"},
    {"canal": "22Web", "inicio": "14:00", "fin": "16:00", "titulo": "Uno más uno tres", "cat": "Periodístico"},
    {"canal": "22Web", "inicio": "16:00", "fin": "17:00", "titulo": "Intimamente", "cat": "Espectáculo"},
    {"canal": "22Web", "inicio": "17:00", "fin": "19:00", "titulo": "Estamos de vuelta", "cat": "Periodístico"},
    {"canal": "22Web", "inicio": "19:00", "fin": "20:00", "titulo": "22 Noticias", "cat": "Noticiero"},
    {"canal": "22Web", "inicio": "20:00", "fin": "22:00", "titulo": "La revancha del 1", "cat": "Periodístico"},
    {"canal": "22Web", "inicio": "22:00", "fin": "00:00", "titulo": "Moranza", "cat": "Periodístico"},

    {"canal": "Perfil", "inicio": "00:00", "fin": "08:00", "titulo": "Repetición", "cat": "Otros"},
    {"canal": "Perfil", "inicio": "08:00", "fin": "10:00", "titulo": "Longobardi", "cat": "Periodístico"},
    {"canal": "Perfil", "inicio": "10:00", "fin": "13:00", "titulo": "Modo Fontevecchia", "cat": "Periodístico"},
    {"canal": "Perfil", "inicio": "13:00", "fin": "14:30", "titulo": "Ronda de investigación", "cat": "Periodístico"},
    {"canal": "Perfil", "inicio": "14:30", "fin": "16:30", "titulo": "Ronda de corresponsales", "cat": "Periodístico"},
    {"canal": "Perfil", "inicio": "16:30", "fin": "18:00", "titulo": "Ronda de economistas", "cat": "Periodístico"},
    {"canal": "Perfil", "inicio": "18:00", "fin": "19:00", "titulo": "Ronda de escritores", "cat": "Periodístico"},
    {"canal": "Perfil", "inicio": "19:00", "fin": "21:00", "titulo": "Ronda de editores", "cat": "Periodístico"},
    {"canal": "Perfil", "inicio": "21:00", "fin": "23:00", "titulo": "QR!", "cat": "Periodístico"},
    {"canal": "Perfil", "inicio": "23:00", "fin": "00:00", "titulo": "Periodismo puro", "cat": "Entrevistas"},
]

programas_jueves = [
    {"canal": "Sol", "inicio": "00:00", "fin": "06:00", "titulo": "Sin programación", "cat": "Otros"},
    {"canal": "Sol", "inicio": "06:00", "fin": "06:30", "titulo": "El club de la Sol", "cat": "Otros"},
    {"canal": "Sol", "inicio": "06:30", "fin": "08:30", "titulo": "La primera de Sol", "cat": "Otros"},
    {"canal": "Sol", "inicio": "08:30", "fin": "13:30", "titulo": "Malas constumbres", "cat": "Radio"},
    {"canal": "Sol", "inicio": "13:30", "fin": "14:30", "titulo": "La segunda de Sol", "cat": "Radio"},
    {"canal": "Sol", "inicio": "14:30", "fin": "17:00", "titulo": "Silencio que hay ruido", "cat": "Radio"},
    {"canal": "Sol", "inicio": "17:00", "fin": "18:00", "titulo": "Clave de Sol", "cat": "Radio"},
    {"canal": "Sol", "inicio": "18:00", "fin": "19:00", "titulo": "La tercera de Sol", "cat": "Radio"},
    {"canal": "Sol", "inicio": "19:00", "fin": "00:00", "titulo": "Programación de noche", "cat": "Radio"},

    {"canal": "PowerMax", "inicio": "00:00", "fin": "05:00", "titulo": "Sin programación", "cat": "Otros"},
    {"canal": "PowerMax", "inicio": "05:00", "fin": "07:00", "titulo": "Amanecer con JR", "cat": "Radio"},
    {"canal": "PowerMax", "inicio": "07:00", "fin": "09:30", "titulo": "El mundo y la región", "cat": "Radio"},
    {"canal": "PowerMax", "inicio": "09:30", "fin": "11:00", "titulo": "Página 104", "cat": "Radio"},
    {"canal": "PowerMax", "inicio": "11:00", "fin": "13:00", "titulo": "Asi son las mañanas", "cat": "Radio"},
    {"canal": "PowerMax", "inicio": "13:00", "fin": "14:00", "titulo": "Sin programación", "cat": "Otros"},
    {"canal": "PowerMax", "inicio": "14:00", "fin": "16:00", "titulo": "El show debe continuar", "cat": "Música"},
    {"canal": "PowerMax", "inicio": "16:00", "fin": "18:00", "titulo": "Radio City", "cat": "Radio"},
    {"canal": "PowerMax", "inicio": "18:00", "fin": "20:00", "titulo": "Todos para uno", "cat": "Radio"},
    {"canal": "PowerMax", "inicio": "20:00", "fin": "21:00", "titulo": "Frecuencia retro", "cat": "Radio"},
    {"canal": "PowerMax", "inicio": "21:00", "fin": "00:00", "titulo": "Sin programación", "cat": "Otros"},

    {"canal": "Next", "inicio": "00:00", "fin": "07:00", "titulo": "Programación de madrugada", "cat": "Otros"},
    {"canal": "Next", "inicio": "07:00", "fin": "10:00", "titulo": "Red Urbana", "cat": "Radio"},
    {"canal": "Next", "inicio": "10:00", "fin": "12:00", "titulo": "Diario Castellanos", "cat": "Radio"},
    {"canal": "Next", "inicio": "12:00", "fin": "14:00", "titulo": "Next Noticias", "cat": "Noticiero"},
    {"canal": "Next", "inicio": "14:00", "fin": "15:00", "titulo": "El Espectador Deportes", "cat": "Deportes"},
    {"canal": "Next", "inicio": "15:00", "fin": "19:00", "titulo": "Programación de tarde", "cat": "Otros"},
    {"canal": "Next", "inicio": "19:00", "fin": "20:00", "titulo": "Sin Rebajes", "cat": "Deportes"},
    {"canal": "Next", "inicio": "20:00", "fin": "22:00", "titulo": "+ Noticias", "cat": "Noticiero"},
    {"canal": "Next", "inicio": "22:00", "fin": "00:00", "titulo": "Programación de noche", "cat": "Otros"},

    {"canal": "Chacra", "inicio": "00:00", "fin": "06:00", "titulo": "La red del campo", "cat": "Agro"},
    {"canal": "Chacra", "inicio": "06:00", "fin": "07:00", "titulo": "Chacra Agro Continental", "cat": "Noticiero"},
    {"canal": "Chacra", "inicio": "07:00", "fin": "12:00", "titulo": "La red del campo", "cat": "Agro"},
    {"canal": "Chacra", "inicio": "12:00", "fin": "13:00", "titulo": "ChacraTV Noticias", "cat": "Noticiero"},
    {"canal": "Chacra", "inicio": "13:00", "fin": "18:00", "titulo": "La red del campo", "cat": "Agro"},
    {"canal": "Chacra", "inicio": "18:00", "fin": "00:00", "titulo": "La red del campo", "cat": "Agro"},

    {"canal": "Taste", "inicio": "00:00", "fin": "06:00", "titulo": "Comida y viajes", "cat": "Cocina"},
    {"canal": "Taste", "inicio": "06:00", "fin": "12:00", "titulo": "Comida y viajes", "cat": "Cocina"},
    {"canal": "Taste", "inicio": "12:00", "fin": "18:00", "titulo": "Comida y viajes", "cat": "Cocina"},
    {"canal": "Taste", "inicio": "18:00", "fin": "00:00", "titulo": "Comida y viajes", "cat": "Cocina"},

    {"canal": "F10", "inicio": "00:00", "fin": "07:00", "titulo": "Programación de madrugada", "cat": "Otros"},
    {"canal": "F10", "inicio": "07:00", "fin": "09:30", "titulo": "F10 Noticias - Primera edición", "cat": "Noticiero"},
    {"canal": "F10", "inicio": "09:30", "fin": "12:30", "titulo": "El show de las mañanas", "cat": "Entretenimiento"},
    {"canal": "F10", "inicio": "12:30", "fin": "13:20", "titulo": "Programación de tarde", "cat": "Otros"},
    {"canal": "F10", "inicio": "13:20", "fin": "15:00", "titulo": "F10 Noticias - Segunda edición", "cat": "Noticiero"},
    {"canal": "F10", "inicio": "15:00", "fin": "18:00", "titulo": "Así es aquí con la aplanadora", "cat": "Cultural"},
    {"canal": "F10", "inicio": "18:00", "fin": "20:00", "titulo": "Programación de tarde", "cat": "Otros"},
    {"canal": "F10", "inicio": "20:00", "fin": "22:00", "titulo": "F10 Noticias - Edición central", "cat": "Noticiero"},
    {"canal": "F10", "inicio": "22:00", "fin": "23:30", "titulo": "Titanes", "cat": "Entretenimiento"},
    {"canal": "F10", "inicio": "23:30", "fin": "00:00", "titulo": "Programación de noche", "cat": "Otros"},

    {"canal": "Litus", "inicio": "00:00", "fin": "05:00", "titulo": "Programación de madrugada", "cat": "Otros"},
    {"canal": "Litus", "inicio": "05:00", "fin": "06:00", "titulo": "Hora cinco", "cat": "Radio"},
    {"canal": "Litus", "inicio": "06:00", "fin": "09:00", "titulo": "Que quede claro", "cat": "Radio"},
    {"canal": "Litus", "inicio": "09:00", "fin": "13:00", "titulo": "Radiosapiens", "cat": "Radio"},
    {"canal": "Litus", "inicio": "13:00", "fin": "13:15", "titulo": "Panorama informativo", "cat": "Radio"},
    {"canal": "Litus", "inicio": "13:15", "fin": "14:00", "titulo": "10 en deportes", "cat": "Deportes"},
    {"canal": "Litus", "inicio": "14:00", "fin": "16:00", "titulo": "Ahí vamos", "cat": "Radio"},
    {"canal": "Litus", "inicio": "16:00", "fin": "18:00", "titulo": "Al derecho y al revés", "cat": "Radio"},
    {"canal": "Litus", "inicio": "18:00", "fin": "19:00", "titulo": "10 en deportes", "cat": "Deportes"},
    {"canal": "Litus", "inicio": "19:00", "fin": "20:00", "titulo": "Algo pasó", "cat": "Radio"},
    {"canal": "Litus", "inicio": "20:00", "fin": "20:15", "titulo": "Panorama informativo", "cat": "Radio"},
    {"canal": "Litus", "inicio": "20:15", "fin": "00:00", "titulo": "Programación de noche", "cat": "Radio"},

    {"canal": "Rafaela", "inicio": "00:00", "fin": "06:00", "titulo": "Sin programación", "cat": "Otros"},
    {"canal": "Rafaela", "inicio": "06:00", "fin": "08:00", "titulo": "Amanece la Región", "cat": "Radio"},
    {"canal": "Rafaela", "inicio": "08:00", "fin": "12:00", "titulo": "Arriba la Mañana", "cat": "Radio"},
    {"canal": "Rafaela", "inicio": "12:00", "fin": "16:00", "titulo": "Nada de Siesta", "cat": "Radio"},
    {"canal": "Rafaela", "inicio": "16:00", "fin": "18:00", "titulo": "Entre Mates", "cat": "Radio"},
    {"canal": "Rafaela", "inicio": "18:00", "fin": "20:00", "titulo": "Nunca es Tarde", "cat": "Radio"},
    {"canal": "Rafaela", "inicio": "20:00", "fin": "00:00", "titulo": "Música de Radio", "cat": "Música"},

    {"canal": "Aire", "inicio": "00:00", "fin": "05:00", "titulo": "La noche al Aire", "cat": "Radio"},
    {"canal": "Aire", "inicio": "05:00", "fin": "06:00", "titulo": "Anticipos", "cat": "Radio"},
    {"canal": "Aire", "inicio": "06:00", "fin": "08:00", "titulo": "CREO", "cat": "Radio"},
    {"canal": "Aire", "inicio": "08:00", "fin": "14:00", "titulo": "Ahora vengo", "cat": "Radio"},
    {"canal": "Aire", "inicio": "14:00", "fin": "14:30", "titulo": "Dale, dale deportivo", "cat": "Deportes"},
    {"canal": "Aire", "inicio": "14:30", "fin": "17:30", "titulo": "Santa siesta", "cat": "Radio"},
    {"canal": "Aire", "inicio": "17:30", "fin": "20:00", "titulo": "Una tarde a la vez", "cat": "Radio"},
    {"canal": "Aire", "inicio": "20:00", "fin": "21:00", "titulo": "Dale, dale deportivo", "cat": "Deportes"},
    {"canal": "Aire", "inicio": "21:00", "fin": "00:00", "titulo": "VIVO AIRE", "cat": "Radio"},

    {"canal": "22Web", "inicio": "00:00", "fin": "00:30", "titulo": "Algo que contar", "cat": "Periodístico"},
    {"canal": "22Web", "inicio": "00:30", "fin": "06:00", "titulo": "Repetición", "cat": "Otros"},
    {"canal": "22Web", "inicio": "06:00", "fin": "11:00", "titulo": "Repetición", "cat": "Otros"},
    {"canal": "22Web", "inicio": "11:00", "fin": "12:00", "titulo": "Infoshow", "cat": "Magazine"},
    {"canal": "22Web", "inicio": "12:00", "fin": "14:00", "titulo": "GreKo", "cat": "Periodístico"},
    {"canal": "22Web", "inicio": "14:00", "fin": "16:00", "titulo": "Uno más uno tres", "cat": "Periodístico"},
    {"canal": "22Web", "inicio": "16:00", "fin": "17:00", "titulo": "Código Luteral", "cat": "Entrevistas"},
    {"canal": "22Web", "inicio": "17:00", "fin": "19:00", "titulo": "Estamos de vuelta", "cat": "Periodístico"},
    {"canal": "22Web", "inicio": "19:00", "fin": "20:00", "titulo": "22 Noticias", "cat": "Noticiero"},
    {"canal": "22Web", "inicio": "20:00", "fin": "22:00", "titulo": "La revancha del 1", "cat": "Periodístico"},
    {"canal": "22Web", "inicio": "22:00", "fin": "00:00", "titulo": "Moranza", "cat": "Periodístico"},

    {"canal": "Perfil", "inicio": "00:00", "fin": "08:00", "titulo": "Repetición", "cat": "Otros"},
    {"canal": "Perfil", "inicio": "08:00", "fin": "10:00", "titulo": "Longobardi", "cat": "Periodístico"},
    {"canal": "Perfil", "inicio": "10:00", "fin": "13:00", "titulo": "Modo Fontevecchia", "cat": "Periodístico"},
    {"canal": "Perfil", "inicio": "13:00", "fin": "14:30", "titulo": "Ronda de investigación", "cat": "Periodístico"},
    {"canal": "Perfil", "inicio": "14:30", "fin": "16:30", "titulo": "Ronda de corresponsales", "cat": "Periodístico"},
    {"canal": "Perfil", "inicio": "16:30", "fin": "18:00", "titulo": "Ronda de economistas", "cat": "Periodístico"},
    {"canal": "Perfil", "inicio": "18:00", "fin": "19:00", "titulo": "Ronda de escritores", "cat": "Periodístico"},
    {"canal": "Perfil", "inicio": "19:00", "fin": "21:00", "titulo": "Ronda de editores", "cat": "Periodístico"},
    {"canal": "Perfil", "inicio": "21:00", "fin": "23:00", "titulo": "QR!", "cat": "Periodístico"},
    {"canal": "Perfil", "inicio": "23:00", "fin": "00:00", "titulo": "Periodismo puro", "cat": "Entrevistas"},
]

programas_viernes = [
    {"canal": "Sol", "inicio": "00:00", "fin": "06:00", "titulo": "Sin programación", "cat": "Otros"},
    {"canal": "Sol", "inicio": "06:00", "fin": "06:30", "titulo": "El club de la Sol", "cat": "Otros"},
    {"canal": "Sol", "inicio": "06:30", "fin": "08:30", "titulo": "La primera de Sol", "cat": "Otros"},
    {"canal": "Sol", "inicio": "08:30", "fin": "13:30", "titulo": "Malas constumbres", "cat": "Radio"},
    {"canal": "Sol", "inicio": "13:30", "fin": "14:30", "titulo": "La segunda de Sol", "cat": "Radio"},
    {"canal": "Sol", "inicio": "14:30", "fin": "17:00", "titulo": "Silencio que hay ruido", "cat": "Radio"},
    {"canal": "Sol", "inicio": "17:00", "fin": "18:00", "titulo": "Clave de Sol", "cat": "Radio"},
    {"canal": "Sol", "inicio": "18:00", "fin": "19:00", "titulo": "La tercera de Sol", "cat": "Radio"},
    {"canal": "Sol", "inicio": "19:00", "fin": "00:00", "titulo": "Programación de noche", "cat": "Radio"},

    {"canal": "PowerMax", "inicio": "00:00", "fin": "05:00", "titulo": "Sin programación", "cat": "Otros"},
    {"canal": "PowerMax", "inicio": "05:00", "fin": "07:00", "titulo": "Amanecer con JR", "cat": "Radio"},
    {"canal": "PowerMax", "inicio": "07:00", "fin": "09:30", "titulo": "El mundo y la región", "cat": "Radio"},
    {"canal": "PowerMax", "inicio": "09:30", "fin": "11:00", "titulo": "Página 104", "cat": "Radio"},
    {"canal": "PowerMax", "inicio": "11:00", "fin": "13:00", "titulo": "Asi son las mañanas", "cat": "Radio"},
    {"canal": "PowerMax", "inicio": "13:00", "fin": "14:00", "titulo": "Sin programación", "cat": "Otros"},
    {"canal": "PowerMax", "inicio": "14:00", "fin": "16:00", "titulo": "El show debe continuar", "cat": "Música"},
    {"canal": "PowerMax", "inicio": "16:00", "fin": "18:00", "titulo": "Radio City", "cat": "Radio"},
    {"canal": "PowerMax", "inicio": "18:00", "fin": "20:00", "titulo": "Todos para uno", "cat": "Radio"},
    {"canal": "PowerMax", "inicio": "20:00", "fin": "21:00", "titulo": "Frecuencia retro", "cat": "Radio"},
    {"canal": "PowerMax", "inicio": "21:00", "fin": "00:00", "titulo": "Sin programación", "cat": "Otros"},

    {"canal": "Next", "inicio": "00:00", "fin": "07:00", "titulo": "Programación de madrugada", "cat": "Otros"},
    {"canal": "Next", "inicio": "07:00", "fin": "10:00", "titulo": "Red Urbana", "cat": "Radio"},
    {"canal": "Next", "inicio": "10:00", "fin": "12:00", "titulo": "Diario Castellanos", "cat": "Radio"},
    {"canal": "Next", "inicio": "12:00", "fin": "14:00", "titulo": "Next Noticias", "cat": "Noticiero"},
    {"canal": "Next", "inicio": "14:00", "fin": "15:00", "titulo": "El Espectador Deportes", "cat": "Deportes"},
    {"canal": "Next", "inicio": "15:00", "fin": "19:00", "titulo": "Programación de tarde", "cat": "Otros"},
    {"canal": "Next", "inicio": "19:00", "fin": "20:00", "titulo": "Sin Rebajes", "cat": "Deportes"},
    {"canal": "Next", "inicio": "20:00", "fin": "22:00", "titulo": "+ Noticias", "cat": "Noticiero"},
    {"canal": "Next", "inicio": "22:00", "fin": "00:00", "titulo": "Programación de noche", "cat": "Otros"},

    {"canal": "Chacra", "inicio": "00:00", "fin": "06:00", "titulo": "La red del campo", "cat": "Agro"},
    {"canal": "Chacra", "inicio": "06:00", "fin": "07:00", "titulo": "Chacra Agro Continental", "cat": "Noticiero"},
    {"canal": "Chacra", "inicio": "07:00", "fin": "12:00", "titulo": "La red del campo", "cat": "Agro"},
    {"canal": "Chacra", "inicio": "12:00", "fin": "13:00", "titulo": "ChacraTV Noticias", "cat": "Noticiero"},
    {"canal": "Chacra", "inicio": "13:00", "fin": "18:00", "titulo": "La red del campo", "cat": "Agro"},
    {"canal": "Chacra", "inicio": "18:00", "fin": "00:00", "titulo": "La red del campo", "cat": "Agro"},

    {"canal": "Taste", "inicio": "00:00", "fin": "06:00", "titulo": "Comida y viajes", "cat": "Cocina"},
    {"canal": "Taste", "inicio": "06:00", "fin": "12:00", "titulo": "Comida y viajes", "cat": "Cocina"},
    {"canal": "Taste", "inicio": "12:00", "fin": "18:00", "titulo": "Comida y viajes", "cat": "Cocina"},
    {"canal": "Taste", "inicio": "18:00", "fin": "00:00", "titulo": "Comida y viajes", "cat": "Cocina"},

    {"canal": "F10", "inicio": "00:00", "fin": "07:00", "titulo": "Programación de madrugada", "cat": "Otros"},
    {"canal": "F10", "inicio": "07:00", "fin": "09:30", "titulo": "F10 Noticias - Primera edición", "cat": "Noticiero"},
    {"canal": "F10", "inicio": "09:30", "fin": "12:30", "titulo": "El show de las mañanas", "cat": "Entretenimiento"},
    {"canal": "F10", "inicio": "12:30", "fin": "13:20", "titulo": "Programación de tarde", "cat": "Otros"},
    {"canal": "F10", "inicio": "13:20", "fin": "15:00", "titulo": "F10 Noticias - Segunda edición", "cat": "Noticiero"},
    {"canal": "F10", "inicio": "15:00", "fin": "18:00", "titulo": "Así es aquí con la aplanadora", "cat": "Cultural"},
    {"canal": "F10", "inicio": "18:00", "fin": "20:00", "titulo": "Programación de tarde", "cat": "Otros"},
    {"canal": "F10", "inicio": "20:00", "fin": "22:00", "titulo": "F10 Noticias - Edición central", "cat": "Noticiero"},
    {"canal": "F10", "inicio": "22:00", "fin": "23:30", "titulo": "Titanes", "cat": "Entretenimiento"},
    {"canal": "F10", "inicio": "23:30", "fin": "00:00", "titulo": "Programación de noche", "cat": "Otros"},

    {"canal": "Litus", "inicio": "00:00", "fin": "05:00", "titulo": "Programación de madrugada", "cat": "Otros"},
    {"canal": "Litus", "inicio": "05:00", "fin": "06:00", "titulo": "Hora cinco", "cat": "Radio"},
    {"canal": "Litus", "inicio": "06:00", "fin": "09:00", "titulo": "Que quede claro", "cat": "Radio"},
    {"canal": "Litus", "inicio": "09:00", "fin": "13:00", "titulo": "Radiosapiens", "cat": "Radio"},
    {"canal": "Litus", "inicio": "13:00", "fin": "13:15", "titulo": "Panorama informativo", "cat": "Radio"},
    {"canal": "Litus", "inicio": "13:15", "fin": "14:00", "titulo": "10 en deportes", "cat": "Deportes"},
    {"canal": "Litus", "inicio": "14:00", "fin": "16:00", "titulo": "Ahí vamos", "cat": "Radio"},
    {"canal": "Litus", "inicio": "16:00", "fin": "18:00", "titulo": "Al derecho y al revés", "cat": "Radio"},
    {"canal": "Litus", "inicio": "18:00", "fin": "19:00", "titulo": "10 en deportes", "cat": "Deportes"},
    {"canal": "Litus", "inicio": "19:00", "fin": "20:00", "titulo": "Algo pasó", "cat": "Radio"},
    {"canal": "Litus", "inicio": "20:00", "fin": "20:15", "titulo": "Panorama informativo", "cat": "Radio"},
    {"canal": "Litus", "inicio": "20:15", "fin": "00:00", "titulo": "Programación de noche", "cat": "Radio"},

    {"canal": "Rafaela", "inicio": "00:00", "fin": "06:00", "titulo": "Sin programación", "cat": "Otros"},
    {"canal": "Rafaela", "inicio": "06:00", "fin": "08:00", "titulo": "Amanece la Región", "cat": "Radio"},
    {"canal": "Rafaela", "inicio": "08:00", "fin": "12:00", "titulo": "Arriba la Mañana", "cat": "Radio"},
    {"canal": "Rafaela", "inicio": "12:00", "fin": "16:00", "titulo": "Nada de Siesta", "cat": "Radio"},
    {"canal": "Rafaela", "inicio": "16:00", "fin": "18:00", "titulo": "Entre Mates", "cat": "Radio"},
    {"canal": "Rafaela", "inicio": "18:00", "fin": "20:00", "titulo": "Nunca es Tarde", "cat": "Radio"},
    {"canal": "Rafaela", "inicio": "20:00", "fin": "00:00", "titulo": "Música de Radio", "cat": "Música"},

    {"canal": "Aire", "inicio": "00:00", "fin": "05:00", "titulo": "La noche al Aire", "cat": "Radio"},
    {"canal": "Aire", "inicio": "05:00", "fin": "06:00", "titulo": "Anticipos", "cat": "Radio"},
    {"canal": "Aire", "inicio": "06:00", "fin": "08:00", "titulo": "CREO", "cat": "Radio"},
    {"canal": "Aire", "inicio": "08:00", "fin": "14:00", "titulo": "Ahora vengo", "cat": "Radio"},
    {"canal": "Aire", "inicio": "14:00", "fin": "14:30", "titulo": "Dale, dale deportivo", "cat": "Deportes"},
    {"canal": "Aire", "inicio": "14:30", "fin": "17:30", "titulo": "Santa siesta", "cat": "Radio"},
    {"canal": "Aire", "inicio": "17:30", "fin": "20:00", "titulo": "Una tarde a la vez", "cat": "Radio"},
    {"canal": "Aire", "inicio": "20:00", "fin": "21:00", "titulo": "Dale, dale deportivo", "cat": "Deportes"},
    {"canal": "Aire", "inicio": "21:00", "fin": "00:00", "titulo": "VIVO AIRE", "cat": "Radio"},

    {"canal": "22Web", "inicio": "00:00", "fin": "00:30", "titulo": "Algo que contar", "cat": "Periodístico"},
    {"canal": "22Web", "inicio": "00:30", "fin": "06:00", "titulo": "Repetición", "cat": "Otros"},
    {"canal": "22Web", "inicio": "06:00", "fin": "09:00", "titulo": "Repetición", "cat": "Otros"},
    {"canal": "22Web", "inicio": "09:00", "fin": "11:00", "titulo": "La mañana de Juan Domingo", "cat": "Periodístico"},
    {"canal": "22Web", "inicio": "11:00", "fin": "12:00", "titulo": "Infoshow", "cat": "Magazine"},
    {"canal": "22Web", "inicio": "12:00", "fin": "14:00", "titulo": "GreKo", "cat": "Periodístico"},
    {"canal": "22Web", "inicio": "14:00", "fin": "16:00", "titulo": "La juntada del domingo", "cat": "Otros"},
    {"canal": "22Web", "inicio": "16:00", "fin": "17:00", "titulo": "Intimamente", "cat": "Espectáculo"},
    {"canal": "22Web", "inicio": "17:00", "fin": "19:00", "titulo": "Estamos de vuelta", "cat": "Periodístico"},
    {"canal": "22Web", "inicio": "19:00", "fin": "20:00", "titulo": "22 Noticias", "cat": "Noticiero"},
    {"canal": "22Web", "inicio": "20:00", "fin": "22:00", "titulo": "La revancha del 1", "cat": "Periodístico"},
    {"canal": "22Web", "inicio": "22:00", "fin": "00:00", "titulo": "Moranza", "cat": "Periodístico"},

    {"canal": "Perfil", "inicio": "00:00", "fin": "08:00", "titulo": "Repetición", "cat": "Otros"},
    {"canal": "Perfil", "inicio": "08:00", "fin": "10:00", "titulo": "Longobardi", "cat": "Periodístico"},
    {"canal": "Perfil", "inicio": "10:00", "fin": "13:00", "titulo": "Modo Fontevecchia", "cat": "Periodístico"},
    {"canal": "Perfil", "inicio": "13:00", "fin": "14:30", "titulo": "Ronda de investigación", "cat": "Periodístico"},
    {"canal": "Perfil", "inicio": "14:30", "fin": "16:30", "titulo": "Ronda de corresponsales", "cat": "Periodístico"},
    {"canal": "Perfil", "inicio": "16:30", "fin": "18:00", "titulo": "Ronda de economistas", "cat": "Periodístico"},
    {"canal": "Perfil", "inicio": "18:00", "fin": "19:00", "titulo": "Ronda de escritores", "cat": "Periodístico"},
    {"canal": "Perfil", "inicio": "19:00", "fin": "21:00", "titulo": "Ronda de editores", "cat": "Periodístico"},
    {"canal": "Perfil", "inicio": "21:00", "fin": "23:00", "titulo": "QR!", "cat": "Periodístico"},
    {"canal": "Perfil", "inicio": "23:00", "fin": "00:00", "titulo": "Periodismo puro", "cat": "Entrevistas"},
]

programas_sabado = [
    {"canal": "Sol", "inicio": "00:00", "fin": "06:00", "titulo": "Programación de madrugada", "cat": "Radio"},
    {"canal": "Sol", "inicio": "06:00", "fin": "12:00", "titulo": "Programación de mañana", "cat": "Radio"},
    {"canal": "Sol", "inicio": "12:00", "fin": "18:00", "titulo": "Programación de tarde", "cat": "Radio"},
    {"canal": "Sol", "inicio": "18:00", "fin": "00:00", "titulo": "Programación de noche", "cat": "Radio"},

    {"canal": "PowerMax", "inicio": "00:00", "fin": "06:00", "titulo": "Sin programación", "cat": "Otros"},
    {"canal": "PowerMax", "inicio": "06:00", "fin": "08:00", "titulo": "Amanecer con JR", "cat": "Radio"},
    {"canal": "PowerMax", "inicio": "08:00", "fin": "10:30", "titulo": "La revista de Analía", "cat": "Radio"},
    {"canal": "PowerMax", "inicio": "10:30", "fin": "13:00", "titulo": "Hoy puede ser un gran dia", "cat": "Radio"},
    {"canal": "PowerMax", "inicio": "13:00", "fin": "18:00", "titulo": "Sin programación", "cat": "Otros"},
    {"canal": "PowerMax", "inicio": "18:00", "fin": "00:00", "titulo": "Sin programación", "cat": "Otros"},

    {"canal": "Next", "inicio": "00:00", "fin": "06:00", "titulo": "Programación de madrugada", "cat": "Otros"},
    {"canal": "Next", "inicio": "06:00", "fin": "12:00", "titulo": "Programación de mañana", "cat": "Otros"},
    {"canal": "Next", "inicio": "12:00", "fin": "18:00", "titulo": "Programación de tarde", "cat": "Otros"},
    {"canal": "Next", "inicio": "18:00", "fin": "00:00", "titulo": "Programación de noche", "cat": "Otros"},

    {"canal": "Chacra", "inicio": "00:00", "fin": "06:00", "titulo": "La red del campo", "cat": "Agro"},
    {"canal": "Chacra", "inicio": "06:00", "fin": "07:00", "titulo": "Chacra Agro Continental", "cat": "Noticiero"},
    {"canal": "Chacra", "inicio": "07:00", "fin": "12:00", "titulo": "La red del campo", "cat": "Agro"},
    {"canal": "Chacra", "inicio": "12:00", "fin": "13:00", "titulo": "ChacraTV Noticias", "cat": "Noticiero"},
    {"canal": "Chacra", "inicio": "13:00", "fin": "18:00", "titulo": "La red del campo", "cat": "Agro"},
    {"canal": "Chacra", "inicio": "18:00", "fin": "00:00", "titulo": "La red del campo", "cat": "Agro"},

    {"canal": "Taste", "inicio": "00:00", "fin": "06:00", "titulo": "Comida y viajes", "cat": "Cocina"},
    {"canal": "Taste", "inicio": "06:00", "fin": "12:00", "titulo": "Comida y viajes", "cat": "Cocina"},
    {"canal": "Taste", "inicio": "12:00", "fin": "18:00", "titulo": "Comida y viajes", "cat": "Cocina"},
    {"canal": "Taste", "inicio": "18:00", "fin": "00:00", "titulo": "Comida y viajes", "cat": "Cocina"},

    {"canal": "F10", "inicio": "00:00", "fin": "06:00", "titulo": "Películas", "cat": "Otros"},
    {"canal": "F10", "inicio": "06:00", "fin": "12:00", "titulo": "Películas", "cat": "Otros"},
    {"canal": "F10", "inicio": "12:00", "fin": "18:00", "titulo": "Peliculas", "cat": "Otros"},
    {"canal": "F10", "inicio": "18:00", "fin": "00:00", "titulo": "Películas", "cat": "Otros"},

    {"canal": "Litus", "inicio": "00:00", "fin": "06:00", "titulo": "Programación de madrugada", "cat": "Otros"},
    {"canal": "Litus", "inicio": "06:00", "fin": "12:00", "titulo": "Programación de mañana", "cat": "Otros"},
    {"canal": "Litus", "inicio": "12:00", "fin": "18:00", "titulo": "Programación de tarde", "cat": "Otros"},
    {"canal": "Litus", "inicio": "18:00", "fin": "00:00", "titulo": "Programación de noche", "cat": "Otros"},

    {"canal": "Rafaela", "inicio": "00:00", "fin": "06:00", "titulo": "Sin programación", "cat": "Otros"},
    {"canal": "Rafaela", "inicio": "06:00", "fin": "08:00", "titulo": "Madrugando con mi gente", "cat": "Radio"},
    {"canal": "Rafaela", "inicio": "08:00", "fin": "13:00", "titulo": "Sábados de Acción", "cat": "Radio"},
    {"canal": "Rafaela", "inicio": "13:00", "fin": "20:00", "titulo": "Música de radio", "cat": "Música"},
    {"canal": "Rafaela", "inicio": "20:00", "fin": "00:00", "titulo": "Reciclando historias", "cat": "Radio"},

    {"canal": "Aire", "inicio": "00:00", "fin": "05:00", "titulo": "La noche al Aire", "cat": "Radio"},
    {"canal": "Aire", "inicio": "05:00", "fin": "06:00", "titulo": "Sin programación", "cat": "Otros"},
    {"canal": "Aire", "inicio": "06:00", "fin": "09:00", "titulo": "6 AM", "cat": "Radio"},
    {"canal": "Aire", "inicio": "09:00", "fin": "14:00", "titulo": "Ahora vengo", "cat": "Radio"},
    {"canal": "Aire", "inicio": "14:00", "fin": "16:00", "titulo": "Escándalo", "cat": "Radio"},
    {"canal": "Aire", "inicio": "16:00", "fin": "20:00", "titulo": "Por ahora", "cat": "Radio"},
    {"canal": "Aire", "inicio": "20:00", "fin": "00:00", "titulo": "¿Dónde está el piloto?", "cat": "Deportes"},

    {"canal": "22Web", "inicio": "00:00", "fin": "06:00", "titulo": "Variedades", "cat": "Otros"},
    {"canal": "22Web", "inicio": "06:00", "fin": "12:00", "titulo": "Variedades", "cat": "Otros"},
    {"canal": "22Web", "inicio": "12:00", "fin": "18:00", "titulo": "Variedades", "cat": "Otros"},
    {"canal": "22Web", "inicio": "18:00", "fin": "00:00", "titulo": "Variedades", "cat": "Otros"},

    {"canal": "Perfil", "inicio": "00:00", "fin": "06:00", "titulo": "Variedades", "cat": "Otros"},
    {"canal": "Perfil", "inicio": "06:00", "fin": "12:00", "titulo": "Variedades", "cat": "Otros"},
    {"canal": "Perfil", "inicio": "12:00", "fin": "18:00", "titulo": "Variedades", "cat": "Otros"},
    {"canal": "Perfil", "inicio": "18:00", "fin": "00:00", "titulo": "Variedades", "cat": "Otros"},
]

programas_domingo = [
    {"canal": "Sol", "inicio": "00:00", "fin": "06:00", "titulo": "Programación de madrugada", "cat": "Radio"},
    {"canal": "Sol", "inicio": "06:00", "fin": "12:00", "titulo": "Programación de mañana", "cat": "Radio"},
    {"canal": "Sol", "inicio": "12:00", "fin": "18:00", "titulo": "Programación de tarde", "cat": "Radio"},
    {"canal": "Sol", "inicio": "18:00", "fin": "00:00", "titulo": "Programación de noche", "cat": "Radio"},

    {"canal": "PowerMax", "inicio": "00:00", "fin": "08:00", "titulo": "Sin programación", "cat": "Otros"},
    {"canal": "PowerMax", "inicio": "08:00", "fin": "10:00", "titulo": "Arriba el domingo", "cat": "Radio"},
    {"canal": "PowerMax", "inicio": "10:00", "fin": "12:00", "titulo": "La revista de Analía", "cat": "Radio"},
    {"canal": "PowerMax", "inicio": "12:00", "fin": "16:00", "titulo": "Te va a gustar", "cat": "Radio"},
    {"canal": "PowerMax", "inicio": "16:00", "fin": "20:00", "titulo": "Sin programación", "cat": "Otros"},
    {"canal": "PowerMax", "inicio": "20:00", "fin": "00:00", "titulo": "Sin programación", "cat": "Otros"},

    {"canal": "Next", "inicio": "00:00", "fin": "06:00", "titulo": "Programación de madrugada", "cat": "Otros"},
    {"canal": "Next", "inicio": "06:00", "fin": "12:00", "titulo": "Programación de mañana", "cat": "Otros"},
    {"canal": "Next", "inicio": "12:00", "fin": "18:00", "titulo": "Programación de tarde", "cat": "Otros"},
    {"canal": "Next", "inicio": "18:00", "fin": "00:00", "titulo": "Programación de noche", "cat": "Otros"},

    {"canal": "Chacra", "inicio": "00:00", "fin": "06:00", "titulo": "La red del campo", "cat": "Agro"},
    {"canal": "Chacra", "inicio": "06:00", "fin": "07:00", "titulo": "Chacra Agro Continental", "cat": "Noticiero"},
    {"canal": "Chacra", "inicio": "07:00", "fin": "12:00", "titulo": "La red del campo", "cat": "Agro"},
    {"canal": "Chacra", "inicio": "12:00", "fin": "13:00", "titulo": "ChacraTV Noticias", "cat": "Noticiero"},
    {"canal": "Chacra", "inicio": "13:00", "fin": "18:00", "titulo": "La red del campo", "cat": "Agro"},
    {"canal": "Chacra", "inicio": "18:00", "fin": "00:00", "titulo": "La red del campo", "cat": "Agro"},

    {"canal": "Taste", "inicio": "00:00", "fin": "06:00", "titulo": "Comida y viajes", "cat": "Cocina"},
    {"canal": "Taste", "inicio": "06:00", "fin": "12:00", "titulo": "Comida y viajes", "cat": "Cocina"},
    {"canal": "Taste", "inicio": "12:00", "fin": "18:00", "titulo": "Comida y viajes", "cat": "Cocina"},
    {"canal": "Taste", "inicio": "18:00", "fin": "00:00", "titulo": "Comida y viajes", "cat": "Cocina"},

    {"canal": "F10", "inicio": "00:00", "fin": "06:00", "titulo": "Películas", "cat": "Otros"},
    {"canal": "F10", "inicio": "06:00", "fin": "12:00", "titulo": "Películas", "cat": "Otros"},
    {"canal": "F10", "inicio": "12:00", "fin": "18:00", "titulo": "Peliculas", "cat": "Otros"},
    {"canal": "F10", "inicio": "18:00", "fin": "00:00", "titulo": "Películas", "cat": "Otros"},

    {"canal": "Litus", "inicio": "00:00", "fin": "06:00", "titulo": "Programación de madrugada", "cat": "Otros"},
    {"canal": "Litus", "inicio": "06:00", "fin": "12:00", "titulo": "Programación de mañana", "cat": "Otros"},
    {"canal": "Litus", "inicio": "12:00", "fin": "18:00", "titulo": "Programación de tarde", "cat": "Otros"},
    {"canal": "Litus", "inicio": "18:00", "fin": "00:00", "titulo": "Programación de noche", "cat": "Otros"},

    {"canal": "Rafaela", "inicio": "00:00", "fin": "06:00", "titulo": "Sin programación", "cat": "Otros"},
    {"canal": "Rafaela", "inicio": "06:00", "fin": "12:00", "titulo": "Sin programación", "cat": "Otros"},
    {"canal": "Rafaela", "inicio": "12:00", "fin": "18:00", "titulo": "Sin programación", "cat": "Otros"},
    {"canal": "Rafaela", "inicio": "18:00", "fin": "00:00", "titulo": "Sin programación", "cat": "Otros"},

    {"canal": "Aire", "inicio": "00:00", "fin": "08:00", "titulo": "Sin programación", "cat": "Otros"},
    {"canal": "Aire", "inicio": "08:00", "fin": "14:00", "titulo": "Algo que decir", "cat": "Radio"},
    {"canal": "Aire", "inicio": "14:00", "fin": "16:00", "titulo": "Con viento a favor", "cat": "Radio"},
    {"canal": "Aire", "inicio": "16:00", "fin": "20:00", "titulo": "Flor de domingo", "cat": "Radio"},
    {"canal": "Aire", "inicio": "20:00", "fin": "00:00", "titulo": "Domingo vivo", "cat": "Radio"},

    {"canal": "22Web", "inicio": "00:00", "fin": "08:00", "titulo": "Variedades", "cat": "Otros"},
    {"canal": "22Web", "inicio": "08:00", "fin": "12:00", "titulo": "Variedades", "cat": "Otros"},
    {"canal": "22Web", "inicio": "12:00", "fin": "16:00", "titulo": "Variedades", "cat": "Otros"},
    {"canal": "22Web", "inicio": "16:00", "fin": "19:00", "titulo": "La juntada del domingo", "cat": "Otros"},
    {"canal": "22Web", "inicio": "19:00", "fin": "00:00", "titulo": "Variedades", "cat": "Otros"},

    {"canal": "Perfil", "inicio": "00:00", "fin": "06:00", "titulo": "Variedades", "cat": "Otros"},
    {"canal": "Perfil", "inicio": "06:00", "fin": "12:00", "titulo": "Variedades", "cat": "Otros"},
    {"canal": "Perfil", "inicio": "12:00", "fin": "18:00", "titulo": "Variedades", "cat": "Otros"},
    {"canal": "Perfil", "inicio": "18:00", "fin": "00:00", "titulo": "Variedades", "cat": "Otros"},
]

def generar_xmltv(dias=30):
    tv = ET.Element(
        "tv",
        {"generator-info-name": "MiGeneradorEPG"}
    )

    todos_programas = (
        programas_lunes + programas_martes +
        programas_miercoles + programas_jueves +
        programas_viernes + programas_sabado +
        programas_domingo
    )

    canales_unicos = sorted(
        set(p["canal"] for p in todos_programas)
    )

    for ch in canales_unicos:
        channel_node = ET.SubElement(
            tv, "channel", id=ch
        )
        ET.SubElement(
            channel_node, "display-name"
        ).text = ch

    # Usar la fecha local argentina, no la fecha UTC.
    hoy = datetime.now(ARG_TZ).date()

    for i in range(dias):
        fecha = hoy + timedelta(days=i)
        dia_semana = fecha.weekday()

        listas = [
            programas_lunes,
            programas_martes,
            programas_miercoles,
            programas_jueves,
            programas_viernes,
            programas_sabado,
            programas_domingo,
        ]

        programas_dia = listas[dia_semana]

        for p in programas_dia:
            # Las horas de las listas son horas de Argentina.
            inicio_local = datetime.strptime(
                f"{fecha:%Y%m%d} {p['inicio']}",
                "%Y%m%d %H:%M"
            ).replace(tzinfo=ARG_TZ)

            fecha_fin = fecha

            # Si termina después de medianoche,
            # el fin corresponde al día siguiente.
            if p["fin"] < p["inicio"]:
                fecha_fin += timedelta(days=1)

            fin_local = datetime.strptime(
                f"{fecha_fin:%Y%m%d} {p['fin']}",
                "%Y%m%d %H:%M"
            ).replace(tzinfo=ARG_TZ)

            # Convertir los instantes a UTC para XMLTV.
            inicio_utc = inicio_local.astimezone(
                timezone.utc
            )
            fin_utc = fin_local.astimezone(
                timezone.utc
            )

            start_ts = (
                inicio_utc.strftime("%Y%m%d%H%M%S")
                + " +0000"
            )
            end_ts = (
                fin_utc.strftime("%Y%m%d%H%M%S")
                + " +0000"
            )

            prog = ET.SubElement(
                tv,
                "programme",
                start=start_ts,
                stop=end_ts,
                channel=p["canal"]
            )

            ET.SubElement(
                prog, "title", lang="es"
            ).text = p["titulo"]

            ET.SubElement(
                prog, "category", lang="es"
            ).text = p["cat"]

    xml_str = minidom.parseString(
        ET.tostring(tv, encoding="utf-8")
    ).toprettyxml(indent="  ")

    with open(
        "guia_30_dias.xml", "w", encoding="utf-8"
    ) as f:
        f.write(xml_str)

    print(
        f"Archivo 'guia_30_dias.xml' generado "
        f"para {dias} días."
    )


generar_xmltv(10)

