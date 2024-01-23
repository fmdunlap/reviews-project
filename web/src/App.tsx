import React, { useEffect } from "react";
import ReviewList from "./components/ReviewList";
import AppButtons from "./components/AppButtons";

const REVIEW_SERVICE_BASE_URL = "http://localhost:8000";

function App() {
  const [selectedAppId, setSelectedAppId] = React.useState("447188370");
  const [reviews, setReviews] = React.useState([]);
  const [loading, setLoading] = React.useState(true);

  useEffect(() => {
    fetch(`${REVIEW_SERVICE_BASE_URL}/reviews?app_id=${selectedAppId}`, {
      headers: {
        "Content-Type": "application/json",
      },
    })
      .then((res) => res.json())
      .then((data) => {
        setReviews(data);
        setLoading(false);
      });
  }, [selectedAppId]);

  return (
    <div className="relative min-w-full bg-slate-500 py-4 min-h-screen">
      {!loading && (
        <>
          <div className="text-center text-2xl font-bold mb-4 text-white ">
            Reviews
          </div>
          <div className="mx-auto px-4 md:px-0 md:w-2/3">
            <div className="flex flex-row py-4 gap-x-4">
              <p className="text-white my-auto text-lg">
                Select an app to view reviews from:
              </p>
              <AppButtons
                onAppSelected={(appId) => {
                  setSelectedAppId(appId);
                }}
              />
            </div>
            <ReviewList reviews={reviews} />
          </div>
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
