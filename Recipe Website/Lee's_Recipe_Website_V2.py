from flask import Flask, render_template, redirect, url_for, session
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///recipe.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "uh3981h89w"
app.debug = True
db = SQLAlchemy(app)

class RegularUser(db.Model):
    __tablename__ = 'regular_users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60))
    email = db.Column(db.String(35))
    username = db.Column(db.String(16))
    password = db.Column(db.String(16))
    def __repr__(self):
        return "{0} - email:{1}, username: {2}, password: {3}".format(self.name, self.email, self.username, self.password)

class ChefUser(db.Model):
    __tablename__ = 'chef_users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60))
    email = db.Column(db.String(35))
    number_of_recipes = db.Column(db.Integer)
    number_of_courses = db.Column(db.Integer)
    username = db.Column(db.String(16))
    password = db.Column(db.String(16))

    recipes = db.relationship("ChefRecipe", back_populates='chef')
    courses = db.relationship("ChefCourse", back_populates="chef")


    def __repr__(self):
        return "{0} - email:{1}, recipes: {2}, courses: {3}, username: {4}, password: {5}".format(self.name, self.email, self.number_of_recipes, self.number_of_courses, self.username, self.password)

class Admin(db.Model):
    __tablename__ = 'admin'
    id = db.Column(db.Integer, primary_key=True)
    number_of_visits = db.Column(db.Integer)
    number_of_registered = db.Column(db.Integer)
    number_of_chefs = db.Column(db.Integer)
    number_of_recipes = db.Column(db.Integer)
    number_of_chef_recipes = db.Column(db.Integer)
    number_of_courses = db.Column(db.Integer)
    def __repr__(self):
        return "visits: {0}, registered: {1}, chefs: {2}, recipes: {3}, chef recipes: {4}, courses:{5}".format(self.number_of_visits, self.number_of_registered, self.number_of_chefs, self.number_of_recipes, self.number_of_chef_recipes, self.number_of_courses)

class Lee_Recipe(db.Model):
    __tablename__ = 'lee_recipe'
    id = db.Column(db.Integer, primary_key=True)
    recipe_type = db.Column(db.String(7))
    recipe_name = db.Column(db.String(40))
    recipe_description = db.Column(db.String(200))
    recipe_instructions = db.Column(db.String(5000)) 
    recipe_image = db.Column(db.String(200))
    def __repr__(self):
        return "{0} - type:{1}, description:{2}, image url={3}".format(self.recipe_name, self.recipe_type, self.recipe_description, self.recipe_image)

class ChefRecipe(db.Model):
    __tablename__ = 'chef_recipe'
    id = db.Column(db.Integer, primary_key=True)
    recipe_type = db.Column(db.String(7))
    recipe_name = db.Column(db.String(40))
    recipe_description = db.Column(db.String(200))
    recipe_instructions = db.Column(db.String(5000)) 
    recipe_image = db.Column(db.String(100))
    recipe_likes = db.Column(db.Integer)
    chef_id = db.Column(db.ForeignKey("chef_users.id"))

    chef = db.relationship("ChefUser", back_populates='recipes')

    def __repr__(self):
        return "{0} - type:{1}, description:{2}, image_url:{3}, likes:{4}, chef id: {5}".format(self.recipe_name, self.recipe_type, self.recipe_description, self.recipe_image, self.recipe_likes, self.chef_id)

class ChefCourse(db.Model):
    __tablename__ = 'chef_course'
    id = db.Column(db.Integer, primary_key=True)
    course_name = db.Column(db.String(40))
    course_description = db.Column(db.String(200))
    course_image = db.Column(db.String(100))
    starter_1_id = db.Column(db.ForeignKey("chef_recipe.id"))
    starter_2_id = db.Column(db.ForeignKey("chef_recipe.id"))
    starter_3_id = db.Column(db.ForeignKey("chef_recipe.id"))
    main_1_id = db.Column(db.ForeignKey("chef_recipe.id"))
    main_2_id = db.Column(db.ForeignKey("chef_recipe.id"))
    main_3_id = db.Column(db.ForeignKey("chef_recipe.id"))
    dessert_1_id = db.Column(db.ForeignKey("chef_recipe.id"))
    dessert_2_id = db.Column(db.ForeignKey("chef_recipe.id"))
    dessert_3_id = db.Column(db.ForeignKey("chef_recipe.id"))

    chef_id = db.Column(db.ForeignKey("chef_users.id"))
    chef = db.relationship("ChefUser", back_populates='courses')

    def __repr__(self):
        return "{0} - recipe description:{1}, image_url:{2}, chef id: {3}".format(self.recipe_name, self.recipe_description, self.recipe_image, self.chef_id)

