import yaml from 'yaml';
import organisersYaml from '../data/organisers.yaml?raw';
import faqYaml from '../data/faq.yaml?raw';
import scheduleYaml from '../data/schedule.yaml?raw';
import speakersYaml from '../data/speakers.yaml?raw';

export interface Person {
  name: string;
  url?: string;
  photo?: string;
}
export interface Team {
  institution: string;
  country: string;
  url?: string;
  logo?: string;
  people: Person[];
}
export interface Schedule {
  note: string;
  days: { title: string; sessions: { time: string; session: string; lead?: string }[] }[];
}
export interface Speakers {
  note: string;
  faculty: { name: string; talk: string }[];
  invited?: (Person & { institution: string; talk: string })[];
}
export interface FaqItem {
  q: string;
  a: string;
}

function parse<T>(text: string): T {
  return yaml.parse(text) as T;
}

export function getOrganisers(): Team[] {
  return parse<{ teams: Team[] }>(organisersYaml).teams;
}

export function getFaq(): FaqItem[] {
  return parse<FaqItem[]>(faqYaml);
}

export function getSchedule(): Schedule {
  return parse<Schedule>(scheduleYaml);
}

export function getSpeakers(): Speakers {
  return parse<Speakers>(speakersYaml);
}
