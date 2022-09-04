# API-Flask

* Esta API é um pequeno projeto utilizando as tecnologias FLask e Postgresql com Psycopg2

* Para iniciar a api, primeiro crie e ative o ambiente virtual.
Mais informações aqui https://flask.palletsprojects.com/en/2.2.x/installation/#virtual-environments .

* Dentro do ambiente ativado, use o seguinte comando para instalar o Flask: pip install Flask

* Agora será necessário criar uma tabela no Postgresql com as seguintes informações:

    CREATE TABLE IF NOT EXISTS public.users
    (
        id serial NOT NULL,
        name character varying NOT NULL,
        email character varying NOT NULL,
        password character varying NOT NULL,
        CONSTRAINT users_pkey PRIMARY KEY (id),
        CONSTRAINT users_email_key UNIQUE (email)
    )

* Instale o Psycopg2 com o comando: pip install psycopg2

* Crie um arquivo dotenv e passe as informações do seu banco de dados postgresql seguindo o .env.example

* Por fim inicialize a aplicação.
