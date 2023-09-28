"""Service"""
import re
from flask import redirect, request
from sqlalchemy.exc import IntegrityError
from flask_openapi3 import OpenAPI, Info, Tag
from src.models import Base
from src.database import engine, get_db_session
from src.config import DATABASE_URL
from src.models import Person
from src.schemas import (
    NewPersonSchema,
    PersonPathSchema,
    NewEventCalendarSchema,
    PersonSchema,
    ErrorSchema,
    SucessSchema,
    UpdatePersonSchema,
    QueryCalendarSchema,
)
from src.client import ClientHoliday, ClientScheduler

Base.metadata.create_all(bind=engine)

info = Info(title="Calendário Pessoal API", version="1.0.0")
app = OpenAPI(__name__, info=info)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL

holiday_client = ClientHoliday()
scheduler_client = ClientScheduler()
regex = re.compile(r"([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+")


person_tag = Tag(name="Pessoa", description="")
calendar_tag = Tag(name="Calendário", description="")


@app.get("/")
def home():
    """Redireciona para o swagger"""
    return redirect("/openapi/swagger")


@app.post(
    "/persons/",
    tags=[person_tag],
    responses={"200": PersonSchema, "400": ErrorSchema},
)
def create_person(body: NewPersonSchema):
    """Create a person route"""
    try:
        if not holiday_client.validate_cpf(body.cpf):
            return {"detail": "CPF inválido"}, 404

        if not re.fullmatch(regex, body.email):
            return {"detail": "E-mail inválido"}, 404

        new_person = Person(**body.dict())
        session = get_db_session()
        session.add(new_person)
        session.commit()
        session.flush()
        response_dict = {
            "id": new_person.id,
            "cpf": new_person.cpf,
            "email": new_person.email,
        }
        session.close()

        return response_dict, 200
    except IntegrityError:
        return {"detail": "Já existe este e-mail ou cpf"}, 400


@app.patch(
    "/persons/<int:id>/",
    tags=[person_tag],
    responses={
        "200": PersonSchema,
        "400": ErrorSchema,
        "404": ErrorSchema,
    },
)
def patch_person(path: PersonPathSchema, body: UpdatePersonSchema):
    """Update a person route"""
    session = get_db_session()
    person = session.query(Person).filter(Person.id == path.id).first()
    if not person:
        return {"detail": "Pessoa não encontrada"}, 404

    if session.query(Person).filter(Person.email == body.email).first():
        return {"detail": "Já existe este e-mail"}, 404

    if body.email:
        if not re.fullmatch(regex, body.email):
            return {"detail": "E-mail inválido"}, 404
        person.email = body.email

    if session.query(Person).filter(Person.cpf == body.cpf).first():
        return {"detail": "Já existe este cpf"}, 404

    if body.cpf:
        if not holiday_client.validate_cpf(body.cpf):
            return {"detail": "CPF inválido"}, 404
        person.cpf = body.cpf

    session.commit()
    session.flush()
    response_dict = {
        "id": person.id,
        "cpf": person.cpf,
        "email": person.email,
    }
    session.close()

    return response_dict, 200


@app.delete(
    "/persons/<int:id>/",
    tags=[person_tag],
    responses={
        "200": SucessSchema,
        "400": ErrorSchema,
        "404": ErrorSchema,
    },
)
def delete_person(path: PersonPathSchema):
    """Delete a person route"""
    session = get_db_session()
    person = session.query(Person).filter(Person.id == path.id).first()
    if not person:
        return {"detail": "Pessoa não encontrada"}, 404
    session.delete(person)
    session.commit()
    session.close()
    return {"detail": "Excluído com sucesso"}, 200


@app.get(
    "/persons/<int:id>/",
    tags=[person_tag],
    responses={
        "200": PersonSchema,
        "400": ErrorSchema,
        "404": ErrorSchema,
    },
)
def get_person(path: PersonPathSchema):
    """Get a person route"""
    print(request.environ.get("HTTP_X_FORWARDED_FOR", request.remote_addr))
    session = get_db_session()
    person = session.query(Person).filter(Person.id == path.id).first()
    if not person:
        return {"detail": "Pessoa não encontrada"}, 404

    return {
        "id": person.id,
        "cpf": person.cpf,
        "email": person.email,
    }


@app.get("/persons/calendar/<int:id>/", tags=[calendar_tag])
def get_calendar(path: PersonPathSchema, query: QueryCalendarSchema):
    """Get personal calendar route"""
    return scheduler_client.get_calendar(path.id, query)


@app.post("/persons/calendar/", tags=[calendar_tag])
def post_calendar(body: NewEventCalendarSchema):
    """Create an event in personal calendar route"""
    return scheduler_client.create_event(body.user_id, body.date, body.title)
