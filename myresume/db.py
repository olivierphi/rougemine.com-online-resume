import functools
import logging
import tomllib
from typing import TYPE_CHECKING, Any, NotRequired

from . import settings

if TYPE_CHECKING:
    from datetime import date
    from typing import TypedDict

    from .domain import Lang

_logger = logging.getLogger(__name__)


@functools.cache
def pages() -> "list[PageData]":
    return _parse_data_file("pages.toml")["pages"]  # type: ignore


@functools.cache
def i18n(lang: "Lang") -> dict[str, dict[dict, str | list]]:
    return _parse_data_file("i18n.toml", lang=lang)  # type: ignore


@functools.cache
def document(lang: "Lang") -> "DocumentData":
    return _parse_data_file("document.toml", lang=lang)  # type: ignore


@functools.cache
def bio(lang: "Lang") -> "BioData":
    return _parse_data_file("bio.toml", lang=lang)  # type: ignore


@functools.cache
def tech() -> "TechnologiesData":
    return _parse_data_file("technologies.toml")  # type: ignore


@functools.cache
def job_experience(lang: "Lang") -> "JobExperiencesData":
    return _parse_data_file("job_experience.toml", lang=lang)  # type: ignore


@functools.cache
def projects(lang: "Lang") -> "ProjectsData":
    return _parse_data_file("projects.toml", lang=lang)  # type: ignore


def clear_cache() -> None:
    for cached_function in (pages, i18n, document, bio, tech, projects, job_experience):
        cached_function.cache_clear()  # type: ignore
    _logger.info("DB cache cleared")


if TYPE_CHECKING:

    class PageData(TypedDict):
        url_path: str
        target_static_html: str
        target_static_pdf: NotRequired[str]

    class DocumentData(TypedDict):
        subtitle: str
        meta: "DocumentMetaData"

    class DocumentMetaData(TypedDict):
        title: str
        description: str
        keywords: list[str]

    class BioData(TypedDict):
        name: str
        birth: "date"
        job_title: str
        email: str
        url: str
        mastodon: str
        github_id: str

    class TechnologiesData(TypedDict):
        main: list["MainTechnologyData"]
        others: list["OtherTechnologyData"]

    class MainTechnologyData(TypedDict):
        title: str
        icon: str
        url: NotRequired[str]

    class OtherTechnologyData(TypedDict):
        title: str
        icon: str
        url: NotRequired[str]
        contributor_url: NotRequired[str]
        not_on_pdf: NotRequired[bool]

    class JobExperiencesData(TypedDict):
        jobs: list["JobData"]

    class OrganisationData(TypedDict):
        name: str
        url: NotRequired[str]

    class JobData(TypedDict):
        period: str
        content: str
        organisation: NotRequired[OrganisationData]
        not_on_pdf: NotRequired[bool]
        current: NotRequired[bool]

    class ProjectsData(TypedDict):
        projects: list["ProjectData"]

    class ProjectData(TypedDict):
        title: str
        content: str
        not_on_pdf: NotRequired[bool]


def _parse_data_file(file_name: str, *, lang: "Lang | None" = None) -> Any:
    file_path = (
        settings.DATA_DIR / lang / file_name if lang else settings.DATA_DIR / file_name
    )
    with file_path.open("rb") as file:
        return tomllib.load(file)
