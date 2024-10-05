import { parseDate } from "@/lib/helper";
import { EventProps, LabelProps } from "@/model/event";
import Image from "next/image";
import Link from "next/link";

export default function EventCard(props: EventProps) {

  return (
    <div className="w-72 min-w-72 p-2 mr-4 border rounded-md">
      <Image
        className="rounded-sm"
        src={props.coverImageURL}
        width={368}
        height={1000}
        alt="Image of event"
      />
      <h3 className="text-black text-xl pt-2">
        {props.name ? props.name : "Unknown name"}
      </h3>
      <p className="text-gray-500">
        {(props.startTime && props.endTime) ? parseDate(props.startTime) + " - " + parseDate(props.endTime) : "unknown - unknown"}
      </p>
      <p className="text-gray-500">
        {props.location ? props.location : "unknown location"}
      </p>
      <p className="text-black line-clamp-3 pt-4">
        {props.description ? props.description : ""}
      </p>
      <p className="text-black pt-4">
        Relevance:
      </p>
      <div className="w-full h-6 bg-gray-300 rounded">
        <div 
          className="h-full rounded bg-gradient-to-r from-primary to-secondary"
          style={{width: `${Math.min(100, Math.max(0, props.relevance * 100))}%`}}
        ></div>
      </div>

      <Link href={`/event/${props.id}`} className="flex flex-row pt-1">
        <img src="/info.svg" alt="View details" className="-ml-0.5" />
        <p className="text-black pl-1">View details:</p>
      </Link>

    </div>
  )
}