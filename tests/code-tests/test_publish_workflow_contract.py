from pathlib import Path


PUBLISH_WORKFLOW = Path(".github/workflows/publish.yml")


def test_publish_workflow_is_tag_only():
    text = PUBLISH_WORKFLOW.read_text(encoding="utf-8")

    assert 'tags:\n      - "v*"' in text
    assert "workflow_dispatch" not in text


def test_publish_workflow_matches_pypi_trusted_publisher_contract():
    text = PUBLISH_WORKFLOW.read_text(encoding="utf-8")

    assert "id-token: write" in text
    assert "environment: pypi" not in text
    assert "GITHUB_REF_NAME" in text
    assert "RELEASE_TAG" in text
    assert "if: github.event_name == 'push'" not in text
