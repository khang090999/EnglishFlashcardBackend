import pathlib
import re

from django.conf import settings

import mistune

H_LEVEL = 2
VERSION_FORMAT = r"\d{1,2}\.\d{1,2}\.\d{1,3}$"


class ChangelogRenderer(mistune.HTMLRenderer):
    """Renderer for changelog page.

    It expects style like `## X.Y.Z` for versions in changelog.

    """

    def heading(self, text: str, level: int, **attrs) -> str:
        """Override to add anchors for changelog versions headers."""
        if re.fullmatch(VERSION_FORMAT, text) and level == H_LEVEL:
            tag = f"h{level}"
            anchor = f"{text.replace('.', '').lower()}"
            return f"<{tag} id={anchor}><a href=#{anchor}>{text}</a></{tag}>"

        return super().heading(text, level, **attrs)


def get_changelog_html(changelog_name: str) -> str:
    """Convert changelog text to html."""
    changelog_path = pathlib.Path(f"{settings.BASE_DIR}/docs/{changelog_name}")
    if not changelog_path.exists():
        return ""  # pragma: no cover

    with pathlib.Path(changelog_path).open() as file:
        changelog = file.read()

    markdown = mistune.create_markdown(renderer=ChangelogRenderer())
    return markdown(changelog)


def get_latest_version(changelog_filepath: str) -> str:
    """Get latest version from changelog file.

    Args:
        changelog_filepath (str):Path to changelog file

    Raises:
        ValueError: if we couldn't find any versions in changelog file

    """
    atx = "#" * H_LEVEL
    version_regex = rf"(?<=^{atx} ){VERSION_FORMAT}$"
    re_rule = re.compile(version_regex)

    with pathlib.Path(f"docs/{changelog_filepath}").open() as file:
        for line in file:
            search = re_rule.search(line)
            if search:
                return search.group()

    raise ValueError(  # pragma: no cover
        "Incorrect changelog file, couldn't find version number for "
        f"{changelog_filepath}",
    )


def get_git_hash() -> str:
    """Get current git commit hash of deployed app.

    .git_hash file is generated before buildpack image is built during
    deployment and contains the current git commit hash.

    """
    git_hash_path = pathlib.Path(f"{settings.BASE_DIR}/.git_hash")
    return (
        git_hash_path.read_text().strip()
        if git_hash_path.exists()
        else "unknown"
    )