class LoginForm(FlaskForm):
    username = StringField("Username")
    password = PasswordField("Password")
    submit = SubmitField("Log in")

class RegisterForm(FlaskForm):
    name = StringField("Name")
    email = StringField("Email")
    membership_type = StringField("Membership Type")
    username = StringField("Username")
    password = PasswordField("Password")
    repeat_password = PasswordField("Reenter Password")
    submit = SubmitField("Sign up")

class AdminCreateRecipeForm(FlaskForm):
    recipe_type = StringField("Recipe Type")
    recipe_name = StringField("Name")
    recipe_description = StringField("Recipe Description")
    recipe_instructions = StringField("Recipe Instructions")
    recipe_image = StringField("Image URL")
    submit = SubmitField("Create Recipe")

class ChefCreateRecipeForm(FlaskForm):
    recipe_type = StringField("Recipe Type")
    recipe_name = StringField("Name")
    recipe_description = StringField("Recipe Description")
    recipe_instructions = StringField("Recipe Instructions")
    recipe_image = StringField("Image URL")
    submit = SubmitField("Create Recipe")

class ChefCreateCourseForm(FlaskForm):
    course_name = StringField("Course Name")
    course_description = StringField("Course Description")
    course_image = StringField("Image URL")
    starter_1_name = StringField("Starter 1")
    starter_2_name = StringField("Starter 2")
    starter_3_name = StringField("Starter 3")
    main_1_name = StringField("Main 1")
    main_2_name = StringField("Main 2")
    main_3_name = StringField("Main 3")
    dessert_1_name = StringField("Dessert 1")
    dessert_2_name = StringField("Dessert 2")
    dessert_3_name = StringField("Dessert 3")

    submit = SubmitField("Create Course")

class LikeRecipe(FlaskForm):
    like = SubmitField("Like Recipe")

class DeleteRecipe(FlaskForm):
    delete = SubmitField("Delete Recipe")

admin = Admin(number_of_visits = 0, number_of_registered = 0, number_of_chefs = 0, number_of_recipes = 0, number_of_chef_recipes=0, number_of_courses = 0)
db.session.add(admin)
db.session.commit()

#Unregistered#
#----------------------------------------#
@app.route("/")
def welcome():
    old_admin = Admin.query.first()
    old_admin.number_of_visits += 1
    db.session.commit()
    return render_template("Welcome.html")

@app.route("/about_us")
def about_us():
    return render_template("About_us.html")

@app.route("/starters")
def lee_starters():
    posts =  Lee_Recipe.query.filter_by(recipe_type="starter").all()
    return render_template("Starters.html", posts=posts)

@app.route("/lee_mains")
def lee_mains():
    posts =  Lee_Recipe.query.filter_by(recipe_type="main").all()
    return render_template("Mains.html", posts=posts)

@app.route("/lee_desserts")
def lee_desserts():
    posts =  Lee_Recipe.query.filter_by(recipe_type="dessert").all()
    return render_template("Desserts.html", posts=posts)

@app.route("/recipe/<recipe_id>")
def recipe(recipe_id):
    recipe_to_display = Lee_Recipe.query.filter_by(id=recipe_id).first()
    return render_template("Recipe.html", recipe_to_display=recipe_to_display)

