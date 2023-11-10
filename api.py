from fastapi import FastAPI, HTTPException, status, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from datetime import timedelta, datetime
from typing import Annotated

from bdtest import fake_users_db
import bdd
import models
import crud
import classes
import schemas
from database import SessionLocal, engine
from get_db import get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

database = r"bdd.db"


@app.get("/scores_europe")
def get_scores_europe():
    conn = bdd.create_connection(database)
    scores = bdd.select_scores(conn, "ScoresEurope")
    for i in range(len(scores)):
        scores[i] = classes.to_object_score(scores[i])
    return scores


@app.get("/scores_afrique")
def get_scores_afrique():
    conn = bdd.create_connection(database)
    scores = bdd.select_scores(conn, "ScoresAfrique")
    for i in range(len(scores)):
        scores[i] = classes.to_object_score(scores[i])
    return scores


@app.get("/scores_asie")
def get_scores_asie():
  conn = bdd.create_connection(database)
  scores = bdd.select_scores(conn, "ScoresAsie")
  for i in range(len(scores)):
    scores[i] = classes.to_object_score(scores[i])
  return scores

@app.get("/scores_monde")
def get_scores_monde():
    conn = bdd.create_connection(database)
    scores = bdd.select_scores(conn, "ScoresMonde")
    for i in range(len(scores)):
        scores[i] = classes.to_object_score(scores[i])
    return scores


@app.post("/add_score_europe")
def add_score_europe(score: classes.Score):
    conn = bdd.create_connection(database)
    bdd.create_score(conn, "ScoresEurope", score.temps, score.erreurs, score.joueur)


@app.post("/add_score_afrique")
def add_score_afrique(score: classes.Score):
    conn = bdd.create_connection(database)
    bdd.create_score(conn, "ScoresAfrique", score.temps, score.erreurs, score.joueur)


@app.post("/add_score_asie")
def add_score_asie(score: classes.Score):
  conn = bdd.create_connection(database)
  bdd.create_score(conn, "ScoresAsie", score.temps, score.erreurs, score.joueur)


@app.post("/add_score_monde")
def add_score_monde(score: classes.Score):
    conn = bdd.create_connection(database)
    bdd.create_score(conn, "ScoresMonde", score.temps, score.erreurs, score.joueur)

#TODO: A refaire
@app.post("/signup", response_model=schemas.UserInDb)
def signup_user(user: schemas.UserInDb, db: Session = Depends(get_db)):
    try:
        user: schemas.UserInDb = crud.create_user(db=db, user=user)
        return user
    except IntegrityError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="L'email ou le nom d'utilisateur éxiste déjà!",
            headers={"WWW-Authenticate": "Bearer"},
        )


@app.post("/token", response_model=schemas.Token)
def login_for_access_token(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        db: Session = Depends(get_db)
):
    user = crud.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=crud.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = crud.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


# #TODO: A refaire
# @app.delete("/users/me")
# async def delete_user(current_user: Annotated[schemas.User, Depends(crud.get_current_active_user)]):
#     del fake_users_db[current_user.username]
#     return {"message": "User deleted successfully"}
#

#TODO: A refaire
@app.get("/users/me/", response_model=schemas.UserData)
async def read_users_me(
        current_user: Annotated[schemas.UserData, Depends(crud.get_current_active_user)]
):
    return current_user


@app.delete("/users/", response_model=schemas.UserData)
def delete_user(
        #TODO: checker si le user est admin
        user: Annotated[schemas.UserData, Depends(crud.get_current_active_user)],
        user_id: int,
        db: Session = Depends(get_db)
):
    return delete_user(db=db, id=user_id)


@app.post("/score/", response_model=schemas.GameInDb)
def create_game(
        #TODO erreur bizarre
        game: schemas.Game,
        db: Session = Depends(get_db),
):
    return create_game(game=game, db=db)
