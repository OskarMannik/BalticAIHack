import { parseDate } from "@/lib/helper";
import { EventProps } from "@/model/event";
import Image from "next/image";
import Link from "next/link";

export default function EventPage({ params }: { params: { eventID: string } }) {
  const eventID = params.eventID;

  // later fetch through eventID
  const eventData: EventProps = {
    id: "fd23fce0-c438-4a27-aae5-878ac0c54da1",
    name: "HTG rebaste ristimine",
    startTime: 1728054000,
    endTime: 1728064800,
    location: "Munga 12, 51007 Tartu, Estonia",
    coverImageURL: "/olli-the-polite-cat.jpg",
    description: "The \"HTG rebaste ristimine\" event on September 24, 2020, revolves around the theme of \"Countries.\" During the day, participants (called freshmen) will compete in various Olympic-style challenges, while the evening will culminate in a glamorous Eurovision-inspired show. Each class is assigned a country, and students must wear outfits that match their class color and the country's theme, including specific required items. The event emphasizes creativity and team spirit, with students encouraged to prepare flags, mascots, and costumes, all while refraining from makeup and hairstyling products. They must also carry their school supplies in trash bags instead of backpacks. In the evening, each class must perform a dance routine based on music drawn from their assigned country, with all members required to participate. Additionally, the class must prepare a national anthem, which will be performed at Eurovision, and the entire event is scored to determine the overall winner. Stealing other classes' flags for extra points is allowed but must be done without violence. The day concludes with the Eurovision contest, so students are expected to clear their schedules. Strict rules on health and safety, including hand hygiene and mask usage, are also emphasized.",
    labels: [
      {
        labelName: "transport",
        labelColor: "#32a852"
      }
    ],
    relevance: 0.85
  };

  return <div className="px-48 pt-24 w-screen min-h-screen bg-white">
    <Link href="/" className="absolute top-[104px] left-20">
      <img src="/arrowback.svg"></img>
    </Link>
    <div className="flex flex-row items-end gap-12">
      <div className="flex flex-col w-1/2 h-full">
        <h1 className="text-primary text-5xl">{eventData.name}</h1>
      </div>
      <div className="flex flex-col  w-1/2 h-full">
        <h2 className="text-primary text-3xl">Here's what can happen:</h2>
      </div>
    </div>
    <div className="flex flex-row gap-12 h-full pt-8">
      <div className="flex flex-col w-1/2 h-full">
        <Image
          className="rounded-xl"
          src={eventData.coverImageURL}
          alt="Image of event"
          width={1200}
          height={400}
        />
        <div className="flex flex-row pt-4">
          <img src="/calendar.svg" className="mb-0.5 mr-1" />
          <p className="text-black text-xl">{parseDate(eventData.startTime) + " - " + parseDate(eventData.endTime)}</p>
        </div>
        <div className="flex flex-row pt-1">
          <img src="/location.svg" className="mb-0.5 mr-1" />
          <p className="text-black text-xl">{`${eventData.location}, TODO km away`}</p>
        </div>
        <div className="flex flex-col pt-4">
          {eventData.description.split("\n").map((paragraph: string, i) => {
            return <p key={i} className="text-black">{paragraph}</p>
          })}
        </div>
      </div>
      <div className="flex flex-col w-1/2 h-full gap-4 items-start">
        <p className="text-black">Hosting a freshman initiation event at Hugo Treffner Gymnasium, just 400 meters away, presents a prime opportunity to significantly boost your business during and after the event. These initiation activities can last several hours, leaving large groups of students hungry and looking for quick, convenient food. Given your fast food restaurant's proximity, you’re ideally positioned to capture this demand. Freshmen will likely head straight to your place, seeking affordable, satisfying meals to recharge after the high-energy activities. With dozens, if not hundreds, of students gathering in one location, you can expect a sharp increase in foot traffic throughout the event.</p>
        <p className="text-black">To maximize this opportunity, consider preparing for a surge in orders and promoting special group offers or meal deals. Students tend to socialize after initiation events, making your restaurant an attractive spot for post-event gatherings. By offering discounts for groups, or quick combo meals, you can encourage students to choose your place for both convenience and a fun, casual dining experience. A well-planned strategy during this event can create a lasting impression on the new students, driving not only immediate sales but also encouraging repeat visits throughout the school year.</p>
        <p className="text-gray-400">NB: this text is AI generated, double-check important information</p>
      </div>
    </div>
  </div>
}