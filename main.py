from fastapi import FastAPI, HTTPException, status
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
    {
        "id": 3,
        "title": "Fantastic Four",
        "director": "Matt Shakman",
        "year": 2025,
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
def get_movies(
    id: int | None = None,
    min_year: int | None = None,
    director: str | None = None,
):
    if id is not None:
        index = find_movie_index(id)
        if index is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Movie not found"
            )
        return movies[index]  

    result = movies

    if min_year is not None:
        result = [movie for movie in result if movie["year"] >= min_year]

    if director is not None:
        result = [
            movie
            for movie in result
            if director.lower() in movie["director"].lower()
        ]

    return result


@app.post("/movies", status_code=status.HTTP_201_CREATED)
def create_movie(movie: MovieCreate):
    new_id = max((m["id"] for m in movies), default=0) + 1
    new_movie = {"id": new_id, **movie.model_dump()}
    movies.append(new_movie)
    return new_movie


@app.put("/movies/{id}")
def replace_movie(id: int, movie: MovieCreate):
    index = find_movie_index(id)
    if index is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Movie not found"
        )

    updated_movie = {"id": id, **movie.model_dump()}
    movies[index] = updated_movie
    return updated_movie

@app.patch("/movies/{id}")
def patch_Movies(id: int, movie: MovieUpdate) :
    index = find_movie_index(id)
    if index is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail = "Movie not found"
        )
    update_data = movie.model_dump(exclude_unset=True)
    movies[index].update(update_data)
    return movies[index]

@app.delete("/movies/{id}", status_code = status.HTTP_204_NO_CONTENT)
def delete_movie(id: int):
    index = find_movie_index(id)
    if index is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail = "Movie not found"
            )
    movies.pop(index)
    return None