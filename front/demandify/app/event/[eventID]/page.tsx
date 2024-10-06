import { parseDate } from "@/lib/helper";
import { EventProps } from "@/model/event";
import Image from "next/image";
import Link from "next/link";

export default function EventPage({ params }: { params: { eventID: string } }) {
  const eventID = params.eventID;

  // later fetch through eventID
  const eventData: EventProps = {
    id: "68",
    name: "CuFa RC Drifti ja Vaba Aja Keskuse külastus",
    startTime: 1710691200,
    endTime: 1733097540 ,
    location: "Estonia, Harjumaa, Tallinn, Tuulemaa 20, Tallinn",
    coverImageURL: "https://vgxifmuuonfxuwoperyd.supabase.co/storage/v1/object/public/diffusion_pictures/diffusion_pictures/event_8.jpg",
    description: "Mudelautodega driftimine on põnev sõiduharrastus, kus entusiastid võtavad oma väikesed mudelautod ja viivad need piirini, kogedes kontrollitud libisemist, kiirust ja täpset manööverdamist. See dünaamiline tegevus on inspireeritud suurte autospordiürituste driftivõistlustest, kuid mahutatud mudelmaailma, tuues kaasa adrenaliinirikkaid hetki ja tehnilisi väljakutseid.Sõidutehnika on võtmeelement, kus harrastajad õpivad kaalu ülekandmise abil kontrollima mudelauto tagaosas tekkivat libisemist. Käsirooli tehnikat kasutades ja oskuslikult manööverdades loovad driftijad muljetavaldavaid sõidustiile, mõnikord isegi matkides suurte professionaalsete driftivõistlejate trikke.Drifti simulaatorid on põnevad digitaalsed platvormid, mis toovad autospordi kire otse sinu arvutiekraanile. Need realistlikud mängud pakuvad võimalust kogeda driftimise dünaamikat ja oskusi virtuaalselt. Mängijad saavad istuda rooli mitmekesistes sõidukites ning harjutada täpset sõidutehnikat.",
    labels: [
      
    ],
    relevance: 0.55
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