/**
 * fetch-source-deck.test.mjs — unit tests for scripts/fetch-source-deck.mjs
 *
 * Run: node --test scripts/tests/fetch-source-deck.test.mjs
 *
 * HubSpot is never called: every test passes a fake fetch that answers like
 * the Files API v3.
 */

import { test } from 'node:test';
import assert from 'node:assert/strict';
import { mkdtempSync, readFileSync, existsSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { fetchSourceDeck, pickNewest } from '../fetch-source-deck.mjs';

const PPTX = Buffer.concat([Buffer.from('PK'), Buffer.alloc(2000, 1)]);
const SIGNED = 'https://signed.example/leadsos.pptx?sig=1';

function fakeHubSpot({ folder = true, files = null, signedStatus = 200, body = PPTX } = {}) {
  const calls = [];
  const json = (status, b) => ({ status, ok: status < 300, text: async () => JSON.stringify(b) });
  const results = files ?? [
    { id: '1', name: 'SMBTeam LeadsOS Client Proposal Deck - FINAL (1)', extension: 'pptx', parentFolderId: '9', updatedAt: '2026-11-17T10:00:00Z' },
  ];
  const fetchImpl = async (url) => {
    calls.push(url);
    if (url === SIGNED) return { ok: true, status: 200, arrayBuffer: async () => body };
    const path = url.replace('https://api.hubapi.com', '');
    if (path.startsWith('/files/v3/folders/')) return folder ? json(200, { id: '9' }) : json(404, { message: 'nope' });
    if (path.startsWith('/files/v3/files/search')) return json(200, { results });
    if (/\/signed-url$/.test(path)) return signedStatus < 300 ? json(200, { url: SIGNED }) : json(signedStatus, { message: 'denied' });
    throw new Error(`unexpected ${url}`);
  };
  return { fetchImpl, calls };
}

const out = () => join(mkdtempSync(join(tmpdir(), 'src-')), 'nested', 'LeadsOS.pptx');

test('downloads the LeadsOS deck through a signed URL', async () => {
  const { fetchImpl, calls } = fakeHubSpot();
  const o = out();
  const r = await fetchSourceDeck({ token: 't', out: o, fetchImpl });
  assert.equal(r.ok, true, r.error);
  assert.equal(r.file_id, '1');
  assert.ok(existsSync(o));
  assert.equal(readFileSync(o).length, PPTX.length);
  assert.ok(calls.some(c => c.endsWith('/files/v3/files/1/signed-url')));
});

test('picks the newest matching file and ignores other decks', () => {
  const f = pickNewest([
    { id: 'a', name: 'LeadsOS deck v1', extension: 'pptx', updatedAt: '2026-11-10T00:00:00Z' },
    { id: 'b', name: 'leadsos deck v2', extension: 'pptx', updatedAt: '2026-11-20T00:00:00Z' },
    { id: 'c', name: 'ProfitOS deck', extension: 'pptx', updatedAt: '2026-12-01T00:00:00Z' },
    { id: 'd', name: 'LeadsOS old', extension: 'pptx', updatedAt: '2026-12-02T00:00:00Z', archived: true },
    { id: 'e', name: 'LeadsOS notes', extension: 'pdf', updatedAt: '2026-12-03T00:00:00Z' },
  ], 'LeadsOS', '9');
  assert.equal(f.id, 'b');
});

test('missing folder, missing file and missing token fail with a reason', async () => {
  assert.match((await fetchSourceDeck({ token: '', out: out() })).error, /HUBSPOT_TOKEN/);
  assert.match((await fetchSourceDeck({ token: 't', out: out(), fetchImpl: fakeHubSpot({ folder: false }).fetchImpl })).error, /not found/);
  assert.match((await fetchSourceDeck({ token: 't', out: out(), fetchImpl: fakeHubSpot({ files: [] }).fetchImpl })).error, /No \.pptx/);
});

test('refuses a download that is not a pptx', async () => {
  const r = await fetchSourceDeck({ token: 't', out: out(), fetchImpl: fakeHubSpot({ body: Buffer.from('<html>error</html>') }).fetchImpl });
  assert.equal(r.ok, false);
  assert.match(r.error, /not a \.pptx/);
});

test('a refused signed URL explains the scope', async () => {
  const r = await fetchSourceDeck({ token: 't', out: out(), fetchImpl: fakeHubSpot({ signedStatus: 403 }).fetchImpl });
  assert.match(r.error, /files` scope/);
});
