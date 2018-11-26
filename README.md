# Simple REST-application
## Installation
<code>git clone https://github.com/nautics889/simplerestapp.git</code>

<code>cd simplerestapp</code>

<code>pip install -r req.txt</code>
## Usage
Move to directory which contains <code>manage.py</code>.
Create and perform migrations:

<code>python manage.py make migrations</code>

<code>python manage.py migrate</code>

<i>Assumed you have an empty database and configured restfulapp/dev_settings.py file.</i>

Get a server up:

<code>python manage.py runserver</code>
### Request-response guide
POST-Request to *create_user/*:
```
{
	"username": "foobar8",
	"email": "foobar8@gmail.com",
	"password": "foobar777" 
}
```
Response:
```
{
    "username": "foobar8",
    "email": "foobar8@gmail.com",
    "first_name": "",
    "last_name": ""
}
STATUS: 201
```
________________________________
POST-Request to *authenticate/*:
```
{
	"username": "foobar8", 
	"password": "foobar777" 
}
```
Response:
```
{
    {
    "token": "<hash>"
    }
}
STATUS: 200
```
_____________________________________
POST-Request to *posts/create_post/*:
```
{
	"title": "Sample", 
	"content": "Lorem ipsum" 
}
headers: {"token": "JWT <hash>"}
```
Response:
```
{
	"title": "Sample", 
	"content": "Lorem ipsum" 
}
STATUS: 201
```
__________________________
GET-Request to *posts/1/*:
```
headers: {"token": "JWT <hash>"}
```
Response:
```
{
	"title": "Sample", 
	"content": "Lorem ipsum" 
}
STATUS: 200
```
________________________
GET-Request to *posts/*:
```
headers: {"token": "JWT <hash>"}
```
Response:
```
{
	"title": "Sample", 
	"content": "Lorem ipsum" 
},
...
{
	"title": "Sample_x", 
	"content": "Lorem ipsum" 
}
STATUS: 200
```
______________________________
GET-Request to *posts/1/like*:
```
headers: {"token": "JWT <hash>"}
```
Response:
```
{
	"response": "Post №1 has been liked."
}
STATUS: 200
```
______________________________
GET-Request to *posts/1/like*:
```
headers: {"token": "JWT <hash>"}
```
Response:
```
{
	"response": "Post №1 has been unliked."
}
STATUS: 200
```
