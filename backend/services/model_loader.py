from pathlib import Path


def detect_framework(file_path: str, fallback_framework: str) -> str:
    suffix = Path(file_path).suffix.lower()
    if suffix in {".pt", ".pth"}:
        return "pytorch"
    if suffix in {".h5"}:
        return "tensorflow"
    if suffix in {".onnx"}:
        return "onnx"
    if suffix in {".pkl"}:
        return "sklearn"
    return fallback_framework
