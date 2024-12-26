import urllib.parse

import aiohttp
import asyncio
import dataclasses
import logging

from file_collector import FileData


logger = logging.getLogger(__name__)


@dataclasses.dataclass
class TranslatedFragment:
    filename: str
    index: int
    data: str


class Translator:
    URL = "https://translate.googleapis.com/translate_a/single"
    newline_encoding = urllib.parse.quote("\n")

    BLOCK_MAX_SIZE = 2000

    def _get_params(self, text: str):
        return {
            "client": "gtx",
            "sl": "auto",
            "tl": "en",
            "dt": "t",
            "q": text.replace("\n", self.newline_encoding),
        }

    def __init__(self, session):
        self.session = session

    async def async_translate_file_fragment(self, path, index, to_translate: str):
        async with self.session.get(
            self.URL, params=self._get_params(to_translate)
        ) as translation_result:

            translation_signature = f"{path} {index}"

            logger.debug(f"sending {translation_signature}")
            translation_result = await translation_result.json()
            logger.debug(f"received {translation_signature}")
            translated_text = ""
            for translated in translation_result[0]:
                translated_text += translated[0]

            return TranslatedFragment(
                filename=path,
                index=index,
                data=translated_text.replace(self.newline_encoding, "\n"),
            )

    def _generate_tasks(self, files: list[FileData]):
        tasks = []
        for file_data in files:
            blocks = self._get_blocks(file_data.data)
            tasks += [
                self.async_translate_file_fragment(file_data.path, index, blocks[index])
                for index in range(len(blocks))
            ]
        return tasks

    async def translate(self, files: list[FileData]) -> list[FileData]:
        tasks = self._generate_tasks(files)
        results: list[TranslatedFragment] = await asyncio.gather(*tasks)

        # sort by files and then by index
        sorted_results: dict[str, list[TranslatedFragment]] = {}
        for result in results:
            try:
                sorted_results[result.filename].append(result)
            except KeyError:
                sorted_results[result.filename] = [result]

        translated_files = []
        for translated_file in sorted_results.values():
            filename = translated_file[0].filename
            translated_file.sort(key=lambda x: x.index)

            # merge results
            translated_files.append(
                FileData(
                    path=filename,
                    data=" ".join([fragment.data for fragment in translated_file]),
                )
            )

        return translated_files

    async def async_translate(self, text):
        translation_blocks = self._get_blocks(text)
        tasks = [self._translate_block(block) for block in translation_blocks]
        results = await asyncio.gather(*tasks)

        return " ".join(results)

    async def _translate_block(self, text):
        async with self.session.get(
            self.URL, params=self._get_params(text)
        ) as translation_result:
            translation_result = await translation_result.json()
            translated_text = ""
            for translated in translation_result[0]:
                translated_text += translated[0]

            return translated_text.replace(self.newline_encoding, "\n")

    def _get_blocks(self, text: str):
        text_left = text
        blocks = []
        while text_left:
            if len(text_left) < self.BLOCK_MAX_SIZE:
                blocks.append(text_left)
                text_left = ""
            else:
                potential_block = text_left[: self.BLOCK_MAX_SIZE]
                # find last space
                last_space_index = self.BLOCK_MAX_SIZE - potential_block[::-1].find(" ")
                blocks.append(text_left[:last_space_index])
                text_left = text_left[last_space_index:]

        return blocks


async def translate(text):
    async with aiohttp.ClientSession() as session:
        translator = Translator(session)
        return await translator.translate(text)
