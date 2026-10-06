from PIL import Image

from media_pipeline.images import difference_hash, normalize, slugify


def test_slugify_is_filesystem_safe():
    assert slugify("Produto Café / Azul") == "produto-cafe-azul"


def test_normalize_uses_stable_canvas():
    image = Image.new("RGB", (800, 400), "white")
    result = normalize(image, canvas=600, margin=50)
    assert result.size == (600, 600)
    assert result.mode == "RGB"


def test_difference_hash_matches_identical_pixels():
    first = Image.new("RGB", (20, 20), "red")
    second = first.copy()
    assert difference_hash(first) == difference_hash(second)