@app.route("/signup", methods=["GET", "POST"])
def signup():
    form = RegisterForm()
    usernames_list = []
    emails_list = []
    if form.is_submitted():
        name = form.name.data
        email = form.email.data
        membership_type = form.membership_type.data
        username = form.username.data
        password = form.password.data
        repeat_password = form.repeat_password.data
        regular_users = RegularUser.query.all()
        for user in regular_users:
            usernames_list.append(user.username)
            emails_list.append(user.email)
        chef_users = ChefUser.query.all()
        for user in chef_users:
            usernames_list.append(user.username)
            emails_list.append(user.email)
        if username not in usernames_list and email not in emails_list and (membership_type.lower()=="regular" or membership_type.lower()=="chef"):        
            if password == repeat_password:
                old_admin = Admin.query.first()
                old_admin.number_of_registered += 1
                db.session.commit()
                if membership_type.lower()=="regular":
                    new_user = RegularUser(name=name, email=email, username=username, password=password)
                    db.session.add(new_user)
                    db.session.commit()
                    return redirect(url_for("login"))
                elif membership_type.lower()=="chef":
                    old_admin = Admin.query.first()
                    old_admin.number_of_chefs += 1
                    db.session.commit()
                    new_user = ChefUser(name=name, email=email, number_of_recipes=0, number_of_courses=0, username=username, password=password)
                    db.session.add(new_user)
                    db.session.commit()
                    return redirect(url_for("login"))
            else:
                return render_template("Sign_up.html", form=form)
        else:
            return render_template("Sign_up.html", form=form)
    else:
        return render_template("Sign_up.html", form=form)

@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.is_submitted():
        username = form.username.data
        password = form.password.data
        if username=="admin" and password=="admin_control":
                return redirect(url_for("admin_home"))
        else:
            user = RegularUser.query.filter_by(username=username, password=password).first()
            if user != None:
                session["user"] = user.id
                return redirect(url_for("member_welcome"))
            else:
                user = ChefUser.query.filter_by(username=username, password=password).first()
                if user != None:
                    session["user"] = user.id
                    return redirect(url_for("chef_home"))
                else:
                    return render_template("Login.html", form=form)
    else:
        return render_template("Login.html", form=form)


#Registered Member#
#----------------------------------------#
@app.route("/member_welcome")
def member_welcome():
    user_id = session.get("user", -1)
    user = RegularUser.query.filter_by(id=user_id).first()

    starters = ChefRecipe.query.filter_by(recipe_type="starter").all()
    if len(starters) <= 0:
        starter_with_most_likes = ChefRecipe(recipe_type="starter", recipe_name = "You have no starters", recipe_description = "No Description", recipe_instructions = "No instructions", recipe_image = "no image", recipe_likes = -1, chef_id = 0)
    else:
        starter_with_most_likes = ChefRecipe.query.filter_by(recipe_type="starter").first()
        for starter in starters:
            if starter.recipe_likes > starter_with_most_likes.recipe_likes:
                starter_with_most_likes = starter

    mains = ChefRecipe.query.filter_by(recipe_type="main").all()
    if len(mains) <= 0:
        main_with_most_likes = ChefRecipe(recipe_type="main", recipe_name = "You have no mains", recipe_description = "No Description", recipe_instructions = "No instructions", recipe_image = "no image", recipe_likes = -1, chef_id = 0)
    else:
        main_with_most_likes = ChefRecipe.query.filter_by(recipe_type="main").first()
        for main in mains:
            if main.recipe_likes > main_with_most_likes.recipe_likes:
                main_with_most_likes = main

    desserts = ChefRecipe.query.filter_by(recipe_type="dessert").all()
    if len(desserts) <= 0:
        dessert_with_most_likes = ChefRecipe(recipe_type="dessert", recipe_name = "There are no desserts", recipe_description = "No Description", recipe_instructions = "No instructions", recipe_image = "no image", recipe_likes = -1, chef_id = 0)
    else:
        dessert_with_most_likes = ChefRecipe.query.filter_by(recipe_type="dessert").first()
        for dessert in desserts:
            if dessert.recipe_likes > dessert_with_most_likes.recipe_likes:
                dessert_with_most_likes = dessert


    return render_template("Member_welcome.html", user=user, best_starter=starter_with_most_likes, best_main=main_with_most_likes, best_dessert=dessert_with_most_likes)

@app.route("/courses")
def courses():
    courses = ChefCourse.query.all() 
    return render_template("Courses.html", courses=courses)

