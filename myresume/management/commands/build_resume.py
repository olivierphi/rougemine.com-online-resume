import argparse
import time

from django.conf import settings
from django.core import management
from django.core.management.base import BaseCommand
from django.test import Client

from ... import db

try:
    from djlint import reformat as djlint_reformat
except ImportError:
    djlint_reformat = None


class Command(BaseCommand):
    help = "Build resume's static files for deployment"

    def add_arguments(self, parser: argparse.ArgumentParser) -> None:
        parser.add_argument("--prettify", action="store_true")

    def handle(self, *args, prettify: bool, **options):
        settings.DIST_DIR.mkdir(exist_ok=True)

        self.stdout.write("Building Tailwind CSS file...")
        management.call_command("tailwind", "build")
        self.stdout.write("")

        self.stdout.write("Collecting static files...")
        management.call_command(
            "collectstatic", verbosity=0, interactive=False, clear=True
        )
        self.stdout.write("")

        # For some reason DjLint takes more than 20s per file 🤔
        # --> let's make that reformatting an opt-in feature.
        should_reformat = prettify and djlint_reformat
        djlint_config = djlint_reformat.Config("-") if should_reformat else None

        client = Client()
        for page in db.pages():
            self.stdout.write(
                f"Building '{self.style.SUCCESS(page['target_static_html'])}' file..."
            )

            response = client.get(page["url_path"])
            assert response.status_code == 200

            target_file_path = settings.DIST_DIR / page["target_static_html"]
            target_file_path.parent.mkdir(exist_ok=True)
            with target_file_path.open("wt") as f:
                html = response.content.decode()
                if should_reformat:
                    self.stdout.write("Reformatting page with djLint...")
                    start = time.monotonic()
                    html = djlint_reformat.formatter(djlint_config, html)
                    self.stdout.write(
                        f"Reformatting done - took {round(time.monotonic() - start,1)}s."
                    )
                self.stdout.write(
                    f"Writing file '{self.style.SUCCESS(page['target_static_html'])}'..."
                )
                f.write(html)
                self.stdout.write("")

        self.stdout.write(self.style.SUCCESS("Successfully built."))
