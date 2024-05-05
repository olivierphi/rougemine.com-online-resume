import argparse
import time
from pathlib import Path

from django.core.management.base import BaseCommand, CommandError
from PIL import Image, ImageOps

# _DEFAULT_COLOR = "lime"
_DEFAULT_COLOR = "rgb(134, 25, 143)"  # ~deep~ dark purple
_DEFAULT_SUFFIX = ".colorised"
_DEFAULT_DIR = "myresume/staticfiles/img/icons/techs/"


class Command(BaseCommand):
    help = "Create a grayscaled-and-recolorised version of our tech icons"

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
            if source_icon_path.stem.endswith(suffix):
                continue
            target_icon_path = source_icon_path.with_name(
                f"{source_icon_path.stem}{suffix}.png"
            )
            self.stdout.write(f"Colorising '{source_icon_path}'...")
            with Image.open(source_icon_path) as source_image:
                # Thanks StackOverflow! ^_^
                # @link https://stackoverflow.com/questions/12251896/colorize-image-while-preserving-transparency-with-pil#answer-12297772

                # 1. We convert the image to grayscale
                gray_version = ImageOps.grayscale(source_image)
                gray_version = ImageOps.autocontrast(gray_version)
                # 2. We colorise its black parts to the given colours, keeping the white parts white
                result = ImageOps.colorize(gray_version, colour, "#FFF")
                result.save(target_icon_path)

                colourised_images_counter += 1

        self.stdout.write(
            f"Colourised {colourised_images_counter} images in {time.monotonic()-start_time:.1f}s."
        )
