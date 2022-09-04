# API-Flask

* Esta API é um pequeno projeto utilizando as tecnologias FLask e Postgresql com Psycopg2

* Para iniciar a api, primeiro crie o ambiente flask.
Mais informações aqui https://flask.palletsprojects.com/en/2.2.x/installation/.

* Agora será necessário criar uma tabela no Postgresql com as informações a seguir:

CREATE TABLE IF NOT EXISTS public.users
(
    id serial NOT NULL,
    name character varying NOT NULL,
    email character varying NOT NULL,
    password character varying NOT NULL,
    CONSTRAINT users_pkey PRIMARY KEY (id),
    CONSTRAINT users_email_key UNIQUE (email)
)


* Crie um arquivo dotenv e passe as informações do seu banco de dados postgresql seguindo o .env.example

* Por fim inicialize a aplicação.
