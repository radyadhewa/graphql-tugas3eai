import graphene
import sqlite3
from flask import Flask, json, jsonify, request
from graphene import ObjectType, String, Int, List

# init app
app = Flask(__name__)

# define data object
class UserObject(ObjectType):
    id = Int()
    first_name = String()
    last_name = String()
    username = String()
    password = String()
    email = String()
    age = Int()
    phone = String()

# define get data
class Query(ObjectType):
    all_users = List(UserObject)

    def resolve_all_users(root, info):
        conn = sqlite3.connect('mydatabase.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Users")
        users = []
        for row in cursor.fetchall():
            user = UserObject(
                id=row[0],
                first_name=row[1],
                last_name=row[2],
                username=row[3],
                password=row[4],
                email=row[5],
                age=row[6],
                phone=row[7]
            )
            users.append(user)
        conn.close()
        return users

    user_by_id = graphene.Field(UserObject, id=Int(required=True))
    user_by_username = graphene.Field(UserObject, username=String(required=True))

    def resolve_user_by_id(root, info, id):
        conn = sqlite3.connect('mydatabase.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Users WHERE id=?", (id,))
        user_data = cursor.fetchone()
        conn.close()
        if user_data:
            return UserObject(
                id=user_data[0],
                first_name=user_data[1],
                last_name=user_data[2],
                username=user_data[3],
                password='kamu gaboleh tau ya (ini bukan passwordnya serius)',
                email=user_data[5],
                age=user_data[6],
                phone=user_data[7]
            )
        else:
            return "Data with that ID hasn't been created"
      
    def resolve_user_by_username(root, info, username):
        conn = sqlite3.connect('mydatabase.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Users WHERE username=?", (username,))
        user_data = cursor.fetchone()
        conn.close()
        if user_data is not None:
            return UserObject(
                id=user_data[0],
                first_name=user_data[1],
                last_name=user_data[2],
                username=user_data[3],
                password='secret',
                email=user_data[5],
                age=user_data[6],
                phone=user_data[7]
            )
        else:
            return "Data with that username hasn't been created"

# define mutation
class CreateUser(graphene.Mutation):
    class Arguments:
        first_name = String(required=True)
        last_name = String(required=True)
        username = String(required=True)
        password = String(required=True)
        email = String(required=True)
        age = Int(required=True)
        phone = String(required=True)

    user = graphene.Field(UserObject)

    def mutate(root, info, first_name, last_name, username, password, email, age, phone):
        conn = sqlite3.connect('mydatabase.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Users (first_name, last_name, username, password, email, age, phone) VALUES (?, ?, ?, ?, ?, ?, ?)", (first_name, last_name, username, password, email, age, phone))
        user_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return CreateUser(
            user=UserObject(
                id=user_id,
                first_name=first_name,
                last_name=last_name,
                username=username,
                password=password,
                email=email,
                age=age,
                phone=phone
            )
        )

class Mutation(ObjectType):
    create_user = CreateUser.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)

# authentication
def authenticate_request():
    auth_header = request.headers.get('Authorization')
    if auth_header:
        if auth_header == 'bayar_kerjasama_dulu':
            return True
    return False

# add routes
@app.route('/')
def index():
    return '<a href="/graphql">Go to GraphQL Playground</a>'

@app.route('/graphql', methods=['POST'])
def graphql():
    if not authenticate_request():
        return jsonify({'error': 'Unauthorized access (Wrong Password)'}), 401

    data = request.get_json()
    query = data.get('query')
    if not query:
        return jsonify({'error': 'No query provided'}), 400
    
    result = schema.execute(query)
    return json.dumps(result.data), 200, {'Content-Type': 'application/json'}
  
@app.route('/test_db_connection')
def test_db_connection():
    try:
        conn = sqlite3.connect('mydatabase.db')
        conn.close()
        return 'Database connection successful'
    except Exception as e:
        return f'Error connecting to database: {str(e)}', 500

if __name__ == '__main__':
    app.run(debug=True)
