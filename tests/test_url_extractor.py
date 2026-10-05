"""Tests for URL extractor utility."""

from app.utils.url_extractor import extract_urls, find_first_url


class TestURLExtractor:
    def test_extract_single_url(self):
        text = "Check this video https://www.youtube.com/watch?v=dQw4w9WgXcQ"
        urls = extract_urls(text)
        assert urls == ["https://www.youtube.com/watch?v=dQw4w9WgXcQ"]

    def test_extract_multiple_urls(self):
        text = "Here is https://vimeo.com/123456 and also https://tiktok.com/@user/video/789"
        urls = extract_urls(text)
        assert len(urls) == 2
        assert "https://vimeo.com/123456" in urls
        assert "https://tiktok.com/@user/video/789" in urls

    def test_strip_trailing_punctuation(self):
        text = "Look at this link: https://youtube.com/watch?v=abc12345!"
        url = find_first_url(text)
        assert url == "https://youtube.com/watch?v=abc12345"

    def test_no_urls(self):
        assert extract_urls("Just plain text with no links") == []
        assert find_first_url("No link here") is None

    def test_empty_string(self):
        assert extract_urls("") == []
        assert find_first_url("") is None
