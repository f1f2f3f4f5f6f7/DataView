import os
import shutil
import tempfile


def save_upload_to_temp(contents: bytes, suffix: str = "") -> str:
    """
    Guarda bytes en un archivo temporal y devuelve su ruta.
    delete=False es obligatorio para que ExifTool pueda acceder al archivo.
    El llamador es responsable de eliminarlo con cleanup_file().
    """
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        tmp.write(contents)
        return tmp.name


def make_temp_dir() -> str:
    """Crea un directorio temporal y devuelve su ruta."""
    return tempfile.mkdtemp()


def cleanup_file(path: str) -> None:
    """Elimina un archivo si existe."""
    try:
        if path and os.path.exists(path):
            os.unlink(path)
    except OSError:
        pass


def cleanup_dir(path: str) -> None:
    """Elimina un directorio completo si existe."""
    try:
        if path and os.path.exists(path):
            shutil.rmtree(path)
    except OSError:
        pass