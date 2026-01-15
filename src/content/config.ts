import { defineCollection, z } from 'astro:content';

const conditionsCollection = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    description: z.string(),
    lastUpdated: z.string(),
    tags: z.array(z.string()).optional(),
  }),
});

const topicsCollection = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    description: z.string(),
    lastUpdated: z.string(),
    tags: z.array(z.string()).optional(),
  }),
});

export const collections = {
  conditions: conditionsCollection,
  topics: topicsCollection,
};
