import { Review } from "../types/Review";
import RatingStars from "./RatingStars";

interface ReviewEntryProps {
  review: Review;
}

export default function ReviewEntry({ review }: ReviewEntryProps) {
  let date = new Date(review.updated);
  let formattedDate = date.toLocaleTimeString("en-US", {
    year: "numeric",
    month: "long",
    day: "numeric",
  });

  return (
    <div className="flex flex-col bg-white rounded-lg shadow-lg p-6 mb-4">
      <div className="flex flex-row items-center mb-4">
        <div className="flex flex-col">
          <div className="text-lg font-bold">{review.title}</div>
          <div className="text-sm font-bold">{review.authorName}</div>
          <div className="text-sm text-gray-500">{formattedDate}</div>
        </div>
      </div>
      <div className="flex flex-col">
        <div className="text-sm mb-4">{review.content}</div>
        <div className="flex flex-row items-center">
          <div className="text-sm text-gray-500 mr-2">Rating:</div>
          <RatingStars rating={review.rating} />
        </div>
      </div>
    </div>
  );
}
