from django.test import TestCase
from planner.models import Project, Category, Task
from django.contrib.auth import get_user_model

class TestModels(TestCase):

    def create_dummy_user(self):
        User = get_user_model()
        user = User.objects.create_user('binsea', 'binsea@binsea.com', 'binseaPassword')
        return user 

    def create_dummy_project(self, user):
        project_instance = Project.objects.create(title='new project', creator = user)
        return project_instance

    def create_dummy_category(self, project):
        category_instance = Category.objects.create(category_name='new category', project = project)
        return category_instance

    def test_project_model(self):
        #dummy user 
        user = self.create_dummy_user()

        # dummy project 
        project_instance = self.create_dummy_project(user)
    
        # assert project_instance is an instance of Project model
        self.assertTrue(isinstance(project_instance, Project))

        # test the title field of a project returned by str method
        self.assertEqual(project_instance.__str__(), (project_instance.title + ' by ' + user.username))

        # test the creation of project 
        self.assertEqual(project_instance, Project.objects.get(title=project_instance.title))

    def test_category_model(self):
        #dummy user 
        user = self.create_dummy_user()
        #dummy project
        project = self.create_dummy_project(user)
        # dummy category
        category_instance = self.create_dummy_category(project)
    
        # assert category_instance is an instance of Category model
        self.assertTrue(isinstance(category_instance, Category))

        # test the category_name field of a Category returned by str method
        self.assertEqual(category_instance.__str__(), (category_instance.category_name + '(Category of ' + project.title + ')'))

        # test the creation of category_instance 
        self.assertEqual(category_instance, Category.objects.get(category_name=category_instance.category_name))

        #test the foreign key relation between project and category models
        self.assertEqual(category_instance, project.category_set.get(category_name=category_instance.category_name))
       
    def test_task_model(self):
            #dummy user 
            user = self.create_dummy_user()
            #dummy project
            project = self.create_dummy_project(user)
            # dummy category
            category_instance = self.create_dummy_category(project)
            #dummy task
            task_instance = Task.objects.create(text='new task', category=category_instance, author=user)
        
            # assert task_instance is an instance of Task model
            self.assertTrue(isinstance(task_instance, Task))

            # test the creation of category_instance 
            self.assertEqual(task_instance, Task.objects.get(text=task_instance.text))

            #test the foreign key relation between Category and Task models
            self.assertEqual(task_instance, category_instance.task_set.get(text=task_instance.text))
        
