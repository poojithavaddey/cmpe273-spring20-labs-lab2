from flask import Flask, escape, request, jsonify, abort

app = Flask(__name__)
DB  =   {
    "students":[
        {
            "first_name" : "Mark",
            "last_name"  : "Justin",
            "student_id" : 110,
            "course"     : "CMPE273"
         },
         {
            "first_name" : "Sean",
            "last_name"  : "Paul",
            "student_id" : 111,
            "course"     : "CMPE273"
         }
    ],
    "classes" :[
        {
            "class_name" : "CMPE273",
            "class_id"   :  273,
            "instructor" : "Sithu Aung"
        },
        {
            "class_name" : "CMPE272",
            "class_id"   : 272,
            "instructor" : "Rakesh"
        }
    ]
}

@app.route('/')
def hello():
    name = request.args.get("name", "World")
    return f'Hello, {escape(name)}!'


#POST student
@app.route('/students', methods=['POST'])
def create_student():
    data = request.get_json()  
    student = {
            "first_name" : data['first_name'],
            "last_name"  : data['last_name'],
            "student_id" : data['student_id'],
            "course"     : data['course']
        }
    DB['students'].append(student)
    return jsonify({"student" : DB['students']})
    

#GET student ID
@app.route('/students', methods=['GET'])
def get_student():
    if not request.args.get('stu_id'):
        abort(400)
    else:
        student = [stud for stud in DB['students'] if stud["student_id"]== int(request.args.get('stu_id'))]
        return jsonify({"student":student})


#POST classes
@app.route('/classes', methods=['POST'])
def create_class():
    data = request.get_json()
    class_ = {
            "class_name" : data["class_name"],
            "class_id"  : data["class_id"],
            "instructor" : data["instructor"]
        }
    DB['classes'].append(class_)
    return jsonify({"class" : DB['classes']}),201

#GET classes ID
@app.route('/classes', methods=['GET'])
def get_class():  
    if not request.args.get('class_id'):
        abort(400)
    else:
        class_ = [class_ for class_ in DB['classes'] if class_["class_id"]== int(request.args.get('class_id'))]
    return jsonify({"class":class_})


#PATCH class id
@app.route('/classes/<class_id>', methods=['PATCH'])
def patch_class(class_id):
    data = request.get_json()
    class_id = int(request.view_args['class_id'])
    print(class_id)
    student = [stud for stud in DB['students'] if stud["student_id"]== int(data["student_id"])]
    print(student)
    #ind = [i for i,cla in enumerate(DB['classes']) if cla["class_id"]== class_id]
    for i,cla in enumerate(DB['classes']):
        if cla["class_id"]== class_id :
            ind = i 
    
    if "students" in  DB['classes'][ind]:
        for stud in DB['classes'][ind]['students']:
            if stud['student_id'] == int(data["student_id"]):
                return "Student already exists"    
        DB['classes'][ind]['students'].extend(student)
    else:
        DB["classes"][ind].update({'students': student})

    
    return jsonify({"Class" : DB['classes']})
