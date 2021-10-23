import psycopg2
import names
import random

con = psycopg2.connect(database="HRIS", user="postgres", password="1234", port="5432")
cur = con.cursor()

departamentos = ["Gerencia", "Finanzas", "Marketing", "Data Science", "IT", "Ventas", "Recursos Humanos", "Logistica", "Produccion"]
gerentes = [4342, 89, 3891, 678, 92123, 12354, 122, 5912, 43436]

"""
#Insercion de los departamentos
for i in range(len(departamentos)):
    cur.execute("INSERT INTO Departamento VALUES (" + str(i+1) + ", \'" + departamentos[i] + "\', " + str(gerentes[i]) + ", " + str(random.randint(1,2)) + ")")
"""

cargos = [["Asistente", "Administrador", "Contador", "Recepsionista", "Asesor Legal"],
          ["Financiero", "Contador", "Administrador", "Asistente", "Analista"],
          ["Mercadologo", "Investigador", "Publicista", "Diseñador", "Asistente"],
          ["Data Scientist", "Analista", "Programador", "Ingeniero de Datos"],
          ["Ingeniero de Sistemas", "Programador", "Asistente", "Tecnico"],
          ["Contador", "Asistente", "Asesor"],
          ["Jefe de Tienda", "Vendedor", "Administrador", "Supervisor"],
          ["Reclutador", "Administrador", "Motivador", "Asesor", "Asistente"],
          ["Operador", "Mensajero", "Supervisor", "Contador"],
          ["Administrador", "Jefe de Fabrica", "Operador", "Mecanico", "Analista"]]

cargos_lista = ["Gerente", "Asistente", "Administrador", "Contador", "Recepsionista", "Asesor Legal",
          "Financiero", "Analista",
          "Mercadologo", "Investigador", "Publicista", "Diseñador",
          "Data Scientist", "Programador", "Ingeniero de Datos",
          "Ingeniero de Sistemas", "Tecnico",
          "Asesor",
          "Jefe de Tienda", "Vendedor", "Supervisor",
          "Reclutador", "Motivador",
          "Operador", "Mensajero",
          "Jefe de Fabrica", "Mecanico"]

"""
#Insercion de los cargos
for i in range(len(cargos_lista)):
    cur.execute("INSERT INTO Cargo VALUES (" + str(i+1) + ", \'" + cargos_lista[i] + "\')")
"""

with open('C:\\Users\\osjom\\Desktop\\foto1.jpg', 'rb') as file:
    foto1 = file.read()
    
with open('C:\\Users\\osjom\\Desktop\\foto2.jpg', 'rb') as file:
    foto2 = file.read()

#Generar empleados automaticamente
def generarEmpleados(cantidad):
    cur.execute("SELECT MAX(id_empleado) FROM Empleado")
    id_max = cur.fetchone()[0]
    for i in range(cantidad):
        id = id_max + i + 1
        sexo = random.randint(1,2)
        if(sexo == 1):
            nombres = names.get_first_name(gender='female') + " " + names.get_first_name(gender='female')
            foto = foto1
        else:
            nombres = names.get_first_name(gender='male') + " " + names.get_first_name(gender='male')
            foto = foto2
        apellidos = names.get_last_name() + " " + names.get_last_name()
        telefono = str(random.randint(10000000, 99999999))
        fecha_nac = str(random.randint(1940, 2004)) + "-" + str(random.randint(1, 12))  + "-" + str(random.randint(1, 28))
        if (id) in gerentes:
            cargo_id = 1
            salario = str(random.randint(50000, 100000))
            dep_id = gerentes.index(id) + 1
        else:       
            dep_id = random.randint(1, len(departamentos))
            cargo_id = cargos_lista.index(random.choice(cargos[dep_id]))
            salario = str(random.randint(4000, 70000))
        fecha_cont = str(random.randint(1960, 2021)) + "-" + str(random.randint(1, 12))  + "-" + str(random.randint(1, 28))
        email = ''.join(nombres.split()).lower() + "-" + ''.join(apellidos.split()).lower() + "@gmail.com"
        cur.execute("INSERT INTO \"empleado\" VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                    (id, nombres, apellidos, telefono, fecha_nac, cargo_id, salario, foto, dep_id, fecha_cont, email))
        print(i+1)
    con.commit()
    

#Extraer imagen de la base de datos
def getFoto(id_empleado, path):
    cur.execute("SELECT \"id_empleado\", \"foto\" FROM \"empleado\" WHERE \"id_empleado\" = " + str(id_empleado))
    result = cur.fetchall()
    for row in result:
        open(path + '//' + str(row[0]) + '.jpg', 'wb').write(row[1])

#Cambiar la foto de algun emplado ya existente en la base de datos
def actualizarFoto(id_empleado, path):
    with open(path, 'rb') as file:
        foto_nueva = file.read()
    cur.execute("UPDATE Empleado SET foto = %s WHERE id_empleado = %s", (foto_nueva, id_empleado))
    con.commit()

#Insertar un nuevo empleado desde python
def insertarEmpleado(nombres, apellidos, telefono, fecha_nacimiento, id_cargo, salario, foto_path, id_dep, fecha_contratacion, email):
    with open(foto_path, 'rb') as file:
        foto = file.read()
    cur.execute("INSERT INTO Empleado VALUES ((SELECT MAX(id_empleado) + 1 FROM Empleado), %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                (nombres, apellidos, str(telefono), fecha_nacimiento, id_cargo, salario, foto, id_dep, fecha_contratacion, email))
    con.commit()

