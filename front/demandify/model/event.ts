export interface LabelProps {
    labelName: string;
    labelColor: string; // hex code for that label
}

export interface EventProps {
    id: string;
    name: string;
    startTime: number; // as unix timestamp
    endTime: number; // as unix timestamp
    location: string; // as "Address XX, Postal, city, country", maybe split into object?
    // in the future, also show distance to the event

    description: string; // ai generated short description of the event
    coverImageURL: string;
    relevance: number; // float 0 - 1, that represents how relevant a task is
    labels: LabelProps[];
}