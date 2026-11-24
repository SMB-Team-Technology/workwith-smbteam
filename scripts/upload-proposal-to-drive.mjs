import { readFile } from 'node:fs/promises';
import { randomUUID } from 'node:crypto';
import { pathToFileURL } from 'node:url';

const folder = '0AB92lnIjHcNvUk9PVA';
const mimeType = 'application/vnd.openxmlformats-officedocument.presentationml.presentation';
const api = 'https://www.googleapis.com';

const viewUrl = (id) => `https://drive.google.com/file/d/${id}/view`;

function checkFirm(firm) {
  if (!/^[a-z0-9][a-z0-9-]*$/.test(firm)) throw new Error('Expected a firm slug');
}

async function request(fetchImpl, url, options, operation) {
  const response = await fetchImpl(url, options);
  if (!response.ok) throw new Error(`Drive ${operation} failed (HTTP ${response.status})`);
  return response.json();
}

// Search every drive the service account can reach (corpora=allDrives), not
// just its own files: the default can miss a file in a Shared Drive, and then
// every re-run would create a new file with a new link. The parent filter keeps
// it to this folder, whether it is a Shared Drive or a folder inside one.
async function findExisting({ firm, token, fetchImpl }) {
  const query = new URLSearchParams({
    q: `'${folder}' in parents and name = '${firm}-proposal.pptx' and trashed = false`,
    corpora: 'allDrives',
    supportsAllDrives: 'true', includeItemsFromAllDrives: 'true',
    fields: 'nextPageToken,files(id)', pageSize: '2',
  });
  const found = await request(fetchImpl, `${api}/drive/v3/files?${query}`, { headers: { Authorization: `Bearer ${token}` } }, 'lookup');
  if (found.nextPageToken || found.files.length > 1) throw new Error('Drive lookup did not return a unique match');
  return found.files[0]?.id;
}

// Read-only: the existing deck's link, or an error if it was never uploaded.
export async function lookupProposal({ firm, token, fetchImpl = fetch }) {
  if (!token) throw new Error('No Google Drive access token');
  checkFirm(firm);
  const existing = await findExisting({ firm, token, fetchImpl });
  if (!existing) throw new Error(`No deck named ${firm}-proposal.pptx in the Drive folder`);
  return viewUrl(existing);
}

export async function uploadProposal({ firm, file, token, fetchImpl = fetch }) {
  if (!token) throw new Error('No Google Drive access token');
  checkFirm(firm);
  if (!file?.endsWith('.pptx')) throw new Error('Expected a firm slug and a .pptx path');
  const bytes = await readFile(file);
  const name = `${firm}-proposal.pptx`;
  const existing = await findExisting({ firm, token, fetchImpl });
  const metadata = existing ? { name } : { name, parents: [folder], mimeType };
  const boundary = randomUUID();
  const body = Buffer.concat([
    Buffer.from(`--${boundary}\r\nContent-Type: application/json; charset=UTF-8\r\n\r\n${JSON.stringify(metadata)}\r\n--${boundary}\r\nContent-Type: ${mimeType}\r\n\r\n`),
    bytes, Buffer.from(`\r\n--${boundary}--\r\n`),
  ]);
  const suffix = existing ? `/${encodeURIComponent(existing)}` : '';
  const result = await request(fetchImpl, `${api}/upload/drive/v3/files${suffix}?uploadType=multipart&supportsAllDrives=true&fields=id`, {
    method: existing ? 'PATCH' : 'POST',
    headers: { Authorization: `Bearer ${token}`, 'Content-Type': `multipart/related; boundary=${boundary}` }, body,
  }, 'upload');
  if (typeof result.id !== 'string' || !/^[\w-]+$/.test(result.id)) throw new Error('Drive did not return a valid file ID');
  return viewUrl(result.id);
}

if (process.argv[1] && import.meta.url === pathToFileURL(process.argv[1]).href) {
  try {
    // node upload-proposal-to-drive.mjs <friendly-name> <deck.pptx>   upload or update in place
    // node upload-proposal-to-drive.mjs <friendly-name> --lookup       only find the existing link
    const [, , firm, arg] = process.argv;
    const token = process.env.DRIVE_ACCESS_TOKEN;
    const url = arg === '--lookup' ? await lookupProposal({ firm, token }) : await uploadProposal({ firm, file: arg, token });
    console.log(JSON.stringify({ ok: true, url }));
  } catch (error) {
    console.log(JSON.stringify({ ok: false, error: error.message }));
    process.exitCode = 1;
  }
}
