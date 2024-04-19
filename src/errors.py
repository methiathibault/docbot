class ArticleServiceError(Exception):
	pass

class ArticleNotFoundError(ArticleServiceError):
	pass
