# 🎨 Google Fonts Integration Guide for BookKeeper

## Where to Add Google Fonts

### 1. In `templates/base.html` (Line ~20)
Replace this section:
```html
<!-- Font Variables - Replace with Google Fonts -->
<style>
    /* ADD YOUR GOOGLE FONTS HERE */
    /* Example: @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800&display=swap'); */
    /* Then update the CSS variables in style.css:
       --font-primary: 'Poppins', sans-serif;
    */
</style>
```

With your chosen fonts:
```html
<!-- Google Fonts -->
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800&family=Inter:wght@300;400;500;600;700&family=Playfair+Display:wght@400;500;600;700&display=swap" rel="stylesheet">
```

### 2. In `static/css/style.css` (Line ~30)
Update the font variables:
```css
/* Font Variables - Updated with Google Fonts */
--font-primary: 'Inter', 'Segoe UI', system-ui, -apple-system, sans-serif;
--font-secondary: 'Playfair Display', 'Georgia', serif;
--font-accent: 'Poppins', sans-serif;
--font-mono: 'SF Mono', 'Monaco', monospace;
```

## 🚀 Recommended Font Combinations

### Modern & Clean
- **Primary**: Inter or Poppins
- **Headings**: Poppins or Montserrat
- **Accent**: Nunito Sans

```html
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Poppins:wght@400;500;600;700;800&display=swap" rel="stylesheet">
```

### Elegant & Professional
- **Primary**: Open Sans or Source Sans Pro
- **Headings**: Playfair Display or Crimson Text
- **Accent**: Lato

```html
<link href="https://fonts.googleapis.com/css2?family=Open+Sans:wght@300;400;500;600;700&family=Playfair+Display:wght@400;500;600;700&display=swap" rel="stylesheet">
```

### Modern & Playful
- **Primary**: Nunito or Rubik
- **Headings**: Outfit or Space Grotesk
- **Accent**: DM Sans

```html
<link href="https://fonts.googleapis.com/css2?family=Nunito:wght@300;400;500;600;700&family=Outfit:wght@400;500;600;700;800&display=swap" rel="stylesheet">
```

### Tech & Minimal
- **Primary**: IBM Plex Sans
- **Headings**: JetBrains Mono or Fira Code
- **Accent**: Work Sans

```html
<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500;600;700&display=swap" rel="stylesheet">
```

## 🎯 How to Apply Fonts to Specific Elements

Add these classes to your CSS after updating the font variables:

```css
/* Apply fonts to specific elements */
h1, h2, h3, h4, h5, h6 {
    font-family: var(--font-accent) !important; /* For headings */
}

.navbar-brand {
    font-family: var(--font-accent) !important;
}

body {
    font-family: var(--font-primary) !important;
}

.card-title {
    font-family: var(--font-secondary) !important;
}

.btn {
    font-family: var(--font-primary) !important;
}
```

## 📱 Performance Tips

1. **Use `&display=swap`** in your Google Fonts URL for better loading
2. **Preconnect** to Google Fonts domains (already added in base.html)
3. **Limit font weights** - only load what you need
4. **Consider using system fonts** for better performance on mobile

## 🎨 Current Color Palette (Already Implemented)
- **Primary**: #71C9CE (Teal)
- **Light**: #A6E3E9 (Light Teal)  
- **Lighter**: #CBF1F5 (Very Light Teal)
- **Lightest**: #E3FDFD (Pale Mint)

The fonts will work beautifully with this color scheme!

## ✅ Quick Start

1. Pick a font combination from above
2. Add the Google Fonts link to `base.html`
3. Update the CSS variables in `style.css`
4. Refresh your browser
5. Enjoy your beautiful new typography! 🎉

---
*Happy designing! Your BookKeeper app is now ready for some amazing typography.*
