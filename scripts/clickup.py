#!/usr/bin/env python3
"""ClickUp REST helper — the desk's TRACKER layer (tasks + ideas).
Reads CLICKUP_API_TOKEN from the environment ONLY, never from files.

Two lists are required (fields per docs/CLICKUP-SCHEMA.md):
  CLICKUP_TASKS_LIST — the task tracker list ID
  CLICKUP_IDEAS_LIST — the idea pipeline list ID

This module MIRRORS scripts/notion.py's surface (q, create, update, comment,
r_title, r_select, r_number, r_date, r_rich, r_multi, created, edited, url,
TASKS(), IDEAS()) so ideas.py / tracker_audit.py / pending.py work unchanged in
shape. Mapping (see docs/CLICKUP-SCHEMA.md):
  Status   -> native ClickUp status          Owner    -> native assignee (first)
  Priority -> native priority (urgent..low)  Due      -> native due_date
  Category -> native tags                    everything else -> custom fields
Custom-field IDs are fetched ONCE per list per process and cached; a missing
field fails with its NAME spelled out, never a bare KeyError.

Usage: python3 scripts/clickup.py smoke | fields
"""
import os, json, time, datetime, urllib.request, urllib.parse, urllib.error

BASE = 'https://api.clickup.com/api/v2'

PRIO_TO_DESK = {'urgent': 'Highest', 'high': 'High', 'normal': 'Medium', 'low': 'Low'}
DESK_TO_PRIO = {'Highest': 1, 'High': 2, 'Medium': 3, 'Low': 4}
DONE_STATUSES = ('done', 'deferred', 'closed', 'complete', 'cancelled')

def _token():
    v = os.environ.get('CLICKUP_API_TOKEN', '')
    if not v:
        raise SystemExit('CLICKUP_API_TOKEN is not set — see docs/SECRETS-SETUP.md')
    return v

def _listid(env):
    v = os.environ.get(env, '')
    if not v:
        raise SystemExit(f'{env} is not set — see docs/SECRETS-SETUP.md')
    return v

TASKS = lambda: _listid('CLICKUP_TASKS_LIST')
IDEAS = lambda: _listid('CLICKUP_IDEAS_LIST')

def api(method, path, body=None, timeout=60):
    """Returns (http_status, parsed_json). Retries 429/5xx with backoff."""
    req = urllib.request.Request(BASE + path,
        data=json.dumps(body).encode() if body is not None else None, method=method,
        headers={'Authorization': _token(), 'Content-Type': 'application/json'})
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

# ---------------------------------------------------------------- time helpers
def _tz():
    return datetime.timezone(datetime.timedelta(
        minutes=int(os.environ.get('DESK_TZ_OFFSET_MIN', '0'))))

def ms_to_iso(ms):
    """ClickUp millisecond-epoch (str or int) -> ISO-8601 UTC ('...Z')."""
    if ms in (None, '', 0): return None
    return datetime.datetime.fromtimestamp(int(ms) / 1000,
        datetime.timezone.utc).isoformat().replace('+00:00', 'Z')

def ms_to_date(ms):
    """Millisecond-epoch -> local-date ISO (DESK_TZ_OFFSET_MIN), for due dates."""
    if ms in (None, '', 0): return None
    return datetime.datetime.fromtimestamp(int(ms) / 1000, _tz()).date().isoformat()

def iso_to_ms(iso):
    """'YYYY-MM-DD' (or full ISO) -> millisecond-epoch at local noon (tz-safe:
    noon survives any offset conversion landing on the same calendar day)."""
    d = datetime.date.fromisoformat(iso[:10])
    dt = datetime.datetime(d.year, d.month, d.day, 12, 0, tzinfo=_tz())
    return int(dt.timestamp() * 1000)

# ---------------------------------------------------------------- custom fields
_FIELDS = {}   # list_id -> {name: field dict}

def fields(list_id):
    if list_id not in _FIELDS:
        st, r = api('GET', f'/list/{list_id}/field')
        if st != 200:
            raise RuntimeError(f'ClickUp list {list_id} fields: HTTP {st} {r}')
        _FIELDS[list_id] = {f['name']: f for f in r.get('fields', [])}
    return _FIELDS[list_id]

def field_id(list_id, name):
    f = fields(list_id).get(name)
    if not f:
        raise RuntimeError(f"ClickUp list {list_id} has no custom field named "
                           f"'{name}' — create it per docs/CLICKUP-SCHEMA.md")
    return f['id']

