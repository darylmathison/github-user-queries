from app import create_app

app = create_app()
app.config["SECRET_KEY"] = b"\t\xa8\xd0\x80\xa0Pq*\xcbi\x90l qx."
