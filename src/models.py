from pydantic import BaseModel

class NotionArticle(BaseModel):
	id: str
	title: str
	content: str
	url: str # TODO
	last_update: str # TODO