def set_field(task_id, list_id, name, value):
    """Set one custom field by NAME. Dropdowns take the option NAME (resolved to
    its option id here); dates take ISO (converted to ms); numbers/text as-is."""
    f = fields(list_id).get(name)
    if not f:
        raise RuntimeError(f"ClickUp list {list_id} has no custom field named "
                           f"'{name}' — create it per docs/CLICKUP-SCHEMA.md")
    if f['type'] == 'drop_down':
        opts = f.get('type_config', {}).get('options', [])
        hit = next((o for o in opts if o.get('name') == value), None)
        if not hit:
            raise RuntimeError(f"field '{name}': no dropdown option '{value}' "
                               f"(have: {[o.get('name') for o in opts]})")
        value = hit['id']
    elif f['type'] == 'date':
        value = iso_to_ms(value)
    return api('POST', f"/task/{task_id}/field/{f['id']}", {'value': value})

def _cf(task, name):
    for f in task.get('custom_fields', []):
        if f.get('name') == name:
            return f
    return None

# ---------------------------------------------------------------- tasks
def q(list_id, filter=None, sorts=None):
    """Paged list-task fetch -> list of task dicts, newest first, closed included
    (callers filter). `filter`/`sorts` accepted for notion.py surface parity;
    ordering is fixed to date_created descending."""
    out, page = [], 0
    while True:
        st, r = api('GET', f'/list/{list_id}/task?' + urllib.parse.urlencode({
            'page': page, 'include_closed': 'true', 'subtasks': 'true',
            'order_by': 'created', 'reverse': 'true'}))
        if st != 200:
            raise RuntimeError(f'ClickUp query {list_id}: HTTP {st} {r}')
        batch = r.get('tasks', [])
        out += batch
        if not batch or r.get('last_page') is True:
            return out
        page += 1

def get_task(task_id):
    st, r = api('GET', f'/task/{task_id}')
    if st != 200:
        raise RuntimeError(f'ClickUp get_task {task_id}: HTTP {st} {r}')
    return r

def create_task(list_id, name, description='', status=None, priority=None,
                due_iso=None, assignees=None, tags=None, fields_by_name=None):
    """Create a task. priority is desk vocabulary (Highest/High/Medium/Low);
    fields_by_name = {custom field name: value} set after creation (dropdowns by
    option name). Returns the created task dict."""
    body = {'name': name[:1900], 'description': description}
    if status:   body['status'] = status
    if priority: body['priority'] = DESK_TO_PRIO[priority]
    if due_iso:  body['due_date'] = iso_to_ms(due_iso)
    if assignees: body['assignees'] = assignees          # native ClickUp user IDs
    if tags:      body['tags'] = tags
    st, r = api('POST', f'/list/{list_id}/task', body)
    if st != 200:
        raise RuntimeError(f'ClickUp create in {list_id}: HTTP {st} {r}')
    for k, v in (fields_by_name or {}).items():
        set_field(r['id'], list_id, k, v)
    return r

def update(task_id, body):
    """PUT /task — body in ClickUp's own shape ({'status':..,'due_date':ms,..})."""
    return api('PUT', f'/task/{task_id}', body)

def set_due(task_id, new_iso):
    return update(task_id, {'due_date': iso_to_ms(new_iso), 'due_date_time': False})

def comment(task_id, text):
    return api('POST', f'/task/{task_id}/comment',
               {'comment_text': text[:1900], 'notify_all': False})

def comments(task_id):
    st, r = api('GET', f'/task/{task_id}/comment')
    return r.get('comments', []) if st == 200 else []

def c_text(c):
    """Plain text of one comment dict (mirrors the notion rich_text join)."""
    return c.get('comment_text', '') or ''.join(
        b.get('text', '') for b in c.get('comment', []) if isinstance(b, dict))

# ---------------------------------------------------------------- readers
# Same names as notion.py so callers are source-compatible. Special names map to
# native ClickUp features; everything else reads a custom field.
def r_title(task): return task.get('name', '')

def r_select(task, name):
    if name == 'Status':
        s = task.get('status') or {}
        return (s.get('status') or '').title() or None
    if name == 'Owner':
        a = task.get('assignees') or []
        return a[0].get('username') if a else None
    if name == 'Priority':
        p = task.get('priority') or {}
        return PRIO_TO_DESK.get((p or {}).get('priority')) if p else None
    f = _cf(task, name)
    if not f or f.get('value') is None: return None
    if f.get('type') == 'drop_down':
        v = f['value']
        for o in f.get('type_config', {}).get('options', []):
            if o.get('id') == v or o.get('orderindex') == v:
                return o.get('name')
        return None
    return str(f['value'])

