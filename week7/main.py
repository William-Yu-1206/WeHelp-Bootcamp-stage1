import mysql.connector
con = mysql.connector.connect(
    user="root",
    password="123456789",
    host="localhost",
    database="week6"
)

from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from starlette.middleware.sessions import SessionMiddleware

template = Jinja2Templates(directory="templates")

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key="fi23irovn0568mcv1024ufvnkds")

app.mount("/static", StaticFiles(directory="static"))

@app.get("/")
async def root(request:Request):
    return template.TemplateResponse(
        request=request,
        name="root.html"
    )


class SignUp(BaseModel):
    name: str
    username: str
    password: str

@app.post("/signup")
async def signup(body: SignUp):
    with con.cursor() as cursor:
        query="select name, username, password from member where username=%s"
        value=(body.username, )
        cursor.execute(query, value)
        data = cursor.fetchone()
        if data:
            return RedirectResponse("/error?message=帳號已註冊過", status_code=303)
        else:
            query="insert into member(name, username, password) values(%s, %s, %s)"
            value=(body.name, body.username, body.password)
            cursor.execute(query, value)
            con.commit()
            return RedirectResponse("/", status_code=303)
    
@app.get("/error")
async def error(request:Request, message: str | None = None):
    return template.TemplateResponse(
        request=request,
        name="error.html",
        context={
            "message": message
        }
    )


class SignIn(BaseModel):
    username: str
    password: str

@app.post("/signin")
async def signin(body: SignIn, request: Request):
    with con.cursor() as cursor:
        query = "select id, name, username from member where username=%s and password=%s"
        value = (body.username, body.password)
        cursor.execute(query, value)
        data = cursor.fetchone()
        if data:
            request.session["id"] = data[0]
            request.session["name"] = data[1]
            request.session["username"] = data[2]
            return RedirectResponse("/member", status_code=303)
        else:
            return RedirectResponse("/error?message=帳號或密碼輸入錯誤", status_code=303)


@app.get("/member")
async def member(request: Request):
    if request.session:
        with con.cursor() as cursor:
            query = "select member.name, message.id, message.member_id=%s, message.content from message inner join member on message.member_id = member.id order by message.id desc"
            value = (request.session["id"], )
            cursor.execute(query, value)
            data = cursor.fetchall()
        return template.TemplateResponse(
        request=request,
        name="member.html",
        context={
            "name": request.session["name"],
            "message": data
        })
    else:
        return RedirectResponse("/")

@app.get("/signout")
async def signout(request: Request):
    request.session.clear()
    return RedirectResponse("/")


class CreateMessage(BaseModel):
    message: str

@app.post("/createMessage")
async def createMessage(request: Request, body: CreateMessage):
    if request.session:
        with con.cursor() as cursor:
            query = "insert into message(member_id, content) values(%s, %s)"
            values = (request.session["id"], body.message)
            cursor.execute(query, values)
            con.commit()
        return RedirectResponse("/member", status_code=303)
    else:
        return RedirectResponse("/", status_code=303)


class DeleteMessage(BaseModel):
    message_id: int

@app.post("/deleteMessage")
async def deleteMessage(request: Request, body: DeleteMessage):
    if request.session:
        with con.cursor() as cursor:
            query = "select member_id from message where id = %s"
            value = (body.message_id, )
            cursor.execute(query, value)
            member_id_from_front = cursor.fetchone()[0]
            if member_id_from_front == request.session["id"]:
                query = "delete from message where id = %s"
                value = (body.message_id, )
                cursor.execute(query, value)
                con.commit()
    return RedirectResponse("/member", status_code=303)

@app.get("/api/member")
async def queryName(request: Request, username: str | None = None):
    if request.session:
        with con.cursor() as cursor:
            query = "select id, name, username from member where username = %s"
            value = (username, )
            cursor.execute(query, value)
            data = cursor.fetchone()
            if data:
                result = {
                    "data": {
                        "id": data[0],
                        "name": data[1],
                        "username": data[2]
                    }
                }
            else:
                result = {"data": None}
            return result
    return RedirectResponse("/")

class UpdateName(BaseModel):
    name: str

@app.patch("/api/member")
async def updateName(request: Request, body: UpdateName):
    if request.session:
        with con.cursor() as cursor:
            query = "update member set name = %s where id = %s"
            values = (body.name, request.session["id"])
            cursor.execute(query, values)
            con.commit()
        request.session["name"] = body.name
        return {"ok": True}
    return {"error": True}