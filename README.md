
# Library books GraphQL

GraphQL API for search books from Google Books API and Open Library API, in addition have the capacity to save books inside a DB only referencing book ID and source

## Extensions

* Graphene-python
* Flask
* AIOHTTP
* motor

## Environment Variables

To run this project, you will need to add the following environment variables to your .env file

### **Env variable to database:** ###

`COLLECTION` books

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


## 🔗 Heroku URL - Deploy
https://library-books-app-1e709afa3394.herokuapp.com/books

Examples of use:



## Usage/Examples

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

- [@brian2303](https://github.com/brian2303)


