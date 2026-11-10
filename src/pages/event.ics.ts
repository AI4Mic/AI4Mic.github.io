import type { APIRoute } from 'astro';
import { getCollection } from 'astro:content';

// RFC 5545 text escaping
const esc = (s: string) => s.replace(/[\\;,]/g, (c) => `\\${c}`);

function icsDate(d: Date): string {
  return d.toISOString().slice(0, 10).replace(/-/g, '');
}

export const GET: APIRoute = async () => {
  const event = (await getCollection('event')).at(0)?.data;
  if (!event) return new Response('event data missing', { status: 500 });
  const endInclusive = new Date(event.end.getTime() + 86_400_000); // day after end, all-day DTEND is exclusive
  const lines = [
    'BEGIN:VCALENDAR',
    'VERSION:2.0',
    'PRODID:-//AI in Action//EN',
    'BEGIN:VEVENT',
    `UID:${icsDate(event.start)}-ai4mic@ai4mic.github.io`,
    'DTSTAMP:20260101T000000Z',
    `SUMMARY:${esc(`${event.shortName} workshop, ${event.venue.city}`)}`,
    `DTSTART;VALUE=DATE:${icsDate(event.start)}`,
    `DTEND;VALUE=DATE:${icsDate(endInclusive)}`,
    `LOCATION:${esc(`${event.venue.name}, ${event.venue.city}, ${event.venue.country}`)}`,
    `URL:https://ai4mic.github.io/`,
    'END:VEVENT',
    'END:VCALENDAR',
  ];
  return new Response(lines.join('\r\n'), {
    headers: { 'Content-Type': 'text/calendar; charset=utf-8' },
  });
};
