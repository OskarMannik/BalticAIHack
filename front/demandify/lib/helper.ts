import { format } from "date-fns";
import { et } from "date-fns/locale";

/** 
 * 
 * @param timestamp unix timestamp in seconds
 * @returns date in human-readable format
 */
export function parseDate(timestamp: number) {
    return format(timestamp * 1000, "dd.MM.yyyy HH:mm", {locale: et})
} 