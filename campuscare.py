from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = "supersecretkey"

# In-memory storage
admins = {"admin": "admin123"}
students = {}
teachers = {}

# ------------------ ROUTES ------------------

@app.route("/")
def home():
    return render_template("index.html")

# ------------------ ADMIN LOGIN ------------------

@app.route("/admin_login", methods=["GET", "POST"])
def admin_login():
    error = None
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if admins.get(username) == password:
            session["user"] = "admin"
            return redirect(url_for("admin_dashboard"))
        else:
            error = "Invalid credentials"

    return render_template("admin_login.html", error=error)


@app.route("/admin_dashboard")
def admin_dashboard():
    if session.get("user") != "admin":
        return redirect(url_for("admin_login"))
    return render_template("admin_dashboard.html",
                           students=students,
                           teachers=teachers)

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))

# ------------------ STUDENT REGISTRATION ------------------

@app.route("/register_student", methods=["GET", "POST"])
def register_student():
    if request.method == "POST":
        student_id = request.form.get("student_id")
        name = request.form.get("name")
        section = request.form.get("section")
        department = request.form.get("department")

        students[student_id] = {
            "id": student_id,
            "name": name,
            "section": section,
            "department": department,
            "role": "student"
        }

        return redirect(url_for("update_health_page",
                                role="student",
                                user_id=student_id))

    return render_template("register_student.html")

# ------------------ TEACHER REGISTRATION ------------------

@app.route("/register_teacher", methods=["GET", "POST"])
def register_teacher():
    if request.method == "POST":
        teacher_id = request.form.get("teacher_id")
        name = request.form.get("name")
        department = request.form.get("department")

        teachers[teacher_id] = {
            "id": teacher_id,
            "name": name,
            "department": department,
            "role": "teacher"
        }

        return redirect(url_for("update_health_page",
                                role="teacher",
                                user_id=teacher_id))

    return render_template("register_teacher.html")


# ------------------ HEALTH UPDATE PAGE ------------------

@app.route("/update_health/<role>/<user_id>", methods=["GET", "POST"])
def update_health_page(role, user_id):
    if role == "student":
        user = students.get(user_id)
    elif role == "teacher":
        user = teachers.get(user_id)
    else:
        return "<h3>Invalid role</h3>"

    if not user:
        return f"<h3>{role.capitalize()} not found</h3>"

    if request.method == "POST":
        # Save health info
        user["temperature"] = request.form.get("temperature")
        user["symptoms"] = request.form.get("symptoms")

        # Calculate health status
        try:
            temp = float(user["temperature"])
        except:
            temp = 0

        if temp < 37.5:
            status = "SAFE"
            status_class = "safe"
            desc = "Normal temperature. Good job staying healthy!"
        elif 37.5 <= temp <= 38.0:
            status = "MONITOR"
            status_class = "monitor"
            desc = "Slightly elevated. Monitor your condition."
        else:
            status = "HIGH TEMPERATURE"
            status_class = "high"
            desc = "High temperature detected. Seek medical assistance."

        return render_template("update_health_status.html",
                               user=user,
                               health_status=status,
                               health_status_class=status_class,
                               health_status_desc=desc)

    return render_template("update_health_status.html", user=user)


# ------------------ RUN APP ------------------

if __name__ == "__main__":
    app.run(debug=True)
