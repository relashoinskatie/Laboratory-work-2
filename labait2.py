from fastapi import FastAPI, HTTPException
import wikipedia
import uvicorn
from pydantic import BaseModel

app = FastAPI(title="miniwikipedia")


class ForPast(BaseModel):  # тип данных
    text: str


class ForFind(BaseModel):
    tags: list


class ForPage(BaseModel):
    titl: str
    url: str


@app.get("/{find}", response_model=ForFind)
def find(find: str):
    return ForFind(tags=(wikipedia.search(find)))


@app.post("/", response_model=ForPage)
def designation(page: str):
    try:  # просматриваем исключения
        wiki_page = wikipedia.page(page)
    except Exception as e:  # ловими
        raise HTTPException(status_code=400, detail=str(e))
    else:
        return ForPage(url=wiki_page.url,
                       titl=wiki_page.title)


@app.post("/text", response_model=ForPast)
def content(sr: ForPast):
    return ForPast(text=wikipedia.page(sr.text).content)


if __name__ == '__main__':
    uvicorn.run(app=app, host='0.0.0.0', port=8000)
    # Данная строчка запускает код без запуска команды из терминала.
    # Она задаёт app, host 0.0.0.0 задаёт доступ для всех внутри сети
    # Елси разрешено, конечно и задаёт порт 8000. reload=True значит,
    # что веб-сервер перезапускается автоматически при изменении кода

