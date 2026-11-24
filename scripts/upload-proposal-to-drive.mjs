import { readFile } from 'node:fs/promises';
import { randomUUID } from 'node:crypto';
import { pathToFileURL } from 'node:url';

const folder = '0AB92lnIjHcNvUk9PVA';
const mimeType = 'application/vnd.openxmlformats-officedocument.presentationml.presentation';
const api = 'https://www.googleapis.com';

export async function uploadProposal({ firm, file, token, fetchImpl = fetch }) {
  if (!token) throw new Error('No Google Drive access token');
  if (!/^[a-z0-9][a-z0-9-]*$/.test(firm) || !file?.endsWith('.pptx')) throw new Error('Expected a firm slug and a .pptx path');
  const bytes = await readFile(file);
  const name = `${firm}-proposal.pptx`;
  const headers = { Authorization: `Bearer ${token}` };
  async function request(url, options, operation) {
    const response = await fetchImpl(url, options);
    if (!response.ok) throw new Error(`Drive ${operation} failed (HTTP ${response.status})`);
    return response.json();
  }
  const query = new URLSearchParams({
    q: `'${folder}' in parents and name = '${name}' and trashed = false`,
    supportsAllDrives: 'true', includeItemsFromAllDrives: 'true',
    fields: 'nextPageToken,files(id)', pageSize: '2',
  });
  const found = await request(`${api}/drive/v3/files?${query}`, { headers }, 'lookup');
  if (found.nextPageToken || found.files.length > 1) throw new Error('Drive lookup did not return a unique match');
  const existing = found.files[0]?.id;
  const metadata = existing ? { name } : { name, parents: [folder], mimeType };
  const boundary = randomUUID();
  const body = Buffer.concat([
    Buffer.from(`--${boundary}\r\nContent-Type: application/json; charset=UTF-8\r\n\r\n${JSON.stringify(metadata)}\r\n--${boundary}\r\nContent-Type: ${mimeType}\r\n\r\n`),
    bytes, Buffer.from(`\r\n--${boundary}--\r\n`),
  ]);
  const suffix = existing ? `/${encodeURIComponent(existing)}` : '';
  const result = await request(`${api}/upload/drive/v3/files${suffix}?uploadType=multipart&supportsAllDrives=true&fields=id`, {
    method: existing ? 'PATCH' : 'POST',
    headers: { ...headers, 'Content-Type': `multipart/related; boundary=${boundary}` }, body,
  }, 'upload');
  if (typeof result.id !== 'string' || !/^[\w-]+$/.test(result.id)) throw new Error('Drive did not return a valid file ID');
  return `https://drive.google.com/file/d/${result.id}/view`;
}

if (process.argv[1] && import.meta.url === pathToFileURL(process.argv[1]).href) {
  try {
    const [, , firm, file] = process.argv;
    const url = await uploadProposal({ firm, file, token: process.env.DRIVE_ACCESS_TOKEN });
    console.log(JSON.stringify({ ok: true, url }));
  } catch (error) {
    console.log(JSON.stringify({ ok: false, error: error.message }));
    process.exitCode = 1;
  }
}
