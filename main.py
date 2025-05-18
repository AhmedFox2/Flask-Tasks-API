from flask import Flask, request
from flask_restful import Resource, Api
import json
import os

app = Flask(__name__)
api = Api(app)

python_file = os.path.dirname(__file__)

# قاعدة بيانات وهمية في الذاكرة

def load_json_file():
    with open(f"{python_file}/tasks.json","r") as f:
         return json.load(f)

def save_json_file(data):
    with open(f"{python_file}/tasks.json","w") as f:
         json.dump(data,f,indent=4)

tasks = load_json_file()

class Main(Resource):
    def get(self):
        return {"message": "Welcome"}, 200

# المورد الأساسي
class Task(Resource):
    def get(self, task_id):
        if task_id in tasks:
            return tasks[task_id], 200
        return {"message": "Not Found"}, 404

    def delete(self, task_id):
        if task_id in tasks:
            del tasks[task_id]
            return {"message": "Deleted"}, 200
        return {"message": "Not Found"}, 404

# مورد للكل
class TaskList(Resource):
    def get(self):
        return tasks

    def post(self):
        data = request.get_json()
        task_id = max(tasks.keys(), default=0) + 1
        tasks[task_id] = {
            "title": data.get("title", f"مهمة {task_id}"),
            "done": data.get("done", False)
        }
        return tasks[task_id], 201

class TaskAddByQuery(Resource):
    def get(self):
        title = request.args.get("title", "مهمة بدون عنوان")
        done = request.args.get("done", "false").lower() == "true"

        # توليد رقم تلقائي للمهمة
        task_id = max(map(int, tasks.keys()), default=0) + 1

        tasks[task_id] = {
            "title": title,
            "done": done
        }

        save_json_file(tasks)
        return {
            "message": "The task has been added",
            "task_id": task_id,
            "task": tasks[task_id]
        }, 201


# ربط الموارد بالروابط
api.add_resource(TaskList, '/tasks')
api.add_resource(TaskAddByQuery, '/tasks/add')
api.add_resource(Task, '/tasks/<int:task_id>')
api.add_resource(Main, '/')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000,debug=True)
