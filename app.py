from flask import Flask, render_template, request
import psycopg2

# -------------- variáveis de ambiente --------------- #
import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), ".env")
load_dotenv(dotenv_path)

DB_NAME = os.environ.get("DB_NAME")
DB_USER = os.environ.get("DB_USER")
DB_PASSWORD = os.environ.get("DB_PASSWORD")
DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")


app = Flask(__name__)

conn = psycopg2.connect(
    f"dbname={DB_NAME} user={DB_USER} password={DB_PASSWORD} host={DB_HOST} port={DB_PORT}")

cursor = conn.cursor()


# ----------------------------- INDEX ---------------------------- #

@app.route("/", methods=["GET"])
def AllRoutes():
    return render_template("index.html")


# ---------------------------- CREATE ---------------------------- #


@app.route('/register', methods=["GET", "POST"])
def register():

    try:

        if request.method == "GET":
            return render_template("register.html")

        if request.method == "POST":
            name = request.form["name"]
            email = request.form["email"]
            password = request.form["password"]
            confirmPassword = request.form["confirmPassword"]

            if len(name) == 0:
                return "digite seu nome completo", 422

            if len(email) == 0:
                return "digite um email válido", 422
            
            if len(password) < 8:
                return "A senha deve ter no minimo 8 caracteres", 422

            if password != confirmPassword:
                return "As senhas não estão iguais", 422

            # ---- checking if email exist ---- #

            cursor.execute(
                f"SELECT * FROM users WHERE email = %(email)s", ({'email': email}))

            checkemail = cursor.fetchall()

            if bool(checkemail) == True:
                return "email ja está em uso"

            cursor.execute(
                "INSERT INTO public.users (name, email, password) VALUES (%s, %s, %s);", (name, email, password))

            conn.commit()

            return render_template("response.html", text="criado"), 201

    except Exception as N:
        return "não foi possivel realizar seu cadastro", 500, print(N)


# ---------------------------- READ ---------------------------- #

@app.route("/users", methods=["GET"])
def allUsers():
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    return render_template("get.html", users=users), 200


@app.route("/users/<int:id>", methods=["GET"])
def oneUser(id):
    cursor.execute(f"SELECT * FROM users WHERE id = %(id)s", ({'id': id}))
    user = cursor.fetchall()
    return render_template("get.html", users=user), 200


# ---------------------------- UPDATE ---------------------------- #


@app.route("/update", methods=["GET", "POST"])
async def updateUser():
    try:

        if request.method == "GET":
            return render_template("update.html")

        if request.method == "POST":
            email = request.form["email"]
            password = request.form["password"]

            newName = request.form["newName"]
            newEmail = request.form["newEmail"]
            newPassword = request.form["newPassword"]
            confirmNewPassword = request.form["confirmNewPassword"]

            # ------------- form validations ------------ #

            if len(email) < 5:
                return "Seu antigo email não é válido", 422

            if len(password) < 8:
                return "digite uma senha válida", 422

            if len(newName) < 3:
                return "digite seu nome completo", 422

            if len(newEmail) < 8:
                return "digite um novo email válido", 422

            if len(newPassword) < 8:
                return "digite uma senha válida", 422

            if newPassword != confirmNewPassword:
                return "Suas novas senhas não estão iguais", 422

            cursor.execute(
                f"SELECT * FROM users WHERE email = %(email)s AND password = %(password)s", ({'email': email, 'password': password}))
            checkEmail = cursor.fetchall()

            if bool(checkEmail) == False:
                return "Email ou senha antigos estão incorretos", 401

            if email != newEmail:

                cursor.execute(
                    f"SELECT * FROM users WHERE email = %(email)s", ({'email': newEmail}))
                checkEmail = cursor.fetchall()

                if bool(checkEmail) == True:
                    return "O email que está tentando cadastrar já está em uso", 422

            cursor.execute(f"UPDATE users SET name = %(newName)s, email = %(newEmail)s, password = %(newPassword)s WHERE email = %(email)s AND password = %(password)s", ({
                        'newName': newName, 'newEmail': newEmail, 'newPassword': newPassword, 'email': email, 'password': password}))

            conn.commit()

            return render_template("response.html", text="atualizado"), 200

    except Exception as N:
        return print(N), 500


# ---------------------------- DELETE ---------------------------- #


@app.route("/delete", methods=["GET", "POST"])
def deletUser():
    if request.method == "GET":
        return render_template("delete.html")

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]
        confirmPassword = request.form["confirmPassword"]

        if len(email) < 5:
            return "Informações inválidas", 400

        if len(password) < 8:
            return "Informações inválidas", 400

        if password != confirmPassword:
            return "As senhas não estão iguais", 400

        # ------------ validating data ------------ #

        cursor.execute(
            f"SELECT * FROM users WHERE email = %(email)s AND password = %(password)s", ({'email': email, 'password': password}))

        checkEmail = cursor.fetchall()

        if bool(checkEmail) == False:
            return "As informações não conferem com banco de dados", 401

        cursor.execute(
            f"DELETE FROM users WHERE email =  %(email)s", ({'email': email}))
        conn.commit()

        return render_template("response.html", text="deletado"), 200

app.run(debug=True)