def r_multi(task, name):
    if name == 'Category':
        return [t.get('name') for t in task.get('tags', [])]
    f = _cf(task, name)
    if not f or not f.get('value'): return []
    opts = {o['id']: o.get('name', o.get('label'))
            for o in f.get('type_config', {}).get('options', [])}
    return [opts.get(v, str(v)) for v in f['value']]

def r_number(task, name):
    f = _cf(task, name)
    if not f or f.get('value') in (None, ''): return None
    try: return float(f['value'])
    except (TypeError, ValueError): return None

def r_date(task, name):
    if name == 'Due':
        return ms_to_date(task.get('due_date'))
    f = _cf(task, name)
    return ms_to_date(f['value']) if f and f.get('value') else None

def r_rich(task, name):
    if name == 'Owner':      # multi-assignee rendering
        return ', '.join(a.get('username', '') for a in task.get('assignees') or [])
    f = _cf(task, name)
    return str(f['value']) if f and f.get('value') is not None else ''

def created(task): return ms_to_iso(task.get('date_created')) or ''
def edited(task):  return ms_to_iso(task.get('date_updated')) or ''
def url(task):     return task.get('url', '')

def assignee_ids(task):
    return [a.get('id') for a in task.get('assignees') or []]

def is_done_status(task):
    return (r_select(task, 'Status') or '').lower() in DONE_STATUSES

# ---------------------------------------------------------------- people
def members(list_id=None):
    """Users on a list (or the workspace team when list_id is None) —
    [{'id','username','email','role'}]. Feeds ORG-STRUCTURE and assignment."""
    if list_id:
        st, r = api('GET', f'/list/{list_id}/member')
        return r.get('members', []) if st == 200 else []
    st, r = api('GET', '/team')
    out = []
    for team in r.get('teams', []) if st == 200 else []:
        for m in team.get('members', []):
            u = m.get('user', {})
            out.append({'id': u.get('id'), 'username': u.get('username'),
                        'email': u.get('email'), 'role': u.get('role')})
    return out

# Custom fields each list must carry (docs/CLICKUP-SCHEMA.md §2–3). The public
# API cannot create custom fields — a missing one is created by hand in ClickUp.
REQUIRED_FIELDS = {
    'Tasks': [('Due moves', 'number'), ('Waiting on', 'short text'),
              ('Source', 'short text')],
    'Ideas': [('State', 'dropdown: Open · Promoted · Merged · Killed'),
              ('ICE', 'number'), ('RICE', 'number'), ('Mentions', 'number'),
              ('Skips', 'number'),
              ('Disposition', 'dropdown: IMMEDIATE · FUTURE · ALREADY-COVERED'),
              ('Reviewed', 'date'), ('Promoted to', 'short text'),
              ('Source', 'short text')],
}

def missing_fields(label, list_id):
    have = fields(list_id)
    return [(n, t) for n, t in REQUIRED_FIELDS[label] if n not in have]

# ---------------------------------------------------------------- CLI
def _smoke():
    for label, lid in (('Tasks', TASKS()), ('Ideas', IDEAS())):
        ts = q(lid)
        open_n = sum(1 for t in ts if not is_done_status(t))
        print(f'{label} list {lid}: {len(ts)} tasks, {open_n} open')
        if ts: print(f'  newest: {r_title(ts[0])[:60]} ({created(ts[0])[:10]})')
        try:
            print(f'  custom fields: {sorted(fields(lid))}')
        except RuntimeError as e:
            print(f'  custom fields: FAIL {e}')

if __name__ == '__main__':
    import sys
    cmd = sys.argv[1] if len(sys.argv) > 1 else 'smoke'
    if cmd == 'fields':
        for label, lid in (('Tasks', TASKS()), ('Ideas', IDEAS())):
            print(f'{label} {lid}:')
            for name, f in sorted(fields(lid).items()):
                print(f"  {f['type']:<12} {name}  ({f['id']})")
    elif cmd == 'missing':
        any_missing = False
        for label, lid in (('Tasks', TASKS()), ('Ideas', IDEAS())):
            miss = missing_fields(label, lid)
            if miss:
                any_missing = True
                print(f'{label} list {lid} — create these custom fields in ClickUp '
                      f'(UI only; the API cannot):')
                for n, t in miss:
                    print(f'  {n}  ({t})')
        if not any_missing:
            print('All required custom fields present on both lists.')
    else:
        _smoke()
