import { test } from 'node:test';
import assert from 'node:assert/strict';
import { mkdtemp, writeFile, rm } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { uploadProposal } from '../upload-proposal-to-drive.mjs';

for (const existing of [false, true]) {
  test(`Drive ${existing ? 'updates in place' : 'creates in the requested folder'}`, async () => {
    const dir = await mkdtemp(join(tmpdir(), 'drive-test-'));
    try {
      const file = join(dir, 'deck.pptx');
      await writeFile(file, 'deck bytes');
      const calls = [];
      const url = await uploadProposal({ firm: 'test-firm', file, token: 'mock', fetchImpl: async (url, options) => {
        calls.push([new URL(url), options]);
        return calls.length === 1 ? Response.json({ files: existing ? [{ id: 'deck-123' }] : [] }) : Response.json({ id: 'deck-123' });
      } });
      assert.equal(url, 'https://drive.google.com/file/d/deck-123/view');
      assert.equal(calls[0][0].searchParams.get('q'), "'0AB92lnIjHcNvUk9PVA' in parents and name = 'test-firm-proposal.pptx' and trashed = false");
      assert.equal(calls[1][0].searchParams.get('supportsAllDrives'), 'true');
      assert.equal(calls[1][0].pathname, `/upload/drive/v3/files${existing ? '/deck-123' : ''}`);
      assert.equal(calls[1][1].method, existing ? 'PATCH' : 'POST');
      const body = calls[1][1].body.toString();
      assert.match(body, /deck bytes/);
      assert.equal(body.includes('"parents":["0AB92lnIjHcNvUk9PVA"]'), !existing);
      assert.equal(calls.length, 2);
    } finally {
      await rm(dir, { recursive: true, force: true });
    }
  });
}

test('Drive upload requires credentials before making any requests', async () => {
  await assert.rejects(uploadProposal({ fetchImpl: () => assert.fail('unexpected request') }), /No Google Drive access token/);
});
