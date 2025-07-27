create table USUARIO (
	id_usuario SERIAL primary key,
	nombre varchar(50),
	foto_perfil varchar(100),
	email varchar(100),
	clave varchar(255),
   sexo varchar(15)
);

create table GENERADOR(
	id_generador SERIAL primary key,
	id_usuario integer not null,
	foreign key (id_usuario) references USUARIO(id_usuario),
	mac_address char(17),
	ciudad varchar(50),
	calle varchar(50),
	numero_vivienda integer
);

create table MEDICION(
	id_medicion SERIAL primary key,
	id_generador integer not null,
	foreign key (id_generador) references GENERADOR(id_generador),
	voltaje integer,
	consumo integer,
	velocidad integer,
	direccion_viento integer,
	humedad integer,
	temperatura integer,
	fecha DATE default CURRENT_DATE,
	hora time default CURRENT_TIME
);

create index email_idx
on USUARIO (email);

create index mac_idx
on GENERADOR (mac_address);
