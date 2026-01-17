export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'tech-blue': '#2A5CAA',
        'pixel-green': '#4CAF50',
        'pixel-red': '#F44336',
        'bg-dark': '#1A2332',
        'bg-darker': '#0F1520',
        'pixel-yellow': '#F5E6CA',
        'pixel-brick': '#B85C38',
        'pixel-olive': '#6B8C42',
        'data-gold': '#FFD700',
        'text-light': '#CCCCCC',
      },
      fontFamily: {
        'pixel': ['monospace'],
      },
    },
  },
  plugins: [],
}