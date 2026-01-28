from flask import Flask,request,jsonify
from models.task import Task

app = Flask(__name__)

tasks = []
task_id_control = 1

@app.route("/tasks",methods=['POST'])
def create_task():
    global task_id_control
    data = request.get_json()
    new_task = Task(id=task_id_control,title=data["title"],description=data.get("description", ""))
    task_id_control+=1
    tasks.append(new_task)

    return jsonify({"message":"New task created"})


@app.route("/tasks",methods=["GET"])
def get_tasks():
    return jsonify({"tasks":[task.to_dict() for task in tasks],"total_tasks": len(tasks)})


@app.route("/tasks/<int:id>",methods=["GET"])
def retriave_task(id):
    for task in tasks:
        if task.id == id:
            return jsonify(task.to_dict())

    return jsonify({"message":"task not found"},404)


@app.route("/tasks/<int:id>",methods=["PUT"])
def update_task(id):
    task = None
    for t in tasks:
        if t.id == id:
            task= t

    if task == None:
        return jsonify({"message":"task not found"},404)
    
    data = request.get_json()
    task.title = data["title"]
    task.description = data["description"]
    task.completed = data["completed"]

    return jsonify({"message": "task updated successfully"})



if __name__ == "__main__":
    app.run(debug=True)