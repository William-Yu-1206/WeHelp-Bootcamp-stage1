# 資料庫連結
import mysql.connector
con = mysql.connector.connect(
    user="root",
    password="123456789", # 密碼空白
    host="localhost",
    database="website"
)

# 後端系統
from typing import Annotated
from fastapi import FastAPI, Request, Form, Body
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse
from starlette.middleware.sessions import SessionMiddleware
import json

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key="qwdnf-werrf-123fds")

template = Jinja2Templates(directory="week6/templates")

app.mount("/static", StaticFiles(directory="week6/static"), name="static")


@app.get("/")
async def root(request: Request, s: str=""):
    return template.TemplateResponse(
        request=request,
        name="homepage.html",
        context={"signup": s}
    )

@app.post("/signup")
async def signup(
    name: Annotated[str, Form()],
    username: Annotated[str, Form()],
    password: Annotated[str, Form()]
):
    with con.cursor() as cursor:
        cursor.execute("select username from member where username = %s", (username,))
        data = cursor.fetchone()
        if data != None:
            return RedirectResponse("/error?message=帳號已重複", status_code=303)
        elif data == None:
            cursor.execute(
                "insert into member(name, username, password) values(%s, %s, %s)",
                (name, username, password)
            )
            con.commit()
            return RedirectResponse("/?s=會員註冊成功", status_code=303)
        
@app.post("/signin")
async def signin(
    username: Annotated[str, Form()],
    password: Annotated[str, Form()],
    request: Request
):   
    with con.cursor() as cursor:
        cursor.execute(
            "select id, name, username, password from member where username=%s and password=%s",
            (username, password)
        )
        data = cursor.fetchone()
        if data:
            request.session["SIGN-IN"] = True
            request.session["member_id"] = data[0]
            request.session["name"] = data[1]
            request.session["username"] = data[2]
            return RedirectResponse("/member", status_code=303)
        return RedirectResponse("/error?message=帳號或密碼錯誤", status_code=303)

@app.get("/member")
async def member(request: Request):
    # determine if the login is correct
    if request.session["SIGN-IN"] != True or request.session == {}:
        request.session.clear()
        request.session["SIGN-IN"] = False
        return RedirectResponse("/")
    # retrieve data for message-display    
    with con.cursor() as cursor:
        sql = "select member.name, message.content, message.member_id=%s, message.id from member inner join message on member.id = message.member_id order by message.id desc"
        val = (request.session["member_id"], )
        cursor.execute(sql, val)
        data = cursor.fetchall()

    return template.TemplateResponse(
        request=request,
        name="member.html",
        context={
            "name": request.session["name"],
            "message": data
        }
    )


@app.get("/error")
async def error(request: Request, message):
    return template.TemplateResponse(
        request=request,
        name="error.html",
        context={"message": message}
    )

@app.get("/signout")
async def signout(request: Request):
    request.session.clear()
    request.session["SIGN-IN"] = False
    return RedirectResponse("/")

@app.post("/createMessage")
async def createMessage(
    request: Request,
    message: Annotated[str, Form()]
):
    with con.cursor() as cursor:
        cursor.execute(
            "insert into message(member_id, content) values(%s, %s)", 
            (request.session["member_id"], message)
        )
        con.commit()

    return RedirectResponse("/member", status_code=303)

@app.post("/deleteMessage")
async def deleteMessage(body=Body(None)):
    data = json.loads(body)
    with con.cursor() as cursor:
        cursor.execute("delete from message where id=%s", (data["message_id"], ))
        con.commit()
    return RedirectResponse("/member", status_code=303)