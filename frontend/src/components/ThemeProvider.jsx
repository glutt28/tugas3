import { createContext, useContext, useEffect, useState } from "react"

const ThemeContext = createContext(undefined)

export function ThemeProvider({ children, ...props }) {
  const [theme, setTheme] = useState(() => {
    if (typeof window !== "undefined") {
      const savedTheme = localStorage.getItem("theme")
      if (savedTheme) {
        return savedTheme
      }
      // Periksa preferensi sistem
      const prefersDark = window.matchMedia("(prefers-color-scheme: dark)").matches
      return prefersDark ? "dark" : "light"
    }
    return "light"
  })

  useEffect(() => {
    const root = window.document.documentElement
    root.classList.remove("light", "dark")
    root.classList.add(theme)
    localStorage.setItem("theme", theme)
  }, [theme])

  const value = {
    theme,
    setTheme,
  }

  return (
    <ThemeContext.Provider {...props} value={value}>
      {children}
    </ThemeContext.Provider>
  )
}

export const useTheme = () => {
  const context = useContext(ThemeContext)
  if (context === undefined)
    throw new Error("useTheme must be used within a ThemeProvider")
  return context
}

