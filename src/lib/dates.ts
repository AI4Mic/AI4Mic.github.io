const DAY_MS = 24 * 60 * 60 * 1000;

export function startOfDay(d: Date): number {
  return Math.floor(d.getTime() / DAY_MS);
}

/** Days from build time; negative means past. */
export function daysFromNow(d: Date): number {
  return startOfDay(d) - startOfDay(new Date());
}

export function formatDate(d: Date): string {
  return new Intl.DateTimeFormat('en-GB', {
    day: 'numeric',
    month: 'long',
    year: 'numeric',
    timeZone: 'UTC',
  }).format(d);
}
