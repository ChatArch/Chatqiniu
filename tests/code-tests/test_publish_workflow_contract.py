from pathlib import Path


PUBLISH_WORKFLOW = Path(".github/workflows/publish.yml")
CI_WORKFLOW = Path(".github/workflows/ci.yml")


def test_publish_workflow_is_tag_only():
    text = PUBLISH_WORKFLOW.read_text(encoding="utf-8")

    assert 'tags:\n      - "v*"' in text
    assert "workflow_dispatch" not in text


def test_publish_workflow_matches_pypi_trusted_publisher_contract():
    text = PUBLISH_WORKFLOW.read_text(encoding="utf-8")

    assert "id-token: write" in text
    assert "environment: pypi" not in text
    assert "git fetch --no-tags origin main:refs/remotes/origin/main" in text
    assert 'git merge-base --is-ancestor "${GITHUB_SHA}" refs/remotes/origin/main' in text
    assert "GITHUB_REF_NAME" in text
    assert "RELEASE_TAG" in text
    assert "if: github.event_name == 'push'" not in text


def test_ci_checks_installed_full_and_brief_trees_and_distributions():
    text = CI_WORKFLOW.read_text(encoding="utf-8")

    assert 'python-version: ["3.10", "3.11", "3.12"]' in text
    assert "chatqiniu --version" in text
    assert "chatqiniu --tree" in text
    assert "chatqiniu --tree-brief" in text
    assert "python -m build" in text
    assert "python -m twine check dist/*" in text
    assert '"$RUNNER_TEMP/chatqiniu-wheel/bin/python" -m pip install dist/*.whl' in text
    assert "mkdocs build --strict" in text
