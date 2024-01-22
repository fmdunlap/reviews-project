import React from "react";
import ReviewEntry from "./ReviewEntry";

interface ReviewListProps {
  reviews: any[];
}

export default function ReviewList({ reviews }: ReviewListProps) {
  return (
    <div className="w-full px-4 md:px-0 md:w-2/3 mx-auto">
      {reviews.map((review) => {
        return <ReviewEntry review={review} />;
      })}
    </div>
  );
}
