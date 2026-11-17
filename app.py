from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

input_data = {
    "feedBtn": False,
    "touchBtn": False,
    "isNear": False,
    "washBtn": False
}

@app.route("/")
def defaultPet():
    return render_template("index.html", name = "Raspberry")

@app.route("/setting")
def setting():
    return render_template("setting.html")

@app.route("/pet/")
@app.route("/pet/<pet_name>")
def newPet(pet_name = "Raspberry"):
    return render_template("index.html", name = pet_name)

@app.route('/get_input/h', methods=['GET'])
def get_input_h():
    global input_data
    response_data = {
        "status": "success",
        "feedBtn": input_data["feedBtn"],
        "touchBtn": input_data["touchBtn"],
        "isNear": input_data["isNear"],
        "washBtn": input_data["washBtn"]
    }
    input_data["feedBtn"] = False
    input_data["touchBtn"] = False
    input_data["washBtn"] = False
    return jsonify(response_data)

@app.route('/get_input/w', methods=['POST'])
def get_input_w():
    global input_data
    data = request.get_json()
    input_data["feedBtn"] = data.get('feedBtn')
    input_data["touchBtn"] = data.get('touchBtn')
    input_data["isNear"] = data.get('isNear')
    input_data["washBtn"] = data.get('washBtn')
    return '', 204

if __name__ == "__main__":
    app.run(debug=True)