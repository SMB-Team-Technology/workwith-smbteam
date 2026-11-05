#!/usr/bin/env node
/**
 * Upload a firm's proposal deck (.pptx) to the HubSpot file manager and print
 * its public link. The link replaces the old workwith.smbteam.com website URL
 * in the HubSpot contact field, the Slack "Proposal ready" message and the
 * seller email.
 *
 * The file is stored as "<friendly-name>-proposal.pptx" in the "AI Proposals"
 * folder with access PUBLIC_NOT_INDEXABLE. The name depends only on the
 * friendly name, so a re-run finds the same file and replaces its contents in
 * place (PUT /files/v3/files/{id}) — the file id, and therefore the link,
 * stays the same.
 *
 * Usage:
 *   node scripts/upload-proposal-to-hubspot.mjs <friendly-name>             upload or replace
 *   node scripts/upload-proposal-to-hubspot.mjs <friendly-name> --lookup    only find the existing link
 *   node scripts/upload-proposal-to-hubspot.mjs <friendly-name> --folder "AI Proposals TEST"
 *   node scripts/upload-proposal-to-hubspot.mjs <friendly-name> --file <path/to/deck.pptx>
 *
 * Env: HUBSPOT_TOKEN (private app token; needs the `files` scope).
 *
 * Prints one JSON line on stdout:
 *   {"ok":true,"url":"https://…","file_id":"…","action":"uploaded|replaced|found","file":"<local pptx>"}
 *   {"ok":false,"error":"…"}
 * Exit codes: 0 ok, 1 failed (JSON is printed either way).
 */

import { readFileSync, readdirSync, statSync, existsSync } from 'fs';
import { join, basename } from 'path';
import { execFileSync } from 'child_process';
import { pathToFileURL } from 'url';

const API = 'https://api.hubapi.com';
export const DEFAULT_FOLDER = 'AI Proposals';
const ACCESS = 'PUBLIC_NOT_INDEXABLE';

export function hubspotFileBaseName(friendlyName) {
  return `${friendlyName}-proposal`;
}

/** Newest *_Proposal.pptx in the firm folder (by last commit time, then mtime). */
export function findProposalPptx(friendlyName) {
  if (!existsSync(friendlyName)) return null;
  const files = readdirSync(friendlyName)
    .filter(f => f.endsWith('_Proposal.pptx'))
    .map(f => join(friendlyName, f));
  if (files.length <= 1) return files[0] || null;
  const when = f => {
    try {
      const ct = execFileSync('git', ['log', '-1', '--format=%ct', '--', f], { encoding: 'utf8' }).trim();
      // Uncommitted (just built) counts as newest.
      return ct ? Number(ct) : Number.MAX_SAFE_INTEGER;
    } catch {
      return statSync(f).mtimeMs / 1000;
    }
  };
  return files.sort((a, b) => when(b) - when(a) || statSync(b).mtimeMs - statSync(a).mtimeMs)[0];
}

async function call(fetchImpl, token, method, path, body) {
  const headers = { Authorization: `Bearer ${token}` };
  if (body && !(body instanceof FormData)) headers['Content-Type'] = 'application/json';
  const res = await fetchImpl(`${API}${path}`, {
    method,
    headers,
    body: body && !(body instanceof FormData) ? JSON.stringify(body) : body,
  });
  const text = await res.text();
  let json = null;
  try { json = text ? JSON.parse(text) : null; } catch { /* not JSON */ }
  return { status: res.status, ok: res.ok, json, text };
}

function apiError(step, r) {
  const msg = r.json?.message || r.text?.slice(0, 300) || '';
  const hint = r.status === 401 || r.status === 403
    ? ' (check the HubSpot token has the `files` scope)'
    : '';
  return `${step} failed: HTTP ${r.status}${msg ? ` — ${msg}` : ''}${hint}`;
}

async function getFolder(fetchImpl, token, folderName, create) {
  const got = await call(fetchImpl, token, 'GET', `/files/v3/folders/${encodeURIComponent(folderName)}`);
  if (got.ok && got.json?.id) return { id: String(got.json.id) };
  if (got.status !== 404) return { error: apiError(`Finding folder "${folderName}"`, got) };
  if (!create) return { id: null };
  const made = await call(fetchImpl, token, 'POST', '/files/v3/folders', { name: folderName });
  if (made.ok && made.json?.id) return { id: String(made.json.id) };
  return { error: apiError(`Creating folder "${folderName}"`, made) };
}

