# Frontend - Product Review Analyzer

Modern React frontend dengan **Vite**, **Tailwind CSS 4**, dan **Framer Motion**.

## ✨ Features

- 🎨 **Modern Design**: Glassmorphism, smooth animations, dark mode
- 📱 **Responsive**: Mobile-first dengan split-screen layout
- 🎭 **Animations**: Framer Motion untuk transisi halus
- 🌙 **Dark Mode**: Theme switching dengan transisi smooth
- 🎠 **Carousel**: Embla Carousel untuk browsing reviews
- ♿ **Accessible**: High contrast, keyboard navigation

## 🚀 Quick Start

```bash
# Install dependencies
npm install

# Start development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview
```

## 🛠️ Tech Stack

- **Vite 5**: Build tool
- **React 18**: UI library
- **Tailwind CSS 4**: Styling
- **Framer Motion**: Animations
- **Radix UI**: Accessible components
- **Embla Carousel**: Carousel
- **Lucide React**: Icons

## 📁 Structure

```
frontend/
├── src/
│   ├── components/
│   │   ├── ui/          # shadcn/ui components
│   │   ├── Header.jsx   # Fixed header with navigation
│   │   ├── ReviewForm.jsx
│   │   ├── ReviewList.jsx
│   │   ├── ReviewCarousel.jsx
│   │   ├── ThemeProvider.jsx
│   │   └── ThemeToggle.jsx
│   ├── lib/
│   │   └── utils.js     # Utility functions
│   ├── App.jsx          # Main app component
│   ├── main.jsx         # Entry point
│   └── index.css        # Global styles & Tailwind
├── index.html
├── vite.config.js
└── tailwind.config.js
```

## 🎨 Design System

Lihat [DESIGN.md](./DESIGN.md) untuk detail design system.

## 🌙 Dark Mode

Dark mode diaktifkan secara default. Toggle di header untuk switch theme.

## 📱 Responsive Breakpoints

- **Mobile**: < 768px (stacked layout)
- **Tablet**: 768px - 1024px
- **Desktop**: > 1024px (split-screen)

## 🔧 Configuration

### Environment Variables

Buat file `.env` (opsional):

```env
VITE_API_URL=http://localhost:8000
```

### Tailwind Config

Customize di `tailwind.config.js` untuk mengubah:
- Colors
- Spacing
- Animations
- Breakpoints

## 🎯 Features Detail

### Split-Screen Layout
- **Desktop**: Carousel fixed di kiri, konten scrollable di kanan
- **Mobile**: Stacked dengan carousel di atas

### Carousel
- Autoplay setiap 5 detik
- Navigation dengan dots dan arrows
- Smooth transitions

### Animations
- Page load: fade + slide
- Cards: hover scale + shadow
- List: stagger animation
- Smooth scroll behavior

### Loading States
- Skeleton loaders untuk better UX
- Loading spinners pada buttons
- Progressive loading

## 📝 Catatan

- Semua komponen menggunakan CSS variables untuk theming
- Glassmorphism effects dengan backdrop-blur
- High contrast untuk accessibility
- Smooth transitions untuk semua interaksi
