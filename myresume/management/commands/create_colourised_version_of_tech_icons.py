import argparse
import time
from pathlib import Path

from django.core.management.base import BaseCommand, CommandError
from PIL import Image, ImageOps

# _DEFAULT_COLOR = "lime" # for testing ^_^
_DEFAULT_COLOR = "rgb(134, 25, 143)"  # halfway between purple and pink :-)
_DEFAULT_SUFFIX = ".colorised"
_DEFAULT_DIR = "myresume/staticfiles/img/icons/techs/"


class Command(BaseCommand):
    help = "Create a greyscaled-and-recolourised version of our tech icons"

    def add_arguments(self, parser: argparse.ArgumentParser) -> None:
        parser.add_argument("--icons-dir", type=Path, default=_DEFAULT_DIR)
        parser.add_argument(
            "--colour",
            type=str,
            default=_DEFAULT_COLOR,
            help="Any format accepted by Pillow",
        )
        parser.add_argument(
            "--suffix",
            type=str,
            default=_DEFAULT_SUFFIX,
            help="Suffix to add to the filename of the colorised icons",
        )

    def handle(self, *args, icons_dir: Path, colour: str, suffix: str, **options):
        if not suffix:
            raise CommandError(
                "Suffix must not be empty (it would override the original icons)"
            )

        start_time = time.monotonic()
        colourised_images_counter = 0
        for source_icon_path in icons_dir.glob("*.png"):
            stem = source_icon_path.stem
            if stem.endswith(suffix):
                continue
            target_icon_path = source_icon_path.with_name(f"{stem}{suffix}.png")
            with Image.open(source_icon_path) as source_image:
                # Thanks StackOverflow! ^_^
                # @link https://stackoverflow.com/questions/12251896/colorize-image-while-preserving-transparency-with-pil#answer-12297772

                self.stdout.write(f"Colourising '{source_icon_path}'...")
                # 1. We convert the image to greyscale
                grey_version = ImageOps.grayscale(source_image)
                grey_version = ImageOps.autocontrast(grey_version)
                # 2. We colorise its black parts to the given colours, keeping the white parts white
                result = ImageOps.colorize(grey_version, colour, "#FFF")
                result.save(target_icon_path)

                colourised_images_counter += 1

        self.stdout.write(
            f"Colourised {colourised_images_counter} images in {time.monotonic()-start_time:.1f}s."
        )
