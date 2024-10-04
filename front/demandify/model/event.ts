export interface EventProps {
    name: string;
    startTime: number; // as unix timestamp
    endTime: number; // as unix timestamp
    location: string; // as "Address XX, Postal, city, country", maybe split into object?
    // in the future, also show distance to the event

    description: string; // ai generated short description of the event
    coverImageURL: string;
}