import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime

Base = declarative_base()
engine = create_engine('sqlite:///recipe.db', echo=True)
Session = sessionmaker(bind=engine)

class RegularUser(Base):
    __tablename__ = 'regular_users'
    id = Column(Integer, primary_key=True)
    name = Column(String(60))
    email = Column(String(35))
    username = Column(String(16))
    password = Column(String(16))
    def __repr__(self):
        return "{0} - email:{1}, username: {2}, password: {3}".format(self.realname, self.email, self.username, self.password)

class ChefUser(Base):
    __tablename__ = 'chef_users'
    id = Column(Integer, primary_key=True)
    name = Column(String(60))
    email = Column(String(35))
    number_of_recipes = Column(Integer)
    number_of_courses = Column(Integer)
    username = Column(String(16))
    password = Column(String(16))

    recipes = relationship("ChefRecipe", back_populates="chef")
    courses = relationship("ChefCourse", back_populates="chef")

    def __repr__(self):
        return "{0} - email:{1}, recipes: {2}, courses: {3}, username: {4}, password: {5}".format(self.realname, self.email, self.number_of_recipes, self.number_of_courses, self.username, self.password)

class Admin(Base):
    __tablename__ = 'admin'
    id = Column(Integer, primary_key=True)
    number_of_visits = Column(Integer)
    number_of_registered = Column(Integer)
    number_of_chefs = Column(Integer)
    number_of_recipes = Column(Integer)
    number_of_chef_recipes = Column(Integer)
    number_of_courses = Column(Integer)
    def __repr__(self):
        return "visits: {0}, registered: {1}, chefs: {2}, recipes: {3}, chef recipes: {4}, courses:{5}".format(self.number_of_visits, self.number_of_registered, self.number_of_chefs, self.number_of_recipes, self.number_of_chef_recipes, self.number_of_courses)

class Lee_Recipe(Base):
    __tablename__ = 'lee_recipe'
    id = Column(Integer, primary_key=True)
    recipe_type = Column(String(7))
    recipe_name = Column(String(40))
    recipe_description = Column(String(200))
    recipe_instructions = Column(String(5000)) 
    recipe_image = Column(String(100))
    def __repr__(self):
        return "{0} - type:{1}, description:{2}, image_url:{3}".format(self.recipe_name, self.recipe_type, self.recipe_description, self.recipe_image)

class ChefRecipe(Base):
    __tablename__ = 'chef_recipe'
    id = Column(Integer, primary_key=True)
    recipe_type = Column(String(7))
    recipe_name = Column(String(40))
    recipe_description = Column(String(200))
    recipe_instructions = Column(String(5000)) 
    recipe_image = Column(String(100))
    recipe_likes = Column(Integer)
    chef_id = Column(ForeignKey("chef_users.id"))

    chef = relationship("ChefUser", back_populates='recipes')

    def __repr__(self):
        return "{0} - type:{1}, description:{2}, image_url:{3}, likes:{4}, chef id: {5}".format(self.recipe_name, self.recipe_type, self.recipe_description, self.recipe_image, self.recipe_likes, self.chef_id)

class ChefCourse(Base):
    __tablename__ = 'chef_course'
    id = Column(Integer, primary_key=True)
    course_name = Column(String(40))
    course_description = Column(String(200))
    course_image = Column(String(100))
    starter_1_id = Column(ForeignKey("chef_recipe.id"))
    starter_2_id = Column(ForeignKey("chef_recipe.id"))
    starter_3_id = Column(ForeignKey("chef_recipe.id"))
    main_1_id = Column(ForeignKey("chef_recipe.id"))
    main_2_id = Column(ForeignKey("chef_recipe.id"))
    main_3_id = Column(ForeignKey("chef_recipe.id"))
    dessert_1_id = Column(ForeignKey("chef_recipe.id"))
    dessert_2_id = Column(ForeignKey("chef_recipe.id"))
    dessert_3_id = Column(ForeignKey("chef_recipe.id"))

    chef_id = Column(ForeignKey("chef_users.id"))
    chef = relationship("ChefUser", back_populates='courses')

    def __repr__(self):
        return "{0} - recipe description:{1}, image_url:{2}, chef id: {3}".format(self.recipe_name, self.recipe_description, self.recipe_image, self.chef_id)

if __name__ == "__main__":  
    Base.metadata.create_all(engine)
    session = Session()
    session.commit()