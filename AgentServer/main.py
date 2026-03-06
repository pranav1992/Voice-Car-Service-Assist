import uvicorn


def main():
    print("Hello from fastapitutotial!")


if __name__ == "__main__":
    main()
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)