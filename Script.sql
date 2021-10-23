--Se crean todas las tablas
CREATE TABLE  IF NOT EXISTS Lugar(
	id_lugar integer,
	pais varchar(50),
	estado_prov varchar(50),
	ciudad varchar(50),
	direccion varchar(50),
	PRIMARY KEY (id_lugar)
);

CREATE TABLE IF NOT EXISTS Departament(
	id_dep integer,
	nombre_dep varchar(50),
	id_gerente integer,
	id_lugar integer,
	PRIMARY KEY (id_dep),
	FOREIGN KEY (id_lugar) REFERENCES Lugar(id_lugar)
);

CREATE TABLE IF NOT EXISTS Cargo(
	id_cargo integer,
	titulo_cargo varchar(50),
	PRIMARY KEY (id_cargo)
);

CREATE TABLE IF NOT EXISTS Empleado(
	id_empleado integer,
	nombres varchar(30),
	apellidos varchar(30),
	telefono varchar(8),
	fecha_nacimiento date,
	id_cargo integer,
	salario float,
	foto bytea,
	id_dep integer,
	fecha_contratacion date,
	email varchar(60),
	PRIMARY KEY (id_empleado),
	FOREIGN KEY (id_cargo) REFERENCES Cargo(id_cargo),
	FOREIGN KEY (id_dep) REFERENCES Departamento(id_dep)
);

--Se insertan las ubicaciones
INSERT INTO Lugar VALUES 
	(1, 'Guatemala', 'Guatemala', 'Ciudad de Guatemala', 'Zona 2'),
	(2, 'Guatemala', 'Guatemala', 'Ciudad de Guatemala', 'Zona 9');

--Se deben insertar los datos generados desde python

--Luego de insertar los datos, se agrega el fk para id_gerente en la tabla de Departamento
ALTER TABLE Departamento 
ADD CONSTRAINT fk_gerente 
FOREIGN KEY (id_gerente)
REFERENCES Empleado (id_empleado);

--CONSULTAS

-- 1. Creacion de nuevos empleados
-- Se crea un procedimiento almacenado para insertar empelados
CREATE OR REPLACE PROCEDURE insertarEmpleado(nom VARCHAR, ap VARCHAR, tel VARCHAR, fn DATE, idc INTEGER,
											 sal FLOAT, idd INTEGER, fc DATE, em VARCHAR) 
LANGUAGE plpgsql
AS
$$
BEGIN
	INSERT INTO Empleado
	VALUES ((SELECT MAX(id_empleado) + 1 FROM Empleado), nom, ap, tel, fn, idc, sal, NULL, idd, fc, em);
	COMMIT;
END
$$;
-- Utilizacion del procedimiento almacenado
CALL insertarEmpleado('nombres', 'apellidos', 'tel', '2000-10-10', 9, 20000, 4, '2021-10-19', 'test@email.com');

--2. Actualizacion de datos de un empleado
UPDATE Empleado
SET campo = 
WHERE id_empleado = 123456789;

-- 3. Eliminacion de datos

--Eliminar empleado
DELETE FROM Empleado WHERE id_emplado = 123456789;

--Procedimiento para eliminar un cargo 
CREATE OR REPLACE PROCEDURE eliminarCargo(idc INTEGER) 
LANGUAGE plpgsql
AS
$$
BEGIN
	UPDATE Empleado
	SET id_cargo = NULL
	WHERE id_cargo = idc;

	DELETE FROM Cargo
	WHERE id_cargo = idc;
	
	COMMIT;
END
$$;
--Test eliminar cargo
INSERT INTO Cargo VALUES (100, 'Traductor');
CALL insertarEmpleado('nombres', 'apellidos', 'tel', '2000-10-10', 100, 20000, 4, '2021-10-19', 'test@email.com');
SELECT * FROM Cargo;
SELECT * FROM Empleado ORDER BY id_empleado DESC LIMIT 100;
CALL eliminarCargo(100);

--Procedimiento para eliminar un departamento
CREATE OR REPLACE PROCEDURE eliminarDepartamento(idd INTEGER) 
LANGUAGE plpgsql
AS
$$
BEGIN
	UPDATE Empleado
	SET id_dep = NULL
	WHERE id_dep = idd;

	DELETE FROM Departamento
	WHERE id_dep = idd;
	
	COMMIT;
END
$$;
--Test eliminar departamento
INSERT INTO Departamento VALUES (100, 'Limpieza');
CALL insertarEmpleado('nombres', 'apellidos', 'tel', '2000-10-10', 9, 20000, 100, '2021-10-19', 'test@email.com');
SELECT * FROM Departamento;
SELECT * FROM Empleado ORDER BY id_empleado DESC LIMIT 100;
CALL eliminarDepartamento(100);

--Procedimiento para eliminar un lugar
CREATE OR REPLACE PROCEDURE eliminarLugar(idl INTEGER) 
LANGUAGE plpgsql
AS
$$
BEGIN
	UPDATE Departamento
	SET id_lugar= NULL
	WHERE id_lugar = idl;

	DELETE FROM Lugar
	WHERE id_lugar = idl;
	
	COMMIT;
END
$$;
--Test eliminar lugar
INSERT INTO Lugar VALUES (3, 'Estados Unidos', 'Florida', 'Miami', 'fjjld  djfl djsalfd')
INSERT INTO Departamento VALUES (100, 'Limpieza', NULL, 3);
SELECT * FROM Lugar;
SELECT * FROM Departamento;
CALL eliminarLugar(3);
