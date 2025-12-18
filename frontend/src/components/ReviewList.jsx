import React, { useState } from "react"
import { motion, AnimatePresence } from "framer-motion"
import { Trash2, MoreVertical } from "lucide-react"
import { Card, CardContent, CardHeader } from "./ui/card"
import { Skeleton } from "./ui/skeleton"
import { Badge } from "./ui/badge"
import { Button } from "./ui/button"
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "./ui/dialog"

function ReviewList({ reviews, loading, onDelete }) {
  const [deleteDialogOpen, setDeleteDialogOpen] = useState(false)
  const [reviewToDelete, setReviewToDelete] = useState(null)
  const [deleting, setDeleting] = useState(false)
  const getSentimentColor = (sentiment) => {
    switch (sentiment?.toLowerCase()) {
      case "positive":
        return "bg-green-500/20 text-green-400 border-green-500/30"
      case "negative":
        return "bg-red-500/20 text-red-400 border-red-500/30"
      case "neutral":
        return "bg-yellow-500/20 text-yellow-400 border-yellow-500/30"
      default:
        return "bg-gray-500/20 text-gray-400 border-gray-500/30"
    }
  }

  const getSentimentEmoji = (sentiment) => {
    switch (sentiment?.toLowerCase()) {
      case "positive":
        return "😊"
      case "negative":
        return "😞"
      case "neutral":
        return "😐"
      default:
        return "❓"
    }
  }

  const getSentimentLabel = (sentiment) => {
    switch (sentiment?.toLowerCase()) {
      case "positive":
        return "Positif"
      case "negative":
        return "Negatif"
      case "neutral":
        return "Netral"
      default:
        return sentiment || "Tidak Diketahui"
    }
  }

  if (loading && reviews.length === 0) {
    return (
      <div className="space-y-4">
        <h2 className="text-2xl font-bold">Hasil Analisis</h2>
        {[1, 2, 3].map((i) => (
          <Card key={i} className="glass-card">
            <CardHeader>
              <Skeleton className="h-6 w-1/4" />
            </CardHeader>
            <CardContent className="space-y-2">
              <Skeleton className="h-20 w-full" />
              <Skeleton className="h-4 w-3/4" />
            </CardContent>
          </Card>
        ))}
      </div>
    )
  }

  if (reviews.length === 0) {
    return (
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="text-center py-12"
      >
        <div className="text-6xl mb-4">📊</div>
        <h3 className="text-xl font-semibold mb-2">Belum ada review</h3>
        <p className="text-muted-foreground">
          Kirim review pertama Anda untuk memulai analisis!
        </p>
      </motion.div>
    )
  }

  const handleDeleteClick = (review) => {
    setReviewToDelete(review)
    setDeleteDialogOpen(true)
  }

  const handleConfirmDelete = async () => {
    if (!reviewToDelete) return
    
    setDeleting(true)
    try {
      await onDelete(reviewToDelete.id)
      setDeleteDialogOpen(false)
      setReviewToDelete(null)
    } catch (error) {
      console.error("Error deleting review:", error)
    } finally {
      setDeleting(false)
    }
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h2 className="text-2xl font-bold">Hasil Analisis</h2>
        <Badge variant="outline" className="text-sm">
          {reviews.length} {reviews.length === 1 ? "review" : "review"}
        </Badge>
      </div>

      <div className="grid gap-4">
        <AnimatePresence>
          {reviews.map((review, index) => (
            <motion.div
              key={review.id}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20, scale: 0.95 }}
              transition={{ delay: index * 0.1 }}
              whileHover={{ scale: 1.02 }}
            >
              <Card className="glass-card hover:shadow-xl hover:shadow-primary/20 transition-all group">
                <CardHeader>
                  <div className="flex items-center justify-between flex-wrap gap-2">
                    <div className="flex items-center space-x-3">
                      <span className="text-2xl">
                        {getSentimentEmoji(review.sentiment)}
                      </span>
                      <Badge
                        className={`${getSentimentColor(
                          review.sentiment
                        )} uppercase text-xs font-semibold`}
                      >
                        {getSentimentLabel(review.sentiment)}
                      </Badge>
                    </div>
                    <div className="flex items-center space-x-2">
                      <span className="text-xs text-muted-foreground">
                        {new Date(review.created_at).toLocaleString()}
                      </span>
                      <Button
                        variant="ghost"
                        size="icon"
                        className="h-8 w-8 opacity-0 group-hover:opacity-100 transition-opacity text-destructive hover:text-destructive hover:bg-destructive/10"
                        onClick={(e) => {
                          e.stopPropagation()
                          handleDeleteClick(review)
                        }}
                      >
                        <Trash2 className="h-4 w-4" />
                      </Button>
                    </div>
                  </div>
                </CardHeader>
              <CardContent className="space-y-4">
                <div>
                  <h4 className="text-sm font-semibold mb-2 text-muted-foreground uppercase tracking-wide">
                    Review
                  </h4>
                  <p className="text-sm leading-relaxed text-foreground/90">
                    {review.review_text}
                  </p>
                </div>
                {review.key_points && (
                  <div className="pt-4 border-t border-border/50">
                    <h4 className="text-sm font-semibold mb-3 text-muted-foreground uppercase tracking-wide">
                      Poin Penting
                    </h4>
                    <div className="space-y-2">
                      {review.key_points
                        .split("\n")
                        .filter((point) => point.trim())
                        .map((point, i) => (
                          <motion.div
                            key={i}
                            initial={{ opacity: 0, x: -10 }}
                            animate={{ opacity: 1, x: 0 }}
                            transition={{ delay: i * 0.05 }}
                            className="flex items-start space-x-2 text-sm text-foreground/80"
                          >
                            <span className="text-primary mt-1">•</span>
                            <span>{point.trim().replace(/^[-•]\s*/, "")}</span>
                          </motion.div>
                        ))}
                    </div>
                  </div>
                )}
              </CardContent>
            </Card>
          </motion.div>
        ))}
        </AnimatePresence>
      </div>

      {/* Dialog Konfirmasi Hapus */}
      <Dialog open={deleteDialogOpen} onOpenChange={setDeleteDialogOpen}>
        <DialogContent className="glass-card">
          <DialogHeader>
            <DialogTitle>Hapus Review</DialogTitle>
            <DialogDescription>
              Apakah Anda yakin ingin menghapus review ini? Tindakan ini tidak dapat dibatalkan.
            </DialogDescription>
          </DialogHeader>
          {reviewToDelete && (
            <div className="py-4">
              <p className="text-sm text-muted-foreground mb-2">Review:</p>
              <p className="text-sm bg-muted/50 p-3 rounded-md">
                {reviewToDelete.review_text.length > 100
                  ? `${reviewToDelete.review_text.substring(0, 100)}...`
                  : reviewToDelete.review_text}
              </p>
            </div>
          )}
          <DialogFooter>
            <Button
              variant="outline"
              onClick={() => {
                setDeleteDialogOpen(false)
                setReviewToDelete(null)
              }}
              disabled={deleting}
            >
              Batal
            </Button>
            <Button
              variant="destructive"
              onClick={handleConfirmDelete}
              disabled={deleting}
            >
              {deleting ? "Menghapus..." : "Hapus"}
            </Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </div>
  )
}

export { ReviewList }
export default ReviewList
