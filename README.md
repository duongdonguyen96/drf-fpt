- Thư viện:
 ```pip install django==3.*
 pip install django-rest-swagger
 pip install django-sql-utils
 pip install mysqlclient
 pip install django-debug-toolbar
 ```
 
 - Migrate:
 
 ```
 python manage.py makemigrations
 python manage.py migrate
 ```
 
 - Runserver:
 ```
 python manage.py runserver
 
 ```
- Cấu trúc Project

```
├── api
│   └── v1
│      ├── albums    
│      ├── singers  
│      ├── songs    
│      └── example
│            ├── seriazalers         
│            ├── urls        
│            └── views 
│
├── core  
│   ├── albums   
│   ├── singer
│   ├── songs
│   │   ├── views
│   │   └── views  
│   ├── base model 
│   └──  migrations
│   
│
│  
├── drf-fpt  
│   ├── asgy.py         
│   ├── setting.py         
│   ├── urls.py        
│   └── wsgi.py
├── function         // các hàm dùng chung
└──requirement      // các thư viện  
```