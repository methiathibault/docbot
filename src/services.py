from typing import Generator, Iterator

import meilisearch.client
from models import NotionArticle
from fastapi import Depends
import meilisearch
from settings import settings
from errors import ArticleNotFoundError, ArticleServiceError
from meilisearch.errors import MeilisearchApiError

def meilisearch_client_dependency() -> Generator[meilisearch.Client, None, None]:
	yield meilisearch.Client(settings.meilisearch_url, "masterKey")

def article_service_dependency(meilisearch_client: meilisearch.Client = Depends(meilisearch_client_dependency)) -> Iterator["ArticleService"]:
	yield ArticleService(meilisearch_client)

class ArticleService():
	def __init__(self, meilisearch_client: meilisearch.Client) -> None:
		self.meilisearch_client = meilisearch_client
		self.meilisearch_index = self.meilisearch_client.index("articles")
	
	def delete_article(self, id: str) -> None:
		self.meilisearch_index.delete_document(id)

	def delete_all_articles(self) -> None:
		self.meilisearch_index.delete_all_documents()

	def create_article(self, article: NotionArticle) -> NotionArticle:
		return self.create_articles([article])[0]
	
	def create_articles(self, articles: list[NotionArticle]) -> list[NotionArticle]:
		self.meilisearch_index.add_documents([article.model_dump() for article in articles])
		return articles
	
	def get_article(self, article_id:str) -> NotionArticle:
		try:
			return NotionArticle(**dict(self.meilisearch_index.get_document(article_id)))
		except MeilisearchApiError as exc:  
			if exc.status_code == 404:
				raise ArticleNotFoundError
			raise ArticleServiceError from exc
		