import React, { useState, useEffect } from "react"
import { motion } from "framer-motion"
import { ThemeProvider } from "./components/ThemeProvider"
import { Header } from "./components/Header"
import { ReviewForm } from "./components/ReviewForm"
import { ReviewList } from "./components/ReviewList"
import { ReviewCarousel } from "./components/ReviewCarousel"
import { Skeleton } from "./components/ui/skeleton"
import { Card } from "./components/ui/card"

const API_BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:8000"

function App() {
  const [reviews, setReviews] = useState([])
  const [loading, setLoading] = useState(false)
  const [initialLoading, setInitialLoading] = useState(true)
  const [error, setError] = useState(null)

  const fetchReviews = async () => {
    try {
      setLoading(true)
      setError(null)
      const response = await fetch(`${API_BASE_URL}/api/reviews`, {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
        },
      })
      if (!response.ok) {
        const errorText = await response.text()
        let errorMessage = "Gagal mengambil review"
        try {
          const errorData = JSON.parse(errorText)
          errorMessage = errorData.detail || errorMessage
        } catch {
          errorMessage = `Error server: ${response.status} ${response.statusText}`
        }
        throw new Error(errorMessage)
      }
      const data = await response.json()
      setReviews(data)
    } catch (err) {
      // Periksa apakah ini error jaringan
      if (err.message === "Failed to fetch" || err.name === "TypeError") {
        setError(
          "Tidak dapat terhubung ke server backend. Pastikan backend sedang berjalan di http://localhost:8000"
        )
      } else {
        setError(err.message)
      }
    } finally {
      setLoading(false)
      setInitialLoading(false)
    }
  }

  useEffect(() => {
    // Periksa kesehatan backend terlebih dahulu
    const checkBackend = async () => {
      try {
        const response = await fetch(`${API_BASE_URL}/api/health`)
        if (response.ok) {
          const health = await response.json()
          console.log("Backend health:", health)
        }
      } catch (err) {
        console.warn("Backend health check failed:", err)
      }
    }
    
    checkBackend()
    fetchReviews()
  }, [])

  const handleReviewSubmit = async (reviewText) => {
    try {
      setLoading(true)
      setError(null)
      const response = await fetch(`${API_BASE_URL}/api/analyze-review`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ review_text: reviewText }),
      })

      if (!response.ok) {
        let errorMessage = "Gagal menganalisis review"
        try {
          const errorData = await response.json()
          errorMessage = errorData.detail || errorMessage
        } catch {
          errorMessage = `Error server: ${response.status} ${response.statusText}`
        }
        throw new Error(errorMessage)
      }

      const newReview = await response.json()
      setReviews([newReview, ...reviews])
      setError(null) // Clear any previous errors on success
    } catch (err) {
      // Periksa apakah ini error jaringan
      if (err.message === "Failed to fetch" || err.name === "TypeError") {
        setError(
          "Tidak dapat terhubung ke server backend. Pastikan backend sedang berjalan di http://localhost:8000"
        )
      } else {
        setError(err.message)
      }
    } finally {
      setLoading(false)
    }
  }

  const handleDeleteReview = async (reviewId) => {
    try {
      setLoading(true)
      setError(null)
      const response = await fetch(`${API_BASE_URL}/api/reviews/${reviewId}`, {
        method: "DELETE",
        headers: {
          "Content-Type": "application/json",
        },
      })

      if (!response.ok) {
        let errorMessage = "Gagal menghapus review"
        try {
          const errorData = await response.json()
          errorMessage = errorData.detail || errorMessage
        } catch {
          errorMessage = `Error server: ${response.status} ${response.statusText}`
        }
        throw new Error(errorMessage)
      }

      // Hapus dari state
      setReviews(reviews.filter((review) => review.id !== reviewId))
      setError(null)
    } catch (err) {
      // Periksa apakah ini error jaringan
      if (err.message === "Failed to fetch" || err.name === "TypeError") {
        setError(
          "Tidak dapat terhubung ke server backend. Pastikan backend sedang berjalan di http://localhost:8000"
        )
      } else {
        setError(err.message)
      }
    } finally {
      setLoading(false)
    }
  }

  return (
    <ThemeProvider>
      <div className="min-h-screen bg-background smooth-scroll">
        <Header />
        
        <main className="pt-16">
          {/* Tata Letak Layar Terpisah */}
          <div className="flex flex-col lg:flex-row h-[calc(100vh-4rem)]">
            {/* Sisi Kiri - Carousel (Tetap pada Desktop) */}
            <motion.div
              initial={{ x: -100, opacity: 0 }}
              animate={{ x: 0, opacity: 1 }}
              transition={{ duration: 0.5 }}
              className="w-full lg:w-1/2 border-r border-border/50 p-4 lg:p-6 overflow-hidden"
            >
              <div className="h-full flex flex-col">
                <div className="mb-4">
                  <h2 className="text-2xl font-bold text-gradient mb-2">
                    Review Terbaru
                  </h2>
                  <p className="text-sm text-muted-foreground">
                    Jelajahi review yang telah dianalisis
                  </p>
                </div>
                {initialLoading ? (
                  <div className="flex-1 space-y-4">
                    {[1, 2, 3].map((i) => (
                      <Card key={i} className="p-6">
                        <Skeleton className="h-4 w-1/4 mb-4" />
                        <Skeleton className="h-20 w-full mb-2" />
                        <Skeleton className="h-4 w-3/4" />
                      </Card>
                    ))}
                  </div>
                ) : (
                  <ReviewCarousel reviews={reviews.slice(0, 5)} />
                )}
              </div>
            </motion.div>

            {/* Sisi Kanan - Konten (Dapat digulir) */}
            <motion.div
              initial={{ x: 100, opacity: 0 }}
              animate={{ x: 0, opacity: 1 }}
              transition={{ duration: 0.5, delay: 0.2 }}
              className="w-full lg:w-1/2 overflow-y-auto smooth-scroll"
              id="analyze"
            >
              <div className="p-4 lg:p-6 space-y-6">
                {/* Bagian Hero */}
                <div className="text-center space-y-4 mb-8">
                  <motion.h1
                    initial={{ y: 20, opacity: 0 }}
                    animate={{ y: 0, opacity: 1 }}
                    transition={{ delay: 0.3 }}
                    className="text-4xl lg:text-5xl font-bold"
                  >
                    <span className="text-gradient">Analisis Review</span>
                    <br />
                    <span className="text-foreground">Produk</span>
                  </motion.h1>
                  <motion.p
                    initial={{ y: 20, opacity: 0 }}
                    animate={{ y: 0, opacity: 1 }}
                    transition={{ delay: 0.4 }}
                    className="text-muted-foreground text-lg"
                  >
                    Analisis sentimen dan ekstraksi poin penting berbasis AI
                  </motion.p>
                </div>

                {/* Pesan Error */}
                {error && (
                  <motion.div
                    initial={{ scale: 0.95, opacity: 0 }}
                    animate={{ scale: 1, opacity: 1 }}
                    className="glass-card p-4 border-destructive/50 bg-destructive/10"
                  >
                    <div className="flex items-start space-x-3">
                      <span className="text-xl">⚠️</span>
                      <div className="flex-1">
                        <p className="text-sm font-semibold text-destructive mb-1">
                          Error Koneksi
                        </p>
                        <p className="text-sm text-destructive/80">{error}</p>
                        <p className="text-xs text-muted-foreground mt-2">
                          Pastikan server backend sedang berjalan:
                          <code className="ml-1 px-1.5 py-0.5 bg-background/50 rounded text-xs">
                            cd backend && python main.py
                          </code>
                        </p>
                      </div>
                    </div>
                  </motion.div>
                )}

                {/* Form Ulasan */}
                <motion.div
                  initial={{ y: 20, opacity: 0 }}
                  animate={{ y: 0, opacity: 1 }}
                  transition={{ delay: 0.5 }}
                >
                  <ReviewForm onSubmit={handleReviewSubmit} loading={loading} />
                </motion.div>

                {/* Daftar Ulasan */}
                <motion.div
                  initial={{ y: 20, opacity: 0 }}
                  animate={{ y: 0, opacity: 1 }}
                  transition={{ delay: 0.6 }}
                  id="reviews"
                >
                  <ReviewList reviews={reviews} loading={loading} onDelete={handleDeleteReview} />
                </motion.div>
              </div>
            </motion.div>
          </div>
        </main>
      </div>
    </ThemeProvider>
  )
}

export default App
