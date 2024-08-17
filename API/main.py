from flask import Flask, request, jsonify, render_template, redirect
import sqlite3
app = Flask(__name__)

userLogado = ""
connection = sqlite3.connect("data.db", check_same_thread=False)

cursor = connection.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS todo (
    todo_name TEXT,
    todo_user, TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS usuarios (
    user TEXT,
    password TEXT
)
""")
@app.route("/")
def home():
    cursor.execute('SELECT * FROM usuarios')
    usuarios = cursor.fetchall()
    return render_template("index.html")

@app.route("/todoslist")
def todoslist():
    cursor.execute('SELECT * FROM todo')
    todos = cursor.fetchall()
    lista_todos = []
    for todo in todos: #TO ENTENDENDO PORRA NENHUMA A PARTIR DAQUI
        newItem = ''.join(todo)
        lista_todos.append(newItem)
    return render_template("todolist.html", todos=lista_todos) # --

@app.route("/criar_todo", methods=["POST"])
def criar_todo():
    nome_todo = request.form['todo_name']
    cursor.execute(f"INSERT INTO todo VALUES ('{nome_todo}')")
    connection.commit()
    return redirect('/')

@app.route("/deletar_todo", methods=["POST"])
def deletar_todo():
    todo_name = request.form['todo_name']
    cursor.execute("DELETE FROM todo WHERE todo_name = ?", (todo_name,))
    return redirect('/')

connection.commit()
if __name__ == "__main__":
    app.run(debug=True)
connection.close()