@app.route("/course/<course_id>")
def course(course_id):
    course = ChefCourse.query.filter_by(id=course_id).first()
    starter_1=ChefRecipe.query.filter_by(id=course.starter_1_id).first()
    starter_2=ChefRecipe.query.filter_by(id=course.starter_2_id).first()
    starter_3=ChefRecipe.query.filter_by(id=course.starter_3_id).first()
    main_1=ChefRecipe.query.filter_by(id=course.main_1_id).first()
    main_2=ChefRecipe.query.filter_by(id=course.main_2_id).first()
    main_3=ChefRecipe.query.filter_by(id=course.main_3_id).first()
    dessert_1=ChefRecipe.query.filter_by(id=course.dessert_1_id).first()
    dessert_2=ChefRecipe.query.filter_by(id=course.dessert_2_id).first()
    dessert_3=ChefRecipe.query.filter_by(id=course.dessert_3_id).first()
    return render_template("Course.html", course=course, starter_1=starter_1, starter_2=starter_2, starter_3=starter_3, main_1=main_1, main_2=main_2, main_3=main_3, dessert_1=dessert_1, dessert_2=dessert_2, dessert_3=dessert_3)

@app.route("/member_starters")
def member_starters():
    posts =  ChefRecipe.query.filter_by(recipe_type="starter").all()
    return render_template("Member_Starters.html", posts=posts)

@app.route("/membermains")
def member_mains():
    posts =  ChefRecipe.query.filter_by(recipe_type="main").all()
    return render_template("Member_Mains.html", posts=posts)

@app.route("/member_desserts")
def member_desserts():
    posts =  ChefRecipe.query.filter_by(recipe_type="dessert").all()
    return render_template("Member_Desserts.html", posts=posts)

@app.route("/member_recipe/<recipe_id>", methods=["GET", "POST"])
def member_recipe(recipe_id):
    form=LikeRecipe()
    if form.is_submitted():
        old_recipe = ChefRecipe.query.filter_by(id=recipe_id).first()
        old_recipe.recipe_likes += 1
        db.session.commit()
    recipe_to_display = ChefRecipe.query.filter_by(id=recipe_id).first()
    chef = ChefUser.query.filter_by(id=recipe_to_display.chef_id).first()
    return render_template("Member_Recipe.html", recipe_to_display=recipe_to_display, chef_name=chef.name, form=form)
    

#Chef#
#----------------------------------------#
@app.route("/chef_home")
def chef_home():
    user_id = session.get("user", -1)
    user = ChefUser.query.filter_by(id=user_id).first()

    starters = ChefRecipe.query.filter_by(recipe_type="starter", chef_id=user.id).all()
    if len(starters) <= 0:
        starter_with_most_likes = ChefRecipe(recipe_type="starter", recipe_name = "You have no starters", recipe_description = "No Description", recipe_instructions = "No instructions", recipe_image = "no image", recipe_likes = -1, chef_id = user.id)
    else:
        starter_with_most_likes = ChefRecipe.query.filter_by(recipe_type="starter", chef_id=user.id).first()
        for starter in starters:
            if starter.recipe_likes > starter_with_most_likes.recipe_likes:
                starter_with_most_likes = starter

    mains = ChefRecipe.query.filter_by(recipe_type="main", chef_id=user.id).all()
    if len(mains) <= 0:
        main_with_most_likes = ChefRecipe(recipe_type="main", recipe_name = "You have no mains", recipe_description = "No Description", recipe_instructions = "No instructions", recipe_image = "no image", recipe_likes = -1, chef_id = user.id)
    else:
        main_with_most_likes = ChefRecipe.query.filter_by(recipe_type="main", chef_id=user.id).first()
        for main in mains:
            if main.recipe_likes > main_with_most_likes.recipe_likes:
                main_with_most_likes = main

    desserts = ChefRecipe.query.filter_by(recipe_type="dessert", chef_id=user.id).all()
    if len(desserts) <= 0:
        dessert_with_most_likes = ChefRecipe(recipe_type="dessert", recipe_name = "You have no desserts", recipe_description = "No Description", recipe_instructions = "No instructions", recipe_image = "no image", recipe_likes = -1, chef_id = user.id)
    else:
        dessert_with_most_likes = ChefRecipe.query.filter_by(recipe_type="dessert", chef_id=user.id).first()
        for dessert in desserts:
            if dessert.recipe_likes > dessert_with_most_likes.recipe_likes:
                dessert_with_most_likes = dessert

    return render_template("Chef_Home.html", user=user, best_starter=starter_with_most_likes, best_main=main_with_most_likes, best_dessert=dessert_with_most_likes)

