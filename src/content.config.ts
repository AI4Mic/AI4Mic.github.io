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
    }),
    format: z.string(),
    intro: z.string(),
    audience: z.string(),
    applications: z.object({
      opens: z.coerce.date(),
      closes: z.coerce.date(),
      url: z.string(),
    }),
    timeline: z.array(z.object({ date: z.coerce.date(), label: z.string() })),
    learn: z.array(z.object({ title: z.string(), text: z.string() })),
    bursary: z.object({ heading: z.string(), text: z.string() }),
    funders: z.array(z.object({ name: z.string(), url: z.string(), logo: z.string().optional() })),
    note: z.string(),
  }),
});

export const collections = { event };
