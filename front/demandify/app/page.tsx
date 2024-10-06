import EventCard from "@/components/event_card";
import { EventProps } from "@/model/event";



export default function Home() {

  const hcevent: EventProps = {
    id: "fd23fce0-c438-4a27-aae5-878ac0c54da1",
    name: "HTG rebaste ristimine",
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
    relevance: 0.4
  };


  // back is deployed but we didn't have time to connect :(
  const events: EventProps[] = [
    {
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
    },
    {
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
    }
  ];

  return (
    <div className="flex flex-col px-60 w-screen h-screen bg-white">

      <h1 className="text-black text-4xl pt-12">Hi, <span className="text-primary">Burger World</span></h1>
      <h2 className="text-black text-2xl pt-8">Upcoming events:</h2>
      <p className="text-gray-700">Events, we think will affect Your business</p>
      <div className="flex flex-row pt-4 overflow-x-scroll">
        {
          events.map((event: EventProps, i) => {
            return EventCard(event);
          }
          )
        }
      </div>

    </div>
  );
}
