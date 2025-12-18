# Design System - Product Review Analyzer

## Color Palette

### Dark Theme (Default)
- **Background**: Deep blue-black (`hsl(222, 47%, 11%)`)
- **Foreground**: Light gray-white (`hsl(213, 31%, 91%)`)
- **Primary**: Bright blue (`hsl(217, 91%, 60%)`)
- **Secondary**: Dark blue-gray (`hsl(217, 33%, 17%)`)
- **Muted**: Medium gray (`hsl(215, 20%, 65%)`)
- **Border**: Subtle gray (`hsl(217, 33%, 25%)`)

### Accent Colors
- **Positive**: Green (`#4caf50`)
- **Negative**: Red (`#f44336`)
- **Neutral**: Yellow/Amber (`#ff9800`)

## Typography

- **Headings**: Bold, clean sans-serif
- **Body**: Regular weight, optimal line-height for readability
- **Spacing**: Consistent 4px base unit

## Components

### Glassmorphism
- Backdrop blur with semi-transparent backgrounds
- Subtle borders for depth
- Shadow effects for elevation

### Cards
- Rounded corners (`--radius: 0.75rem`)
- Hover effects with scale and shadow
- Smooth transitions

### Buttons
- Multiple variants (default, outline, ghost, etc.)
- Icon support
- Loading states
- Hover animations

## Layout

### Split-Screen
- **Desktop**: 50/50 split with fixed carousel left, scrollable content right
- **Mobile**: Stacked layout with full-width sections

### Responsive Breakpoints
- Mobile: < 768px
- Tablet: 768px - 1024px
- Desktop: > 1024px

## Animations

### Framer Motion
- Page transitions: fade + slide
- Card hover: scale + shadow
- List items: stagger animation
- Smooth scroll behavior

### Timing
- Fast: 0.2s
- Normal: 0.3s
- Slow: 0.5s

## Accessibility

- High contrast text
- Focus states on interactive elements
- Keyboard navigation support
- Screen reader friendly
- ARIA labels where needed

## Best Practices

1. **Consistent Spacing**: Use Tailwind spacing scale
2. **Color Usage**: Always use CSS variables for theming
3. **Animations**: Keep them subtle and purposeful
4. **Loading States**: Always show skeleton loaders
5. **Error Handling**: Clear, user-friendly messages

