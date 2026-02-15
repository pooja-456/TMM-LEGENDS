from datetime import datetime
from bs4 import BeautifulSoup


def extract_legends(raw_json):

    published = raw_json["props"]["pageProps"]["LegendsClubData"]["publishedAt"]
    year = datetime.fromisoformat(published.replace("Z", "")).year

    legends_blocks = raw_json["props"]["pageProps"]["LegendsClubData"]["legendsClub"]

    records = []

    for block in legends_blocks:

        if block.get("tabName") != "Overall":
            continue

        table_html = block.get("content")

        soup = BeautifulSoup(table_html, "html.parser")
        table = soup.find("table")

        if not table:
            continue

        rows = table.find_all("tr")[1:]  # skip header

        for row in rows:
            cols = [col.text.strip() for col in row.find_all("td")]

            if len(cols) < 6:
                continue

            record = {
                "NAME": cols[0],
                "GENDER": cols[1],
                "CITY": cols[2],
                "STATE": cols[3],
                "NO. OF MARATHONS": int(cols[4]) if cols[4].isdigit() else None,
                "STARS": cols[5],
                "YEAR": year
            }

            records.append(record)

    return year, records
