from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List
import os
from dotenv import load_dotenv

from database import get_db, engine, Base
from models import Review
from schemas import ReviewCreate, ReviewResponse
from sentiment_analyzer import analyze_sentiment
from key_points_extractor import extract_key_points

load_dotenv()

# Buat tabel database (ditunda - hanya saat diperlukan)
def init_database():
    """Initialize database tables"""
    try:
        Base.metadata.create_all(bind=engine)
        return True
    except Exception as e:
        print(f"Warning: Could not create database tables: {e}")
        return False

app = FastAPI(title="Product Review Analyzer API", version="1.0.0")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],  # React dev servers
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Product Review Analyzer API", "version": "1.0.0"}

@app.post("/api/analyze-review", response_model=ReviewResponse, status_code=status.HTTP_201_CREATED)
async def analyze_review(review: ReviewCreate, db: Session = Depends(get_db)):
    """
    Analyze a product review:
    - Analyze sentiment (positive/negative/neutral) using Hugging Face
    - Extract key points using Gemini
    - Save to database
    """
    try:
        # Validate input
        if not review.review_text or len(review.review_text.strip()) == 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Review text cannot be empty"
            )
        
        # Analyze sentiment
        sentiment = analyze_sentiment(review.review_text)
        
        # Extract key points
        key_points = extract_key_points(review.review_text)
        
        # Save to database
        db_review = Review(
            review_text=review.review_text,
            sentiment=sentiment,
            key_points=key_points
        )
        db.add(db_review)
        db.commit()
        db.refresh(db_review)
        
        return db_review
    
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error analyzing review: {str(e)}"
        )

@app.get("/api/reviews", response_model=List[ReviewResponse])
async def get_reviews(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Get all reviews from the database.
    Supports pagination with skip and limit parameters.
    """
    try:
        reviews = db.query(Review).order_by(Review.created_at.desc()).offset(skip).limit(limit).all()
        return reviews
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching reviews: {str(e)}"
        )

@app.get("/api/reviews/{review_id}", response_model=ReviewResponse)
async def get_review(review_id: int, db: Session = Depends(get_db)):
    """
    Get a single review by ID.
    """
    try:
        review = db.query(Review).filter(Review.id == review_id).first()
        
        if not review:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Review with id {review_id} not found"
            )
        
        return review
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching review: {str(e)}"
        )

@app.delete("/api/reviews/{review_id}", status_code=status.HTTP_200_OK)
async def delete_review(review_id: int, db: Session = Depends(get_db)):
    """
    Delete a review by ID.
    """
    try:
        # Find the review
        review = db.query(Review).filter(Review.id == review_id).first()
        
        if not review:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Review with id {review_id} not found"
            )
        
        # Delete the review
        db.delete(review)
        db.commit()
        
        return {
            "message": "Review deleted successfully",
            "id": review_id
        }
    
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting review: {str(e)}"
        )

@app.on_event("startup")
async def startup_event():
    """Initialize database on startup"""
    init_database()

@app.get("/api/health")
def health_check():
    """Health check endpoint"""
    try:
        # Coba sambungkan ke database
        from database import engine
        with engine.connect() as conn:
            db_status = "connected"
            # Coba lakukan query
            conn.execute("SELECT 1")
    except Exception as e:
        db_status = f"error: {str(e)}"
    
    return {
        "status": "healthy",
        "database": db_status,
        "api_version": "1.0.0"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

