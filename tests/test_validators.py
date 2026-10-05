"""Tests for URL validator and SSRF protection."""

from app.utils.validators import is_ssrf_safe, validate_download_url, is_private_ip


class TestURLValidator:
    def test_valid_urls(self):
        valid, _ = validate_download_url("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
        assert valid is True

        valid, _ = validate_download_url("http://vimeo.com/12345678")
        assert valid is True

    def test_rejected_schemes(self):
        valid, reason = validate_download_url("file:///etc/passwd")
        assert valid is False
        assert "Unsupported scheme" in reason

        valid, reason = validate_download_url("ftp://example.com/file.mp4")
        assert valid is False

        valid, reason = validate_download_url("javascript:alert(1)")
        assert valid is False

    def test_ssrf_rejection(self):
        assert is_ssrf_safe("localhost") is False
        assert is_ssrf_safe("127.0.0.1") is False
        assert is_ssrf_safe("10.0.0.1") is False
        assert is_ssrf_safe("192.168.1.1") is False
        assert is_ssrf_safe("169.254.169.254") is False

        valid, reason = validate_download_url("http://localhost:8000/video.mp4")
        assert valid is False
        assert "restricted host" in reason

        valid, reason = validate_download_url("http://192.168.0.1/video.mp4")
        assert valid is False

    def test_private_ip_helper(self):
        assert is_private_ip("127.0.0.1") is True
        assert is_private_ip("10.1.2.3") is True
        assert is_private_ip("8.8.8.8") is False
