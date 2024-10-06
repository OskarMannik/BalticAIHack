import { parseDate } from "@/lib/helper";
import { EventProps } from "@/model/event";
import Image from "next/image";
import Link from "next/link";

export default function EventPage({ params }: { params: { eventID: string } }) {
  const eventID = params.eventID;

  let eventData: EventProps = {
    id: "68",
    name: "CuFa RC Drifti ja Vaba Aja Keskuse külastus",
    startTime: 1701943200,
    endTime: 1701972000,
    location: "Estonia, Harjumaa, Tallinn, Tuulemaa 20, Tallinn",
    coverImageURL: "https://vgxifmuuonfxuwoperyd.supabase.co/storage/v1/object/public/diffusion_pictures/diffusion_pictures/event_8.jpg",
    description: "Mudelautodega driftimine on põnev sõiduharrastus, kus entusiastid võtavad oma väikesed mudelautod ja viivad need piirini, kogedes kontrollitud libisemist, kiirust ja täpset manööverdamist. See dünaamiline tegevus on inspireeritud suurte autospordiürituste driftivõistlustest, kuid mahutatud mudelmaailma, tuues kaasa adrenaliinirikkaid hetki ja tehnilisi väljakutseid.Sõidutehnika on võtmeelement, kus harrastajad õpivad kaalu ülekandmise abil kontrollima mudelauto tagaosas tekkivat libisemist. Käsirooli tehnikat kasutades ja oskuslikult manööverdades loovad driftijad muljetavaldavaid sõidustiile, mõnikord isegi matkides suurte professionaalsete driftivõistlejate trikke.Drifti simulaatorid on põnevad digitaalsed platvormid, mis toovad autospordi kire otse sinu arvutiekraanile. Need realistlikud mängud pakuvad võimalust kogeda driftimise dünaamikat ja oskusi virtuaalselt. Mängijad saavad istuda rooli mitmekesistes sõidukites ning harjutada täpset sõidutehnikat.",
    labels: [

    ],
    relevance: 0.55
  };

  // later fetch through eventID

  if (eventID == "68") {
    eventData = {
      id: "68",
      name: "CuFa RC Drifti ja Vaba Aja Keskuse külastus",
      startTime: 1701943200,
      endTime: 1701972000,
      location: "Estonia, Harjumaa, Tallinn, Tuulemaa 20, Tallinn",
      coverImageURL: "https://vgxifmuuonfxuwoperyd.supabase.co/storage/v1/object/public/diffusion_pictures/diffusion_pictures/event_8.jpg",
      description: "Mudelautodega driftimine on põnev sõiduharrastus, kus entusiastid võtavad oma väikesed mudelautod ja viivad need piirini, kogedes kontrollitud libisemist, kiirust ja täpset manööverdamist. See dünaamiline tegevus on inspireeritud suurte autospordiürituste driftivõistlustest, kuid mahutatud mudelmaailma, tuues kaasa adrenaliinirikkaid hetki ja tehnilisi väljakutseid.Sõidutehnika on võtmeelement, kus harrastajad õpivad kaalu ülekandmise abil kontrollima mudelauto tagaosas tekkivat libisemist. Käsirooli tehnikat kasutades ja oskuslikult manööverdades loovad driftijad muljetavaldavaid sõidustiile, mõnikord isegi matkides suurte professionaalsete driftivõistlejate trikke.Drifti simulaatorid on põnevad digitaalsed platvormid, mis toovad autospordi kire otse sinu arvutiekraanile. Need realistlikud mängud pakuvad võimalust kogeda driftimise dünaamikat ja oskusi virtuaalselt. Mängijad saavad istuda rooli mitmekesistes sõidukites ning harjutada täpset sõidutehnikat.",
      labels: [

      ],
      relevance: 0.55
    };
  } else if (eventID == "4") {
    eventData = {
      id: "4",
      name: "Park Minigolf",
      startTime: 1701943200,
      endTime: 1701972000,
      location: "Park Minigolf, Nautica Centre 2. floor, Tallinn, Estonia",
      coverImageURL: "https://vgxifmuuonfxuwoperyd.supabase.co/storage/v1/object/public/diffusion_pictures/diffusion_pictures/event_4.jpg",
      description: "WELCOME TO PARK MINIGOLF!\nPark Minigolf is a green, warm and light indoor minigolf centre. It never rains here.\nMinigolf is easy sports activity, suitable for all ages. Come and try popular entertainment among trees, bushes, flowers, fountains and fish ponds. We guarantee positive emotions in unique environment and bring excitement to dull everyday. Park Minigolf is situated in Estonian capital Tallinn, on the second floor of Nautica shopping centre.Boasting the only Rimi hypermarket in central Tallinn, Park Minigolf, a lot of shops and extensive dining options coupled with its unbeatable location between Tallinn old town and the port, Nautica shopping center provides for a great shopping experience under one roof for tourists and those living and working in the area.EVERYONE CAN PLAY HERE!\nPark Minigolf consists of two parts: Park course and Wild Wild West Saloon. Park course, which has 16 holes, is suitable for all ages and positive emotions are guaranteed here.Wild Wild West Saloon is ment for more adventurous players, who are looking for adrenaline and are willing to take risks.",
      labels: [

      ],
      relevance: 0.65
    };
  }

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
          <p className="text-black text-xl">{`${eventData.location}, 5 km away`}</p>
        </div>
        <div className="flex flex-col pt-4">
          {eventData.description.split("\n").map((paragraph: string, i) => {
            return <p key={i} className="text-black">{paragraph}</p>
          })}
        </div>
      </div>
      <div className="flex flex-col w-1/2 h-full gap-4 items-start">
        {eventID == "4" ? (<>
              <p className="text-black">
                The opening of Park Minigolf in Tallinn's Nautica shopping centre presents
                a golden opportunity for restaurants in the vicinity to tap into the
                influx of visitors, including families, tourists, and locals. We estimate
                a significant increase in foot traffic, with an average of 500-700
                customers arriving at the minigolf centre daily, creating a substantial
                captive audience for nearby restaurants.
              </p>
              <p className="text-black">
                The target audience skewed towards families, first-time visitors, and
                adventurous patrons can be segmented based on their preferences and
                demographics:
              </p>
              <ul className="list-disc pl-4">
                <li className="text-black">
                  Families with Children (30-40% of visitors): Parents may be accompanied
                  by kids aged 4-12, requiring kid-friendly restaurants that cater to
                  their needs and preferences.
                </li>
                <li className="text-black">
                  Adventurous Young Adults (20-30% of visitors): Young adults (18-30) may
                  prefer restaurants offering a lively atmosphere, craft beers, or unique
                  beverage experiences to complement the rush of playing minigolf.
                </li>
                <li className="text-black">
                  Tourists (20-30% of visitors): Visitors coming to Tallinn may seek
                  restaurants serving international cuisine, late-night food options, or
                  specialty food stores.
                </li>
                <li className="text-black">
                  Locals (10-20% of visitors): Residents working or living in the area may
                  look for quick bites or restaurants serving breakfast options, express
                  meals, or healthier snacks.
                </li>
              </ul>
              <p className="text-black">To capitalize on the influx of customers, restaurants could offer:</p>
              <ul className="list-disc pl-4">
                <li className="text-black">
                  Family-friendly dining and entertainment: Kid-centric restaurants with
                  creative menus, arcade games, or activities catering to families may see
                  an uptick in business.
                </li>
                <li className="text-black">
                  Quick bites, late-night food, and convenience: Counters like pizzerias,
                  kebab stands, or breakfast shops can profit from busy lunch and
                  late-night hour traffic brought by the shopping centre.
                </li>
                <li className="text-black">
                  Specialty and international food: Restaurants offering multicultural
                  cuisine, specialty stores, or signature desserts might attract curious
                  visitors and locals seeking an authentic experience.
                </li>
                <li className="text-black">
                  Safeguards: Healthy, fast-serve, and grab-to-go options: As time runs
                  out when on the course, restaurants serving fresh goods will be
                  selected.
                </li>
              </ul>
              <p className="text-black">Potential Traffic Numbers:</p>
              <p className="text-black">
                Assuming one-third of the Park Minigolf centre's daily visitors (215-235
                people) choose to dine out nearby, the projected number of customers for
                nearby restaurants could reach:
              </p>
              <ul className="list-disc pl-4">
                <li className="text-black">
                  High-side scenario: 635 people (weekly average: 435 people visiting
                  every day, including those dining, weekly total: 3,070-3,120 visitors)
                </li>
              </ul>
              <p className="text-black">OR</p>
              <ul className="list-disc pl-4">
                <li className="text-black">
                  Mid-estimated scenario: 493 visitors (weekly average: 345 individuals
                  dining after visiting the minigolf park, weekly total: 1,831).
                </li>
              </ul>
              <p className="text-gray-400">
                NB: this text is AI generated, double-check important information.
              </p>
            </>
          ) 
          :
          (<>
            <p className="text-black">Mudeldriftimise üritus võib burgerirestoranile tuua olulist lisakäivet ja nähtavust, kui osata seda nutikalt ära kasutada. Kuna tegemist on adrenaliinirikka ja tehnilise spordialaga, tõmbab üritus ligi nii entusiastlikke võistlejaid kui ka pealtvaatajaid, kes soovivad osa saada sellest põnevast kogemusest. Restoran saab kasu ürituse suurenenud külastajate voost, pakkudes erimenüüd, mis sobituks temaatiliselt autospordiga – näiteks kiiruse ja jõu sümbolina nimetatud burgerid või erilised „drifti-kombo“ pakkumised. Samuti võib koostada piiratud aja jooksul kehtivaid sooduspakkumisi, et meelitada rohkem inimesi sisse astuma. Võistluse pauside ajal on suurepärane võimalus pakkuda kiiret ja maitsvat toitu, mis sobib spordivõistluse tempoga.</p>
            <p className="text-black">Lisaks sellele avab üritus võimaluse brändinguks ja koostööks. Mudeldriftimise osalejad ja fännid on tihti aktiivsed sotsiaalmeedia kasutajad, kes jagavad oma elamusi laiemale publikule. Restoran võiks pakkuda sotsiaalmeedia kampaaniaid, kus külastajad saavad postitada pilte oma toidust ja driftimisest teatud teemaviidet kasutades, vastutasuks allahindluste või auhindade eest. Üritusel osalemine, näiteks oma burgeriputka seadmine võistluspaiga lähedale, võib suurendada nähtavust ja tuua restorani uudishimulikke kliente ka tulevikus.</p>
            <p className="text-gray-400">NB: this text is AI generated, double-check important information</p>
          </>)
        }

      </div>
    </div>
  </div>
}