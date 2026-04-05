"""Unit tests for GenerateRequest schema validation."""

import pytest
from pydantic import ValidationError

from app.schemas.generate import GenerateRequest


class TestValidPrompt:
    def test_accepts_normal_prompt(self):
        req = GenerateRequest(prompt="hello world")
        assert req.prompt == "hello world"

    def test_trims_leading_whitespace(self):
        req = GenerateRequest(prompt="  hello")
        assert req.prompt == "hello"

    def test_trims_trailing_whitespace(self):
        req = GenerateRequest(prompt="hello  ")
        assert req.prompt == "hello"

    def test_trims_both_sides(self):
        req = GenerateRequest(prompt="  hello world  ")
        assert req.prompt == "hello world"

    def test_accepts_max_length_prompt(self):
        prompt = "a" * 1000
        req = GenerateRequest(prompt=prompt)
        assert len(req.prompt) == 1000


class TestInvalidPrompt:
    def test_rejects_empty_string(self):
        with pytest.raises(ValidationError) as exc_info:
            GenerateRequest(prompt="")
        assert "empty" in str(exc_info.value).lower()

    def test_rejects_whitespace_only(self):
        with pytest.raises(ValidationError) as exc_info:
            GenerateRequest(prompt="   ")
        assert "empty" in str(exc_info.value).lower()

    def test_rejects_oversized_prompt(self):
        with pytest.raises(ValidationError) as exc_info:
            GenerateRequest(prompt="x" * 1001)
        assert "1000" in str(exc_info.value)

    def test_rejects_none_prompt(self):
        with pytest.raises(ValidationError):
            GenerateRequest(prompt=None)  # type: ignore[arg-type]

    def test_rejects_integer_prompt(self):
        with pytest.raises(ValidationError):
            GenerateRequest(prompt=42)  # type: ignore[arg-type]

    def test_rejects_missing_prompt(self):
        with pytest.raises(ValidationError):
            GenerateRequest()  # type: ignore[call-arg]
