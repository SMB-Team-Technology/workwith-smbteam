import { test } from 'node:test';
import assert from 'node:assert/strict';
import { mkdtempSync, readFileSync, writeFileSync, rmSync } from 'node:fs';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import { spawnSync } from 'node:child_process';

for (const workflow of ['audit-write', 'resend-audit-email']) {
  const source = readFileSync(new URL(`../../.github/workflows/${workflow}.yml`, import.meta.url), 'utf8');
  const command = source.match(/          BODY=\$\(jq -en[\s\S]*? end'\)/)?.[0];

  test(`${workflow}: writes full decision as a HubSpot string property`, () => {
    assert.ok(command, 'workflow contains the JSON payload builder');
    const dir = mkdtempSync(join(tmpdir(), 'roadmap-json-'));
    try {
      const decision = { package: 'Growth "Plus"', notes: 'Line 1\nLine 2 — freedom', investment: { total: 1234 }, products: ['A', 'B'] };
      writeFileSync(join(dir, 'package_decision.json'), JSON.stringify(decision));
      const result = spawnSync('bash', ['-e', '-c', `${command}\nprintf '%s' "$BODY"`], {
        encoding: 'utf8', env: { ...process.env, FRIENDLY_NAME: dir, DECK_URL: 'https://drive.google.com/file/d/deck-123/view' },
      });
      assert.equal(result.status, 0, result.stderr);
      const { properties } = JSON.parse(result.stdout);
      assert.equal(properties.growth_profit_and_freedom_roadmap, 'https://drive.google.com/file/d/deck-123/view');
      assert.equal(typeof properties.growth_profit_and_freedom_roadmap_json, 'string');
      assert.deepEqual(JSON.parse(properties.growth_profit_and_freedom_roadmap_json), decision);

      for (const invalid of ['', '{broken', 'null', '[]', '{}\n{}']) {
        writeFileSync(join(dir, 'package_decision.json'), invalid);
        const failure = spawnSync('bash', ['-e', '-c', command], {
          encoding: 'utf8', env: { ...process.env, FRIENDLY_NAME: dir, DECK_URL: 'https://drive.google.com/file/d/deck-123/view' },
        });
        assert.notEqual(failure.status, 0, `must reject invalid decision: ${invalid}`);
      }
      rmSync(join(dir, 'package_decision.json'));
      assert.notEqual(spawnSync('bash', ['-e', '-c', command], {
        env: { ...process.env, FRIENDLY_NAME: dir, DECK_URL: 'https://drive.google.com/file/d/deck-123/view' },
      }).status, 0, 'must reject missing decision file');
      assert.match(source, /if: env\.TEST_MODE != 'true' && steps\.upload\.outputs\.ok == 'true'/);
    } finally {
      rmSync(dir, { recursive: true, force: true });
    }
  });
}
