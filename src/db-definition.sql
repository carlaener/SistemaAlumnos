create database if not exists alumnos;
use alumnos;

create table alumnos (
	id int not null auto_increment,
    nombre varchar (255),
    correo varchar (255),
    foto varchar (1000),
    dni varchar (10,)
    primary key (id)
);