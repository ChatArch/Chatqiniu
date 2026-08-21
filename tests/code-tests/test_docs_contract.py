from pathlib import Path

from chatstyle import render_click_tree

from chatqiniu.cli import main


ROOT = Path(__file__).resolve().parents[2]


def _text_blocks(path: Path) -> list[str]:
    text = path.read_text(encoding="utf-8")
    return [chunk.split("```", 1)[0].rstrip() for chunk in text.split("```text\n")[1:]]


def test_bilingual_cli_tree_docs_match_registered_full_and_brief_trees():
    expected = [
        render_click_tree(main, root_name="chatqiniu"),
        render_click_tree(main, root_name="chatqiniu", brief=True),
    ]

    for path in (ROOT / "docs" / "cli-tree.md", ROOT / "docs" / "cli-tree.en.md"):
        text = path.read_text(encoding="utf-8")
        assert "chatstyle.add_tree_option()" in text
        assert _text_blocks(path)[:2] == expected


def test_public_docs_expose_version_full_and_brief_tree_commands():
    paths = [
        ROOT / "README.md",
        ROOT / "README.en.md",
        ROOT / "docs" / "index.md",
        ROOT / "docs" / "index.en.md",
        ROOT / "docs" / "cli-tree.md",
        ROOT / "docs" / "cli-tree.en.md",
        ROOT / "DEVELOP.md",
    ]

    for path in paths:
        text = path.read_text(encoding="utf-8")
        assert "chatqiniu --version" in text, path
        assert "chatqiniu --tree" in text, path
        assert "chatqiniu --tree-brief" in text, path