async function findExisting(fetchImpl, token, folderId, base) {
  const q = new URLSearchParams({ name: base, extension: 'pptx', parentFolderIds: folderId, limit: '100' });
  const r = await call(fetchImpl, token, 'GET', `/files/v3/files/search?${q}`);
  if (!r.ok) return { error: apiError('Searching for the existing deck', r) };
  const hits = (r.json?.results || []).filter(f =>
    f && !f.archived && f.name === base && (f.extension || '').toLowerCase() === 'pptx'
    && String(f.parentFolderId ?? folderId) === String(folderId));
  return { file: hits[0] || null };
}

function fileLink(f) {
  return f?.url || f?.defaultHostingUrl || null;
}

async function linkWorks(fetchImpl, url) {
  try {
    const res = await fetchImpl(url, { method: 'GET', headers: { Range: 'bytes=0-0' }, redirect: 'follow' });
    return res.status >= 200 && res.status < 300;
  } catch {
    return false;
  }
}

/**
 * Upload (or replace) the deck. Returns the result object printed by the CLI.
 * fetchImpl is injectable for tests.
 */
export async function uploadProposal({
  friendlyName, token, folder = DEFAULT_FOLDER, lookup = false, fetchImpl = fetch, pptxPath,
}) {
  if (!token) return { ok: false, error: 'HUBSPOT_TOKEN is not set' };
  const base = hubspotFileBaseName(friendlyName);

  const folderRes = await getFolder(fetchImpl, token, folder, !lookup);
  if (folderRes.error) return { ok: false, error: folderRes.error };
  if (!folderRes.id) return { ok: false, error: `Folder "${folder}" not found in HubSpot` };

  const existing = await findExisting(fetchImpl, token, folderRes.id, base);
  if (existing.error) return { ok: false, error: existing.error };

  if (lookup) {
    const url = fileLink(existing.file);
    return url
      ? { ok: true, url, file_id: String(existing.file.id), action: 'found' }
      : { ok: false, error: `No ${base}.pptx in HubSpot folder "${folder}"` };
  }

  const local = pptxPath || findProposalPptx(friendlyName);
  if (!local || !existsSync(local)) {
    return { ok: false, error: `No *_Proposal.pptx found in ${friendlyName}/` };
  }
  const blob = new Blob([readFileSync(local)], {
    type: 'application/vnd.openxmlformats-officedocument.presentationml.presentation',
  });

  const form = new FormData();
  form.append('file', blob, `${base}.pptx`);
  let r;
  let action;
  if (existing.file) {
    form.append('options', JSON.stringify({ access: ACCESS }));
    r = await call(fetchImpl, token, 'PUT', `/files/v3/files/${existing.file.id}`, form);
    action = 'replaced';
  } else {
    form.append('folderId', folderRes.id);
    form.append('fileName', `${base}.pptx`);
    form.append('options', JSON.stringify({
      access: ACCESS,
      overwrite: false,
      duplicateValidationStrategy: 'NONE',
      duplicateValidationScope: 'EXACT_FOLDER',
    }));
    r = await call(fetchImpl, token, 'POST', '/files/v3/files', form);
    action = 'uploaded';
  }
  if (!r.ok) return { ok: false, error: apiError(action === 'replaced' ? 'Replacing the deck' : 'Uploading the deck', r) };

  const url = fileLink(r.json) || fileLink(existing.file);
  if (!url) return { ok: false, error: 'HubSpot returned no file URL' };
  const result = { ok: true, url, file_id: String(r.json?.id ?? existing.file?.id), action, file: local };
  const previous = fileLink(existing.file);
  if (previous && previous !== url) result.warning = `Link changed on replace (was ${previous})`;

  if (!(await linkWorks(fetchImpl, url))) {
    return { ok: false, error: `Uploaded, but the link does not open: ${url}` };
  }
  return result;
}

async function main() {
  const args = process.argv.slice(2);
  const valueOf = flag => (args.indexOf(flag) >= 0 ? args[args.indexOf(flag) + 1] : undefined);
  const friendlyName = args.find((a, i) => !a.startsWith('--') && !['--folder', '--file'].includes(args[i - 1]));
  const folder = valueOf('--folder') ?? DEFAULT_FOLDER;
  const pptxPath = valueOf('--file') || undefined;
  if (!friendlyName || !folder) {
    console.log(JSON.stringify({ ok: false, error: 'Usage: upload-proposal-to-hubspot.mjs <friendly-name> [--lookup] [--folder <name>] [--file <pptx>]' }));
    process.exit(1);
  }
  let result;
  try {
    result = await uploadProposal({
      friendlyName: basename(friendlyName),
      token: process.env.HUBSPOT_TOKEN,
      folder,
      lookup: args.includes('--lookup'),
      pptxPath,
    });
  } catch (e) {
    result = { ok: false, error: `Unexpected error: ${e.message}` };
  }
  console.log(JSON.stringify(result));
  process.exit(result.ok ? 0 : 1);
}

if (import.meta.url === pathToFileURL(process.argv[1]).href) {
  main();
}
