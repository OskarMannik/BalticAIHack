import { EventProps } from "@/model/event";

export default function EventPage({ params }: { params: { eventID: string } }) {
  const eventID = params.eventID;

  // later fetch through eventID
  const eventData: EventProps = {
    id: "fd23fce0-c438-4a27-aae5-878ac0c54da1",
    name: "New event",
    startTime: 1728054000,
    endTime: 1728064800,
    location: "Munga 12, 51007 Tartu, Estonia",
    coverImageURL: "/olli-the-polite-cat.jpg",
    description: "Ad ut esse culpa cupidatat elit cupidatat amet est non in voluptate laborum reprehenderit elit. Non nisi culpa proident velit veniam officia deserunt voluptate duis ad ut et. Aliqua minim ut consequat excepteur consequat enim occaecat magna. Duis nulla eu elit eiusmod pariatur Lorem reprehenderit laborum nostrud aliqua Lorem. Lorem anim laboris amet tempor aute cillum incididunt duis amet aliqua. Commodo sunt aliqua deserunt voluptate officia nostrud consectetur eiusmod officia.",
    labels: [
      {
        labelName: "transport",
        labelColor: "#32a852"
      }
    ],
    relevance: 0.85
  };

  return <div className="flex flex-row px-60 pt-24 w-screen h-screen bg-white">
    <div className="flex flex-col  w-1/2 h-full">
      <h1 className="text-black text-5xl">{eventData.name}</h1>
    </div>
    <div className="flex flex-col  w-1/2 h-full">
      <h2 className="text-black text-3xl">Here's what can happen:</h2>
    </div>
  </div>
}