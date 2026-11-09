"""
Stage 2 of the pipeline: splitting documents into chunks.

⚠️ THIS IS THE FILE YOU CHANGE IN MILESTONE 3.

`split_documents` below is deliberately plain. It cuts every document into
fixed-size pieces with a fixed overlap and pays no attention to where sentences
or paragraphs end. It works, and it is not good.

On a corpus of short posts it may not cut anything at all: `campus_life` comes
out as 88 documents and 88 chunks, because almost nothing in it reaches 800
characters. That is the baseline, not a bug — Milestone 3 is where you decide
whether one post should stay one chunk.

Your job in Milestone 3 is to replace the *body* of `split_documents` with a
strategy that fits the documents you actually read in Milestone 1. Keep the
name and the shape of what it returns — the rest of the pipeline calls it, and
your README has to name the function that produced your chunks.

If you get stuck for 30 minutes, `fallback_split` is the original. Switch back
to it, write down what you saw, and move on. That's a real observation about
your pipeline, not giving up.
"""

from dataclasses import dataclass

import config
from ingest import Document


@dataclass
class Chunk:
    """One piece of one document."""

    text: str
    source: str        # which file it came from
    index: int         # which chunk within that file, starting at 0
    produced_by: str   # the function that made it — cite this in your README

    @property
    def label(self) -> str:
        return f"{self.source}#{self.index}"


def fallback_split(
    documents: list[Document],
    chunk_size: int | None = None,
    overlap: int | None = None,
) -> list[Chunk]:
    """
    The starter's original chunker. Fixed-size character windows with overlap.

    Keep this function. Milestone 3's stop rule points back at it, and having
    something to compare your own strategy against is useful in unit 2.
    """
    chunk_size = chunk_size or config.CHUNK_SIZE
    overlap = overlap or config.CHUNK_OVERLAP

    if overlap >= chunk_size:
        raise ValueError("overlap has to be smaller than chunk_size")

    chunks: list[Chunk] = []
    for doc in documents:
        start = 0
        index = 0
        while start < len(doc.text):
            piece = doc.text[start : start + chunk_size].strip()
            if piece:
                chunks.append(
                    Chunk(
                        text=piece,
                        source=doc.source,
                        index=index,
                        produced_by="chunker.py::fallback_split",
                    )
                )
                index += 1
            start += chunk_size - overlap

    return chunks


# Section-aware chunking for the city_guides corpus. Every guide is a short
# markdown file (~2,000 characters) divided by `## ` headings, and each section
# is a self-contained topic (e.g. "Eat and drink", "Getting there"). So the
# section is the chunk. No overlap: a section never continues into the next one,
# so there is no half-thought to carry across a boundary.
MIN_CHUNK = 150    # a section shorter than this is joined to the one after it
MAX_CHUNK = 1000   # a section longer than this is split on paragraph breaks


def _sections(text: str) -> tuple[str, list[tuple[str, str]]]:
    """Return (document title, [(heading, body), ...]) from one markdown guide."""
    title = ""
    sections: list[tuple[str, list[str]]] = [("", [])]
    for line in text.split("\n"):
        if line.startswith("## "):
            sections.append((line[3:].strip(), []))
        elif line.startswith("# ") and not title:
            title = line[2:].strip()
        else:
            sections[-1][1].append(line)
    return title, [(h, "\n".join(body).strip()) for h, body in sections]


def _split_long(body: str) -> list[str]:
    """Pack paragraphs into pieces of at most MAX_CHUNK characters."""
    pieces: list[str] = []
    current = ""
    for para in body.split("\n\n"):
        if current and len(current) + len(para) + 2 > MAX_CHUNK:
            pieces.append(current)
            current = para
        else:
            current = f"{current}\n\n{para}" if current else para
    if current:
        pieces.append(current)
    return pieces


def split_documents(documents: list[Document]) -> list[Chunk]:
    """
    Split each guide into one chunk per `##` section.

    Each chunk starts with "<guide title> — <section heading>" so it still says
    which town and topic it is about once it is separated from its document
    (without that, "Everything closes by 9pm" doesn't say where). Sections under
    MIN_CHUNK characters are merged into the next section; sections over
    MAX_CHUNK are split on paragraph breaks, repeating the heading line. A guide's
    intro paragraph (before its first heading) is joined to the first section.
    """
    chunks: list[Chunk] = []
    for doc in documents:
        title, sections = _sections(doc.text)

        # (heading, body) pairs, with too-short sections carried into the next.
        merged: list[tuple[str, str]] = []
        carry_heading, carry_body = "", ""
        for heading, body in sections:
            if not body and not carry_body:
                continue  # the empty text before the first heading
            heading = f"{carry_heading} / {heading}" if carry_heading and heading else (heading or carry_heading)
            body = f"{carry_body}\n\n{body}".strip() if carry_body else body
            if len(body) < MIN_CHUNK or not heading:
                carry_heading, carry_body = heading, body
            else:
                merged.append((heading, body))
                carry_heading, carry_body = "", ""
        if carry_body:  # a short final section: attach to the previous chunk
            if merged:
                h, b = merged[-1]
                merged[-1] = (h, f"{b}\n\n{carry_body}")
            else:
                merged.append((carry_heading, carry_body))

        index = 0
        for heading, body in merged:
            label = f"{title} — {heading}" if heading else title
            for piece in _split_long(body):
                chunks.append(
                    Chunk(
                        text=f"{label}\n\n{piece}",
                        source=doc.source,
                        index=index,
                        produced_by="chunker.py::split_documents",
                    )
                )
                index += 1
    return chunks


def describe(chunks: list[Chunk]) -> str:
    """A one-line summary, printed after indexing."""
    if not chunks:
        return "0 chunks"
    lengths = [len(c.text) for c in chunks]
    return (
        f"{len(chunks)} chunks, "
        f"{sum(lengths) // len(lengths)} characters on average "
        f"(shortest {min(lengths)}, longest {max(lengths)}), "
        f"produced by {chunks[0].produced_by}"
    )


if __name__ == "__main__":
    from ingest import load_documents

    chunks = split_documents(load_documents())
    print(describe(chunks))
