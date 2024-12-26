import dataclasses
import os
import asyncio


@dataclasses.dataclass
class FileData:
    path: str
    data: str


class FileCollector:
    async def collect_md_files(self, path):
        files = self._get_md_files(path)
        read_operations = [self.async_collect_file(path) for path in files]

        return await asyncio.gather(*read_operations)

    async def async_collect_file(self, path):
        with open(path, "r") as f:
            return FileData(path=path, data=f.read())

    def _get_md_files(self, path):
        files = []
        for root, dirs, filenames in os.walk(path):
            for filename in filenames:
                if not filename.endswith(".md"):
                    continue
                files.append(os.path.join(root, filename))

        return files

    async def async_write_file(self, file_data: FileData):
        with open(file_data.path, "w") as f:
            f.write(file_data.data)

    async def write_files(self, files: list[FileData]):
        tasks = [self.async_write_file(file_data) for file_data in files]

        return await asyncio.gather(*tasks)
