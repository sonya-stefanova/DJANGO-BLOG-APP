# DJANGO-BLOG-APP
This is a Django Blog App created in connection with Softuni Python Develoment Web Course project requierments.The application is implemented using Django Framework.
<h2>Introduction</h2>
Django blog app is a multi-user blogging application with options to the registered users to perform full CRUD article operations, meaning that they can create, update, delete and read articles.
Users that are not logged in can only read articles. The users with profiles can favourite a particular article, change their profile settings, password, log in, log out, store all favourited articles. When a user is register, s/he automatically sign in. 
<h2>Administration</h2>
SuperUser and ArticleCreators Group Users can perform full CRUD article operations. Customized admin panel was created with filters, list display, ordering, search option, approval of articles upon submission by superusers and ArticleCreators. 
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
The project uses Django Template Language. Bootstrap, custom CSS and ready-made template with adjustments in alignment with the project aims have been used. The application has public and private part. 
Pagination was implemented where a list view is added. 
Next/prev functionality is added
<h2>Deployment</h2>
Docker Compose files, NGINX, Gunicorn were configured. AWS service was used for creating an instance for deployment. 
DockerHub file:https://hub.docker.com/layers/sonyaharalambieva/blog_app_production/latest/images/sha256:8c8fd3892f4fab78a5c612bbd2be571f8126ee85e025fedd098bfe1be3a2028a 
<h2>Screenshots</h2>
