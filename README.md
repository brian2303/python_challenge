
# Library books GraphQL

GraphQL API for search books from Google Books API and Open Library API, in addition have the capacity to save books inside a DB only referencing book ID and source

## Extensions

* Graphene-python
* Flask
* AIOHTTP
* motor
* Flask-JWT-Extended

## Environment Variables

To run this project, you will need to add the following environment variables to your .env file

### **Env variable to database:** ###

`COLLECTION` books

`COLLECTION_USERS` books

`SECRET_KEY` <your_secret_key>

`DB_NAME` pythonChallenge

`PASSWORD` <your_mongodb_password>

`USER` <your_mongodb_user>

`STR_CONNECT` mongodb+srv://{username}:{password}@<hostname>/?retryWrites=true&w=majority

### **Env variables to APIs** ###

`GOOGLE_API` https://www.googleapis.com/books/v1/volumes/
 
`OPEN_LIBRARY_BOOK` https://openlibrary.org/search.json

## Run Locally

Clone the project

```bash
  git clone https://github.com/brian2303/python_challenge
```

Go to the project directory

```bash
  cd python_challenge
```

Create virtual environment

```bash
  python3.8-venv -m venv venv
```

Activate virtual environment

```bash
  source venv/bin/activate
```

Install dependencies

```bash
  pip install -r requirements.txt
```

Start the server

```bash
  python3 main.py
```


## 🔗 Heroku URLs - Deploy

You need to create a user so you can log in and get the access token later

method: **POST**:

https://library-books-app-1e709afa3394.herokuapp.com/create-user

**JSON payload**

```
{
    "username": "user_name_here",
    "password": "password_here"
}
```
----------------------------------------------------

You need to login a user to receive the access token

method: **POST** :

https://library-books-app-1e709afa3394.herokuapp.com/login

**JSON payload**

```
{
    "username": "user_name_here",
    "password": "password_here"
}
```


## Usage/Examples

You should include token generated previously like **Bearer Token** authentication method to each GraphQL request

https://library-books-app-1e709afa3394.herokuapp.com/books

Search a book using a query:

```
query BookSearch {
    bookSearch(search: "Alicia en el pais de las maravillas") {
      id
      resource
      title
      subtitle
    }
}
```

Save a book using a mutation:

```
mutation CreateBook {
    createBook(id: "c2hvzgEACAAJ", resource: "GOOGLE_API") {
        book {
          id
          message
          title
          subtitle
        }
    }
}
```

Delete a book using a mutation:

```
mutation DeleteBook {
    deleteBook(bookId: "x2JmDgAAQBAJ") {
        success
        message
    }
}
```
## Authors

- [@brian2303](https://github.com/brian2303) GitHub
- [LinkedinProfile](https://www.linkedin.com/in/bolarte)


