# vmart-assignment

1. Create admin user "python manage.py createsuperuser" 
2. Run server on localhost "python manage.py runserver"
3. Go to  http://127.0.0.1:8000/admin and login as admin
4. CRUD APIs to perform on Company and User:
    Use X-CSRFToken in header.
    For Company:
    1. Create Company POST API:
       url : http://127.0.0.1:8000/company/
       payload : {
          "name": "ABC",
          "description": "storage company",
          "address": "Mahadevapura",
          "city": "Bangalore",
          "state": "Karnataka",
          "postal_code": "560042",
          "email": "storage@abc.com",
          "phone_number": "9761234567",
          "website": "http://abc.com",
          "no_of_employees": 0
       }
    2. Update Company PUT API:
       url : http://127.0.0.1:8000/company/<id>
       payload : {
          "name": "ABC",
          "description": "storage company",
          "address": "Mahadevapura",
          "city": "Bangalore",
          "state": "Karnataka",
          "postal_code": "560042",
          "email": "storage@abc.com",
          "phone_number": "9761234567",
          "website": "http://abc.com",
          "no_of_employees": 0
       }
    3. Delete Company DELETE API:
       url : http://127.0.0.1:8000/company/<id>
    4. Get all Companies GET API:
       url : http://127.0.0.1:8000/company/
    5. Get Company GET API:
       url : http://127.0.0.1:8000/company/<id>

    For Users:
    1. Create User POST API:
       url : http://127.0.0.1:8000/users/
       payload : {
          "position": "Developer",
          "phone_number": "9876543210",
          "email": "hello@gmail.com",
          "user": {"username": "Shreya", "password": "Sh12345"},
          "company": 1
       }
    2. Update User PUT API:
       url : http://127.0.0.1:8000/users/<id>
       payload : {
          "position": "Developer",
          "phone_number": "9876543210",
          "email": "hello@gmail.com",
          "company": 1
       }
    3. Delete User DELETE API:
       url : http://127.0.0.1:8000/users/<id>
    4. Get all Users GET API:
       url : http://127.0.0.1:8000/users/
    5. Get User GET API:
       url : http://127.0.0.1:8000/users/<id>

5. Sign up/ Login for Users from UI, go to home page url http://127.0.0.1:8000
6. Prerequisite: Atleast one company should be already created.
7. After sign up, it will redirect to login page
8. Login directly if already sign up 
9. After login, it will redirect to User Details page
10. From User Details page, user can edit details or Logout
        

