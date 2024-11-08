import csv
import json
import os.path
from abc import ABC, abstractmethod
from io import StringIO


class ExportStrategy(ABC):
    @abstractmethod
    def export(self, participation_id: int, data: list) -> str: ...


class CSVExportStrategy(ExportStrategy):
    def export(self, participation_id: int, data: list[dict]) -> str:
        filename = f"{participation_id}_results.csv"
        file_path = os.path.join("/tmp", filename)  # noqa: PTH118, S108

        output = StringIO()
        writer = csv.writer(output)
        writer.writerow(
            ["company_user_id", "company_id", "quiz_id", "correct_answers"]
        )

        for result in data:
            writer.writerow(
                [
                    result["company_user_id"],
                    result["company_id"],
                    result["quiz_id"],
                    result["correct_answers"],
                ]
            )

        with open(file_path, "w", encoding="utf-8") as f:  # noqa: PTH123
            f.write(output.getvalue())

        return file_path


class JSONExportStrategy(ExportStrategy):
    def export(self, participation_id: int, data: list) -> str:
        filename = f"{participation_id}_results.json"
        file_path = os.path.join("/tmp", filename)  # noqa: PTH118, S108

        export_data = {"result": data}

        with open(file_path, "w", encoding="utf-8") as file:  # noqa: PTH123
            json.dump(export_data, file, ensure_ascii=False, indent=4)

        return file_path


class ExportContext:
    def __init__(self, strategy: ExportStrategy):
        self._strategy = strategy

    def set_strategy(self, strategy: ExportStrategy):
        self._strategy = strategy

    def export(self, participation_id: int, data: list) -> str:
        return self._strategy.export(participation_id, data)
