# DJANGO-BLOG-APP
This is a Django Blog App created in connection with Softuni Python Development Web Course project requirements.The application is implemented using Django Framework and uses class-based views and a couple of function-based views.
<h2>Introduction</h2>
Django blog app is a multi-user blogging application with options to the registered users to perform full CRUD article operations, meaning that they can create, update, delete and read articles.
Users who are not logged in can only read articles. The users with profiles can favourite a particular article, change their profile settings, password, log in, log out, store all favourited articles. When a user is registered, s/he automatically sign in. 
<h2>Administration</h2>
SuperUser and ArticleCreators Group Users can perform full CRUD article operations. A customized admin panel was created with filters, list display, ordering, search option, and approval of articles upon submission by superusers and ArticleCreators. 
<h2>User management</h2>
Custom BaseUser and Profile one-to-one relationship is added. A signal helps profile automatic creation upon user registration. 
<h2>Database Management</h2>
PostgreSQL is used as a Database Service. 
The views present filtering of articles by author, profile, favourited articles, category, tags, etc. 
Foreign keys, one-to-one, and many-to-many relationships were implemented to serve table relationships.
<h2>Forms</h2>
Model forms and Crispy forms were used. 
CAPTCHA was added to the comment form. 

<h2>Cache Management</h2>
Redis service has been configured.
<h2>Templates and functionalities</h2>
The project uses Django Template Language. Bootstrap, custom CSS and ready-made template with customizations to meet the project needs. The application has public and private part. 
Pagination was implemented where a list view is added. 
Next/prev functionality is added.
Section of the most read articles is added. 
Section for the related articles is available, too.
<h2>Deployment</h2>
Docker Compose files, NGINX, Gunicorn were configured. AWS service was used for creating an instance for deployment. 
DockerHub file:https://hub.docker.com/layers/sonyaharalambieva/blog_app_production/latest/images/sha256:8c8fd3892f4fab78a5c612bbd2be571f8126ee85e025fedd098bfe1be3a2028a 
<h2>Screenshots</h2>
![admin](https://github.com/sonya-stefanova/DJANGO-BLOG-APP/assets/72320076/6f73091d-24ec-461d-9f32-4398853f5986)
![authors page](https://github.com/sonya-stefanova/DJANGO-BLOG-APP/assets/72320076/d1b4bc4c-e4eb-42b1-91f7-e92038e1385b)
![groups](https://github.com/sonya-stefanova/DJANGO-BLOG-APP/assets/72320076/2f5fd639-f153-41e6-93fe-55900ad5fa62)
![index1](https://github.com/sonya-stefanova/DJANGO-BLOG-APP/assets/72320076/26a825bb-c3fe-487c-a9e5-aac2382de956)
![index](https://github.com/sonya-stefanova/DJANGO-BLOG-APP/assets/72320076/6e7f670c-6c28-42ed-ae82-dabb9f32f9af)
![profile page](https://github.com/sonya-stefanova/DJANGO-BLOG-APP/assets/72320076/dae33608-f267-470d-b605-c95bd0495d9c)
![rich_article](https://github.com/sonya-stefanova/DJANGO-BLOG-APP/assets/72320076/8ddfeb2b-738a-4b75-bac4-4178aeecc9f9)
![image](https://github.com/sonya-stefanova/DJANGO-BLOG-APP/assets/72320076/94dced4f-0823-4cb1-a7b9-2e5012575678)
<a href="https://sonya-deanova.nimbusweb.me/share/9398954/45dvbcmdakcir2vpy106">Link to the AWS screenshot</a>

