from datetime import datetime
from bs4 import BeautifulSoup


def clean_records(rows: list):
    """
    Fix broken table rows where marathon count
    appears in the next row (split row issue).
    """
    cleaned = []
    i = 0

    while i < len(rows):
        row = rows[i]

        if not row or len(row) < 2:
            i += 1
            continue

        name = row[0].strip()
        gender = row[1].strip()

        # Detect continuation row
        if name == '"' or gender.isdigit():
            if cleaned:
                prev = cleaned[-1]

                # Fix marathon count
                if gender.isdigit():
                    prev[4] = gender

                # Fix stars column
                if len(row) > 2 and row[2].strip():
                    prev[5] = row[2].strip()

            i += 1
            continue

        cleaned.append(row)
        i += 1

    return cleaned


def extract_legends(raw_json):
    """
    Extract and structure Legends Club data from raw website JSON.
    """

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

        rows = table.find_all("tr")[1:]

        raw_rows = []
        for row in rows:
            cols = [col.text.strip() for col in row.find_all("td")]
            if cols:
                raw_rows.append(cols)

        cleaned_rows = clean_records(raw_rows)

        for cols in cleaned_rows:
            if len(cols) < 6:
                continue

            record = {
                "NAME": cols[0],
                "GENDER": cols[1],
                "CITY": cols[2],
                "STATE": cols[3].replace('"', '').strip(),
                "NO. OF MARATHONS": int(cols[4]) if cols[4].isdigit() else None,
                "STARS": cols[5],
                "YEAR": year
            }

            records.append(record)

    return year, records
