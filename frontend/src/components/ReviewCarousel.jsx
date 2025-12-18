import { motion } from "framer-motion"
import { ChevronLeft, ChevronRight } from "lucide-react"
import { useCallback, useEffect, useState } from "react"
import useEmblaCarousel from "embla-carousel-react"
import { Button } from "./ui/button"
import { Card, CardContent } from "./ui/card"

export function ReviewCarousel({ reviews }) {
  const [emblaRef, emblaApi] = useEmblaCarousel({ loop: true, align: "start" })
  const [selectedIndex, setSelectedIndex] = useState(0)

  const scrollPrev = useCallback(() => {
    if (emblaApi) emblaApi.scrollPrev()
  }, [emblaApi])

  const scrollNext = useCallback(() => {
    if (emblaApi) emblaApi.scrollNext()
  }, [emblaApi])

  const onSelect = useCallback(() => {
    if (!emblaApi) return
    setSelectedIndex(emblaApi.selectedScrollSnap())
  }, [emblaApi])

  useEffect(() => {
    if (!emblaApi) return
    onSelect()
    emblaApi.on("select", onSelect)
    emblaApi.on("reInit", onSelect)

    // Putar otomatis
    const autoplay = setInterval(() => {
      emblaApi.scrollNext()
    }, 5000)

    return () => {
      emblaApi.off("select", onSelect)
      clearInterval(autoplay)
    }
  }, [emblaApi, onSelect])

  const getSentimentColor = (sentiment) => {
    switch (sentiment?.toLowerCase()) {
      case "positive":
        return "from-green-500/20 to-emerald-500/10 dark:from-green-500/20 dark:to-emerald-500/10"
      case "negative":
        return "from-red-500/20 to-rose-500/10 dark:from-red-500/20 dark:to-rose-500/10"
      case "neutral":
        return "from-yellow-500/20 to-amber-500/10 dark:from-yellow-500/20 dark:to-amber-500/10"
      default:
        return "from-gray-500/20 to-slate-500/10 dark:from-gray-500/20 dark:to-slate-500/10"
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

  if (!reviews || reviews.length === 0) {
    return (
      <div className="flex items-center justify-center h-full">
        <p className="text-muted-foreground">Tidak ada review untuk ditampilkan</p>
      </div>
    )
  }

  return (
    <div className="relative h-full flex flex-col">
      <div className="flex-1 overflow-hidden" ref={emblaRef}>
        <div className="flex h-full">
          {reviews.map((review, index) => (
            <div key={review.id} className="flex-[0_0_100%] min-w-0 px-4">
              <motion.div
                initial={{ opacity: 0, scale: 0.9 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ duration: 0.3 }}
                className="h-full"
              >
                <Card className={`h-full bg-gradient-to-br ${getSentimentColor(review.sentiment)}`}>
                  <CardContent className="p-6 h-full flex flex-col">
                    <div className="flex items-center justify-between mb-4">
                      <div className="flex items-center space-x-2">
                        <span className="text-2xl">{getSentimentEmoji(review.sentiment)}</span>
                        <span className="text-sm font-semibold uppercase tracking-wider">
                          {getSentimentLabel(review.sentiment)}
                        </span>
                      </div>
                      <span className="text-xs text-muted-foreground">
                        {new Date(review.created_at).toLocaleDateString()}
                      </span>
                    </div>
                    <div className="flex-1 overflow-y-auto">
                      <p className="text-sm leading-relaxed mb-4">{review.review_text}</p>
                      {review.key_points && (
                        <div className="mt-4 pt-4 border-t border-border/50">
                          <h4 className="text-xs font-semibold mb-2 text-muted-foreground uppercase tracking-wide">
                            Poin Penting
                          </h4>
                          <div className="space-y-1 text-xs text-foreground/80">
                            {review.key_points.split("\n").map((point, i) => (
                              point.trim() && (
                                <div key={i} className="flex items-start">
                                  <span className="mr-2">•</span>
                                  <span>{point.trim()}</span>
                                </div>
                              )
                            ))}
                          </div>
                        </div>
                      )}
                    </div>
                  </CardContent>
                </Card>
              </motion.div>
            </div>
          ))}
        </div>
      </div>

      {/* Navigasi */}
      <div className="flex items-center justify-center space-x-2 mt-4">
        <Button
          variant="outline"
          size="icon"
          onClick={scrollPrev}
          className="rounded-full"
        >
          <ChevronLeft className="h-4 w-4" />
        </Button>
        <div className="flex space-x-1">
          {reviews.map((_, index) => (
            <button
              key={index}
              onClick={() => emblaApi?.scrollTo(index)}
              className={`h-2 rounded-full transition-all ${
                index === selectedIndex
                  ? "w-8 bg-primary"
                  : "w-2 bg-muted hover:bg-muted-foreground/50"
              }`}
            />
          ))}
        </div>
        <Button
          variant="outline"
          size="icon"
          onClick={scrollNext}
          className="rounded-full"
        >
          <ChevronRight className="h-4 w-4" />
        </Button>
      </div>
    </div>
  )
}

