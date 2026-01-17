import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import { ReactInjectorVitePlugin } from 'yunji-tagger'
import path from 'path'

export default defineConfig({
  plugins: [react(), ReactInjectorVitePlugin()],
  build: {
    outDir: 'dist',
    emptyOutDir: true,
  },
  server: {
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
        secure: false,
      },
    },
  },
})