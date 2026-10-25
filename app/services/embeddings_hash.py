import hashlib
import math
import re
import unicodedata

DIM = 512


def _tokens(texto: str) -> list[str]:
    texto = unicodedata.normalize("NFD", texto.lower())
    texto = "".join(c for c in texto if unicodedata.category(c) != "Mn")
    palabras = re.findall(r"[a-z0-9]+", texto)
    # palabras + bigramas, para que el orden aporte algo
    return palabras + [f"{a}_{b}" for a, b in zip(palabras, palabras[1:])]


class HashEmbeddings:
    """Embeddings locales sin descargas (no importa LangChain: cumple la interfaz por duck typing): bolsa de palabras hasheada a 512 dimensiones.

    Es el plan B cuando el modelo de fastembed no se puede bajar (sin internet o
    bloqueado). Busca por palabras compartidas, no por significado.
    """

    def _vector(self, texto: str) -> list[float]:
        v = [0.0] * DIM
        for t in _tokens(texto):
            h = int(hashlib.md5(t.encode()).hexdigest(), 16)
            v[h % DIM] += 1.0 if (h >> 64) & 1 else -1.0
        norma = math.sqrt(sum(x * x for x in v)) or 1.0
        return [x / norma for x in v]

    def embed_documents(self, textos: list[str]) -> list[list[float]]:
        return [self._vector(t) for t in textos]

    def embed_query(self, texto: str) -> list[float]:
        return self._vector(texto)
