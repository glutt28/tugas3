import { motion } from "framer-motion"
import { Menu, X } from "lucide-react"
import { useState } from "react"
import { ThemeToggle } from "./ThemeToggle"
import { Button } from "./ui/button"

export function Header() {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false)

  return (
    <motion.header
      initial={{ y: -100 }}
      animate={{ y: 0 }}
      className="fixed top-0 left-0 right-0 z-50 glass border-b border-border/50"
    >
      <div className="container mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="flex items-center space-x-2"
          >
            <h1 className="text-xl font-bold text-gradient">📊 Analisis Review</h1>
          </motion.div>

          {/* Navigasi Desktop */}
          <nav className="hidden md:flex items-center space-x-6">
            <a href="#analyze" className="text-foreground/80 hover:text-foreground transition-colors">
              Analisis
            </a>
            <a href="#reviews" className="text-foreground/80 hover:text-foreground transition-colors">
              Review
            </a>
            <ThemeToggle />
          </nav>

          {/* Tombol Menu Mobile */}
          <div className="flex items-center space-x-2 md:hidden">
            <ThemeToggle />
            <Button
              variant="ghost"
              size="icon"
              onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
            >
              {mobileMenuOpen ? (
                <X className="h-5 w-5" />
              ) : (
                <Menu className="h-5 w-5" />
              )}
            </Button>
          </div>
        </div>

        {/* Menu Mobile */}
        {mobileMenuOpen && (
          <motion.div
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: "auto" }}
            exit={{ opacity: 0, height: 0 }}
            className="md:hidden py-4 border-t border-border/50"
          >
            <nav className="flex flex-col space-y-4">
              <a
                href="#analyze"
                onClick={() => setMobileMenuOpen(false)}
                className="text-foreground/80 hover:text-foreground transition-colors"
              >
                Analisis
              </a>
              <a
                href="#reviews"
                onClick={() => setMobileMenuOpen(false)}
                className="text-foreground/80 hover:text-foreground transition-colors"
              >
                Review
              </a>
            </nav>
          </motion.div>
        )}
      </div>
    </motion.header>
  )
}

