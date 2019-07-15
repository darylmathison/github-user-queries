from app import create_app

if __name__ == '__main__':
    app = create_app()
    app.config["SECRET_KEY"] = "kjdfks;lkfa;fkasflkklkkkkdkdkdkdkdsk"
    app.run()
