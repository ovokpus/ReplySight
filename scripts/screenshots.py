"""Headless Playwright screenshots of the running stack (docker compose up) -> docs/screenshots/.
Runs WITHOUT an OpenAI/Tavily key, so the reply screen shows the real no-key error, not a generated reply."""
import json
import urllib.request
from pathlib import Path

from playwright.sync_api import sync_playwright

OUT = Path(__file__).resolve().parent.parent / 'docs' / 'screenshots'
UI, API = 'http://localhost:3000', 'http://localhost:8000'


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as p:
        b = p.chromium.launch()
        pg = b.new_page(viewport={'width': 1366, 'height': 900}, device_scale_factor=2)
        for path, name in [('/', 'chat'), ('/workflow', 'workflow')]:
            pg.goto(UI + path, wait_until='load'); pg.wait_for_timeout(3000)
            pg.screenshot(path=OUT / f'{name}.png', full_page=True)
        pg.goto(UI + '/', wait_until='load'); pg.wait_for_timeout(2000)
        pg.locator('textarea').first.fill('My new earbuds stopped charging after two days and I need them for a flight tomorrow.')
        pg.locator('button[type=submit]').first.click()
        pg.wait_for_timeout(15000)
        pg.screenshot(path=OUT / 'chat-no-key.png', full_page=True)
        pg.goto(API + '/docs'); pg.wait_for_selector('.opblock')
        pg.screenshot(path=OUT / 'api-docs.png')
        b.close()
    samples = {u: json.load(urllib.request.urlopen(API + u)) for u in ['/health', '/workflow/graph']}
    (OUT / 'api-samples.json').write_text(json.dumps(samples, indent=2, default=str))


if __name__ == '__main__':
    main()
