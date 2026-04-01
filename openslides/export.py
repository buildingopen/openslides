"""
Export Engine
HTML slides -> PDF, PNG, PPTX via Playwright.
"""
from __future__ import annotations

import asyncio
import tempfile
from pathlib import Path

from PyPDF2 import PdfReader, PdfWriter
from PyPDF2.generic import (
    ArrayObject, DictionaryObject, NameObject, NumberObject, TextStringObject,
)


class ExportEngine:
    """
    Export slides to PDF/PNG/PPTX.

    Usage:
        async with ExportEngine() as engine:
            pdf = await engine.export_pdf(slides, "./deck.pdf")
            pngs = await engine.export_png(slides, "./pngs/")
    """

    def __init__(self, width: int = 1920, height: int = 1080):
        self.width = width
        self.height = height
        self._pw = None
        self._browser = None

    async def _browser_instance(self):
        if self._browser is None:
            from playwright.async_api import async_playwright
            self._pw = await async_playwright().start()
            import shutil
            chrome_path = shutil.which("google-chrome-stable") or shutil.which("google-chrome") or shutil.which("chromium")
            launch_kwargs = {"headless": True}
            if chrome_path:
                launch_kwargs["executable_path"] = chrome_path
            self._browser = await self._pw.chromium.launch(**launch_kwargs)
        return self._browser

    async def export_pdf(
        self,
        slides: list[str],
        output_path: str | Path,
        links: list[dict] | None = None,
    ) -> Path:
        """
        Export slides as a single merged PDF with proper text rendering.

        Each slide is rendered to PDF via Playwright's page.pdf() (preserves text),
        then merged with PyPDF2. Optionally adds clickable link annotations.

        Args:
            slides: list of HTML strings
            output_path: destination PDF path
            links: optional list of {"page": int, "x1", "y1", "x2", "y2", "url"}
        """
        output_path = Path(output_path).expanduser()
        output_path.parent.mkdir(parents=True, exist_ok=True)

        browser = await self._browser_instance()

        with tempfile.TemporaryDirectory() as tmpdir:
            pdf_paths = []
            for i, html in enumerate(slides):
                page = await browser.new_page(
                    viewport={"width": self.width, "height": self.height}
                )
                await page.set_content(html, wait_until="networkidle")
                # Wait for fonts
                await page.evaluate("() => document.fonts.ready")
                await page.evaluate('async () => { await document.fonts.load("400 48px \\"DM Serif Display\\"").catch(() => {}); }')

                pdf_path = Path(tmpdir) / f"slide-{i:02d}.pdf"
                await page.pdf(
                    path=str(pdf_path),
                    width=f"{self.width}px",
                    height=f"{self.height}px",
                    margin={"top": "0", "right": "0", "bottom": "0", "left": "0"},
                    print_background=True,
                    prefer_css_page_size=True,
                )
                await page.close()
                pdf_paths.append(pdf_path)

            # Merge PDFs
            writer = PdfWriter()
            for pdf_path in pdf_paths:
                for pg in PdfReader(str(pdf_path)).pages:
                    writer.add_page(pg)

            # Add link annotations
            if links:
                for link in links:
                    _add_pdf_link(
                        writer,
                        page_index=link["page"],
                        x1=link["x1"],
                        y1=link["y1"],
                        x2=link["x2"],
                        y2=link["y2"],
                        url=link["url"],
                    )

            with open(output_path, "wb") as f:
                writer.write(f)

        return output_path

    async def export_png(
        self,
        slides: list[str],
        output_dir: str | Path,
        prefix: str = "slide",
    ) -> list[Path]:
        """Export each slide as PNG."""
        output_dir = Path(output_dir).expanduser()
        output_dir.mkdir(parents=True, exist_ok=True)

        browser = await self._browser_instance()
        paths = []

        for i, html in enumerate(slides, 1):
            page = await browser.new_page(
                viewport={"width": self.width, "height": self.height}
            )
            await page.set_content(html, wait_until="networkidle")
            await page.evaluate("() => document.fonts.ready")

            path = output_dir / f"{prefix}-{i:02d}.png"
            await page.screenshot(path=str(path), full_page=False, type="png")
            await page.close()
            paths.append(path)

        return paths

    async def close(self):
        if self._browser:
            await self._browser.close()
            self._browser = None
        if self._pw:
            await self._pw.stop()
            self._pw = None

    async def __aenter__(self):
        return self

    async def __aexit__(self, *_):
        await self.close()


def export_pdf_sync(slides: list[str], output_path: str | Path, links: list[dict] | None = None) -> Path:
    """Synchronous PDF export."""
    return asyncio.run(_async_export_pdf(slides, output_path, links))


def export_png_sync(slides: list[str], output_dir: str | Path) -> list[Path]:
    """Synchronous PNG export."""
    return asyncio.run(_async_export_png(slides, output_dir))


async def _async_export_pdf(slides, output_path, links):
    async with ExportEngine() as engine:
        return await engine.export_pdf(slides, output_path, links)


async def _async_export_png(slides, output_dir):
    async with ExportEngine() as engine:
        return await engine.export_png(slides, output_dir)


def export_pptx(slides: list[str], output_path: str | Path) -> Path:
    """
    Export slides as PPTX.

    Creates a simplified PPTX from HTML slides. Each slide becomes an image
    embedded in a PowerPoint slide (preserves exact visual layout).
    """
    from pptx import Presentation
    from pptx.util import Inches, Emu

    output_path = Path(output_path).expanduser()
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # First render to PNGs
    with tempfile.TemporaryDirectory() as tmpdir:
        pngs = export_png_sync(slides, tmpdir)

        prs = Presentation()
        # Set slide dimensions to 16:9
        prs.slide_width = Emu(12192000)   # 10 inches * 914400
        prs.slide_height = Emu(6858000)   # 7.5 inches * 914400

        blank_layout = prs.slide_layouts[6]  # blank layout

        for png_path in pngs:
            slide = prs.slides.add_slide(blank_layout)
            slide.shapes.add_picture(
                str(png_path),
                left=Emu(0),
                top=Emu(0),
                width=prs.slide_width,
                height=prs.slide_height,
            )

        prs.save(str(output_path))

    return output_path


def _add_pdf_link(writer: PdfWriter, page_index: int, x1: float, y1: float, x2: float, y2: float, url: str):
    """Add a clickable link annotation to a PDF page."""
    if page_index >= len(writer.pages):
        return
    page = writer.pages[page_index]
    link = DictionaryObject({
        NameObject("/Type"): NameObject("/Annot"),
        NameObject("/Subtype"): NameObject("/Link"),
        NameObject("/Rect"): ArrayObject([
            NumberObject(int(x1)), NumberObject(int(y1)),
            NumberObject(int(x2)), NumberObject(int(y2)),
        ]),
        NameObject("/Border"): ArrayObject([
            NumberObject(0), NumberObject(0), NumberObject(0),
        ]),
        NameObject("/A"): DictionaryObject({
            NameObject("/S"): NameObject("/URI"),
            NameObject("/URI"): TextStringObject(url),
        }),
    })
    if "/Annots" not in page:
        page[NameObject("/Annots")] = ArrayObject()
    page[NameObject("/Annots")].append(link)