@app.route("/chef_recipes")
def chef_recipes():
    recipes = ChefRecipe.query.filter_by(chef_id=session.get("user", -1)).all()
    return render_template("Chef_Recipes.html", recipes=recipes)

@app.route("/chef_courses")
def chef_courses():
    courses = ChefCourse.query.filter_by(chef_id=session.get("user", -1)).all()
    return render_template("Chef_Courses.html", courses=courses)    

@app.route("/chef_create_recipe", methods=["GET", "POST"])
def chef_create_recipe():
    form=ChefCreateRecipeForm()
    if form.is_submitted():
        recipe_type = form.recipe_type.data
        recipe_name = form.recipe_name.data
        recipe_description = form.recipe_description.data
        recipe_instructions = form.recipe_instructions.data
        recipe_image = form.recipe_image.data
        if recipe_type.lower()=="starter" or recipe_type.lower()=="main" or recipe_type.lower()=="dessert":
            new_recipe = ChefRecipe(recipe_type=recipe_type.lower(), recipe_name=recipe_name.title(), recipe_description=recipe_description, recipe_instructions=recipe_instructions, recipe_image=recipe_image, recipe_likes=0, chef_id=session.get("user", -1))
            db.session.add(new_recipe)
            db.session.commit()
            old_admin = Admin.query.first()
            old_admin.number_of_recipes += 1
            old_admin.number_of_chef_recipes += 1
            db.session.commit()
            return redirect(url_for("chef_home"))
        else:
            return render_template("Chef_Create_Recipe.html", form=form)
        
    else:
        return render_template("Chef_Create_Recipe.html", form=form)
    
@app.route("/chef_create_course", methods=["GET", "POST"])
def chef_create_course():
    form=ChefCreateCourseForm()
    user_id = session.get("user", -1)
    if form.is_submitted():
        course_name = form.course_name.data
        course_description = form.course_description.data
        course_image = form.course_image.data
        starter_1_name = form.starter_1_name.data
        starter_2_name = form.starter_2_name.data
        starter_3_name = form.starter_3_name.data
        main_1_name = form.main_1_name.data
        main_2_name = form.main_2_name.data
        main_3_name = form.main_3_name.data
        dessert_1_name = form.dessert_1_name.data
        dessert_2_name = form.dessert_2_name.data
        dessert_3_name = form.dessert_3_name.data
        if (starter_1_name!=starter_2_name and starter_1_name!=starter_3_name and starter_2_name!=starter_3_name) and (main_1_name!=main_2_name and main_1_name!=main_3_name and main_2_name!=main_3_name) and (dessert_1_name!=dessert_2_name and dessert_1_name!=dessert_3_name and dessert_2_name!=dessert_3_name):
            try:
                starter_1 = ChefRecipe.query.filter_by(chef_id=user_id, recipe_type="starter", recipe_name=starter_1_name.title()).one()
                starter_2 = ChefRecipe.query.filter_by(chef_id=user_id, recipe_type="starter", recipe_name=starter_2_name.title()).one()
                starter_3 = ChefRecipe.query.filter_by(chef_id=user_id, recipe_type="starter", recipe_name=starter_3_name.title()).one()
                main_1 = ChefRecipe.query.filter_by(chef_id=user_id, recipe_type="main", recipe_name=main_1_name.title()).one()
                main_2 = ChefRecipe.query.filter_by(chef_id=user_id, recipe_type="main", recipe_name=main_2_name.title()).one()
                main_3 = ChefRecipe.query.filter_by(chef_id=user_id, recipe_type="main", recipe_name=main_3_name.title()).one()
                dessert_1 = ChefRecipe.query.filter_by(chef_id=user_id, recipe_type="dessert", recipe_name=dessert_1_name.title()).one()
                dessert_2 = ChefRecipe.query.filter_by(chef_id=user_id, recipe_type="dessert", recipe_name=dessert_2_name.title()).one()
                dessert_3 = ChefRecipe.query.filter_by(chef_id=user_id, recipe_type="dessert", recipe_name=dessert_3_name.title()).one()
                new_course = ChefCourse(course_name=course_name, course_description=course_description, course_image=course_image, starter_1_id=starter_1.id, starter_2_id=starter_2.id, starter_3_id=starter_3.id, main_1_id=main_1.id, main_2_id=main_2.id, main_3_id=main_3.id, dessert_1_id=dessert_1.id, dessert_2_id=dessert_2.id, dessert_3_id=dessert_3.id, chef_id=user_id)
                db.session.add(new_course)
                db.session.commit()
                old_admin = Admin.query.first()
                old_admin.number_of_courses += 1
                old_admin.number_of_chef_courses += 1
                db.session.commit()
                return redirect(url_for("chef_home"))
            except:
                return render_template("Chef_Create_Course.html", form=form)
        else:
            return render_template("Chef_Create_Course.html", form=form)
    else:
        return render_template("Chef_Create_Course.html", form=form)

