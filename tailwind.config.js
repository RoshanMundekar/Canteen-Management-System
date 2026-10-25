/** Tailwind build for the Django templates. Rebuild with: npm run build:css */
module.exports = {
  content: [
    './templates/**/*.html',
    './*/templates/**/*.html',
  ],
  theme: {
    extend: {
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
        serif: ['"Source Serif 4"', 'Georgia', 'serif'],
      },
      colors: {
        navy: { 50: '#EEF3FA', 100: '#D9E3F2', 200: '#B3C7E4', 300: '#7F9FCC', 400: '#4C76B0', 500: '#2B5A96', 600: '#1F4A80', 700: '#183C69', 800: '#122F53', 900: '#0B1F3A', 950: '#06142A' },
        gold: { 50: '#FBF7E9', 100: '#F5ECC9', 300: '#E3CB72', 400: '#D9B84A', 500: '#C9A227', 600: '#A8861A', 700: '#836913' },
      },
      boxShadow: { card: '0 1px 2px rgba(11,31,58,.06), 0 4px 16px rgba(11,31,58,.06)' },
    },
  },
};
