"""Unit tests for error-handling helpers."""

from unittest.mock import MagicMock

from app.core.errors import _validation_message, error_response


class TestErrorResponse:
    def test_returns_json_response(self):
        resp = error_response("invalid_request", "bad input", 422)
        assert resp.status_code == 422

    def test_body_structure(self):
        resp = error_response("not_found", "resource not found", 404)
        body = resp.body.decode()
        import json

        parsed = json.loads(body)
        assert parsed == {
            "error": {
                "code": "not_found",
                "message": "resource not found",
            }
        }

    def test_500_error_response(self):
        resp = error_response("internal_error", "internal server error", 500)
        assert resp.status_code == 500


class TestValidationMessage:
    def _make_exc(self, errors: list[dict]) -> MagicMock:
        exc = MagicMock()
        exc.errors.return_value = errors
        return exc

    def test_missing_prompt(self):
        exc = self._make_exc(
            [{"loc": ("body", "prompt"), "type": "missing", "msg": "Field required"}]
        )
        assert _validation_message(exc) == "prompt is required"

    def test_wrong_type_prompt(self):
        exc = self._make_exc(
            [{"loc": ("body", "prompt"), "type": "string_type", "msg": "Input should be a valid string"}]
        )
        assert _validation_message(exc) == "prompt must be a string"

    def test_value_error_message(self):
        exc = self._make_exc(
            [{"loc": ("body", "prompt"), "type": "value_error", "msg": "Value error, prompt must not be empty"}]
        )
        assert _validation_message(exc) == "prompt must not be empty"

    def test_generic_fallback(self):
        exc = self._make_exc([])
        assert _validation_message(exc) == "invalid request"

    def test_non_prompt_field_with_custom_message(self):
        exc = self._make_exc(
            [{"loc": ("body", "other"), "type": "value_error", "msg": "some custom error"}]
        )
        assert _validation_message(exc) == "some custom error"
