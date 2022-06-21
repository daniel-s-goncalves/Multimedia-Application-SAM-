import bin

if __name__ == "__main__":
    app = bin.create_app()
    app.run(host="0.0.0.0", port=5000)