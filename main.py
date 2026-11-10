from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


movies = [
    {
        "id": 1,
        "title": "Inception",
        "director": "Christopher Nolan",
        "year": 2010,
    },
    {
        "id": 2,
        "title": "Interstellar",
        "director": "Christopher Nolan",
        "year": 2014,
    },
]


class MovieCreate(BaseModel):
    title: str
    director: str
    year: int

class MovieUpdate(BaseModel):
    title: str | None = None
    director: str | None = None
    year: int | None = None

#Helper function to find array index of a movie by ID
def find_movie_index(movie_id: int) -> int | None:
    for index, movie in enumerate(movies):
        if movie["id"] == movie_id:
            return index
        return None


@app.get("/movies")
def get_movies():
    return movies

@app.get("/movies/{id}")
def getMovies(id: int):
    index = find_movie_index(id)
    if index is None:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND, detail = "Movie not found"
        )
    return movies[index]


@app.post("/movies", status_code=status.HTTP_201_CREATED)
def create_movie(movie: MovieCreate):
    new_id = max((m["id"] for m in movies), default=0) + 1
    new_movie = {"id": new_id, **movie.model_dump()}
    movies.append(new_movie)
    return new_movie


app.put("/movies/{id}")
def putMovies(id: int):
    index = find_movie_index(id)
    if index is None:
        raise HTTPException(
                    status_code = status.HTTP_404_NOT_FOUND, detail = "Movie not found"
                )
    update_movie = {"id": id, movie:MovieUpdate}
