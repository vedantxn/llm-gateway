"""Unit tests for inference service."""

import re

from app.services.inference import InferenceResult, generate_output, new_request_id


class TestGenerateOutput:
    def test_new_request_id_format(self):
        request_id = new_request_id()
        assert re.fullmatch(r"req_[0-9a-f]{8}", request_id)

    def test_returns_inference_result(self):
        result = generate_output("test prompt")
        assert isinstance(result, InferenceResult)

    def test_request_id_format(self):
        result = generate_output("test")
        # req_ prefix + 8 hex characters
        assert re.fullmatch(r"req_[0-9a-f]{8}", result.request_id)

    def test_request_id_length(self):
        result = generate_output("test")
        assert len(result.request_id) == 12

    def test_output_contains_prompt(self):
        result = generate_output("hello there")
        assert "hello there" in result.output

    def test_unique_request_ids(self):
        ids = {generate_output("same").request_id for _ in range(20)}
        assert len(ids) == 20, "request IDs should be unique across calls"


class TestInferenceResultImmutability:
    def test_frozen_dataclass(self):
        result = generate_output("test")
        with __import__("pytest").raises(AttributeError):
            result.output = "tampered"  # type: ignore[misc]
