module.exports = {
  content: [
    "./templates/**/*.html",
    "./static/js/**/*.js",
    // Add other paths to your content files here
  ],
  theme: {
    extend: {
      fontFamily: {
        display: ["Poppins", "sans-serif"],
      },
      colors: {
        primary: {
          100: "#E3F2F0",
          200: "#B9E0D8",
          300: "#8ECCBF",
          400: "#63B9A6",
          500: "#1A4D2E", // Base primary color
          600: "#164426",
          700: "#11331E",
          800: "#0C2215",
          900: "#06110B",
        },
        secondary: {
          100: "#E2E9E6",
          200: "#B6C4BE",
          300: "#8A9F95",
          400: "#5D7A6D",
          500: "#4F6F52", // Base secondary color
          600: "#445F48",
          700: "#374E3C",
          800: "#2A3C30",
          900: "#1D2923",
        },
        neutral: {
          100: "#FFFFFF",
          200: "#FAF9F7",
          300: "#F5EFE6", // Base neutral color
          400: "#EDE4D4",
          500: "#E5D8C1",
          600: "#DCCBAE",
          700: "#D3BE9B",
          800: "#CAB187",
          900: "#C1A373",
        },
        accent: {
          100: "#F8F4EC",
          200: "#F0E7D5",
          300: "#E8DFCA", // Base accent color
          400: "#DCCCB0",
          500: "#D0B896",
          600: "#C4A57D",
          700: "#B79163",
          800: "#A97D49",
          900: "#9C6930",
        },
      },
      fontFamily: {
        kode: ['"Kode Mono"', "monospace"],
        poppins: ["Poppins", "sans-serif"],
      },
    },
  },
  plugins: [],
};
