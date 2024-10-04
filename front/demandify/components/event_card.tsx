import { parseDate } from "@/lib/helper";
import { EventProps } from "@/model/event";
import Image from "next/image";

export default function EventCard(props: EventProps) {

  return (
    <div className="w-72 min-w-72 p-2 mr-4 border rounded-md">
      <Image
        src={props.coverImageURL}
        width={368}
        height={1000}
        alt="Image of event"
      />
      <h3 className="text-black text-xl">
        {props.name ? props.name : "Unknown name"}
        </h3>
      <p className="text-gray-500">
        {(props.startTime && props.endTime) ? parseDate(props.startTime) + " - " + parseDate(props.endTime) : "unknown - unknown"}
        </p>
      <p className="text-gray-500">
        {props.location ? props.location : "unknown location"}
      </p>
      <p className="text-black line-clamp-3">
        {props.description ? props.description : ""}
      </p>


    </div>
  )
}