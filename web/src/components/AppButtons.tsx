import { useState } from "react";

interface AppButtonsProps {
  onAppSelected: (app: string) => void;
}

const apps = [
  { id: "447188370", name: "Snapchat" },
  { id: "719972451", name: "Door Dash" },
  { id: "544007664", name: "Youtube" },
];

export default function AppButtons({ onAppSelected }: AppButtonsProps) {
  const [selectedAppIndex, setSelectedAppIndex] = useState(0);

  return (
    <div className="flex flex-row">
      {apps.map((app, i) => {
        return (
          <button
            key={i}
            className={`${
              i === selectedAppIndex
                ? "bg-white text-slate-800"
                : "bg-slate-500 text-white"
            } px-4 py-2 rounded-md`}
            onClick={() => {
              setSelectedAppIndex(i);
              onAppSelected(app.id);
            }}
          >
            {app.name}
          </button>
        );
      })}
    </div>
  );
}
