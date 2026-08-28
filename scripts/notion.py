#!/usr/bin/env python3
"""Notion REST helper — the desk's tracker layer. Reads NOTION_API_KEY from the
environment ONLY, never from files.

Two databases are required (create them per docs/NOTION-SCHEMA.md and share BOTH
with the integration — Notion permissions are PAGE-LEVEL: an unshared database
returns empty results or 404, silently):
  NOTION_TASKS_DB — the task tracker
  NOTION_IDEAS_DB — the idea pipeline

Usage: from notion import api, q, create, update, comment, ...
"""
import os, json, time, urllib.request, urllib.error

BASE = 'https://api.notion.com/v1'
VER = '2022-06-28'

def _dbid(env):
    v = os.environ.get(env, '')
    if not v:
        raise SystemExit(f'{env} is not set — see docs/SECRETS-SETUP.md')
    return v

def api(method, path, body=None, timeout=60):
    req = urllib.request.Request(BASE + path,
        data=json.dumps(body).encode() if body is not None else None, method=method,
        headers={'Authorization': f'Bearer {os.environ["NOTION_API_KEY"]}',
                 'Notion-Version': VER, 'Content-Type': 'application/json'})
    for attempt in range(4):
        try:
            with urllib.request.urlopen(req, timeout=timeout) as r:
                t = r.read().decode()
                return r.status, (json.loads(t) if t.strip() else {})
        except urllib.error.HTTPError as e:
            t = e.read().decode()
            if e.code == 429 or e.code >= 500:
                time.sleep(2 ** (attempt + 1)); continue
            return e.code, (json.loads(t) if t.strip().startswith('{') else {'raw': t[:400]})
    return 599, {}

def q(db_id, filter=None, sorts=None):
    """Paged database query -> list of pages."""
    out, cursor = [], None
    while True:
        body = {}
        if filter: body['filter'] = filter
        if sorts: body['sorts'] = sorts
        if cursor: body['start_cursor'] = cursor
        st, r = api('POST', f'/databases/{db_id}/query', body)
        if st != 200:
            raise RuntimeError(f'Notion query {db_id}: HTTP {st} {r}')
        out += r.get('results', [])
        if not r.get('has_more'):
            return out
        cursor = r.get('next_cursor')

def create(db_id, props, children=None):
    body = {'parent': {'database_id': db_id}, 'properties': props}
    if children: body['children'] = children
    return api('POST', '/pages', body)

def update(page_id, props):
    return api('PATCH', f'/pages/{page_id}', {'properties': props})

def comment(page_id, text):
    return api('POST', '/comments', {'parent': {'page_id': page_id},
        'rich_text': [{'type': 'text', 'text': {'content': text[:1900]}}]})

def comments(page_id):
    st, r = api('GET', f'/comments?block_id={page_id}&page_size=50')
    return r.get('results', []) if st == 200 else []

# ---------------- property builders (write) ----------------
def p_title(s):  return {'title': [{'text': {'content': s[:1900]}}]}
def p_rich(s):   return {'rich_text': [{'text': {'content': s[:1900]}}]}
def p_select(s): return {'select': {'name': s}}
def p_multi(xs): return {'multi_select': [{'name': x} for x in xs]}
def p_number(n): return {'number': n}
def p_date(iso): return {'date': {'start': iso}}
def para(s):
    return {'object': 'block', 'type': 'paragraph',
            'paragraph': {'rich_text': [{'type': 'text', 'text': {'content': s[:1900]}}]}}

# ---------------- property readers ----------------
def _p(page, name): return page.get('properties', {}).get(name, {})
def r_title(page):
    for k, v in page.get('properties', {}).items():
        if v.get('type') == 'title':
            return ''.join(t.get('plain_text', '') for t in v.get('title', []))
    return ''
def r_select(page, name):
    s = _p(page, name).get('select');  return s.get('name') if s else None
def r_multi(page, name):
    return [x.get('name') for x in _p(page, name).get('multi_select', [])]
def r_number(page, name): return _p(page, name).get('number')
def r_date(page, name):
    d = _p(page, name).get('date');  return d.get('start') if d else None
def r_rich(page, name):
    return ''.join(t.get('plain_text', '') for t in _p(page, name).get('rich_text', []))
def created(page): return page.get('created_time', '')
def edited(page):  return page.get('last_edited_time', '')
def url(page):     return page.get('url', '')

TASKS = lambda: _dbid('NOTION_TASKS_DB')
IDEAS = lambda: _dbid('NOTION_IDEAS_DB')
