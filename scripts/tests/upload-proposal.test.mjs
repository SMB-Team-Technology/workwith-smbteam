/**
 * upload-proposal.test.mjs — unit tests for scripts/upload-proposal-to-hubspot.mjs
 *
 * Run: node --test scripts/tests/upload-proposal.test.mjs
 *
 * HubSpot is never called: every test passes a fake fetch that records the
 * requests and answers like the Files API v3.
 */

import { test } from 'node:test';
import assert from 'node:assert/strict';
import { mkdtempSync, writeFileSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { uploadProposal, hubspotFileBaseName } from '../upload-proposal-to-hubspot.mjs';

const FILE_URL = 'https://12345.fs1.hubspotusercontent-na1.net/hubfs/12345/AI%20Proposals/acme-law-proposal.pptx';

function deck() {
  const dir = mkdtempSync(join(tmpdir(), 'deck-'));
  const p = join(dir, 'Acme_Law_November_1_2026_Proposal.pptx');
  writeFileSync(p, 'pptx bytes');
  return p;
}

function fakeHubSpot({ folderExists = true, existing = null, uploadStatus = 201, linkStatus = 200 } = {}) {
  const calls = [];
  const json = (status, body) => ({ status, ok: status >= 200 && status < 300, text: async () => JSON.stringify(body) });
  const fetchImpl = async (url, opts = {}) => {
    const method = opts.method || 'GET';
    calls.push({ method, url, body: opts.body });
    if (url === FILE_URL) return { status: linkStatus, ok: linkStatus < 300, text: async () => '' };
    const path = url.replace('https://api.hubapi.com', '');
    if (method === 'GET' && path.startsWith('/files/v3/folders/')) {
      return folderExists ? json(200, { id: '77', name: 'AI Proposals' }) : json(404, { message: 'not found' });
    }
    if (method === 'POST' && path === '/files/v3/folders') return json(201, { id: '78' });
    if (method === 'GET' && path.startsWith('/files/v3/files/search')) {
      return json(200, { results: existing ? [existing] : [] });
    }
    if (method === 'POST' && path === '/files/v3/files') {
      return json(uploadStatus, uploadStatus < 300 ? { id: '900', url: FILE_URL } : { message: 'This app hasn\'t been granted all required scopes' });
    }
    if (method === 'PUT' && path.startsWith('/files/v3/files/')) {
      return json(200, { id: path.split('/').pop(), url: FILE_URL });
    }
    return json(500, { message: `unexpected ${method} ${path}` });
  };
  return { calls, fetchImpl };
}

test('file name depends only on the friendly name', () => {
  assert.equal(hubspotFileBaseName('acme-law'), 'acme-law-proposal');
});

test('first upload creates the file in the AI Proposals folder, public but not indexable', async () => {
  const hs = fakeHubSpot();
  const r = await uploadProposal({ friendlyName: 'acme-law', token: 't', fetchImpl: hs.fetchImpl, pptxPath: deck() });
  assert.equal(r.ok, true);
  assert.equal(r.action, 'uploaded');
  assert.equal(r.url, FILE_URL);
  const post = hs.calls.find(c => c.method === 'POST' && c.url.endsWith('/files/v3/files'));
  assert.ok(post, 'uploaded with POST /files/v3/files');
  assert.equal(post.body.get('folderId'), '77');
  assert.equal(post.body.get('fileName'), 'acme-law-proposal.pptx');
  assert.equal(JSON.parse(post.body.get('options')).access, 'PUBLIC_NOT_INDEXABLE');
});

test('creates the folder when it does not exist yet', async () => {
  const hs = fakeHubSpot({ folderExists: false });
  const r = await uploadProposal({ friendlyName: 'acme-law', token: 't', fetchImpl: hs.fetchImpl, pptxPath: deck() });
  assert.equal(r.ok, true);
  assert.ok(hs.calls.some(c => c.method === 'POST' && c.url.endsWith('/files/v3/folders')));
  assert.equal(hs.calls.find(c => c.method === 'POST' && c.url.endsWith('/files/v3/files')).body.get('folderId'), '78');
});

test('a re-run replaces the existing file in place, so the link stays the same', async () => {
  const existing = { id: '555', name: 'acme-law-proposal', extension: 'pptx', parentFolderId: '77', url: FILE_URL };
  const hs = fakeHubSpot({ existing });
  const r = await uploadProposal({ friendlyName: 'acme-law', token: 't', fetchImpl: hs.fetchImpl, pptxPath: deck() });
  assert.equal(r.ok, true);
  assert.equal(r.action, 'replaced');
  assert.equal(r.file_id, '555');
  assert.equal(r.url, FILE_URL);
  assert.equal(r.warning, undefined);
  assert.ok(hs.calls.some(c => c.method === 'PUT' && c.url.endsWith('/files/v3/files/555')));
  assert.ok(!hs.calls.some(c => c.method === 'POST' && c.url.endsWith('/files/v3/files')), 'no second file created');
});

test('a file with a different name in the folder is not replaced', async () => {
  const other = { id: '556', name: 'acme-law-proposal-old', extension: 'pptx', parentFolderId: '77', url: FILE_URL };
  const hs = fakeHubSpot({ existing: other });
  const r = await uploadProposal({ friendlyName: 'acme-law', token: 't', fetchImpl: hs.fetchImpl, pptxPath: deck() });
  assert.equal(r.action, 'uploaded');
});

test('an upload error is reported, never a link', async () => {
  const hs = fakeHubSpot({ uploadStatus: 403 });
  const r = await uploadProposal({ friendlyName: 'acme-law', token: 't', fetchImpl: hs.fetchImpl, pptxPath: deck() });
  assert.equal(r.ok, false);
  assert.equal(r.url, undefined);
  assert.match(r.error, /HTTP 403/);
  assert.match(r.error, /files` scope/);
});

test('a link that does not open is reported as a failure', async () => {
  const hs = fakeHubSpot({ linkStatus: 404 });
  const r = await uploadProposal({ friendlyName: 'acme-law', token: 't', fetchImpl: hs.fetchImpl, pptxPath: deck() });
  assert.equal(r.ok, false);
  assert.match(r.error, /does not open/);
});

test('no token: fails without calling HubSpot', async () => {
  const hs = fakeHubSpot();
  const r = await uploadProposal({ friendlyName: 'acme-law', token: '', fetchImpl: hs.fetchImpl, pptxPath: deck() });
  assert.equal(r.ok, false);
  assert.equal(hs.calls.length, 0);
});

test('lookup finds the existing link without uploading', async () => {
  const existing = { id: '555', name: 'acme-law-proposal', extension: 'pptx', parentFolderId: '77', url: FILE_URL };
  const hs = fakeHubSpot({ existing });
  const r = await uploadProposal({ friendlyName: 'acme-law', token: 't', lookup: true, fetchImpl: hs.fetchImpl });
  assert.deepEqual(r, { ok: true, url: FILE_URL, file_id: '555', action: 'found' });
  assert.ok(!hs.calls.some(c => c.method === 'PUT' || c.method === 'POST'));
});

test('lookup with no file returns an error', async () => {
  const hs = fakeHubSpot();
  const r = await uploadProposal({ friendlyName: 'acme-law', token: 't', lookup: true, fetchImpl: hs.fetchImpl });
  assert.equal(r.ok, false);
});
