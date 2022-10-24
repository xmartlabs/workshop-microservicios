# Workshop Microservicios
## Crear la base de datos
- Bajar el servicio anterior **ctrl+c** en la ventana donde está corriendo

- Levantar el compose nuevamente:

```docker-compose up --build customer-db pgadmin```

- Administrar DB. [conectarse al pgadmin](http://localhost:5050)
- User: admin@workshop.com
- Password: admin

### Crear conexión al servidor:
- Object / Register Server
- host: customer-db
- port: 5432
- username: workshop
- password: workshop

- Botón secundario sobre la DB "postgres"
- Query tool
```
CREATE DATABASE workshop_dev
    WITH
    OWNER = workshop
    ENCODING = 'UTF8'
    LC_COLLATE = 'en_US.utf8'
    LC_CTYPE = 'en_US.utf8'
    TABLESPACE = pg_default
    CONNECTION LIMIT = -1
    IS_TEMPLATE = False;
```
- Conectarse a la db "workshop_dev"
- Query Tool
```
CREATE TABLE IF NOT EXISTS public.customer
(
    id character varying(36) COLLATE pg_catalog."default" NOT NULL,
    name character varying(50) COLLATE pg_catalog."default",
    address character varying(50) COLLATE pg_catalog."default",
    created_date timestamp with time zone,
    bank_account character varying(50) COLLATE pg_catalog."default",
    CONSTRAINT customer_pkey PRIMARY KEY (id)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.customer
    OWNER to workshop;
```

### Rehacer el orchestrator:
- Bajar el servicio anterior **ctrl+c** en la ventana donde está corriendo
```
docker-compose build orchestrator
docker-compose up
```
[abrir documentación del orquestador](http://localhost/docs) 