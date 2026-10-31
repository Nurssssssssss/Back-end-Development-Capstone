"""Screenshots from a genuine running Django app, NOT generated mock screenshots."""
import argparse
from pathlib import Path
from playwright.sync_api import sync_playwright

parser=argparse.ArgumentParser()
parser.add_argument('--base',default='http://127.0.0.1:8000')
parser.add_argument('--out',default='evidence')
a=parser.parse_args()
out=Path(a.out);out.mkdir(parents=True,exist_ok=True)
with sync_playwright() as p:
    browser=p.chromium.launch(headless=True,args=['--no-sandbox'])
    page=browser.new_page(viewport={'width':1360,'height':880},device_scale_factor=1)
    def shot(path,name):
        resp=page.goto(a.base.rstrip('/')+path,wait_until='domcontentloaded',timeout=30000)
        assert resp is not None and resp.status==200,(path,resp.status if resp else None)
        if page.locator('img').count():
            page.wait_for_function('Array.from(document.images).every(i => i.complete && i.naturalWidth > 0)')
        page.screenshot(path=str(out/name),type='jpeg',quality=90,full_page=True)
        print('CAPTURED:',out/name)
    shot('/','django-app-browser.jpg')
    resp=page.goto(a.base.rstrip('/')+'/songs/',wait_until='domcontentloaded')
    assert resp.status==200
    btn=page.get_by_role('button',name='View lyrics').first
    assert btn.count()>0, 'Songs page must contain a real song'
    btn.click()
    assert page.locator('dialog[open]').count()>0,'Modal must be opened'
    page.screenshot(path=str(out/'django-song-modal.jpg'),type='jpeg',quality=90,full_page=False)
    print('CAPTURED:',out/'django-song-modal.jpg')
    shot('/photos/','django-photos.jpg')
    assert page.locator('img').first.evaluate('(img) => img.complete && img.naturalWidth > 0'), 'Gallery photo must load'
    browser.close()
