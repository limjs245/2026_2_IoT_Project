from flask import Flask, render_template, jsonify

app = Flask(__name__)

input_data = {
    "feedBtn": False,
    "touchBtn": False,
    "isNear": False
}

@app.route("/")
def defaultPet():
    return render_template("index.html", name = "Raspberry")

@app.route("/pet/<pet_name>")
def newPet(pet_name):
    if (pet_name is None):
        pet_name = "Raspberry"
    return render_template("index.html", name = pet_name)

@app.route('/get_input', methods=['GET'])
def get_input():
    global input_data
    response_data = {
        "status": "success",
        "feedBtn": input_data["feedBtn"],
        "touchBtn": input_data["touchBtn"],
        "isNear": input_data["isNear"]
    }
    input_data["feedBtn"] = False
    input_data["touchBtn"] = False
    return jsonify(response_data)

if __name__ == "__main__":
    app.run(debug=True)