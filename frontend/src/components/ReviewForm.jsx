import React, { useState } from "react"
import { motion } from "framer-motion"
import { Send, Loader2 } from "lucide-react"
import { Button } from "./ui/button"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "./ui/card"
import { Skeleton } from "./ui/skeleton"

export function ReviewForm({ onSubmit, loading }) {
  const [reviewText, setReviewText] = useState("")

  const handleSubmit = (e) => {
    e.preventDefault()
    if (reviewText.trim()) {
      onSubmit(reviewText)
      setReviewText("")
    }
  }

  return (
    <Card className="glass-card">
      <CardHeader>
        <CardTitle className="flex items-center space-x-2">
          <span>📝</span>
          <span>Analisis Review</span>
        </CardTitle>
        <CardDescription>
          Masukkan review produk untuk menganalisis sentimen dan mengekstrak poin penting
        </CardDescription>
      </CardHeader>
      <CardContent>
        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="space-y-2">
            <label
              htmlFor="review-text"
              className="text-sm font-medium text-foreground"
            >
              Teks Review
            </label>
            <textarea
              id="review-text"
              value={reviewText}
              onChange={(e) => setReviewText(e.target.value)}
              placeholder="Ketik review produk Anda di sini... Contoh: Produk ini sangat bagus! Kualitasnya mantap dan pengiriman cepat. Sangat direkomendasikan!"
              rows="6"
              disabled={loading}
              required
              className="w-full px-4 py-3 rounded-lg bg-background/50 border border-input text-foreground placeholder:text-muted-foreground focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed transition-all resize-none"
            />
            <p className="text-xs text-muted-foreground">
              {reviewText.length} karakter
            </p>
          </div>
          <Button
            type="submit"
            disabled={loading || !reviewText.trim()}
            className="w-full group"
            size="lg"
          >
            {loading ? (
              <>
                <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                Menganalisis...
              </>
            ) : (
              <>
                <Send className="mr-2 h-4 w-4 group-hover:translate-x-1 transition-transform" />
                Analisis Review
              </>
            )}
          </Button>
        </form>
      </CardContent>
    </Card>
  )
}
