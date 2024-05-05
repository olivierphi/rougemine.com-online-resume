import re
from textwrap import dedent
from typing import TYPE_CHECKING

from django import template
from django.conf import settings
from django.templatetags.static import static
from django.utils.safestring import mark_safe

from .. import theme

if TYPE_CHECKING:
    from typing import Final

    from myresume.db import MainTechnologyData, OtherTechnologyData

register = template.Library()


_THEME: "Final[dict[str, str]]" = {
    "META_THEME_COLOR": theme.META_THEME_COLOR,
    "BODY": str(theme.BODY),
    "TITLE": str(theme.TITLE),
    "SUBTITLE": str(theme.SUBTITLE),
    "BLOCK_ABOUT": str(theme.BLOCK_ABOUT),
    "MAIN_SECTION_TITLE": str(theme.MAIN_SECTION_TITLE),
    "MAIN_SECTION_TITLE_ICON": str(theme.MAIN_SECTION_TITLE_ICON),
    "HIGHLIGHT": str(theme.HIGHLIGHT),
}

_SVG_ICONS_PATH = settings.BASE_DIR / "myresume" / "assets-src" / "img" / "icons"
_SVG_ICONS_ROOT_ELEMENT_PATTERN = re.compile(r"""<svg +(?P<attrs>[^>]+)>""")
_CONTENT_LINK_PATTERN = re.compile(r"""<a +(?P<href>href="https://[^"]+") *>""")
_JOB_CONTENT_COMPANY_NAME_PATTERN = re.compile(r"<b>")
_PROJECT_CONTENT_TECH_PATTERN = re.compile(
    r"""<span +class="tech +tech-with-icon +(?P<tech>\w+)" *>"""
)

_HIGHLIGHT_CLASSES = f"font-medium {_THEME['HIGHLIGHT']}"


@register.simple_tag
def svg_icon(icon: str, *, classes: str = "size-6"):
    icon_content = (_SVG_ICONS_PATH / f"{icon}.svg").read_text()
    return mark_safe(
        _SVG_ICONS_ROOT_ELEMENT_PATTERN.sub(
            rf"""<svg \g<attrs> class="{classes}">""",
            icon_content,
        )
    )


@register.simple_tag
def about_section_icon(icon: str):
    return mark_safe(f'<img src="{static(icon)}" width="40" height="40" alt="">')


@register.simple_tag(name="theme")
def theme_element(*, element_id: str) -> str:
    return _THEME[element_id]


@register.simple_tag
def layout_debug(*, border_color: str) -> str:
    if not settings.DEBUG_LAYOUT:
        return ""
    return f"border border-solid border-{border_color}"


@register.simple_tag
def about_section_title(title: str):
    return mark_safe(
        f'<h4 class="text-lg mt-1 mb-2 print:text-base print:mt-0 print:mb-1">{title}</h4>'
    )


@register.inclusion_tag("myresume/main/tags/main_section_title.html")
def main_section_title(title: str, *, icon: str):
    return {
        "title": title,
        "icon": icon,
    }


@register.inclusion_tag("myresume/main/tags/main_tech.html")
def main_section_main_tech(tech: "MainTechnologyData") -> dict:
    return tech | {
        "icon_url": static(f"img/icons/techs/{tech['icon']}.colorised.png"),
    }


@register.inclusion_tag("myresume/main/tags/other_tech.html")
def main_section_other_tech(tech: "OtherTechnologyData") -> dict:
    return tech | {
        "icon_url": static(f"img/icons/techs/{tech['icon']}.colorised.png"),
    }


@register.simple_tag
def tech_with_schema(*, title: str, url: str | None = None) -> str:
    if url:
        url_part = f"""<meta itemprop="url" content="{url}" />"""
    else:
        url_part = ""

    return mark_safe(
        dedent(
            f"""<span itemprop="knowsAbout" itemscope itemtype="https://schema.org/SoftwareApplication">
                <span itemprop="name">{ title }</span>
                {url_part}
            </span>"""
        )
    )


@register.filter
def processed_job_content(content: str) -> str:
    content = _CONTENT_LINK_PATTERN.sub(
        r"""<a \g<href> class="underline" target="_blank" rel="noopener">""",
        content,
    )
    content = _JOB_CONTENT_COMPANY_NAME_PATTERN.sub(
        rf"""<b class="{_HIGHLIGHT_CLASSES}">""",
        content,
    )
    return content


@register.filter
def processed_project_content(content: str) -> str:
    content = _CONTENT_LINK_PATTERN.sub(
        r"""<a \g<href> class="underline" target="_blank" rel="noopener">""",
        content,
    )

    content = _PROJECT_CONTENT_TECH_PATTERN.sub(
        _process_project_tech_pattern,
        content,
    )

    return content


def _process_project_tech_pattern(match: re.Match) -> str:
    return (
        f"""<span class="{_HIGHLIGHT_CLASSES} text-nowrap font-semibold">"""
        # We no longer include the tech icons in the project content,
        # to make it more readable. Uncomment the following lines to include them.
        # f"""<img src="{static(f"img/icons/techs/{match['tech']}.png")}" """
        # """class="size-4 inline-block" width="16" height="16" alt=""> """
    )
