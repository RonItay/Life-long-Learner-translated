from pathlib import Path
import os
import shutil

from translator import translate
from file_collector import FileCollector
import asyncio

BASE_DIR = Path(os.getcwd()).parent
ORIGINAL_DIR = BASE_DIR / Path("original")
TRANSLATED_DIR = BASE_DIR / Path("translated")


async def main():
    # first copy all
    if Path(TRANSLATED_DIR).exists():
        shutil.rmtree(TRANSLATED_DIR)
    shutil.copytree(ORIGINAL_DIR, TRANSLATED_DIR)

    file_collector = FileCollector()
    files_to_translate = await file_collector.collect_md_files(TRANSLATED_DIR)

    translated = await translate(files_to_translate)

    await file_collector.write_files(translated)


if __name__ == "__main__":
    asyncio.run(main())
