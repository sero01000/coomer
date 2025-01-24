from typing import List

from .parser import Parser
from .utils import IMAGE_EXTS


class Post:
    def __init__(self, parser: Parser, data: dict):
        self.parser = parser
        self.parse(data)

    def __str__(self) -> str:
        attributes = ", ".join(f"{key}={value}" for key, value in vars(self).items())
        return f"Post({attributes})"

    def parse(self, data: dict):
        self.id = data.get("id")
        self.id_int = int(self.id)
        self.user = data.get("user")
        self.service = data.get("service")
        self.title = data.get("title")
        self.content = data.get("content")
        self.embed = data.get("embed")
        self.shared_file = data.get("shared_file")
        self.added = data.get("added")
        self.published = data.get("published")
        self.edited = data.get("edited")
        self.file = data.get("file")
        self.attachments = data.get("attachments")
        self.poll = data.get("poll")
        self.captions = data.get("captions")
        self.tags = data.get("tags")
        self.files = self.get_all_file_urls()

    def has_media(self) -> bool:
        if len(self.attachments) != 0 or len(self.file) != 0:
            return True
        return False

    def get_all_file_urls(self) -> List[str]:
        urls = []
        if len(self.attachments) != 0:
            urls = [
                f"{self.parser.base_url}{attachment['path']}"
                for attachment in self.attachments
                if "path" in attachment
            ]
            urls.extend(urls)

        if len(self.file) != 0:
            url = f"{self.parser.base_url}{self.file['path']}"
            urls.append(url)

        if self.parser.images_as_thumbnails:
            for i, url in enumerate(urls):
                path = url.split(self.parser.base_url)[-1]
                ext = path.split(".")[-1]
                if ext in IMAGE_EXTS:
                    urls[i] = f"{self.parser.thumbnail_url}{path}"
        urls = set(urls)
        return urls


def filter_posts_with_media(posts: List[Post]) -> Post:
    for post in posts:
        if post.has_media():
            yield post


def filter_posts_from_start_id(posts: List[Post], start_id: int) -> Post:
    for post in posts:
        if post.id_int <= start_id:
            yield post