@app.route("/chef_recipe/<recipe_id>", methods=["GET", "POST"])
def chef_recipe(recipe_id):
    form=DeleteRecipe()
    user_id = session.get("user", -1)
    if form.is_submitted():
        ChefRecipe.query.filter_by(id=recipe_id).delete()
        db.session.commit()
        old_admin = Admin.query.first()
        old_admin.number_of_recipes -= 1
        old_admin.number_of_chef_recipes -= 1
        db.session.commit()
        return redirect(url_for("chef_home"))
        
    else:
        chef = ChefUser.query.filter_by(id=user_id).first()
        recipe_to_display = ChefRecipe.query.filter_by(id=recipe_id).first()
        return render_template("Chef_Recipe.html", recipe_to_display=recipe_to_display, chef=chef, form=form)
    
@app.route("/chef_course/<course_id>") 
def chef_course(course_id):
    user_id = session.get("user", -1)
    course = ChefCourse.query.filter_by(id=course_id).first()
    starter_1=ChefRecipe.query.filter_by(id=course.starter_1_id).first()
    starter_2=ChefRecipe.query.filter_by(id=course.starter_2_id).first()
    starter_3=ChefRecipe.query.filter_by(id=course.starter_3_id).first()
    main_1=ChefRecipe.query.filter_by(id=course.main_1_id).first()
    main_2=ChefRecipe.query.filter_by(id=course.main_2_id).first()
    main_3=ChefRecipe.query.filter_by(id=course.main_3_id).first()
    dessert_1=ChefRecipe.query.filter_by(id=course.dessert_1_id).first()
    dessert_2=ChefRecipe.query.filter_by(id=course.dessert_2_id).first()
    dessert_3=ChefRecipe.query.filter_by(id=course.dessert_3_id).first()
    return render_template("Chef_Course.html", course=course, starter_1=starter_1, starter_2=starter_2, starter_3=starter_3, main_1=main_1, main_2=main_2, main_3=main_3, dessert_1=dessert_1, dessert_2=dessert_2, dessert_3=dessert_3)


#Admin#
#----------------------------------------#
@app.route("/admin_home")
def admin_home():
    data = Admin.query.first()
    return render_template("Admin.html", data=data)

@app.route("/create_recipe", methods=["GET", "POST"])
def create_recipe():
    form = AdminCreateRecipeForm()
    if form.is_submitted():
        recipe_type = form.recipe_type.data
        recipe_name = form.recipe_name.data
        recipe_description = form.recipe_description.data
        recipe_instructions = form.recipe_instructions.data
        recipe_image = form.recipe_image.data
        if recipe_type.lower()=="starter" or recipe_type.lower()=="main" or recipe_type.lower()=="dessert":
            new_recipe = Lee_Recipe(recipe_type=recipe_type.lower(), recipe_name=recipe_name.title(), recipe_description=recipe_description, recipe_instructions=recipe_instructions, recipe_image=recipe_image)
            db.session.add(new_recipe)
            db.session.commit()
            old_admin = Admin.query.first()
            old_admin.number_of_recipes += 1
            db.session.commit()
            return redirect(url_for("admin_home"))
        else:
            return render_template("Admin_Create_Recipe.html", form=form)
    else:
        return render_template("Admin_Create_Recipe.html", form=form)


#Common
#----------------------------------------#
@app.route("/logout", methods=["GET", "POST"])
def logout():
    try:
        del session["user"]
    except:
        pass
    return redirect(url_for("welcome"))


if __name__ == "__main__":
    app.run()