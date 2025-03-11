from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os
import mistletoe

app = FastAPI()

app.mount("/gen", StaticFiles(directory="gen"), name="static")

templates = Jinja2Templates(directory=".")

data = {}

@app.get("/items/{id}", response_class=HTMLResponse)
async def read_item(request: Request, id: str) -> HTMLResponse:
    return templates.TemplateResponse(
        request=request, name="index.html", context={"blogs": data}
    )

def generate_posts() -> None:
    with os.scandir("./md") as it:
        for entry in it:
            with open(entry, "r") as file:
                lines = file.readlines()
                metadata = {}
                content_start = 0
                if lines[0].strip() == "---":
                    for i, line in enumerate(lines[1:], start=1):
                        if line.strip() == "---":
                            content_start = i + 1
                            break
                        key, value = line.split(":", 1)
                        metadata[key.strip()] = value.strip()
                content = "".join(lines[content_start:])
                rendered = mistletoe.markdown(content)
                rendered = "<link rel='stylesheet' type='text/css' href='/gen/style.css'>" + rendered
                with open(f"./gen/{entry.name}.html", "w") as f:
                    f.write(rendered)
                data[f"/gen/{entry.name}.html"] = metadata

if __name__ == "__main__":
    import uvicorn
    generate_posts()
    uvicorn.run(app, host="0.0.0.0", port=8099)