from pathlib import Path

from PIL import Image

from media_pipeline.pipeline import process_directory


def test_pipeline_detects_duplicate_and_writes_manifest(tmp_path: Path):
    source = tmp_path / "source"; output = tmp_path / "output"; source.mkdir()
    image = Image.new("RGB", (80, 40), "#336699")
    image.save(source / "Front View.png")
    image.save(source / "Front View Copy.png")
    manifest = process_directory(source, output, canvas=300)
    assert manifest["source_count"] == 2
    assert manifest["duplicate_count"] == 1
    assert (output / "manifest.json").is_file()
    assert (output / "contact-sheet.png").is_file()
