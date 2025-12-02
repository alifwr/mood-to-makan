/** @type {import('tailwindcss').Config} */
module.exports = {
    content: [
        "./app/components/**/*.{js,vue,ts}",
        "./app/layouts/**/*.vue",
        "./app/pages/**/*.vue",
        "./app/plugins/**/*.{js,ts}",
        "./app/app.vue",
        "./app/error.vue",
    ],
    theme: {
        extend: {
            colors: {
                // Nature Distilled Palette
                nature: {
                    50: '#f7f6f4', // Lightest clay/paper
                    100: '#ebe9e4',
                    200: '#dcd8d0',
                    300: '#c6c0b3', // Muted beige
                    400: '#a8a090', // Clay
                    500: '#8c8372', // Earth
                    600: '#706859', // Deep soil
                    700: '#565044',
                    800: '#403b33', // Dark wood
                    900: '#2d2a24', // Almost black
                    950: '#1a1815',
                },
                // Accent colors (muted organic tones)
                leaf: {
                    400: '#9cb096', // Sage green
                    500: '#7a9174',
                    600: '#5c7057',
                },
                stone: {
                    400: '#a3a3a3',
                    500: '#78716c',
                    600: '#57534e',
                },
                sand: {
                    400: '#e3d5ca',
                    500: '#d5bdaf',
                    600: '#b09b8e',
                }
            },
            fontFamily: {
                sans: ['Outfit', 'Inter', 'sans-serif'],
                serif: ['Playfair Display', 'serif'], // For elegant headings
            },
            borderRadius: {
                'organic': '30% 70% 70% 30% / 30% 30% 70% 70%',
                'organic-2': '60% 40% 30% 70% / 60% 30% 70% 40%',
            },
            animation: {
                'float': 'float 6s ease-in-out infinite',
                'breathe': 'breathe 4s ease-in-out infinite',
            },
            keyframes: {
                float: {
                    '0%, 100%': { transform: 'translateY(0)' },
                    '50%': { transform: 'translateY(-20px)' },
                },
                breathe: {
                    '0%, 100%': { transform: 'scale(1)' },
                    '50%': { transform: 'scale(1.05)' },
                }
            }
        },
    },
    plugins: [],
}
