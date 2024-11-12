import uvicorn

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True, ssl_keyfile="C:/Users/Hi/key.pem",
        ssl_certfile="C:/Users/Hi/cert.pem")
