import asyncio
from playwright.async_api import async_playwright
from datetime import datetime
import pandas as pd
urls = [""]

async def process_page(page, url):
    await page.goto(url)
    await page.wait_for_timeout(3000)
    content = await page.inner_text("article")
    result = await extract_elements(content.split("\n"))  
    result['url'] = url  # url도 같이 저장
    return result

async def run():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        results = []
        for url in urls:
            res = await process_page(page, url)
            results.append(res)

        await browser.close()

    to_excel(results)


async def extract_elements(content):
    result = {
        "id" : None,
        "time": None,
        "mention": None,
        "views_info": []
    }

    datetime_str = None
    clean_string = []
    words = [e.strip() for e in content]
    for word in words:
        # id 찾기
        if word.startswith("@"):
            result["id"] = word
        # 날짜 변환
        if "AM" in word or "PM" in word:
            if "·" in word and "," in word:
                datetime_str = word.strip()
                # datetime 객체로 변환
                if datetime_str:
                    clean_dt = " ".join([x.strip() for x in datetime_str.split("·")])
                    dt = datetime.strptime(clean_dt, "%I:%M %p %b %d, %Y")
                    result["time"] = dt.strftime("%Y-%m-%d %H:%M:%S")

        if "Views" in word:
            idx = words.index("Views")
            filtered = words[idx-1:idx+3]
            filtered.remove("Views")
            result["views_info"] = filtered
        
        if "Translate post" in word:
            idx = words.index("Translate post")
            clean_string = words[2:idx]
            result["mention"] = '\n'.join([e.strip() for e in clean_string if e.strip()])

    return result


def to_excel(data_list):
    rows = []
    for data in data_list:
        views_values = data.get("views_info", [None, None, None])
        row = {
        "멘션" : data.get("mention"),
        "게재 URL" : data.get("url"),
        "계정": data.get("id"),
        "게시날짜": data.get("time"),
        "조회수": views_values[0],
        "재게시": views_values[1],
        "좋아요": views_values[2]
        } 
        rows.append(row)

    df = pd.DataFrame(rows)
    df.insert(0, "No", range(1, len(df) + 1))
    df.to_excel("test.xlsx", index=False)


asyncio.run(run())
