import React, { useEffect } from "react";
import ReviewList from "./components/ReviewList";

function App() {
  const [reviews, setReviews] = React.useState([]);
  const [loading, setLoading] = React.useState(true);

  useEffect(() => {
    fetch("http://localhost:8000/reviews?app_id=447188370", {
      headers: {
        "Content-Type": "application/json",
      },
    })
      .then((res) => res.json())
      .then((data) => {
        setReviews(data);
        setLoading(false);
      });
  }, []);

  return (
    <div className="relative min-w-full bg-slate-500 py-4 min-h-screen">
      {!loading && (
        <>
          <div className="text-center text-2xl font-bold mb-4 text-white ">
            Reviews
          </div>
          <ReviewList reviews={reviews} />
        </>
      )}
      {loading && (
        <div className="absolute top-0 w-full h-full bg-slate-700 text-center">
          <p className="text-3xl text-white font-bold pt-24">Loading...</p>
        </div>
      )}
    </div>
  );
}

export default App;
