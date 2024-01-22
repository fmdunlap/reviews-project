interface RatingStarsProps {
  rating: number;
}

function RatingStarSvg() {
  return (
    <svg
      className="w-4 h-4 fill-current text-yellow-500 my-auto"
      viewBox="0 0 24 24"
    >
      <path d="M12 17.27L18.18 21l-1.64-7.03L22 9.24l-7.19-.61L12 2 9.19 8.63 2 9.24l5.46 4.73L5.82 21z" />
    </svg>
  );
}

export default function RatingStars({ rating }: RatingStarsProps) {
  return (
    <div className="flex flex-row">
      <p className="pr-2">{rating}</p>
      {Array(Math.floor(rating))
        .fill(0)
        .map((_, i) => {
          return (
            <>
              <RatingStarSvg key={i} />
            </>
          );
        })}
    </div>
  );
}
