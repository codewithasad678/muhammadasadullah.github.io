#!/usr/bin/env python3
"""Stamp a new site version (automatic cache-buster).

Run this before every commit/push:   python3 scripts/bump-version.py

It writes one new version number to:
  - version.json                     (the live site checks this file and reloads itself when it changes)
  - index.html                       (<meta name="site-version"> and SITE_VERSION in the script)
  - ?v=<version> on local images, icons, manifest and the CV link (so browsers fetch the new files)
  - sitemap.xml <lastmod> and the structured-data dateModified
"""
import datetime, json, pathlib, re

root = pathlib.Path(__file__).resolve().parent.parent
now = datetime.datetime.now(datetime.timezone.utc)
version = now.strftime('%Y%m%d%H%M')
today = now.strftime('%Y-%m-%d')

html_path = root / 'index.html'
html = html_path.read_text(encoding='utf-8')

html = re.sub(r'(<meta name="site-version" content=")[^"]*(")', lambda m: m.group(1) + version + m.group(2), html)
html = re.sub(r"(const SITE_VERSION = ')[^']*(')", lambda m: m.group(1) + version + m.group(2), html)

asset = re.compile(
    r'((?:src|href|content)=")'
    r'((?:https://muhammadasadullah\.com/)?(?:images/[^"?#]+|favicon\.svg|site\.webmanifest|Muhammad-Asadullah-CV\.pdf))'
    r'(?:\?v=[^"]*)?(")'
)
html = asset.sub(lambda m: f'{m.group(1)}{m.group(2)}?v={version}{m.group(3)}', html)
html = re.sub(r'("dateModified": ")[^"]*(")', lambda m: m.group(1) + today + m.group(2), html)
html_path.write_text(html, encoding='utf-8')

(root / 'version.json').write_text(json.dumps({'version': version}) + '\n', encoding='utf-8')

sm = root / 'sitemap.xml'
if sm.exists():
    sm.write_text(re.sub(r'(<lastmod>)[^<]*(</lastmod>)', lambda m: m.group(1) + today + m.group(2), sm.read_text(encoding='utf-8')), encoding='utf-8')

print('Site version stamped:', version)
