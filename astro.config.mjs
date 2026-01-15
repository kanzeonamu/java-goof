import { defineConfig } from 'astro/config';

export default defineConfig({
  site: 'https://standing.one',
  integrations: [],
  output: 'static',
  build: {
    format: 'directory'
  }
});
