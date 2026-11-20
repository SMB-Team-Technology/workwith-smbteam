#!/usr/bin/env node
/**
 * Download a product source deck (e.g. Vanessa's LeadsOS marketing deck) from
 * the HubSpot file manager so the proposal deck engine can copy its slides.
 *
 * The decks live as PRIVATE files in the "Proposal Source Decks" folder — the
 * repo is public, so they are never committed. Each build downloads the
 * newest .pptx in that folder whose name contains the keyword ("LeadsOS"), so
 * a new version can be uploaded under any name ("… FINAL (2)", "v3").
 *
 * Usage:
 *   node scripts/fetch-source-deck.mjs                       LeadsOS → .source-decks/LeadsOS.pptx
 *   node scripts/fetch-source-deck.mjs --keyword LeadsOS --out .source-decks/LeadsOS.pptx
 *
 * Env: HUBSPOT_TOKEN (private app token; needs the `files` scope).
 *
 * Prints one JSON line on stdout:
 *   {"ok":true,"file":".source-decks/LeadsOS.pptx","name":"…","file_id":"…","updated":"…"}
 *   {"ok":false,"error":"…"}
 * Exit codes: 0 ok, 1 failed (JSON is printed either way).
 */

import { mkdirSync, writeFileSync } from 'fs';
import { dirname } from 'path';
import { pathToFileURL } from 'url';

const API = 'https://api.hubapi.com';
export const SOURCE_FOLDER = 'Proposal Source Decks';

async function call(fetchImpl, token, path) {
  const res = await fetchImpl(`${API}${path}`, { headers: { Authorization: `Bearer ${token}` } });
  const text = await res.text();
  let json = null;
  try { json = text ? JSON.parse(text) : null; } catch { /* not JSON */ }
  return { status: res.status, ok: res.ok, json, text };
}

function apiError(step, r) {
  const msg = r.json?.message || r.text?.slice(0, 300) || '';
  const hint = r.status === 401 || r.status === 403 ? ' (check the HubSpot token has the `files` scope)' : '';
  return `${step} failed: HTTP ${r.status}${msg ? ` — ${msg}` : ''}${hint}`;
}

/** Newest non-archived .pptx in the folder whose name contains the keyword. */
export function pickNewest(results, keyword, folderId) {
  const k = keyword.toLowerCase();
  const time = f => Date.parse(f.updatedAt || f.createdAt || 0) || 0;
  return (results || [])
    .filter(f => f && !f.archived && (f.extension || '').toLowerCase() === 'pptx'
      && String(f.name || '').toLowerCase().includes(k)
      && (f.parentFolderId == null || String(f.parentFolderId) === String(folderId)))
    .sort((a, b) => time(b) - time(a))[0] || null;
}

export async function fetchSourceDeck({
  token, keyword = 'LeadsOS', out = '.source-decks/LeadsOS.pptx', folder = SOURCE_FOLDER, fetchImpl = fetch,
}) {
  if (!token) return { ok: false, error: 'HUBSPOT_TOKEN is not set' };

  const f = await call(fetchImpl, token, `/files/v3/folders/${encodeURIComponent(folder)}`);
  if (f.status === 404) return { ok: false, error: `Folder "${folder}" not found in HubSpot` };
  if (!f.ok || !f.json?.id) return { ok: false, error: apiError(`Finding folder "${folder}"`, f) };
  const folderId = String(f.json.id);

  const q = new URLSearchParams({ parentFolderIds: folderId, extension: 'pptx', limit: '100' });
  const s = await call(fetchImpl, token, `/files/v3/files/search?${q}`);
  if (!s.ok) return { ok: false, error: apiError('Searching the source decks', s) };
  const file = pickNewest(s.json?.results, keyword, folderId);
  if (!file) return { ok: false, error: `No .pptx with "${keyword}" in its name in HubSpot folder "${folder}"` };

  // Private files have no public link: ask for a short-lived signed URL.
  const u = await call(fetchImpl, token, `/files/v3/files/${encodeURIComponent(file.id)}/signed-url`);
  if (!u.ok || !u.json?.url) return { ok: false, error: apiError(`Getting a download link for "${file.name}"`, u) };

  const dl = await fetchImpl(u.json.url);
  if (!dl.ok) return { ok: false, error: `Downloading "${file.name}" failed: HTTP ${dl.status}` };
  const bytes = Buffer.from(await dl.arrayBuffer());
  // A .pptx is a zip: refuse an HTML error page or an empty body.
  if (bytes.length < 1000 || bytes[0] !== 0x50 || bytes[1] !== 0x4b) {
    return { ok: false, error: `Downloaded "${file.name}" is not a .pptx file (${bytes.length} bytes)` };
  }
  mkdirSync(dirname(out), { recursive: true });
  writeFileSync(out, bytes);
  return { ok: true, file: out, name: file.name, file_id: String(file.id), updated: file.updatedAt || null };
}

if (import.meta.url === pathToFileURL(process.argv[1] || '').href) {
  const args = process.argv.slice(2);
  const opt = name => { const i = args.indexOf(name); return i >= 0 ? args[i + 1] : undefined; };
  const keyword = opt('--keyword') || 'LeadsOS';
  const out = opt('--out') || `.source-decks/${keyword}.pptx`;
  const result = await fetchSourceDeck({ token: process.env.HUBSPOT_TOKEN, keyword, out });
  console.log(JSON.stringify(result));
  process.exit(result.ok ? 0 : 1);
}
