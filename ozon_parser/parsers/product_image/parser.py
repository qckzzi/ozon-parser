from bs4 import BeautifulSoup


class ProductImagesParser:
    def __str__(self) -> str:
        return f"[{self.__class__.__name__}]"

    def parse(self, html: str) -> list[str]:
        soup: BeautifulSoup = BeautifulSoup(html, "html.parser")
        low_quality_image_links: list[str] = [x.attrs["src"] for x in soup.find_all("img", class_="ju b900-a")]
        hight_quality_image_links: list[str] = []

        for link in low_quality_image_links:
            start_index: int = link.find("/wc") + 3
            end_index: int = link.find("/", start_index)
            hight_quality_image_links.append(link[:start_index] + "1000" + link[end_index:])

        return hight_quality_image_links
