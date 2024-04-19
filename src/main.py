from fastapi import Depends, FastAPI, HTTPException,status
from services import ArticleService, article_service_dependency
from models import NotionArticle
from errors import ArticleNotFoundError

app = FastAPI()

@app.post("/article")
async def create_article(article: NotionArticle, article_service: ArticleService = Depends(article_service_dependency)) -> NotionArticle:
	return article_service.create_article(article)

@app.post("/articles")
async def create_articles(articles: list[NotionArticle], article_service: ArticleService = Depends(article_service_dependency)) -> list[NotionArticle]:
	return article_service.create_articles(articles)

@app.delete("/article/")
async def delete_all_articles(article_service:  ArticleService = Depends(article_service_dependency)) -> None:
	article_service.delete_all_articles()

@app.delete("/article/{article_id}")
async def delete_article(article_id: str, article_service: ArticleService = Depends(article_service_dependency)) -> None:
	article_service.delete_article(article_id)

@app.get("/article/{article_id}",
		 responses={
			 404: {"description": "Article not found"}
		 })
async def get_article(article_id: str,  article_service: ArticleService = Depends(article_service_dependency)) -> NotionArticle:
	try:
		return article_service.get_article(article_id)
	except ArticleNotFoundError:
		raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Article not found")