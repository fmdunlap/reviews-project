import React from "react";
import ReviewEntry from "./ReviewEntry";

interface ReviewListProps {
  reviews: any[];
}

export default function ReviewList({ reviews }: ReviewListProps) {
  return (
    <div className="w-full">
      {reviews.map((review, i) => {
        return <ReviewEntry key={i} review={review} />;
      })}
    </div>
  );
}
