from typing import Annotated
from fastapi import FastAPI, Form, Request
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware
app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key="random_key_asdgew")

templates = Jinja2Templates(directory="templates")

@app.post("/signin")
def signin(
    request: Request,
    username: Annotated[str, Form()],
    password: Annotated[str, Form()]):
    if username == "" or password == "":
        return RedirectResponse("/error?message=Please enter username and password.", status_code=302)
    elif username == "test" and password == "test":
        request.session["SIGN-IN"] = "TRUE"
        return RedirectResponse("/member", status_code=302)
    else: 
        return RedirectResponse("/error?message=Username or password is not correct.", status_code=302)

@app.get("/signout")
def signout(request: Request):
    request.session["SIGN-IN"] = "FALSE"
    return RedirectResponse("/")

# 測試用
# @app.get("/test_sign_status")
# def testSignStatus(requst: Request):
#     status = requst.session.get("SIGN-IN", "FALSE")
#     return {'message': status}

@app.get("/member")
def member(requset: Request):
    if requset.session["SIGN-IN"] == "FALSE":
        return RedirectResponse("/")
    else:
        return templates.TemplateResponse(
            request=requset,
            name="member.html"
        )

@app.get("/error")
def error(request: Request, message):
    return templates.TemplateResponse(
        request=request,
        name="error.html",
        context={"message": message}
    )

app.mount("/", StaticFiles(directory="static", html=True))
