import { defineCollection, z } from 'astro:content';
import { file } from 'astro/loaders';
import yaml from 'yaml';

// Each YAML file is the single source of truth; the schemas only validate shape.
// file() on a single object stores it under the key 'event'; arrays need ids, so
// faq (array) is loaded through a small typed helper in src/lib/content.ts instead.
const event = defineCollection({
  loader: file('src/data/event.yaml', {
    parser: (text) => ({ event: yaml.parse(text) }),
  }),
  schema: z.object({
    shortName: z.string(),
    title: z.string(),
    subtitle: z.string(),
    start: z.coerce.date(),
    end: z.coerce.date(),
    datesDisplay: z.string(),
    timezone: z.string(),
    venue: z.object({
      name: z.string(),
      city: z.string(),
      country: z.string(),
      url: z.string().optional(),
      campus: z.string(),
      map: z.string(),
    }),
    contact: z.string(),
    format: z.string(),
    intro: z.string(),
    audience: z.string(),
    applications: z.object({
      opens: z.coerce.date(),
      closes: z.coerce.date(),
      url: z.string(),
      text: z.string(),
      needs: z.array(z.string()),
    }),
    timeline: z.array(z.object({ date: z.coerce.date(), label: z.string() })),
    learn: z.array(z.object({ title: z.string(), text: z.string() })),
    fees: z.object({
      rows: z.array(z.object({ attendance: z.string(), standard: z.string(), tableC: z.string() })),
      notes: z.array(z.string()),
    }),
    fellowships: z.object({
      heading: z.string(),
      text: z.string(),
      tiers: z.array(z.object({ name: z.string(), text: z.string() })),
      notes: z.array(z.string()),
    }),
    travel: z.array(z.object({ title: z.string(), text: z.string() })),
    accessibility: z.string(),
    cancellation: z.array(z.object({ name: z.string(), text: z.string() })),
    funders: z.array(z.object({ name: z.string(), url: z.string(), logo: z.string().optional() })),
    note: z.string(),
  }),
});

export const collections = { event };
