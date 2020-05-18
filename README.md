# API reference
## Getting Started
* Base URL : At present the frontend React app is run locally on localhost:3000, not hosted on a base URL. The flask backend is served at 127.0.0.1:5000.
* API Keys /Authentication is not required at the moment
## Error Handling
Errors are returned as JSON Objects in the following format
```{
        "success": False,
        "error": 400,
        "message": "bad request"
   }
```
The API returns the following response codes in case of an error:
* 400, Bad Request
* 404, Method not allowed
* 422, Unprocessable request
## Endpoint library
### GET /books
* General
  * Returns a list of book objects, success value and the total number of books
  * Results are paginated by 8 books per page. To access a particular page add a page argument to the url.
* Sample request: `curl http://127.0.0.1/books`
```
{
   "books":[
      {
         "author":"Stephen King",
         "id":1,
         "rating":2,
         "title":"The Outsider: A Novel"
      },
      {
         "author":"Kristin Hannah",
         "id":3,
         "rating":2,
         "title":"The Great Alone"
      },
      {
         "author":"Tara Westover",
         "id":4,
         "rating":2,
         "title":"Educated: A Memoir"
      },
      {
         "author":"Jojo Moyes",
         "id":5,
         "rating":2,
         "title":"Still Me: A Novel"
      },
      {
         "author":"Leila Slimani",
         "id":6,
         "rating":2,
         "title":"Lullaby"
      },
      {
         "author":"Amitava Kumar",
         "id":7,
         "rating":5,
         "title":"Immigrant, Montana"
      },
      {
         "author":"Madeline Miller",
         "id":8,
         "rating":5,
         "title":"CIRCE"
      },
      {
         "author":"Gina Apostol",
         "id":9,
         "rating":5,
         "title":"Insurrecto: A Novel"
      }
   ],
   "success":true,
   "total_books":17
}
```
### POST /books
* General
  * Creates a new book from the give title, author and rating. Returns a list of book objects, success value, the total number of books and the id of the new book created.
* Sample request: `curl -X POST "http://127.0.0.1:5000/books?page=3"  -H "Content-type: application/json" -d '{"title":"The Hunger Games","author":"Suzanne Collins","rating":4}'`
```
{
   "books":[
      {
         "author":"Suzanne Collins",
         "id":25,
         "rating":4,
         "title":"The Hunger Games"
      }
   ],
   "created":26,
   "success":true,
   "total_books":19
}
```
### DELETE /books/{book_id}
* General 
  * Deletes a book of given id if it exists in the database. Returns a list of book objects, success value, the total number of books and the id of the book deleted.
  * Sample request: `curl -X DELETE "http://127.0.0.1:5000/books/23"`
```
{
   "books":[
      {
         "author":"Stephen King",
         "id":1,
         "rating":2,
         "title":"The Outsider: A Novel"
      },
      {
         "author":"Kristin Hannah",
         "id":3,
         "rating":2,
         "title":"The Great Alone"
      },
      {
         "author":"Tara Westover",
         "id":4,
         "rating":2,
         "title":"Educated: A Memoir"
      },
      {
         "author":"Jojo Moyes",
         "id":5,
         "rating":2,
         "title":"Still Me: A Novel"
      },
      {
         "author":"Leila Slimani",
         "id":6,
         "rating":2,
         "title":"Lullaby"
      },
      {
         "author":"Amitava Kumar",
         "id":7,
         "rating":5,
         "title":"Immigrant, Montana"
      },
      {
         "author":"Madeline Miller",
         "id":8,
         "rating":5,
         "title":"CIRCE"
      },
      {
         "author":"Gina Apostol",
         "id":9,
         "rating":5,
         "title":"Insurrecto: A Novel"
      }
   ],
   "deleted":23,
   "success":true,
   "total_books":18
}
```
### PATCH /books/{book_id}
* General
  * Updated the rating of the book id. Returns success value and the id of the book modified.
* Sample: `curl -X PATCH "http://127.0.0.1:5000/books/25" -H "Content-type: application/json" -d '{"rating":"3"}'`
```
    {
   "id":25,
   "success":true
   }
```
